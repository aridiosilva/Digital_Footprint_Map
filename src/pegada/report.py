from __future__ import annotations

from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf(rows: list[dict], path: Path, subject: str = "Aridio Silva") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], alignment=TA_CENTER,
                              fontSize=25, leading=31, textColor=colors.HexColor("#123B5D")))
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm,
                            topMargin=1.6*cm, bottomMargin=1.6*cm,
                            title=f"Mapa da Pegada Digital — {subject}")
    story = [Spacer(1, 5*cm), Paragraph("MAPA DA PEGADA DIGITAL", styles["Cover"]),
             Spacer(1, .5*cm), Paragraph(subject, styles["Heading1"]),
             Spacer(1, 1*cm), Paragraph("Relatório auditável de evidências públicas", styles["Normal"]),
             PageBreak(), Paragraph("Resumo executivo", styles["Heading1"]),
             Paragraph(f"Foram registradas {len(rows)} evidências. Itens pendentes exigem validação humana para excluir homônimos.", styles["BodyText"]),
             Spacer(1, .4*cm)]
    counts = Counter(r["category"] for r in rows)
    table = Table([["Categoria", "Quantidade"]] + [[k, str(v)] for k, v in sorted(counts.items())],
                  colWidths=[12*cm, 3*cm])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#123B5D")),
                               ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                               ("GRID", (0,0), (-1,-1), .25, colors.grey),
                               ("VALIGN", (0,0), (-1,-1), "TOP"),
                               ("PADDING", (0,0), (-1,-1), 6)]))
    story += [table, PageBreak(), Paragraph("Evidências", styles["Heading1"])]
    for row in rows:
        story += [Paragraph(row["title"], styles["Heading2"]),
                  Paragraph(f"<b>Fonte:</b> {row['source']} | <b>Categoria:</b> {row['category']}", styles["BodyText"]),
                  Paragraph(f"<b>URL:</b> {row['url']}", styles["BodyText"]),
                  Paragraph(f"<b>Status:</b> {row['identity_status']} | <b>Confiança:</b> {row['confidence']:.0%}", styles["BodyText"]),
                  Paragraph(row.get("snippet") or row.get("notes") or "Sem resumo.", styles["BodyText"]), Spacer(1, .3*cm)]
    story += [PageBreak(), Paragraph("Metodologia e limitações", styles["Heading1"]),
              Paragraph("A coleta registra conteúdo público, URL, origem, data e impressão digital. Resultados automáticos são candidatos, não prova de identidade. Google Acadêmico e Biblioteca Nacional dependem de importação e confirmação manual. O relatório não inclui dados privados nem contorna controles de acesso.", styles["BodyText"])]
    doc.build(story)
