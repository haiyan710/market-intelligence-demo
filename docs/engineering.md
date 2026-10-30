# Engineering notes

This page describes the implemented **private system pattern** behind the case study. The code and content in this public portfolio repository are an **offline reference slice** for fictional Avenra Travel on Caelora. They do not reproduce the private system's scheduler, data stores, model access, delivery path or hosted reader application.

## End-to-end design

```text
Local schedule
   → source collection and normalization (Python)
   → article and edition state (SQLite)
   → model-assisted classification and specialist desks (shared adapter)
   → one editorial consolidation pass
   → canonical, typed edition artifact
   → deterministic reader and QC renders
   → private delivery and archive
```

The scheduled pipeline runs locally. Python handles collection, normalization, orchestration and validation; SQLite stores source and cross-edition state. The model-assisted stages receive bounded source context through a common adapter. They produce candidate analyses and an editorial selection, while the final renderers consume a validated artifact. This keeps presentation deterministic after the editorial decision is made.

## Contracts and checks

| Concern | Private system pattern | What the public slice shows |
| --- | --- | --- |
| Source provenance | Preserve a source's title, link, publisher and date; associate each claim with the source that supports it. | Embedded, dated **fictional** cards linked from the fictional brief. |
| Novelty | Compare developments with recent editions, suppress unchanged repeats and keep historical material from becoming new news. | A documented editorial rule and a single illustrative edition. |
| Product coverage | Validate that both flight and hotel lines have central, usable signals before release. | An edition with visible flight and hotel examples. |
| Canonical artifact | Validate a typed edition object before any reader or QC rendering. | A simplified offline representation of the resulting reader view. |
| Reader versus QC | Render the full brief inline; put coverage, confidence and source-quality notes in a separate operator view. | Reader-facing sample plus explanatory documentation. |
| Reliability | Check critical dependencies and pipeline outcomes; record stage failures and distinguish warnings from delivery failures. | A description of the behavior, without the private operational environment. |

The checks act as release safeguards. Model output is treated as a candidate that must satisfy the artifact contract and source rules; a fluent paragraph alone does not establish provenance or editorial quality.

## Verification approach

The private project uses offline unit and integration tests for article handling, artifact validation, editorial constraints, renderers and failure paths. External model and network calls are blocked in routine tests. A scheduled run still needs operational observation because passing tests cannot prove that external sources, credentials or delivery are healthy on that day.

The public slice is intended to be inspected and opened locally. Its example facts belong to the fictional world and are not evidence of real market conditions or measured business outcomes.
