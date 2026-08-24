.PHONY: install test lint demo clean
install:
	python -m pip install -e '.[dev]'
test:
	pytest -q
lint:
	ruff check .
demo:
	pegada init
	pegada import-seed data/seed/evidencias_iniciais.json
	pegada export --all
	pegada report --format pdf
clean:
	python -c "from pathlib import Path; [p.unlink() for p in Path('output').glob('*') if p.is_file()]"
