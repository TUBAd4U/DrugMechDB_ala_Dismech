# DrugMechDB justfile — Phase 2 QC entrypoints.
#
# All targets shell out to scripts/qc.py (the layer orchestrator) using the
# Python 3.10 virtualenv at .venv-py310/. To bootstrap:
#
#     /opt/homebrew/Cellar/python@3.10/3.10.4/.../python3.10 -m venv .venv-py310
#     .venv-py310/bin/pip install -e ".[dev]"
#
# Then `just qc` runs the full pipeline. Pass arbitrary args after `--` to
# qc, e.g. `just qc -- kb/paths/DB00002_MESH_D003110_1.yaml --profile ai_curated`.

PY := ".venv-py310/bin/python"

# default target
default: qc

# Run the full QC pipeline with profile auto-detection (default).
qc *ARGS:
    {{PY}} scripts/qc.py {{ARGS}}

# Force the legacy profile (Layers 1, 2, 3; evidence not required).
qc-legacy *ARGS:
    {{PY}} scripts/qc.py --profile legacy {{ARGS}}

# Force the ai_curated profile (Layers 1, 2, 3, 4; evidence required).
qc-ai *ARGS:
    {{PY}} scripts/qc.py --profile ai_curated {{ARGS}}

# Run a single layer (Layer N) across all files or given args.
qc-layer N *ARGS:
    {{PY}} scripts/qc.py --layer {{N}} {{ARGS}}

# Machine-readable JSON output.
qc-json *ARGS:
    {{PY}} scripts/qc.py --json {{ARGS}}

# Phase-1 / 1.5 maintenance helpers (one-shot data cleanups).
normalize:
    {{PY}} scripts/phase1_normalize_paths.py --dry-run

normalize-write:
    {{PY}} scripts/phase1_normalize_paths.py

canonicalize:
    {{PY}} scripts/canonicalize_predicates.py

canonicalize-write:
    {{PY}} scripts/canonicalize_predicates.py --write

rebuild-index:
    {{PY}} scripts/rebuild_index.py

# Pytest suite (tests/).
test *ARGS:
    {{PY}} -m pytest {{ARGS}}

# Show what got installed and which Python is in use.
env-info:
    @echo "Python:" $({{PY}} --version)
    @echo "Venv:" $(dirname $(dirname {{PY}}))
    @{{PY}} -c "import linkml, linkml_runtime, linkml_term_validator, linkml_reference_validator; \
        print(f'linkml={linkml.__version__}'); \
        print(f'linkml-runtime={linkml_runtime.__version__}'); \
        print(f'linkml-term-validator={linkml_term_validator.__version__ if hasattr(linkml_term_validator, \"__version__\") else \"?\"}'); \
        print(f'linkml-reference-validator={linkml_reference_validator.__version__ if hasattr(linkml_reference_validator, \"__version__\") else \"?\"}')"
