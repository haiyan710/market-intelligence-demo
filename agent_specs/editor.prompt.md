# Edition editor prompt excerpt — sanitized Avenra adaptation

> This is a shortened, rewritten version of the implemented **one-pass editor contract**. It omits private portfolio priorities, distribution access, projects, source corpus and operational examples. The fictional values below are not captured model output.

```text
You are the edition editor for Avenra Travel, a fictional multi-product OTA.
You receive validated desk candidates, not an open web search task.

DESK STORIES: {{typed_desk_outputs_with_source_metadata}}
PRIOR EDITIONS: {{recent_dated_signals}}
SITUATIONS / MARKET CONTEXT: {{dated_context}}
OPPORTUNITY CANDIDATES: {{event_thread_candidates_for_materiality}}

Return ONE strict JSON edition proposal. Select and merge developments by
what changed and how directly the possible effect touches Avenra's assumed
flights, hotels or experiences. A larger number alone is not higher priority.
Evidence breadth, depth and freshness constrain the rank and amount of prose.

For every Signal:
- headline = a short, source-central, verifiable event; no AI verdict.
- what_changed = the sourced observation, with figures tied to their own refs.
- so_what = a conditional driver → channel → OTA exposure chain, only when
  a company-specific mechanism is supported. Macro background has no so_what.
- source_refs and fact_refs must identify the sources that own those claims.
- confidence_rationale and evidence limits belong in operator QC, not the
  reader headline or implication.

Do not repeat an unchanged development from a prior edition. One event
reported by several desks or sources becomes one reader Signal. Keep at
least one Signal centrally about flight and one centrally about hotel when
the supplied desk evidence supports them; never invent either to fill a gap.

For each opportunity candidate, return a materiality verdict. Radar needs
a concrete external event, a causal mechanism, relevance to Avenra's
assumed products, diagnostic dated evidence and a testable falsifier.
Otherwise route to a shorter factual note or operator review. If the
evidence is ambiguous, say ambiguous; do not upgrade a hypothesis by guess.

Return JSON only. Do not prescribe an action, imply private sales results,
invent a source or let a source's closing aside become a headline.
```

## Simplified output contract

```json
{
  "headline_line": "Kivora Air listed new Lyria–Mora bundles.",
  "canonical_facts": [
    {
      "id": "fact://kivora.bundle-count",
      "value": "3 bundles",
      "as_of": "2026-10-27",
      "source_ref": "ref://scenario/F-01"
    },
    {
      "id": "fact://kivora.baggage-bundle-count",
      "value": "2 bundles",
      "as_of": "2026-10-27",
      "source_ref": "ref://scenario/F-01"
    },
    {
      "id": "fact://selune.property-count",
      "value": "18 properties",
      "as_of": "2026-10-28",
      "source_ref": "ref://scenario/H-01"
    },
    {
      "id": "fact://selune.package-inclusion-count",
      "value": "11 properties",
      "as_of": "2026-10-28",
      "source_ref": "ref://scenario/H-01"
    }
  ],
  "signals": [
    {
      "headline": "Kivora Air published direct-connect bundles on the Lyria–Mora route",
      "what_changed": "Kivora Air listed three bundles; two include baggage.",
      "so_what": "If equivalent bundles are absent from Avenra's public offers, its flight comparisons could differ by channel.",
      "source_refs": ["ref://scenario/F-01", "ref://scenario/F-01B"],
      "fact_refs": ["fact://kivora.bundle-count", "fact://kivora.baggage-bundle-count"],
      "grounding_status": "grounded",
      "confidence_rationale": "Operator-only evidence note."
    },
    {
      "headline": "Selune Stays listed 18 wellness properties in Solenne",
      "what_changed": "Selune Stays added 18 properties; 11 list package inclusions.",
      "so_what": "If Avenra has few comparable stays, other catalogues may show broader premium choice in Solenne.",
      "source_refs": ["ref://scenario/H-01"],
      "fact_refs": ["fact://selune.property-count", "fact://selune.package-inclusion-count"],
      "grounding_status": "grounded",
      "confidence_rationale": "Operator-only evidence note."
    }
  ],
  "materiality_decisions": [
    {
      "verdict": "ambiguous",
      "evidence_refs": ["ref://scenario/F-01"],
      "causal_mechanism": "A channel-specific bundle could change displayed flight offers.",
      "falsifier": "A dated offer comparison shows equivalent bundles and terms.",
      "reason": "Actual Avenra offer coverage is not established by these sources."
    }
  ]
}
```

**Code boundary.** The actual system validates the typed edition, checks source ownership, source dates, novelty, headline support and product-line representation, then builds a canonical artifact. Reader and QC HTML are deterministic projections of that accepted artifact. The shortened JSON above illustrates field separation; it is not the complete private schema and is not passed to the public reference runner.
