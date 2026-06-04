---
provider: openai
model: gpt-5
drug: Infliximab
disease: Crohn's Disease
query: 'Research the mechanism by which Infliximab affects Crohn''s Disease.


  Produce a markdown response with EXACTLY this structure:


  ## Proposed mechanism summary

  2–3 paragraphs describing the mechanistic pathway from Infliximab to its effect

  on Crohn''s Disease, with inline (PMID:XXXX) citations.


  ## Candidate PMIDs

  Bulleted list, 5–15 PMIDs ordered by relevance:

  - PMID:XXXXXXXX — One-sentence relevance note.

  - ...


  Only include PMIDs you verified exist via web search.


  ## Mechanism graph proposal (advisory)

  Drug → intermediate1 → intermediate2 → ... → Disease


  Each arrow labeled with a Biolink-style predicate (e.g., "decreases activity

  of", "positively regulates", "contributes to"). This topology is advisory —

  the curation agent will validate it.


  Output ONLY the markdown body. No preamble or closing remarks.

  '
generated_at: '2026-06-02T20:12:45+00:00'
ttl_days: 30
candidate_pmids:
- PMID:7640345
- PMID:19188093
- PMID:15685549
- PMID:11284774
- PMID:11788561
- PMID:14684579
- PMID:12806611
- PMID:21875498
- PMID:17013447
- PMID:16307694
- PMID:11673664
- PMID:9321530
notes: input_tokens=71350, output_tokens=7160
---

## Proposed mechanism summary
Infliximab is a chimeric IgG1 monoclonal antibody that binds both soluble and transmembrane TNF-α, preventing TNF from engaging TNFR1/TNFR2 and thereby dampening downstream NF-κB–driven inflammatory programs in the gut. It also engages Fc-dependent effector mechanisms and, when bound to transmembrane TNF, can trigger “reverse signaling” in the TNF-expressing cell, promoting anti-inflammatory outputs such as IL-10 and cell-cycle arrest/apoptosis (PMID:7640345; PMID:19188093; PMID:15685549). In Crohn’s mucosa, infliximab’s local immunomodulation includes reduced Th1/Th17-type cytokine production by lamina propria mononuclear cells without generalized systemic immunosuppression (PMID:11284774).

A central therapeutic effect in Crohn’s disease is the rapid induction of apoptosis in pathogenic mucosal immune cells. Infliximab increases apoptosis of lamina propria CD3+ T cells in vivo and reverses the characteristic defect in mucosal T‑cell death via a caspase-dependent pathway; importantly, this apoptosis is seen with infliximab but not with the soluble TNF receptor etanercept, highlighting a transmembrane TNF–dependent mechanism (PMID:11788561; PMID:14684579; PMID:12806611). Anti‑TNF antibodies also dismantle a tnTNF→TNFR2 survival axis delivered by intestinal CD14+ macrophages to T cells, thereby restoring activation‑induced T‑cell apoptosis; collectively these actions reduce activated mucosal lymphocytes/macrophages, downshift proinflammatory cytokines/adhesion molecules, and promote mucosal healing (PMID:21875498; PMID:17013447; PMID:16307694).

## Candidate PMIDs
- PMID:12806611 — Infliximab, but not etanercept, binds lymphocytes and induces apoptosis of lamina propria T cells from Crohn’s patients (mechanistic class difference).
- PMID:11788561 — In vivo study showing rapid, specific increase of apoptotic mucosal T lymphocytes after infliximab in Crohn’s disease.
- PMID:14684579 — Demonstrates sustained reversal of defective mucosal T‑cell death by infliximab via a caspase‑dependent pathway.
- PMID:15685549 — Shows infliximab induces outside‑to‑inside (reverse) signaling through transmembrane TNF, driving IL‑10 production, cell‑cycle arrest, and apoptosis.
- PMID:21875498 — Anti‑TNF antibodies induce T‑cell apoptosis via TNFR2, mediated by intestinal CD14+ macrophages in IBD patients.
- PMID:7640345 — cA2 (infliximab) binds transmembrane TNF and can activate immune effector functions, supporting membrane‑targeted mechanisms.
- PMID:19188093 — Comparative biophysics showing anti‑TNF mAbs (including infliximab) can mediate complement/ADCC against mTNF‑expressing cells.
- PMID:11284774 — In Crohn’s patients, infliximab decreases Th1 cytokine production in lamina propria cells with minimal systemic immunosuppression.
- PMID:17013447 — Reports reduction of activated mucosal lymphocytes following infliximab therapy in Crohn’s disease.
- PMID:16307694 — Correlates sustained mucosal healing on infliximab with reductions in macrophages (CD68) and mucosal TNF expression.
- PMID:11673664 — In vivo removal of TNF‑α–producing cells in Crohn’s disease after cA2 (infliximab) administration.
- PMID:9321530 — Landmark randomized trial establishing clinical efficacy of anti‑TNF (cA2/infliximab) in Crohn’s disease (context for target validity).

## Mechanism graph proposal (advisory)
Infliximab → decreases activity of → TNF-α (soluble and transmembrane) → negatively regulates → TNFR1/TNFR2–NF-κB signaling in intestinal immune cells → increases → apoptosis of activated lamina propria T cells and macrophages → decreases → mucosal proinflammatory cytokines/adhesion molecules and leukocyte recruitment → ameliorates → Crohn’s disease
