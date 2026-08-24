from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from .collectors import GitHubCollector, OpenAlexCollector, WebCollector
from .config import db_path, load_config, output_path
from .db import Repository
from .exporters import export_csv, export_json, export_markdown
from .importers import from_csv, from_json
from .notion_sync import sync
from .report import build_pdf


def repository() -> Repository: return Repository(db_path())


def cmd_init(_: argparse.Namespace) -> None:
    repository().init(); output_path().mkdir(parents=True, exist_ok=True)
    print(f"Banco inicializado: {db_path()}")


def cmd_import_seed(args: argparse.Namespace) -> None:
    target = repository(); target.init(); items = from_json(args.path)
    for item in items: target.upsert(item)
    print(f"{len(items)} evidências importadas.")


def cmd_import_csv(args: argparse.Namespace) -> None:
    target = repository(); target.init(); items = from_csv(args.path, args.kind)
    for item in items: target.upsert(item)
    print(f"{len(items)} evidências importadas.")


def cmd_collect(args: argparse.Namespace) -> None:
    cfg, target = load_config(args.config), repository(); target.init()
    options, total = cfg.get("collection", {}), 0
    for source in cfg.get("sources", []):
        if not source.get("enabled", True): continue
        if source["type"] == "github": collector = GitHubCollector(source["username"], os.getenv("GITHUB_TOKEN"))
        elif source["type"] == "openalex": collector = OpenAlexCollector(source["query"])
        elif source["type"] == "web": collector = WebCollector(source["url"], source["name"], options.get("user_agent", "PegadaDigital/1.0"), options.get("timeout_seconds", 20), options.get("delay_seconds", 1), options.get("respect_robots_txt", True))
        else: print(f"Tipo desconhecido: {source['type']}"); continue
        try:
            items = collector.collect()
            for item in items: target.upsert(item)
            total += len(items); print(f"{source['name']}: {len(items)}")
        except Exception as exc: print(f"{source['name']}: falhou ({exc})")
    print(f"Total coletado/atualizado: {total}")


def cmd_export(args: argparse.Namespace) -> None:
    rows, out = repository().all(), output_path(); out.mkdir(parents=True, exist_ok=True)
    export_json(rows, out / "evidencias.json")
    if args.all:
        export_csv(rows, out / "evidencias.csv"); export_markdown(rows, out / "mapa_pegada_digital.md")
    print(f"Exportação concluída em {out}")


def cmd_report(_: argparse.Namespace) -> None:
    path = output_path() / "Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf"
    build_pdf(repository().all(), path); print(f"Relatório gerado: {path}")


def cmd_notion(args: argparse.Namespace) -> None:
    load_dotenv()
    rows = repository().all()
    if args.only_reviewed:
        rows = [row for row in rows if row["identity_status"] == "reviewed"]
    result = sync(rows, dry_run=args.dry_run)
    mode = "Simulação" if args.dry_run else "Sincronização"
    print(f"{mode} concluída: {result.created} novos, {result.updated} atualizados.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pegada", description="Coleta e gera o Mapa da Pegada Digital")
    sub = parser.add_subparsers(required=True)
    p = sub.add_parser("init"); p.set_defaults(func=cmd_init)
    p = sub.add_parser("import-seed"); p.add_argument("path", type=Path); p.set_defaults(func=cmd_import_seed)
    p = sub.add_parser("import-csv"); p.add_argument("path", type=Path); p.add_argument("--kind", required=True); p.set_defaults(func=cmd_import_csv)
    p = sub.add_parser("collect"); p.add_argument("--config", type=Path, default=Path("config/collector.toml")); p.set_defaults(func=cmd_collect)
    p = sub.add_parser("export"); p.add_argument("--all", action="store_true"); p.set_defaults(func=cmd_export)
    p = sub.add_parser("report"); p.add_argument("--format", choices=["pdf"], default="pdf"); p.set_defaults(func=cmd_report)
    p = sub.add_parser("notion-sync")
    p.add_argument("--dry-run", action="store_true", help="simula sem gravar no Notion")
    p.add_argument("--only-reviewed", action="store_true", help="envia apenas itens revisados")
    p.set_defaults(func=cmd_notion)
    return parser


def main() -> None:
    args = build_parser().parse_args(); args.func(args)


if __name__ == "__main__": main()
