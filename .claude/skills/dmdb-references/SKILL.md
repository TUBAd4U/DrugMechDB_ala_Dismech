---
name: dmdb-references
description: Add, validate, and repair per-edge evidence on DrugMechDB paths so every snippet is a verbatim substring of its cited source. Use when adding evidence, when QC Layer 4 (reference verification) fails, or when backfilling PMIDs onto a path. Mirrors Dismech's dismech-references.
---

# dmdb-references — evidence & verbatim snippets

This skill backs **QC Layer 4** (`scripts/validate_references.py`, via
`linkml-reference-validator`). It enforces the one contract that makes the KB
machine-verifiable: **a snippet must appear verbatim in the source it cites.**

## The contract

Each `EvidenceItem` on an edge:

```yaml
links:
  - key: decreases activity of
    source: MESH:D000068818
    target: UniProt:P00533
    evidence:
      - reference: PMID:12345678        # the cited source
        snippet: "exact substring copied from that source's text"
        supports: SUPPORT               # SUPPORT | PARTIAL | REFUTE | NO_EVIDENCE | WRONG_STATEMENT
        evidence_source: HUMAN_CLINICAL  # HUMAN_CLINICAL | MODEL_ORGANISM | IN_VITRO | COMPUTATIONAL | OTHER
        explanation: "optional curator note"
```

- **Never fabricate a snippet.** It must be a literal substring of the referenced
  document. The validator does exact substring matching against the cached text.
- An edge with no supporting source uses `supports: NO_EVIDENCE` + an `explanation`,
  rather than a guessed citation.

## Workflow

1. **Fetch the source into the cache first** (the validator reads `references_cache/`):
   - `.venv-py310/bin/python scripts/pubmed_fetch.py search "<query>"`
   - `.venv-py310/bin/python scripts/pubmed_fetch.py fetch PMID:12345678`
   This writes `references_cache/PMID_12345678.md`.
2. **Copy the snippet verbatim** from that cached abstract into the edge.
3. **Validate offline** (deterministic, no network):
   `just qc-layer 4 kb/paths/<file>.yaml` or `just qc <file>` — Layer 4 runs `--offline`
   against the committed cache. The pre-edit hook does the same on every write.

## Source-policy note (read before scaling)

The *machinery* is source-agnostic — it verifies "snippet ⊂ cited source" regardless of
source. The **policy** of *which* sources are admissible is unsettled (see project
`CLAUDE.md` §Flags): the PRD makes PubMed verbatim snippets the only sanctioned evidence,
while Su's steer to us is to cite the **secondary source that asserts the established
mechanism** (DrugBank MoA, reviews) and bars primary-literature reconstruction. Confirm
the evidence-source policy with Jayden + Su before a large backfill/forwardfill run.
Until then, keep snippets verbatim and the `reference` honest about its source.
