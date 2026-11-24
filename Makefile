PYTHON ?= python3
SOURCE ?= examples/spec.csv
OUTPUT ?= build/spec.bin

.PHONY: run test style

run:
	$(PYTHON) -m src.assembler "$(SOURCE)" "$(OUTPUT)" --test

test:
	$(PYTHON) -m pytest tests/ -q

style:
	$(PYTHON) -m scripts.check_style
