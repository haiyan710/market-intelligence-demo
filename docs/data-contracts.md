# Data contracts and lineage

The private system uses typed records at each analytical handoff. The shapes below are deliberately simplified for a shareable portfolio. They describe field roles and relationships without publishing the private schema, source corpus or operational identifiers. The [`examples/` fixture](../examples/fixture.json) and [`reference_pipeline/` fixture](../reference_pipeline/fixtures/sources.json) are two smaller, separate fictional contracts.

## Core records

| Record | Identity and key fields | Purpose |
| --- | --- | --- |
| Source article | Article ID, publisher, original title and URL, published date, preserved text | Establish what was actually reported and when. |
| Article annotation | Article ID, product/market classification, entity roles and deterministic text measures | Support bounded desk selection and cross-checks without altering the source record. |
| Desk output | Run ID, desk, generation time, candidate stories, opportunity signals, forwards, context vintage | Give the editor and ledger a dated, structured handoff. |
| Candidate story | Title, named entities, cited key facts, analysis, relevance, confidence, source references | Keep reported facts and analyst framing together while retaining citation boundaries. |
| Opportunity candidate | Factual event summary, subject, demand/supply/price driver, mechanism, target outcome, hypothesis, source-specific evidence and falsifier | Distinguish an event from a possible business effect and make later evidence testable. |
| Canonical fact | Fact ID, label, value, as-of date, owning source reference | Prevent a number from being attributed to an unrelated article. |
| Edition signal | Signal ID, rank, factual headline and `what_changed`, conditional `so_what`, source/fact references, product line, scope, QC metadata | Supply the reader view and operator trace from one record. |
| Ledger event / thread / revision | Event identity, linked causal thread, dated change and evidence | Track the same development across desks and editions without treating every mention as new. |
| Edition artifact | Run metadata and coverage window, canonical facts, ranked signals, short notes, situation context, Radar and QC fields | Preserve a validated snapshot for deterministic rendering. |

`Source article` and `canonical fact` are evidence records; `so_what` and a Radar hypothesis are interpretations. A company-specific `so_what` traces an observed development through a directional market mechanism to an assumed OTA exposure. A macro or general backdrop item can remain factual-only. Neither form authorizes an action recommendation.

## Relationship sketch

```text
source_article.article_id ──┬── article_annotation.article_id
                           ├── desk_story.source_refs[]
                           └── opportunity_candidate.evidence_refs[]

desk_story / opportunity_candidate ──> edition_signal.source_refs[]
opportunity_candidate ──> ledger_event ──> causal_thread ──> revision
source_article / dated context ──> canonical_fact.source_ref
edition_signal.fact_refs[] ──> canonical_fact.id

edition_artifact.run_id + coverage_window ──> reader HTML and operator QC HTML
```

The source reference is an ownership boundary: each claim must be supported by the particular record it cites. A signal's sources do not automatically support a different signal, even when both were considered in the same edition. Reader and QC pages are two projections of the same artifact, not two independently generated accounts.

## Contract outcomes

- **Invalid or unresolved provenance:** record for QC or fail closed at the reader boundary; do not invent a source URL or claim.
- **Out-of-window news:** exclude from the current-event evidence set. Historical context may still be used with its original date.
- **Unchanged development:** suppress as a fresh Signal unless there is a material new fact; preserve the comparison for review.
- **No usable central flight or hotel candidate:** hold the reader edition rather than manufacture a story.
- **Ambiguous Radar materiality or missing evidence/falsifier:** keep the candidate in review rather than publish it as a confirmed opportunity.

## Fictional reference contracts

| Layer | Input contract | Output and boundary |
| --- | --- | --- |
| Curated reader and toy builder under `examples/` | Fictional scenario declaration, edition date, company and continent; four synthetic flight/hotel records with invented publisher, factual in-world headline, hypothesis and reasoning trace. | `build_demo.py` checks required fields and dates, applies a simple score and writes `sample_brief.html`. `interactive-demo.html` is a richer curated artifact. Neither uses SQLite or a model. |
| Executable `reference_pipeline/` | CSV publisher registry plus JSON edition metadata and six fictional external source records. Each has `source_id`, `development_id`, line, publication date, headline, fact, hypothesis, falsifier and illustrative relevance/depth inputs. | `run.py` ingests into `sources.sqlite` and writes `edition.json`, `reader.html`, `qc.html`. It models idempotent ingest, date filtering, development grouping, rank components, source lineage and flight/hotel release checks. It is not the private `RunArtifact` or multi-edition ledger. |
| Implemented private system pattern | Real public sources, bounded context, typed desk outputs, cross-edition state and editorial decisions. | Canonical typed edition artifact, deterministic reader/QC views, private delivery and archive. These inputs and outputs are not included here. |

To inspect the executable reference contract, run `python3 reference_pipeline/run.py --output /tmp/avenra-reference` from the **portfolio repository root** and open `/tmp/avenra-reference/edition.json` alongside the generated reader and QC HTML. Its tests run with `python3 -m unittest discover -s reference_pipeline/tests -v`. They check stable replay, duplicate source retention, provenance/date rejection, line balance and visible source links. The generated reader is simpler than the hand-designed `examples/interactive-demo.html`. None of those tests proves that the private pipeline ran or that Avenra exists.
