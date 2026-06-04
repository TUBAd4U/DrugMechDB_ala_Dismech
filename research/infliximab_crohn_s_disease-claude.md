---
provider: claude
model: claude-opus-4-5
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
generated_at: '2026-06-02T20:08:39+00:00'
ttl_days: 30
candidate_pmids:
- PMID:9321530
- PMID:11788561
- PMID:12806611
- PMID:11677207
- PMID:14684579
- PMID:15685549
- PMID:19136378
- PMID:10597333
- PMID:12498003
- PMID:20200959
- PMID:23021876
notes: input_tokens=138331, output_tokens=2314
---

## Proposed mechanism summary

Infliximab is a chimeric monoclonal IgG1 antibody that targets tumor necrosis factor-alpha (TNF-α), a pivotal pro-inflammatory cytokine implicated in the pathogenesis of Crohn's disease.

Infliximab is a purified, recombinant DNA-derived chimeric IgG monoclonal antibody protein that contains both murine and human components that inhibit TNF-α. TNF-α is a signaling protein involved in acute phase reactions and systemic inflammation.

Crohn's disease is a chronic, debilitating gastrointestinal disorder in which a variety of cellular processes and pro-inflammatory mediators influence the pathogenesis of the disease, and TNF-α has been clearly identified as having a pivotal role in the inflammation of the bowel mucosa.

The main cytokine with a proven role in the pathogenesis of CD is TNF-α, and its increased expression is found in both intestinal inflammatory infiltrates and in the serum of patients.

The primary mechanism by which infliximab exerts its therapeutic effects involves multiple pathways beyond simple TNF-α neutralization.

Infliximab is capable of neutralizing all forms (extracellular-bound, transmembrane-bound, and receptor-bound) of TNF-α.

Critically,

infliximab, a chimeric monoclonal antibody against TNF-alpha, is efficacious in Crohn's disease, and its main mechanism of action is thought to be the induction of apoptosis.

Treatment with infliximab induces remission in about 70% of patients with steroid refractory Crohn's disease. Because Crohn's disease is considered to be mediated by uncontrolled activation of mucosal T lymphocytes, infliximab induces apoptosis of T lymphocytes.

Although both infliximab and etanercept showed powerful TNF-α neutralization, only infliximab was able to bind to peripheral blood lymphocytes and lamina propria T cells and subsequently to induce apoptosis of activated lymphocytes.

The apoptotic effect occurs through binding to membrane-bound TNF-α (mTNF) on inflammatory cells, triggering "reverse signaling."

On TNF-α-producing cells, transmembrane TNF-α acts as a receptor transmitting outside-to-inside signals. Binding of infliximab to mTNF activates several anti-inflammatory mechanisms including 'tmTNF-α reverse signaling-induced apoptosis', in which mTNF acts as a cell surface receptor binding circulating infliximab and thereby activating apoptosis of the mTNF-bearing inflammatory cells.

The downstream intracellular molecular events essential for reverse signaling through mTNF have been revealed, and the biologic effects of mTNF elicited by infliximab should be important action mechanisms of this potent anti-inflammatory agent in addition to the neutralization of soluble TNF-alpha.

Monocyte apoptosis induced by infliximab may be an important mechanism that could explain the powerful anti-inflammatory properties of infliximab in patients with chronic active CD.

This apoptosis involves caspase activation, as

apoptosis is the major mechanism by which infliximab exerts its killing activity on lamina propria T cells in Crohn's disease.

## Candidate PMIDs

- **PMID:9321530** — Landmark 1997 NEJM trial by Targan et al. demonstrating infliximab (cA2) clinical efficacy in treatment-resistant Crohn's disease.
- **PMID:11788561** — ten Hove et al. demonstrating that infliximab induces apoptosis of lamina propria T lymphocytes in Crohn's disease patients in vivo.
- **PMID:12806611** — Van den Brande et al. showing infliximab but not etanercept induces apoptosis in lamina propria T-lymphocytes from Crohn's patients.
- **PMID:11677207** — Lügering et al. demonstrating infliximab induces monocyte apoptosis via a caspase-dependent pathway in Crohn's disease.
- **PMID:14684579** — Di Sabatino et al. showing defective mucosal T cell death is reverted by infliximab through a caspase-dependent pathway.
- **PMID:15685549** — Mitoma et al. describing infliximab's potent anti-inflammatory responses through outside-to-inside signals via transmembrane TNF-α.
- **PMID:19136378** — Study evaluating infliximab's effects on the TNF-α system including enhanced soluble TNFR2 release and IL-10 production.
- **PMID:10597333** — Review on targeting TNF-α in Crohn's disease and mechanisms of infliximab action.
- **PMID:12498003** — Review of the role of TNF-α in Crohn's disease pathogenesis and anti-TNF treatment effects.
- **PMID:20200959** — Horiuchi et al. review on transmembrane TNF-α structure, function, and interaction with anti-TNF agents including reverse signaling mechanisms.
- **PMID:23021876** — Immunohistochemical study on infliximab influence on apoptosis-related protein expression in Crohn's disease.

## Mechanism graph proposal (advisory)

```
Infliximab (Drug)
    │
    ├──[binds to]──> soluble TNF-α
    │                    │
    │                    └──[neutralization prevents]──> TNF receptor activation
    │                                                         │
    │                                                         └──[decreases activity of]──> NF-κB pathway
    │                                                                                           │
    │                                                                                           └──[reduces]──> pro-inflammatory cytokine production
    │
    └──[binds to]──> membrane-bound TNF-α (on macrophages/T cells)
                         │
                         └──[activates]──> reverse signaling (outside-to-inside)
                                              │
                                              └──[induces]──> caspase-3 activation
                                                                  │
                                                                  └──[causes]──> apoptosis of lamina propria T cells and monocytes
                                                                                      │
                                                                                      └──[reduces]──> mucosal inflammation
                                                                                                          │
                                                                                                          └──[treats]──> Crohn's Disease
```

**Simplified linear path:**
Infliximab → [binds to] → TNF-α (soluble and membrane-bound) → [neutralizes/induces reverse signaling] → [decreases activity of] → TNF-α signaling → [induces] → apoptosis of inflammatory T cells/monocytes → [decreases] → mucosal inflammation → [treats] → Crohn's Disease
