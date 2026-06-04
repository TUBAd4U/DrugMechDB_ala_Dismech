---
provider: openai
model: gpt-5
drug: Acyclovir
disease: Herpes Simplex
query: 'Research the mechanism by which Acyclovir affects Herpes Simplex.


  Produce a markdown response with EXACTLY this structure:


  ## Proposed mechanism summary

  2–3 paragraphs describing the mechanistic pathway from Acyclovir to its effect

  on Herpes Simplex, with inline (PMID:XXXX) citations.


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
generated_at: '2026-06-02T20:12:13+00:00'
ttl_days: 30
candidate_pmids:
- PMID:214430
- PMID:202961
- PMID:6282196
- PMID:7192534
- PMID:6271750
- PMID:6285735
- PMID:2988429
- PMID:6256650
- PMID:6275127
- PMID:6270349
- PMID:6313600
- PMID:6264131
notes: input_tokens=57605, output_tokens=5728
---

## Proposed mechanism summary
Acyclovir is an acyclic guanosine analog that is selectively activated in herpes simplex virus (HSV)-infected cells when the viral thymidine kinase (TK; UL23) phosphorylates it to acyclovir monophosphate; host kinases then convert it to the active diphosphate and triphosphate forms. This virus-dependent first phosphorylation step drives selective accumulation of acyclovir triphosphate (ACV-TP) in infected cells and underlies the drug’s therapeutic index (PMID:214430; PMID:202961; PMID:6282196; PMID:7192534).

ACV-TP then targets the HSV DNA polymerase (UL30): it competes with dGTP as a substrate, is preferentially used by the viral enzyme over cellular polymerases, and when incorporated into nascent viral DNA, it terminates chain elongation due to the absence of a 3′-OH; polymerase stalling/dead‑end complex formation further suppresses viral DNA synthesis (PMID:6271750; PMID:6285735; PMID:2988429; PMID:7192534). Genetic studies reinforce this mechanism: resistance maps to loss/alteration of viral TK (reducing acyclovir activation) or to mutations in viral DNA polymerase that diminish ACV‑TP inhibition (PMID:6256650; PMID:6275127; PMID:6270349). Comprehensive biochemical reviews synthesize these findings, linking intracellular ACV‑TP levels and polymerase Ki values to antiviral efficacy (PMID:6313600).

## Candidate PMIDs
- PMID:214430 — Primary demonstration that HSV thymidine kinase phosphorylates acyclovir to its monophosphate, establishing selective activation in infected cells.
- PMID:6271750 — Shows ACV-TP competitively inhibits HSV DNA polymerase with high affinity versus dGTP; defines kinetic basis for selectivity.
- PMID:6285735 — Demonstrates inhibition of viral DNA chain elongation in HSV‑infected cells, consistent with chain termination by incorporated ACV.
- PMID:202961 — Early report defining selective anti‑HSV activity and greater inhibition of viral than cellular polymerases by acyclovir/its triphosphate.
- PMID:7192534 — Compares inhibition of cellular and herpesvirus DNA polymerases by ACV‑TP, supporting preferential targeting of viral polymerases.
- PMID:6282196 — Documents metabolism in infected vs. uninfected cells and persistence/accumulation of ACV‑TP in HSV‑infected cells.
- PMID:6275127 — Identifies ACV‑resistant HSV‑1 mutants with altered DNA polymerase or reduced ACV‑phosphorylating activity, validating TK and Pol as targets.
- PMID:6256650 — Shows altered substrate specificity of HSV TK confers acyclovir resistance, underscoring the requirement for viral TK–mediated activation.
- PMID:2988429 — Dual‑inhibitor studies elucidating ACV‑TP interaction with HSV DNA polymerase, supporting a mechanistic inhibition model.
- PMID:6270349 — Physical mapping links DNA polymerase locus mutations to altered inhibitor sensitivity, reinforcing the polymerase target of ACV‑TP.
- PMID:6313600 — Review summarizing biochemical mechanism: TK‑dependent activation, ACV‑TP levels, and polymerase inhibition predict antiviral effect.
- PMID:6264131 — Shows phosphorylation of acyclovir to mono/di/tri‑phosphates in herpesvirus‑infected lymphoblastoid cells, illustrating required metabolic activation.

## Mechanism graph proposal (advisory)
Acyclovir → Acyclovir monophosphate → Acyclovir triphosphate → HSV DNA polymerase → Viral DNA synthesis → Herpes simplex infection

- Acyclovir → Acyclovir monophosphate [positively regulated by (requires) viral thymidine kinase]
- Acyclovir monophosphate → Acyclovir triphosphate [positively regulated by host kinases]
- Acyclovir triphosphate → HSV DNA polymerase [decreases activity of]
- HSV DNA polymerase → Viral DNA synthesis [decreases rate of (chain termination/stalling)]
- Viral DNA synthesis → Herpes simplex infection [decreases propagation of]
