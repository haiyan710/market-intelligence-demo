# Design decisions behind the brief

This is a public-safe account of decisions I made while building the **private** multi-agent system. The Avenra examples and numbers here are fictional. The public [`reference_pipeline/`](../reference_pipeline/README.md) demonstrates selected data controls, while [AI handoffs](ai-workflow.md) and the richer editorial checks below are described from the private implementation. I do not present a synthetic test as proof that the private pipeline executed.

## 1. Let AI propose; let code decide whether an edition can ship

**Failure mode.** A fluent editor can produce a convincing brief with a citation that belongs to a different article, an old event phrased as new, or no central hotel story. A valid JSON response alone would not catch those errors.

**Decision.** Specialist desks receive bounded dated sources and return structured candidates. One editor pass chooses the edition. Code then checks the schema, source ownership, date window, novelty, evidence weight and flight/hotel representation before a canonical artifact feeds both reader and QC renderers. A hard failure can hold the edition; weaker evidence can warn or lower rank. The model does not control publication by writing HTML directly.

**Tradeoff.** The boundary adds schemas, source IDs and failure handling to maintain. It also means a beautiful model answer can be rejected. The benefit is a reviewable reason for what appeared, what was held and which evidence supports each claim.

**Public evidence.** The reference runner writes one `edition.json` and projects reader/QC HTML from it. Its tests replay the same input byte-for-byte, reject an unregistered publisher or future date before ingest, and block a flight-only edition before reader output. The full private release checks are not in this repository.

## 2. Guarantee product-line representation without inventing a story

**Failure mode.** An OTA selling flights and hotels can receive a brief dominated by aviation or a cross-product technology story. Merely tagging a story `flight, hotel` does not make its headline centrally about either product. A language model can miss a relevant hotel candidate even when the hotel desk supplied one.

**Decision.** The private release path checks for a Signal centrally about flight and one centrally about hotel. If the editor omitted a line, code may add an actual cited desk candidate, last in rank, with the evidence limitation recorded in operator QC. If no usable desk candidate exists, it holds the reader edition. It never invents a hotel fact to satisfy the rule.

**Tradeoff.** A sourced but less prominent story may appear near the end of the brief. This is preferable to silently implying that one product line had no relevant development. The operator can see why it was included and its evidence limits.

**Public evidence.** The reference pipeline has the simpler release rule: both lines must be present, and a flight-only fixture raises before HTML is written. It does **not** implement the private candidate-promotion path. The [fictional case](sample-case.md) shows why Selune is a central hotel story alongside Kivora and Orivo flight stories.

## 3. Protect reader trust against attractive but weak headlines

**Failure mode.** A model can turn a passing mention near the end of a short report into a prominent headline. A reader clicking the source then cannot find the reported event at the center of that article. Ranking only by perceived OTA relevance would reward the attractive interpretation.

**Decision.** The private system gives the editor source titles, dates, kind and length. Code weighs evidence breadth, depth and freshness, and checks whether the actors in a **single-source** headline appear in the source title or opening section. Weak support produces an operator warning and can lower rank; it is not silently deleted. Multi-source synthesis is handled differently because one source title need not contain the whole claim.

**Tradeoff.** A heuristic may flag an unusual but legitimate article or miss a subtle mismatch. Keeping it as a warning/ranking control rather than an automatic truth verdict preserves human review. It complements, rather than replaces, source-specific editorial judgment.

**Public evidence.** This repository explains the contract and includes a simpler source-breadth/depth/freshness score in `reference_pipeline/run.py`. It does not claim to reproduce the private headline-centrality heuristic. In the [Kivora case](sample-case.md), the factual headline stays attached to the two records that centrally describe that announcement; the possible OTA effect remains in `so_what`.

## 4. Treat an uncertain opportunity match as uncertain

**Failure mode.** Repeated coverage of one event can look like a new opportunity. A vague AI match to an earlier thread can also make a hypothesis appear “strengthened” when the new evidence is ambiguous.

**Decision.** The private register and newer event → thread → revision ledger use deterministic matching for clear cases and a bounded model judgment for ambiguous pairs. Invalid or unavailable judgment remains review-visible; it does not automatically become a strengthened reader claim. An editor materiality verdict still determines whether a candidate earns Radar, a factual note, a Signal or operator-only review.

**Tradeoff.** Some ambiguous items wait for review or appear in a smaller form. This limits false novelty and false certainty in a product intended to inform judgment across editions.

**Public evidence.** The reference fixture contains `F-01` and `F-01B` for one Kivora development; the runner retains both sources and emits one Signal. This demonstrates same-edition grouping, **not** the private cross-edition ledger or model matching.

## What this case study can and cannot establish

The design target is a brief that helps an OTA reader notice relevant external changes, trace the evidence, and see what would disprove a hypothesis. The portfolio verifies selected engineering behaviors with synthetic fixtures and tests. It does **not** measure bookings, conversion, revenue, analyst time saved or decision quality at fictional Avenra. Those outcomes would require an evaluation with real readers and authorized business data, outside this public reference.
