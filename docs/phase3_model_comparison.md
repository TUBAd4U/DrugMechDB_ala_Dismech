# Phase-3 Eval — Curating-Model Comparison: Opus 4.8 vs Sonnet 4.6

**Matched A/B:** Opus 4.8 curated P03–P07; Sonnet 4.6 curated P08–P12 (5 vs 5, identical PubMed-only workflow, same prompt template).
**Two data sources:** (a) **run instrumentation** — tool calls, wall-clock, tokens, retries (from the eval runner); (b) **output-file analysis** — deterministic stats parsed from the curated `tests/phase3_eval_outputs/*.yaml` (this report's primary evidence).

---

## Verdict (TL;DR)

1. **The QC gate cannot separate the models.** Both: **5/5 first-pass PASS, 0 retries, 0 prefix violations, 0 legacy prefixes, 100% `SUPPORT`.** Each alone clears the ≥80% Phase-3 gate. So **the model choice is not a quality-gate decision** — the gate is saturated and binary.
2. **The deterministic differences are structural, not pass/fail:** Opus writes **leaner** paths (4.0 nodes / 3.2 edges, denser evidence per edge); Sonnet writes **richer** paths (5.0 nodes / 4.2 edges, more total evidence, models pathogen context via `in taxon`).
3. **Cost vs throughput is the real fork:** Sonnet is **deterministically ~40% cheaper**; Opus is **~2× faster and makes ~2× fewer tool calls** (≈2× less PubMed load).
4. **Mechanism quality is comparable** — and both share the *same* gate-invisible weakness (edge-evidence semantic looseness + reliance on primary literature). This is **not** a model differentiator; it's a methodology gap the human review must close.

---

## 1. Why the gate is non-discriminating

| Run metric (instrumentation) | Opus 4.8 (P03–P07) | Sonnet 4.6 (P08–P12) |
|---|---|---|
| First-pass PASS (all 4 layers) | 5/5 (100%) | 5/5 (100%) |
| Retries | 0 | 0 |
| Avg tool calls | 29.8 | 56.6 (~1.9×) |
| Avg wall-clock | 185 s | 360 s (~1.95×) |
| Avg tokens | 68.1k | 68.2k (≈equal) |
| NCBI 429 (rate-limit) | more (cold cache) | fewer (warm cache) |

Both models *saturate* the QC gate. The gate checks structure / prefix↔type / predicate-in-enum / verbatim-snippet — none of which either model strains. **Conclusion: the gate is the wrong instrument for the model decision.** The decision must come from the dimensions below.

---

## 2. Deterministic structural comparison (from the output files)

| Output-file metric | Opus 4.8 (P03–P07) | Sonnet 4.6 (P08–P12) |
|---|---|---|
| Nodes / path (mean, range) | **4.0** (4–4) | **5.0** (4–6) |
| Edges / path (mean, range) | **3.2** (3–4) | **4.2** (4–5) |
| Evidence items / edge (mean) | **1.88** (30 over 16) | **1.62** (34 over 21) |
| Total evidence items | 30 | 34 |
| Distinct PMIDs / file (mean) | 4.8 | 4.6 |
| Prefix violations / legacy | **0 / 0** | **0 / 0** |
| `supports` distribution | 100% SUPPORT | 100% SUPPORT |
| Snippet length (mean chars) | 146 | 150 |

**Read:** Opus converges on the canonical minimal shape — exactly **Drug → Protein target → 1 intermediate → Disease** (4 nodes), with ~2 evidence items per edge. Sonnet **elaborates the mechanism** — more intermediate biological steps (e.g., P09 methotrexate: 6 nodes / 5 edges, DHFR → tetrahydrofolate → DNA biosynthesis → proliferation → ALL) and models pathogen context with `OrganismTaxon` + `in taxon` edges (P11, P12). Both sit inside the 3–7-link convention; Opus at the lean end, Sonnet mid-range.

Neither is categorically "better": Opus's parsimony is closer to DrugMechDB's "minimal canonical path" convention and is faster to human-review; Sonnet's granularity adds mechanistic resolution but **more edges = more chances for a marginally-supported edge** (borne out in §3).

**Predicate vocabulary** (both draw from the in-repo 67-enum, as required): Opus used `decreases activity of`(5), `positively regulates`(4), `causes`(2), `contributes to`(2), `produces`/`positively correlated with`/`treats`(1 each). Sonnet used `positively regulates`(8), `decreases activity of`(5), `contributes to`(3), `causes`(2), `molecularly interacts with`/`in taxon`/`occurs in`(1 each). *(Note: these are legacy-vocabulary predicates — the same ones the Biolink-4.2.2 drift audit flagged. That's expected and correct: the eval is scored against the current pipeline/enum, not Biolink 4.2.2.)*

---

## 3. Evidence quality — the shared, gate-invisible weakness

**Layer 4 verifies a snippet is a verbatim substring of its cited PMID. It does NOT verify the snippet actually establishes the specific edge between its two specific nodes.** Both models exploit that gap — comparably:

- **Opus, P06 (Tamoxifen → Estrogen Receptor):** the `decreases activity of` edge is supported by a snippet that is literally about **endoxifen** — *"Endoxifen is a potent antiestrogen that binds and blocks estrogen receptor alpha…"* — the active metabolite, not tamoxifen (the edge's source node). Verbatim-valid, topically correct, but the entity in the snippet ≠ the entity on the edge. P06 also adds a **redundant `treats` shortcut** (Tamoxifen → Breast Neoplasms) backed by a **single case report** (*"the patient demonstrated clinical regression"*) — weak sourcing for a top-level claim.
- **Sonnet, P10 (Trastuzumab → HER2):** **two parallel edges** into HER2 (`molecularly interacts with` *and* `decreases activity of`) — mild over-modeling — and the `decreases activity of` edge is supported by **downstream** readouts (*"Trastuzumab partially decreased PI3K…"*, CHK-overexpression mimicry) rather than a direct HER2-activity measurement.

**These are the same class of issue — verbatim-valid evidence whose edge-level semantic precision is loose — and they appear once on each side. It is a property of the PubMed-only methodology + the gate's blind spot, not a model trait.** The <15-min human plausibility review exists precisely to catch this, and it must be done regardless of model.

**Sourcing-policy signal (model-independent):** both models lean on **primary experimental literature** for *canonical* mechanisms — Opus cited a *fly* and a *rat* study for "lisinopril inhibits ACE" (P03); both used many `IN_VITRO`/`MODEL_ORGANISM` sources (Opus 7 model-organism + 8 in-vitro of 30; Sonnet 11 in-vitro of 34). Yet every file's record-level `references:` block carries the **conservative secondary source** (DrugBank MoA + UniProt). So the outputs **straddle both evidence models** — record-level secondary assertion (legacy DrugMechDB style) + edge-level primary PubMed (new style). The edge-level primary-lit reliance is in tension with Su's conservative-sourcing steer. **This is the unresolved evidence-source policy showing up in real data — and it's a methodology decision, not a model difference.**

---

## 4. The dimensions that matter, weighted for *this* project

| Dimension | Opus 4.8 | Sonnet 4.6 | Edge | Weight for this project |
|---|---|---|---|---|
| **Accuracy — QC gate** | 100% | 100% | tie | **Low** (saturated, non-discriminating) |
| **Efficacy — mechanism quality** | strong; leaner, canonical | strong; richer, more edges to verify | **≈tie** (pending human review) | **Highest** — it's a gold-standard KB; quality is the product |
| **Cost** | baseline | **0.6× (−40%), deterministic** | **Sonnet** | **High at scale** (forwardfill = ~4,846 paths) |
| **Time** | **185 s/pair (~2× faster)** | 360 s/pair | **Opus** | **Low** (one-time, parallelizable) |
| **Effort / operational load** | **~30 tool calls; ½ the PubMed hits** | ~57 tool calls; 2× PubMed load | **Opus** | **Medium at scale** (NCBI rate-limit is the real bottleneck) |
| **Ontology hygiene** | 0 violations (no taxon nodes) | 0 violations; used canonical `NCBITaxon:` | tie | Medium |

**Cost is deterministic:** Sonnet 4.6 is priced at exactly **0.6×** Opus 4.8 on *both* input ($3 vs $5 /M) and output ($15 vs $25 /M). With token volume ≈equal, Sonnet costs ~40% less per pair **regardless of the input/output split**. Illustratively, at ~68k tokens/pair that's ≈$0.35–0.42 (Sonnet) vs ≈$0.55–0.70 (Opus) — over a full 4,846-path forwardfill, on the order of **~$1k saved** with Sonnet. Real but modest.

**The countervailing fact:** Sonnet's ~2× tool calls mean ~2× PubMed E-utilities load. At 4,846 paths that doubles the NCBI rate-limit pressure and roughly doubles wall-clock — the operational bottleneck of a bulk run is PubMed throughput, not model $.

---

## 5. What matters most (with the evidence)

For a **gold-standard KB**, the ranking is: **(1) mechanism quality/efficacy → (2) cost at scale → (3) operational load/throughput → (4) wall-clock.**

- **(1) is the highest weight and is ≈tied** on every deterministic proxy (pass rate, evidence density, prefix hygiene, support purity, PMID count) — and the one real quality risk (edge-evidence looseness, §3) is **shared and model-independent.** So quality does **not** currently favor either model; the human review is the deciding input and is still pending.
- **(2) favors Sonnet** (−40%, deterministic) and is decisive *only* at forwardfill scale.
- **(3)+(4) favor Opus** (~2× fewer tool calls / PubMed hits, ~2× faster).

**Therefore the model decision is genuinely close and reduces to:** *modest cost saving (Sonnet) vs. 2× operational efficiency + PubMed-load relief (Opus)*, with quality as a tiebreaker that the human review must supply.

---

## 6. Recommendation

**Finish the eval on Sonnet 4.6.** Reasons: (a) the efficiency penalty is immaterial at the ~17 remaining pairs (~$4 and a few extra minutes parallelized); (b) Sonnet is the front-runner for the *production* curator (cost at scale with comparable quality), so a Sonnet-heavy eval is a **more faithful predictor of production quality** — which is the eval's entire purpose; (c) it accumulates the human-review quality signal on the model we're most likely to deploy. *(The eval is already model-mixed, and the gate is model-robust, so this doesn't compromise the ≥80% number.)*

**For production / forwardfill at scale:** lean **Sonnet as the bulk workhorse + Opus reserved for retries and the hardest pairs** (the cost-optimal hybrid, mirroring Jayden's provider tiering), **and mitigate Sonnet's 2× PubMed load operationally** (NCBI API key + the committed cache + throttling). **Make this final only after the human plausibility review** — if that review finds Sonnet's longer paths meaningfully better or worse, it overrides the cost logic.

---

## 7. Caveats / still missing

- **The human <15-min plausibility review is not yet done** — it is the one input that can break the quality tie, and §3 shows exactly what it must scrutinize (edge-evidence semantic fit; redundant/shortcut edges; primary-vs-secondary sourcing).
- **n=5 per model.** Directional, not statistically tight. Finishing the remaining pairs (on Sonnet) enlarges the production-relevant sample.
- **The sourcing-policy tension is live in the data** (§3) and is a methodology decision for Su/Jayden, independent of model.
- **Cost $/pair is illustrative** (the 0.6× *ratio* is exact; the absolute depends on the in/out token split, which the run instrumentation didn't break out).
