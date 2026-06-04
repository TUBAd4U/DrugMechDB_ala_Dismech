## DrugMechDB validation commands
## Requires: linkml, linkml-term-validator, linkml-reference-validator
## Install: pip install -e ".[dev]"  (or: uv sync --group dev)

SCHEMA     := src/drugmechdb/schema/drugmechdb.yaml
TARGET     := MechanisticPath
KB_DIR     := kb/paths
OAK_CONFIG := conf/oak_config.yaml

# ── Installation ──────────────────────────────────────────────────────────────

install:
	pip install -e ".[dev]"

# ── Schema validation (structure only — fast) ─────────────────────────────────

# Validate a single path file against the schema
# Usage: make validate FILE=kb/paths/DB00619_MESH_D015464_1.yaml
validate:
	linkml-validate --schema $(SCHEMA) --target-class $(TARGET) $(FILE)

# Validate all path files
validate-all:
	@echo "Validating all path files..."
	@failed=0; \
	for f in $(KB_DIR)/*.yaml; do \
		[ "$$(basename $$f)" = "_index.yaml" ] && continue; \
		if ! linkml-validate --schema $(SCHEMA) --target-class $(TARGET) "$$f" 2>&1 | grep -q "No issues found"; then \
			echo "  FAIL: $$f"; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo "Done. Failures: $$failed"

# ── Ontology term validation (node IDs + labels) ──────────────────────────────

# Validate terms in a single file
# Usage: make validate-terms FILE=kb/paths/DB00619_MESH_D015464_1.yaml
validate-terms:
	linkml-term-validator validate-data $(FILE) \
		-s $(SCHEMA) -t $(TARGET) --labels -c $(OAK_CONFIG)

# Validate terms in all path files
validate-terms-all:
	@echo "Validating ontology terms in all path files..."
	@failed=0; \
	for f in $(KB_DIR)/*.yaml; do \
		[ "$$(basename $$f)" = "_index.yaml" ] && continue; \
		out=$$(linkml-term-validator validate-data "$$f" \
			-s $(SCHEMA) -t $(TARGET) --labels -c $(OAK_CONFIG) 2>&1); \
		if ! echo "$$out" | grep -q "Validation passed"; then \
			echo "  FAIL: $$f"; \
			echo "$$out"; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo "Done. Failures: $$failed"

# ── Reference validation (PubMed snippet matching) ────────────────────────────

# Validate evidence snippets in a single file
# Usage: make validate-references FILE=kb/paths/DB00619_MESH_D015464_1.yaml
validate-references:
	linkml-reference-validator validate data $(FILE) \
		--schema $(SCHEMA) --target-class $(TARGET)

# ── Full QC (all three layers) ────────────────────────────────────────────────

# Full validation of a single file
# Usage: make qc FILE=kb/paths/DB00619_MESH_D015464_1.yaml
qc:
	@echo "=== Schema validation ==="
	$(MAKE) validate FILE=$(FILE)
	@echo "=== Term validation ==="
	$(MAKE) validate-terms FILE=$(FILE)
	@echo "=== Reference validation ==="
	$(MAKE) validate-references FILE=$(FILE)
	@echo "=== Done ==="

# ── Data migration ────────────────────────────────────────────────────────────

# Split monolithic YAML into individual path files
split:
	python3 scripts/split_monolith.py

split-dry-run:
	python3 scripts/split_monolith.py --dry-run

.PHONY: install validate validate-all validate-terms validate-terms-all \
        validate-references qc split split-dry-run
