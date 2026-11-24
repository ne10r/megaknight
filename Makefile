PYTHON ?= python3
SOURCE ?= examples/vector_1.csv
OUTPUT ?= build/vector.bin
DUMP ?= build/memory.json
START ?= 200
END ?= 207

.PHONY: run assemble demo test style

assemble:
	$(PYTHON) -m src.assembler "$(SOURCE)" "$(OUTPUT)" --test

run: assemble
	$(PYTHON) -m src.interpreter "$(OUTPUT)" "$(DUMP)" \
		--start "$(START)" --end "$(END)"

demo:
	$(PYTHON) -m scripts.demo_stage5

test:
	$(PYTHON) -m pytest tests/ -q

style:
	$(PYTHON) -m scripts.check_style
