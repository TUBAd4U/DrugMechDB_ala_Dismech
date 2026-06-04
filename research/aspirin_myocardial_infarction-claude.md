---
provider: claude
model: claude-opus-4-5
drug: Aspirin
disease: Myocardial Infarction
query: 'Research the mechanism by which Aspirin affects Myocardial Infarction.


  Produce a markdown response with EXACTLY this structure:


  ## Proposed mechanism summary

  2–3 paragraphs describing the mechanistic pathway from Aspirin to its effect

  on Myocardial Infarction, with inline (PMID:XXXX) citations.


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
generated_at: '2026-05-19T20:34:41+00:00'
ttl_days: 30
candidate_pmids:
- PMID:23422285
- PMID:26408390
- PMID:7002350
- PMID:2500270
- PMID:2899772
- PMID:9563981
- PMID:8145785
- PMID:725852
- PMID:16359516
- PMID:18752570
- PMID:32535107
- PMID:18574266
notes: input_tokens=144497, output_tokens=1938
---

Now let me search for specific PMIDs on aspirin's mechanism in myocardial infarction prevention:

I now have sufficient information to write the mechanism summary. Let me compile the verified PMIDs and create the response.

## Proposed mechanism summary

Aspirin (acetylsalicylic acid) treats and prevents myocardial infarction through irreversible inhibition of platelet cyclooxygenase-1 (COX-1).

Aspirin irreversibly inactivates cyclooxygenase (COX)-1 and suppresses the generation of prostaglandin H2 (a precursor of thromboxane A2). Aspirin achieves this effect through its acetyl group, which becomes covalently attached to Ser529 of the active site of the COX-1 enzyme, blocking the access of arachidonic acid to the hydrophobic channel.

It acetylates Ser529 residue in cyclooxygenase-1 (COX-1) and prevents thromboxane A2 (TXA2) formation from arachidonic acid (AA) in platelets.

The change is due to irreversible inhibition of platelet COX-1, so that aspirin's antiplatelet effect lasts 8-10 days (the life of the platelet).

(PMID:23422285, PMID:26408390)

Thromboxane A2 (TXA2) is a potent mediator of platelet aggregation and vasoconstriction that plays a critical role in arterial thrombosis.

Thromboxane A2 (TxA2) could be one of the precipitating factors in coronary or cerebrovascular ischemia because it is a potent vasoconstrictor that is produced by platelets during their aggregation.

Platelet activation is markedly increased during coronary thrombolysis and limits the response to thrombolytic therapy. A possible mediator of platelet activation in this setting is thromboxane (TX) A2, a potent platelet agonist formed in greatly increased amounts during coronary thrombolysis.

By inhibiting TXA2 synthesis, aspirin prevents platelet aggregation and subsequent coronary artery thrombosis, the primary pathophysiological mechanism underlying acute myocardial infarction (PMID:7002350, PMID:2500270).

The clinical efficacy of this mechanism has been definitively established in large randomized trials.

Published in 1988, ISIS-2 was the first trial to demonstrate the clinical efficacy of the antiplatelet agent aspirin in reducing vascular mortality in acute MI. Among patients with acute MI, aspirin and streptokinase reduced 5-week vascular mortality by 20% and 23%, respectively, when compared to placebo. The combination of aspirin and streptokinase reduced the same outcome by 40%.

ISIS-2 also showed that the benefits of early treatment with aspirin were largely independent of, and additive to, those of fibrinolytic therapy.

(PMID:2899772, PMID:9563981)

## Candidate PMIDs

- PMID:2899772 — ISIS-2 landmark trial demonstrating aspirin reduces vascular mortality in acute myocardial infarction by 20%.
- PMID:9563981 — ISIS-2 10-year follow-up showing sustained survival benefits of aspirin in myocardial infarction.
- PMID:8145785 — Patrono's seminal NEJM review on aspirin as an antiplatelet drug, describing COX-1 inhibition mechanism.
- PMID:23422285 — Direct demonstration of aspirin acetylation at COX-1 Ser529 using monoclonal antibodies.
- PMID:26408390 — Comprehensive PMC review on aspirin mechanisms in arterial thromboembolism prevention (from pmc.ncbi.nlm.nih.gov/articles/PMC4590672).
- PMID:2500270 — Study showing TXA2 mediates platelet activation during coronary thrombolysis; aspirin accelerates reperfusion.
- PMID:7002350 — Early study on TXA2, prostacyclin, and aspirin effects on vascular tone and platelet aggregation.
- PMID:725852 — Study on enhanced thromboxane generation and platelet aggregation in myocardial infarction survivors.
- PMID:16359516 — Demonstrates correlation between platelet TXA2 production and aggregation in aspirin-treated patients.
- PMID:18752570 — Linear relationship between TXA2-mediated platelet aggregation and TXA2 production with aspirin.
- PMID:32535107 — Characterization of COX acetylation at serine-529 (COX-1) and serine-516 (COX-2) by aspirin.
- PMID:18574266 — ACCP clinical guidelines on antiplatelet drugs including aspirin mechanism and clinical evidence.

## Mechanism graph proposal (advisory)

```
Aspirin (CHEBI:15365)
    → [negatively regulates activity of] →
Cyclooxygenase-1 (COX-1/PTGS1, UniProt:P23219)
    → [decreases synthesis of] →
Prostaglandin H2 (CHEBI:15554)
    → [decreases synthesis of] →
Thromboxane A2 (CHEBI:15627)
    → [decreases activity of] →
Platelet Aggregation (GO:0070527)
    → [negatively regulates] →
Coronary Artery Thrombosis (HP:0001677)
    → [prevents] →
Myocardial Infarction (MONDO:0005068)
```
