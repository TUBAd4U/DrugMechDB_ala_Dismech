---
provider: openai
model: gpt-5
drug: Fluoxetine
disease: Major Depressive Disorder
query: 'Research the mechanism by which Fluoxetine affects Major Depressive Disorder.


  Produce a markdown response with EXACTLY this structure:


  ## Proposed mechanism summary

  2–3 paragraphs describing the mechanistic pathway from Fluoxetine to its effect

  on Major Depressive Disorder, with inline (PMID:XXXX) citations.


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
generated_at: '2026-06-02T20:12:22+00:00'
ttl_days: 30
candidate_pmids:
- PMID:2200429
- PMID:7685386
- PMID:7901377
- PMID:15121647
- PMID:11354013
- PMID:8930214
- PMID:11877317
- PMID:11106871
- PMID:19439074
- PMID:18977602
- PMID:12907793
- PMID:3312176
- PMID:23374637
notes: input_tokens=47573, output_tokens=6031
---

## Proposed mechanism summary
Fluoxetine is a selective serotonin reuptake inhibitor that binds the serotonin transporter (SERT) and blocks 5‑HT reuptake, acutely elevating extracellular serotonin in forebrain regions; this has been demonstrated by in vitro SERT inhibition and in vivo microdialysis, and by human PET studies showing substantial SERT occupancy at clinical doses (PMID:2200429; PMID:7685386; PMID:7901377; PMID:15121647). The early rise in synaptic 5‑HT activates somatodendritic 5‑HT1A autoreceptors in the dorsal raphe and transiently suppresses serotonergic neuron firing, although postsynaptic 5‑HT1A signaling in hippocampus can still be engaged (PMID:11354013).

With chronic dosing, 5‑HT1A autoreceptors in raphe neurons desensitize/uncouple from Gi/Go proteins, relieving autoinhibition, restoring (and effectively increasing) serotonergic firing and sustaining higher 5‑HT output to limbic and cortical targets (PMID:8930214; PMID:11877317; PMID:11106871). Downstream, prolonged SSRI exposure enhances neuroplasticity programs, including increased hippocampal BDNF signaling and synaptic protein expression, and promotes adult hippocampal neurogenesis; critically, hippocampal neurogenesis is required for the behavioral effects of chronic fluoxetine in rodent models, linking these adaptations to antidepressant efficacy observed in major depressive disorder (PMID:19439074; PMID:18977602; PMID:12907793; PMID:3312176).

## Candidate PMIDs
- PMID:2200429 — Establishes that fluoxetine and its enantiomers are potent, selective inhibitors of the serotonin transporter (SERT).
- PMID:7685386 — In vivo microdialysis shows fluoxetine acutely increases extracellular serotonin in rat forebrain.
- PMID:7901377 — Demonstrates a 3–4× increase in extracellular hypothalamic serotonin after fluoxetine, augmented by 5‑HTP.
- PMID:15121647 — Human [11C]DASB PET quantifies SERT occupancy across five SSRIs, including fluoxetine, at clinical doses.
- PMID:11354013 — Electrophysiology/neurochemistry indicate that despite acute raphe firing suppression, postsynaptic 5‑HT1A signaling remains activated by fluoxetine.
- PMID:8930214 — Chronic fluoxetine reduces hypothalamic/midbrain Gi/Go and neuroendocrine responses to a 5‑HT1A agonist, evidencing 5‑HT1A autoreceptor desensitization.
- PMID:11877317 — [35S]-GTPγS autoradiography shows chronic fluoxetine uncouples raphe 5‑HT1A autoreceptors without changing receptor density.
- PMID:11106871 — Low-dose chronic fluoxetine desensitizes dorsal raphe 5‑HT1A autoreceptors; effect is prevented by the 5‑HT1A antagonist WAY‑100635.
- PMID:19439074 — Fluoxetine increases mature BDNF protein in hippocampus early during treatment in rodents.
- PMID:18977602 — Chronic fluoxetine increases hippocampal synaptic proteins via TrkB/BDNF signaling.
- PMID:12907793 — Shows hippocampal neurogenesis is required for the behavioral effects of chronic antidepressants, including fluoxetine.
- PMID:23374637 — In MDD, SSRI treatment reduces raphe 5‑HT1A autoreceptor binding by PET, consistent with autoreceptor downregulation.
- PMID:3312176 — Double-blind, placebo-controlled trial demonstrating fluoxetine efficacy in outpatients with major depression.

## Mechanism graph proposal (advisory)
Fluoxetine → serotonin transporter (SERT) → synaptic serotonin (5‑HT) → 5‑HT1A autoreceptor signaling (dorsal raphe) → firing of serotonergic neurons → postsynaptic 5‑HT transmission (hippocampus/cortex) → BDNF/TrkB signaling and adult hippocampal neurogenesis → Major Depressive Disorder
- decreases activity of → 
- decreases clearance of →
- increases level of →
- negatively regulates (acutely); chronic fluoxetine decreases activity of →
- positively regulates →
- positively regulates →
- increases rate of / positively regulates →
- contributes to amelioration of →
