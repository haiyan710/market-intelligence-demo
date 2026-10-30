# Engineering notes

This is a shareable description of the **implemented private system pattern**. Avenra Travel and Caelora are fictional. This repository has two smaller demonstrations: a curated brief and toy builder under [`examples/`](../examples/README.md), plus an executable offline [`reference_pipeline/`](../reference_pipeline/run.py) that exposes selected data engineering controls. Neither contains the private scheduler, model integration, delivery path or full release logic. The [data contracts](data-contracts.md) page distinguishes all three layers.

## Pipeline and state

```text
Daily local refresh: public source intake → normalization → article SQLite store
                    → classification / text measures / entity roles

Edition run:        bounded dated article sets + cross-edition state
                    → four specialist desks → cross-desk coordination
                    → opportunity register and event ledger
                    → one editorial consolidation pass
                    → typed edition artifact
                    → deterministic reader HTML + operator QC HTML
                    → private delivery and archive
```

Python orchestrates the local pipeline. SQLite holds normalized articles, annotations, cross-edition signals and feedback. Each edition has an identifier and coverage window so source selection, novelty comparisons and output files refer to the same run. The reader and QC renderers consume the same validated edition artifact; they do not make independent editorial decisions.

The model-assisted stages receive bounded source and context packs through a shared adapter. Specialist desks propose developments and testable hypotheses; the coordinator checks cross-desk factual conflicts; the edition editor selects and synthesizes the reader narrative in one pass. Deterministic code validates the result, checks release conditions, ranks with evidence and relevance terms, and renders the two views. The model's fluency is never a substitute for a source or a valid artifact.

## Lineage and quality controls

The critical lineage is `source record → desk candidate → canonical fact / signal or ledger event → rendered source line`. A fact carries a source reference and as-of date. A signal keeps its own source references, the observed `what_changed`, a separate conditional `so_what`, and operator-only QC fields. A ledger candidate separates a factual event from a causal hypothesis and a falsifier. That allows the reader to trace an interpretation back to the event that motivated it.

| Control | Failure it addresses | Behavior in the private system |
| --- | --- | --- |
| Source date and edition window | Later reports leaking into an earlier edition | Reject out-of-window news as a current development; retain dated background only as context. |
| Source ownership and headline centrality | A claim attached to the wrong article or buried in an incidental mention | Validate references; warn or demote a weak single-source headline; surface review detail in QC. |
| Evidence weight | Thin, old or single-source material outranking better-supported reporting solely on apparent relevance | Rank with breadth, depth and freshness alongside business implication; a weak source is not silently deleted. |
| Cross-edition novelty | Re-reporting the same event as new | Compare with prior editions and suppress an unchanged near-duplicate unless a material new fact exists. |
| Product-line balance | Flight or hotel developments disappearing from the edition | Require central flight and hotel Signals; use an actual cited desk candidate if one was missed, otherwise hold the edition. |
| Typed artifact and render checks | Invalid model output or incomplete reader/QC page reaching delivery | Validate the edition object and render both views before release. |
| Radar materiality and provenance | A plausible-sounding hypothesis becoming a reader card without diagnostic evidence | Require a concrete event, direct relevance, causal mechanism, falsifier and resolved evidence. Ambiguous or non-renderable cases remain QC-visible. |

These controls have different outcomes. Some block release, some lower rank, and some warn the operator. Calling all of them “gates” would hide that distinction. Source-quality notes stay in QC; substantive uncertainty about a possible business effect can remain in the reader's conditional implication.

## Orchestration and failure behavior

The local schedule runs a lighter collection and annotation path more frequently than the edition path. Noncritical collectors and enrichment steps log a failure and allow downstream work to use available, dated material. A broad classification failure triggers a dependency check before expensive desk work. Desk failure, inability to build or render the canonical edition, and required line-coverage gaps can stop release. A send failure is reported as a failed delivery; a separate publication failure is surfaced without implying the edition itself was not built.

Health checks distinguish a quiet or stale source from a critical dependency or missed edition. Stage logs, output artifacts and delivery markers provide evidence of what completed. The private operational environment and its alert destinations are outside this portfolio.

## Executable offline reference pipeline

The reference pipeline is a **different implementation** of selected mechanics, not an extract of the private code. It uses only Python's standard library and the fictional records in `reference_pipeline/fixtures/`:

```bash
python3 reference_pipeline/run.py --output /tmp/avenra-reference
python3 -m unittest discover -s reference_pipeline/tests -v
```

Run those commands from the **portfolio repository root**. The first writes `sources.sqlite`, `edition.json`, `reader.html` and `qc.html` under the chosen output directory. A CSV registry assigns allowed fictional publishers an input role; a JSON fixture supplies six dated source records. The runner validates provenance and dates before ingest, stores a hash for each source ID, rejects changed content under an existing ID, retains an older record in SQLite but excludes it from this edition, groups two reports of one development into one Signal with both references, scores with explicit relevance/evidence/freshness/breadth terms, and requires central flight and hotel representation. The generated reader is simpler than the curated UI sample and links to embedded fictional source records; QC lists exclusions and duplicate groups.

The included `unittest` suite checks idempotent replay and byte-identical rendered artifacts, duplicate-development lineage, rejection of unregistered or non-fictional provenance and future dates before ingest, flight/hotel release behavior, and reader/QC source and date visibility. These tests verify this small reference code only. There is no scheduled collection, model call, cross-edition novelty store, full typed private artifact or email/app publication in this slice.

## Reproducibility and verification

The private system records run-specific artifacts and source dates so an edition can be inspected as it was built. Its routine tests run offline: model and network calls are blocked while contracts, novelty rules, ranking behavior, renderers and failure paths are exercised with fixtures. A passing test suite cannot prove that external sources, model access or delivery are healthy during a scheduled run, so the first live run after a change still needs observation.

The toy builder is reproducible without network or credentials: `python3 examples/build_demo.py` reads `examples/fixture.json`, checks its fictional declaration, unique IDs, dates, required fields and reasoning trace, applies a small illustrative score, requires both flight and hotel records, and writes `examples/sample_brief.html`. The richer [Avenra reader sample](../examples/interactive-demo.html) is a curated fictional artifact. Both examples and the reference pipeline use invented source records; none is independent evidence about a real market or a reproduction of the private ranking and multi-edition ledger.
