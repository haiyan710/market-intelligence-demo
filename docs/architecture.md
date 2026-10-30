# Architecture

Avenra Travel is a fictional OTA on the fictional continent of Caelora, used to demonstrate a travel market intelligence workflow. Its assumed product lines are flights, hotels and premium stays, and destination experiences. It serves both consumers and travel trade partners. All company and geography details are invented scenario assumptions.

```text
Source records and dated reports
            |
            v
  Collect and normalize
            |
            v
  Classify by market and product line
            |
            v
  Evidence-backed analysis
            |
            v
  Editorial selection and quality checks
            |
            v
  Reader brief + evidence trail
```

## Components

| Component | Responsibility | Output |
| --- | --- | --- |
| Source intake | In the private system, capture public articles and reports with their original URL, publisher and dates. In this offline sample, load clearly labeled fictional source cards embedded in the artifact. | Dated source records |
| Normalization | Extract the factual development, entities, markets and product lines. Preserve the source text for verification. | Comparable records |
| Analysis | Map each development to demand, supply, price or distribution. Draft a conditional transmission chain for the fictional OTA. | Candidate signals and hypotheses |
| Editorial selection | Rank by direct relevance and evidence quality; keep flight and hotel coverage visible. | Ordered reader brief |
| Quality control | Check factual headlines, source ownership, dates, duplication and evidence limits. | Review notes separate from reader copy |
| Presentation | Show the full brief and clickable evidence links in one self-contained view. | Portfolio demo |

## Implemented system pattern and portfolio reference slice

The private project behind this case study implements a scheduled, local source-to-brief pipeline. It gathers external material, stores normalized articles, uses model-assisted classification and specialist analysis, consolidates candidates in an edition editor, and applies deterministic validation before rendering a reader brief and a separate quality-control view. Its delivery and private archive are downstream of the canonical edition artifact. These are architectural descriptions, not a public service offered by this repository.

This portfolio repository contains an **offline reference slice** of that pattern: a fictional OTA profile, invented source cards, a self-contained reader page and the documentation needed to inspect the editorial logic. The source cards are part of the imagined world; they are not external citations. The repository does not contain the full scheduler, collection corpus, model integration, private storage, delivery configuration or production application. Reproducing the page locally does not execute those systems.

## Evidence contract

- A headline describes an observable statement in its cited source record. The demo's records are explicitly fictional.
- In the private production pattern, each real-world factual claim identifies its public publisher, link and as-of date. In this sample, each in-world claim points to a dated embedded fictional source card.
- A company-specific implication is explicitly a hypothesis. It states the assumed product exposure and the mechanism that would connect the sourced development to that exposure.
- An evidence limit or uncertainty belongs in the review record, while the reader brief stays legible.
- A source record dated outside the edition window provides background only; it does not become a new event merely because it was discovered later.

This separation makes it possible to inspect the chain from source to interpretation without treating the interpretation as a verified fact.
