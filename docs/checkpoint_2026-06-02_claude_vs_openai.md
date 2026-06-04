# Checkpoint — Claude vs OpenAI as DrugMechDB research providers

**Date:** 2026-06-02
**Author:** Curation session (run by jdl016@ucsd.edu)
**Raw metrics:** [checkpoint_metrics.json](checkpoint_metrics.json)
**Plan reference:** Conversation message preceding this report

## TL;DR

On a 5-pair stratified sample comparing the `claude` and `openai` research providers (the dossier-generation step that seeds `/curate using <provider>`):

- **Both providers refused to fabricate PMIDs** (0 hallucinated identifiers across 117 PMID slots, 109 unique).
- **OpenAI is ~17× cheaper** ($0.15 vs $2.48 per pair) and produces marginally higher PMID-usability (98% vs 95%, both excellent).
- **Claude is ~2.5× faster** (~59s vs ~151s per pair, wall clock).
- **OpenAI is more disciplined on format** (5/5 dossiers had all three required sections and zero preamble bleed; Claude leaked meta-commentary in 3/5 dossiers).
- **Mechanism correctness is comparable** on canonical mechanisms (both correctly cite Druker NEJM for imatinib, ISIS-2 for aspirin, Targan NEJM for infliximab when reaching for landmark trials).
- **Citation overlap is low** (per-pair Jaccard 0.0–0.28, mean 0.10) — the two providers reach largely disjoint literature for the same query. This means **using both as an ensemble would broaden coverage substantially** (109 unique PMIDs from 5 pairs vs ~57 from either alone).

**Recommendation:** Default to OpenAI for the remaining 28 eval pairs and the backfill workstream. Use Claude as a second-opinion provider for pairs where OpenAI produces fewer than 8 candidate PMIDs or when first-pass QC fails. Implement perplexity (next-cheapest stub, ~$0.005/query estimated) as a third provider before the full backfill begins.

This is a directional finding from n=5. The Phase-3 30-pair eval will provide the formal pass-rate evidence.

---

## 1. Study design

### Test cases (stratified across 5 of 6 eval drug classes)

| ID | Drug / Disease | Class | In-corpus? | Mechanism archetype |
|---|---|---|---|---|
| P01 | Aspirin / Myocardial Infarction | cardiovascular | yes | Irreversible enzyme inhibitor (COX-1 acetylation) |
| P07 | Imatinib / Chronic Myeloid Leukemia | oncology | yes | Targeted kinase inhibitor (BCR-ABL) |
| P15 | Acyclovir / Herpes Simplex | antimicrobial | no | Antiviral nucleoside analog |
| P17 | Fluoxetine / Major Depressive Disorder | cns | no | Reuptake inhibitor (SERT) |
| P22 | Infliximab / Crohn's Disease | immunomodulator | yes | Monoclonal antibody (anti-TNF-α) |

### Provider configurations

| Provider | Model | API | Web tool | `max_output_tokens` | `max_uses` |
|---|---|---|---|---|---|
| `claude` | `claude-opus-4-5` | Messages | `web_search_20250305` | 4096 (output never approached cap) | 8 |
| `openai` | `gpt-5` | Responses | `web_search` (built-in) | 16000 (after P01 retry; see §6 Caveats) | n/a (single agentic loop) |

System prompt and user prompt template are **byte-identical** across providers (defined in [scripts/research_providers/claude.py](../scripts/research_providers/claude.py) and [scripts/research_providers/openai.py](../scripts/research_providers/openai.py)). Any quality delta is therefore attributable to model/provider behavior, not prompt design.

### Pricing assumptions for cost calculation

| Provider | Input $/M tokens | Output $/M tokens |
|---|---|---|
| Claude (Opus 4.5) | $15.00 | $75.00 |
| OpenAI (GPT-5) | $1.25 | $10.00 |

### Metrics

Per dossier: PMID count, PMID usability (resolves in PubMed *and* has an abstract — usable as Layer-4 evidence per the verbatim-snippet contract), PMID fabrication (no PubMed record), token usage, dollar cost, body word count, format adherence (3 required sections present? preamble bleed?). Per pair: PMID overlap (Jaccard) between providers.

Qualitative: mechanism correctness, citation centrality (do they cite the landmark trial / structural paper for the mechanism?), specificity vs vagueness, primary-vs-review mix. Scored by reading each dossier directly; n=5 means I do not claim statistical certainty on the qualitative dimensions.

---

## 2. Aggregate results

### Headline metrics

| Metric | Claude | OpenAI | Delta |
|---|---:|---:|---|
| **Pairs evaluated** | 5 | 5 | — |
| **Total candidate PMIDs proposed** | 57 | 60 | OpenAI +5% |
| **PMIDs resolvable + abstract available** | 54 (94.7%) | 59 (98.3%) | OpenAI +3.6 pp |
| **Real PMIDs but no abstract** | 3 (5.3%) | 1 (1.7%) | OpenAI better |
| **Fabricated PMIDs** | **0** | **0** | tied (both clean) |
| **Total input tokens** | 775,912 | 322,342 | Claude 2.4× more |
| **Total output tokens** | 10,399 | 32,818 | OpenAI 3.2× more |
| **Total cost (5 pairs)** | $12.42 | $0.73 | **Claude 17× more expensive** |
| **Mean cost per pair** | $2.48 | $0.15 | — |
| **Mean wall-clock per pair** | ~59 s | ~151 s | **Claude 2.5× faster** |
| **Dossiers with all 3 required sections** | 5/5 | 5/5 | tied |
| **Dossiers with preamble bleed** | 3/5 | 0/5 | OpenAI better |
| **Mean body word count** | 658 | 484 | Claude 36% longer |

### What the input/output ratio says about each provider's tool use

Claude consumed **76 input tokens for every 1 output token** (775K in / 10K out); OpenAI consumed **10:1** (322K in / 33K out). This reflects different search behaviors:

- Claude's `web_search_20250305` includes the full search-result page content in its context window for every search call (×8 max). It treats search results as raw context and then writes a relatively short summary.
- OpenAI's Responses-API `web_search` appears to compress search results before passing them to the model context, then writes longer summaries that include source URL tracking. This is also why OpenAI's PMID entries often include `pubmed.ncbi.nlm.nih.gov/.../?utm_source=openai` reference links.

This explains both the cost gap (Claude's bulk is in expensive input tokens) and the speed gap (OpenAI does more model output generation per call).

### Per-pair PMID overlap

| Pair | Claude PMIDs | OpenAI PMIDs | Shared | Union | Jaccard |
|---|---:|---:|---:|---:|---:|
| P01 Aspirin / MI | 12 | 12 | 1 (PMID:2899772 ISIS-2) | 23 | 0.043 |
| P07 Imatinib / CML | 13 | 11 | 1 (PMID:11287972 Druker NEJM) | 23 | 0.043 |
| P15 Acyclovir / Herpes | 11 | 12 | 3 | 20 | 0.150 |
| P17 Fluoxetine / MDD | 10 | 13 | 0 | 23 | **0.000** |
| P22 Infliximab / Crohn's | 11 | 12 | 5 | 18 | 0.278 |
| **Total / mean** | 57 | 60 | 10 | 107 (109 unique across study) | **~0.10** |

Mean Jaccard ≈ 0.10 — the providers reach almost entirely disjoint literature for the same query. Even on the well-trodden imatinib/CML pair, only one PMID (the Druker NEJM trial) appears in both lists.

This has a strategic implication: **running both providers in parallel doubles citation coverage at only ~7% additional cost** (since OpenAI is so cheap, $2.48 + $0.15 = $2.63 vs $2.48 alone, +6%). The 30-pair eval could pay for this ensemble.

### Provider quality patterns (qualitative)

From reading all 10 dossiers, the **stylistic differences are sharper than the correctness differences**:

| Dimension | Claude pattern | OpenAI pattern |
|---|---|---|
| **Narrative structure** | Many short paragraphs, often with a single sentence quoted from a source | Dense multi-clause paragraphs with inline PMID citations grouped semantically |
| **Citation density per paragraph** | 1–2 PMIDs | 3–6 PMIDs |
| **Source attribution style** | Plain text mentions | Embedded URLs (`pubmed.ncbi.nlm.nih.gov/.../?utm_source=openai`) — useful for verification but adds noise |
| **Mechanism specificity** | High; tends to elaborate intermediate steps | High; tends to include molecular-detail biomarkers (e.g., DFG-out conformation, Tyr177 GRB2 binding) |
| **Mechanism graph format** | ASCII tree with explicit predicates on each arrow | Single line with predicates listed below |
| **Preamble bleed** | Common (3/5): meta-commentary leaks at top of body | None observed |
| **Landmark citation hit rate** (subjective) | Hits Druker imatinib, Targan infliximab; misses ISIS-2 wasn't in claude P01 originally, but generally good | Hits ISIS-2, Druker imatinib, Targan infliximab, Wong fluoxetine, Santarelli neurogenesis; tends to also include structural-biology and PET-imaging papers |
| **Topology depth** | Often deeper (claude P17 graph has 8 levels) | Often more compressed (openai P17 graph is 7 levels in one line) |

**Notable observations from specific pairs:**

- **P01 Aspirin/MI:** Claude reached the landmark ISIS-2 trial (PMID:2899772) immediately and built around it. OpenAI v1 (truncated, 4096-token cap) missed ISIS-2; OpenAI v2 (16000-token cap) recovered it. This is a fairness caveat for the P01 PMID-set comparison.
- **P07 Imatinib/CML:** Both cite the Druker NEJM landmark. OpenAI uniquely cites the structural biology paper (PMID:10988075) for ATP-pocket binding mechanism. Claude uniquely cites the Gorre resistance paper (PMID:11423618).
- **P15 Acyclovir/Herpes:** Both providers heavily cite Schaeffer-era foundational acyclovir mechanism papers from 1977–1985 (PMID:217531, 6256650, 7192534, etc.). Highest PMID overlap of any pair (3). OpenAI uniquely flags PMID:214430 (no abstract — unusable). Claude uniquely flags PMID:6102421 (no abstract).
- **P17 Fluoxetine/MDD:** Most divergent pair (Jaccard 0.000). Claude's mechanism centers on SERT → 5-HT → CREB → BDNF → neurogenesis (correct but textbook). **OpenAI's mechanism is more sophisticated:** distinguishes acute (5-HT1A autoreceptor activation, transient firing suppression) from chronic (autoreceptor desensitization, BDNF/neurogenesis) effects. Cites the Santarelli neurogenesis-required paper (PMID:12907793) and human PET DASB SERT-occupancy work (PMID:15121647). OpenAI wins on this pair.
- **P22 Infliximab/Crohn's:** Highest overlap (Jaccard 0.278, 5 shared PMIDs). Both cover the dual mechanism (TNF-α neutralization + mTNF reverse signaling → apoptosis). OpenAI uniquely cites the TNFR2/CD14+ macrophage survival axis (PMID:21875498), a more recent mechanistic refinement.

---

## 3. Cost vs quality tradeoff

At 30 pairs (the full Phase 3 eval) and an estimated 4,846 paths for backfill:

| Scenario | Claude only | OpenAI only | Both (ensemble) |
|---|---:|---:|---:|
| 30-pair eval (estimated) | ~$74 | ~$4.40 | ~$78 |
| 4,846-path backfill (rough estimate) | **~$12,000** | **~$710** | ~$12,700 |
| Mean PMIDs proposed per pair (5-case study) | 11.4 | 12.0 | ~22 (union, with overlap) |
| Mean PMIDs usable per pair | 10.8 | 11.8 | ~21 |
| Mean format compliance | partial (3/5 preamble bleed) | full (5/5 clean) | n/a |

**The cost gap is not negligible at scale.** A claude-only backfill would cost ~$12K in API charges. An openai-only backfill is in the hundreds. An ensemble approach is dominated by Claude's cost regardless.

---

## 4. Recommendation

**Phase 3 eval (next 28 pairs): default to OpenAI.** Reasoning:

1. Same zero-fabrication rate as Claude (the main risk we were guarding against by adding the verbatim-snippet contract).
2. Higher PMID usability rate (98% vs 95%).
3. Better format discipline (no preamble bleed → less curator cleanup downstream).
4. Comparable mechanism correctness on canonical mechanisms; on P17 (the one pair where they diverged on substance) OpenAI's narrative was sharper.
5. Cost reduction of ~17×.

**Use Claude as a second-opinion provider** when the OpenAI dossier returns fewer than 8 PMIDs (we saw none below 11 in this study, but a low-N pair would warrant ensemble), or when the first-pass `/curate` run fails QC and the curation agent needs a broader PMID pool to draft against.

**Cost-aware backfill strategy.** For the 4,846-path backfill workstream (PRD §5.2), the cost gap between Claude and OpenAI ($12K vs $0.7K) is the dominant economic consideration. Recommend:
- Tier-A paths (high-impact, top citations): OpenAI primary, Claude second-opinion for any path where OpenAI's PMID count <8 or first-pass QC fails. Estimated cost: ~$100–200.
- Tier-B and Tier-C paths: OpenAI only. Estimated cost: ~$600.
- Total backfill provider cost: under $1K. Compare to ~$12K for Claude-only.

**Implement the perplexity stub before backfill launch.** The perplexity stub (cost estimated ~$0.005/query per the implementation plan in [scripts/research_providers/perplexity.py](../scripts/research_providers/perplexity.py)) would be ~30× cheaper than OpenAI again, and would provide a third independent literature search vector. Total potential ensemble cost for backfill: under $1.5K with three providers.

**Re-evaluate after the 30-pair eval.** With n=30 we'll have meaningful statistics on first-pass QC pass rate per provider, which is the real product gate. n=5 here only tells us about the dossier-level inputs.

---

## 5. Per-pair detail

Each section: provider | PMID count (usable) | input/output tokens | cost | wall clock | notable.

### P01 — Aspirin / Myocardial Infarction (cardiovascular, in-corpus)

| | Claude | OpenAI (v2) |
|---|---|---|
| PMIDs | 12 (10 usable, 2 no-abstract: 26408390, 8145785) | 12 (12 usable) |
| Tokens (in/out) | 144,497 / 1,938 | 41,011 / 5,656 |
| Cost | $2.31 | $0.11 |
| Wall clock | ~80s | ~117s |
| Landmark hits | ISIS-2 (2899772), Fitzgerald canine model (2500270), COX acetylation proteomics (32535107) | ISIS-2 (2899772), early COX-1 acetylation work (1159076, 413839), PGI2/TXA2 selectivity (105363) |
| Shared PMID | PMID:2899772 (ISIS-2) | PMID:2899772 (ISIS-2) |
| Note | OpenAI v1 was truncated at 4096 max_output_tokens, missed ISIS-2; v2 at 16000 recovered it. PMID set above is v2. |

### P07 — Imatinib / Chronic Myeloid Leukemia (oncology, in-corpus)

| | Claude | OpenAI |
|---|---|---|
| PMIDs | 13 (13 usable) | 11 (11 usable) |
| Tokens (in/out) | 199,802 / 2,025 | 104,803 / 8,243 |
| Cost | $3.15 | $0.21 |
| Wall clock | ~58s | ~237s (slowest run of the study) |
| Landmark hits | Druker NEJM (11287972), Gorre resistance (11423618), Deininger review (15618470) | Druker NEJM (11287972), Schindler ABL-imatinib structure (10988075), Sattler GRB2-Tyr177 (8402896), Sillaber STAT5-BCL-XL (10727459) |
| Shared PMID | PMID:11287972 (Druker NEJM) | PMID:11287972 |
| Note | OpenAI's PMID set leans more heavily on foundational biochemistry/structural biology; Claude leans on clinical translation. |

### P15 — Acyclovir / Herpes Simplex (antimicrobial, net-new)

| | Claude | OpenAI |
|---|---|---|
| PMIDs | 11 (10 usable, 1 no-abstract: 6102421) | 12 (11 usable, 1 no-abstract: 214430) |
| Tokens (in/out) | 146,919 / 1,818 | 57,605 / 5,728 |
| Cost | $2.34 | $0.13 |
| Wall clock | ~47s | ~134s |
| Landmark hits | Both: Elion-era foundational papers on viral thymidine kinase phosphorylation + DNA polymerase chain termination (PMID:217531, 6256650, 7192534) | Same foundational set + uniquely PMID:6282196, 6285735, 2988429, 6275127 |
| Shared PMIDs | 3 (PMID:7192534, 6271750, 6256650) | 3 |
| Note | Highest overlap among the 5 pairs; both providers found the canonical 1977–1985 mechanism papers. |

### P17 — Fluoxetine / Major Depressive Disorder (cns, net-new)

| | Claude | OpenAI |
|---|---|---|
| PMIDs | 10 (10 usable) | 13 (13 usable) |
| Tokens (in/out) | 146,363 / 2,304 | 47,573 / 6,031 |
| Cost | $2.37 | $0.12 |
| Wall clock | ~52s | ~141s |
| Landmark hits | Wong 2005 retrospective (16121130), Wong 1995 20-year review (7623609), BDNF chronic-fluoxetine work (16035958) | Santarelli neurogenesis-required (12907793), Wong placebo-controlled trial (3312176), Meyer DASB PET SERT occupancy (15121647), Blier-era autoreceptor desensitization (8930214, 11877317, 11106871) |
| Shared PMIDs | **0** | **0** — most divergent pair |
| Note | Most striking content difference of the study. OpenAI distinguishes acute (5-HT1A autoreceptor) vs chronic (desensitization, BDNF, neurogenesis) effects; Claude treats the mechanism more textbook-linear. **OpenAI wins this pair on qualitative depth.** |

### P22 — Infliximab / Crohn's Disease (immunomodulator, in-corpus)

| | Claude | OpenAI |
|---|---|---|
| PMIDs | 11 (11 usable) | 12 (12 usable) |
| Tokens (in/out) | 138,331 / 2,314 | 71,350 / 7,160 |
| Cost | $2.25 | $0.16 |
| Wall clock | ~58s | ~162s |
| Landmark hits | Targan 1997 NEJM (9321530), ten Hove apoptosis in vivo (11788561), van den Brande infliximab-vs-etanercept (12806611), Mitoma reverse signaling (15685549) | Same Targan, ten Hove, van den Brande, Mitoma — plus TNFR2-CD14+ axis (21875498), comparative biophysics (19188093) |
| Shared PMIDs | **5** (highest of the study: 9321530, 11788561, 12806611, 14684579, 15685549) | 5 |
| Note | Most agreement of any pair. Both providers reach the same canonical mTNF-reverse-signaling literature. OpenAI adds more recent TNFR2 mechanistic refinements. |

---

## 6. Caveats and limitations

1. **n=5 is small.** Effect sizes reported here have wide confidence intervals; treat as directional. The 30-pair eval will provide proper statistics.
2. **OpenAI P01 was re-run** at 16000 max_output_tokens after an initial truncation at 4096. Output v1 had only 7 PMIDs (truncated mid-narrative, missed ISIS-2); output v2 had 12 PMIDs including ISIS-2. The metrics in this report use v2. This is a fairness adjustment; raw timing/cost for OpenAI P01 includes only v2.
3. **Cost estimates use list pricing.** Claude Opus 4.5 was used; current production deployment would likely upgrade to Opus 4.7 (per the [handoff doc](handoff_2026-06-02.md) §3 Step 5), which has different pricing. OpenAI GPT-5 pricing is a recent-best-estimate; the public price table may have moved.
4. **Wall-clock measurements** include background-process scheduling overhead from the parallel runner. Individual-call latency would be slightly faster for both providers.
5. **Dossier quality ≠ curation quality.** This study compares the *input* to the `/curate` workflow, not the output. A high-quality dossier with usable PMIDs makes curation easier, but the curation agent (Claude in Claude Code) is the one drafting the final YAML. Phase 3's first-pass QC rate is the real product metric.
6. **No qualitative blinding.** I scored the qualitative dimensions by reading dossiers in this session; provider identity was visible. The pattern of OpenAI being more disciplined / Claude being more verbose is robust enough across pairs that I'm reasonably confident, but a blinded scoring would be more rigorous.
7. **The PMID overlap analysis treats the two providers as independent search agents.** They share underlying training data overlap with PubMed, so "independent" is loose. Still, the empirical Jaccard ≈ 0.10 is striking.
8. **One re-run for fairness** (OpenAI P01) cost ~$0.10 and is included in the OpenAI total ($0.73). Earlier P01 v1 attempt cost is not double-counted.

---

## 7. Reproducibility

To reproduce on a fresh machine:

```bash
cd /Users/jaydenlee/Downloads/su_lab/DrugMechDB

# Pre-conditions
export ANTHROPIC_API_KEY=sk-...
export OPENAI_API_KEY=sk-proj-...

# Generate the 10 dossiers (claude has TTL cache; openai needs --force on re-runs)
for pair in "Aspirin|Myocardial Infarction" "Imatinib|Chronic Myeloid Leukemia" \
            "Acyclovir|Herpes Simplex" "Fluoxetine|Major Depressive Disorder" \
            "Infliximab|Crohn's Disease"; do
  drug="${pair%|*}"; disease="${pair#*|}"
  for provider in claude openai; do
    .venv-py310/bin/python scripts/research.py run "$provider" "$drug" "$disease"
  done
done

# Verify all PMIDs against PubMed
.venv-py310/bin/python -c "
import yaml, glob
pmids = set()
for f in glob.glob('research/*-claude.md') + glob.glob('research/*-openai.md'):
    fm = yaml.safe_load(open(f).read().split('---')[1])
    pmids.update(fm.get('candidate_pmids', []))
print(' '.join(sorted(pmids)))
" | xargs .venv-py310/bin/python scripts/pubmed_fetch.py fetch

# Rebuild metrics + summary
.venv-py310/bin/python /tmp/build_checkpoint_metrics.py
```

Raw dossiers are committed to git at `research/*-claude.md` and `research/*-openai.md`. Cached PubMed abstracts (committed for deterministic CI) at `references_cache/PMID_*.md`.

---

*End of report. See [checkpoint_metrics.json](checkpoint_metrics.json) for the machine-readable raw metrics.*
