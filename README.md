# Travel Market Intelligence for OTAs

**An architecture case study and runnable, fictional sample of an evidence-led travel intelligence system.** It turns public market developments into a short brief with traceable facts and conditional hypotheses for a multi-product online travel agency (OTA).

**[See the complete sample brief below](#complete-sample-brief)** · [Open the HTML edition](examples/interactive-demo.html)

> **Portfolio disclosure:** Avenra Travel, the continent of Caelora, every supplier, event, number and source record in the sample are invented. The system described here is adapted from a separate private project. This repository is a shareable reference slice, not that project's source code, live pipeline, client data or measured business results.

## Why an OTA would use this

An OTA has to understand flight capacity and distribution, hotel supply, destination discovery and market inputs together. A news feed presents many facts, but leaves the reader to work out which ones touch their product catalogue and what remains uncertain. This system is designed to produce a brief that answers three questions:

1. **What changed?** A factual headline tied to a dated source.
2. **Why might it matter?** A conditional chain from a market change to a specific OTA product line.
3. **What evidence is missing?** The conditions that could strengthen or weaken the hypothesis.

It does not use booking, customer or sales data, and it does not prescribe commercial actions. [The OTA value map](docs/ota-benefits.md) explains the questions it helps analysts frame across product lines.

## System architecture

```mermaid
flowchart TB
    A[Public news, reports and market series] --> B[Collect, normalize and date sources]
    B --> C[(Article store and annotations)]
    C --> D[Four specialist desks]
    D --> E[Cross-desk coordinator]
    D --> F[Opportunity register and event ledger]
    E --> G[Edition editor: one consolidation pass]
    F --> G
    G --> H[Typed edition artifact and release checks]
    H --> I[Reader brief]
    H --> J[Operator QC view]
    I --> K[Private delivery and human feedback]
    J --> K
    K --> F
```

The underlying private system uses local scheduled collection, SQLite article and cross-edition state, model-assisted specialist analysis and one editorial selection pass. A typed edition artifact feeds deterministic reader and quality-control renderers, so the two views share the same facts. Quality checks cover source dates, headline centrality, duplicate developments, line balance and source-to-claim traceability. The [architecture deep dive](docs/architecture-deep-dive.md) maps the stores, contracts, release gates and failure paths; [engineering notes](docs/engineering.md) and [editorial workflow](docs/workflow.md) explain the design decisions.

## Agents and orchestration

The implemented edition runtime has **four specialist desk calls**, a cross-desk check, an opportunity-memory stage and **one edition-editor pass**. It is a bounded workflow with typed handoffs, not dozens of independent agents running freely.

| Role | Owns | Handoff |
| --- | --- | --- |
| Macro and policy desk | FX, energy, policy and ongoing disruptions as travel demand or cost drivers | Dated context and candidate signals |
| Aviation desk | Routes, capacity, fares and air-content distribution | Flight developments and content hypotheses |
| Stay and experiences desk | Hotels, premium stays, destinations and experiences | Stay developments and product-fit hypotheses |
| Distribution and competition desk | OTA channels, travel technology, metasearch and new interfaces | Cross-product channel developments |
| Coordinator | Cross-desk forwards and conflicting factual claims | Alerts and a consistency report |
| Opportunity memory | Earlier signals and event threads | New-versus-existing evidence and radar candidates |
| Edition editor | Selection, ranking and reader narrative | One canonical edition artifact for deterministic validation and rendering |

Classification, situation tracking, entity roles, text measures, health checks and the knowledge maintainer surround that core flow. Some use a model through a shared adapter; others are deterministic. The [agent roster and orchestration guide](docs/agents-and-orchestration.md) distinguishes every role, handoff and rollout state.

## How an opportunity is reasoned about

An opportunity starts with a **dated, source-supported event**. A company-specific `so_what` traces the event through a demand, supply, price or distribution mechanism to an assumed OTA product exposure. A separate Radar hypothesis records what later observation would **falsify** that reading. The editor can route a candidate to a full Signal, a short factual note, Radar, or operator-only review; a falsifier's presence alone does not earn a Radar card.

```text
source fact → market first mover → transmission channel → OTA exposure
            → conditional so_what → testable falsifier → later evidence/revision
```

The [opportunity reasoning guide](docs/opportunity-reasoning.md) provides the decision matrix, evidence limits and an annotated Avenra case. The [offline fixture](examples/fixture.json) and [small builder](examples/build_demo.py) make the first mover, channel, assumed exposure, missing evidence and falsifier inspectable in code. They illustrate the contract; the full cross-edition ledger and editorial gates remain in the private implementation.

| Design decision | Why it matters |
| --- | --- |
| Keep source records and dates attached to claims | The reader can inspect the reported fact behind a headline. |
| Separate observation from hypothesis | A plausible OTA effect is not presented as a market fact. |
| Model demand, supply, price and distribution links | An implication names the mechanism and its limits. |
| Resolve the same development across sources and editions | Repeated coverage does not become a false new signal. |
| Render reader and quality views from one artifact | Editorial review can inspect evidence without crowding the brief. |
| Require flight and hotel representation | One product line does not disappear because another has louder news. |

The [scope and limitations](docs/limitations.md) page distinguishes this portfolio reference from the private implementation.

## Complete sample brief

The sample OTA, **Avenra Travel**, is assumed to sell flights, hotels and premium stays, destination experiences and partner distribution in fictional Caelora.

The full reader edition is displayed below. It contains:

| Reading layer | What the sample shows |
| --- | --- |
| **What changed for us** | A four-line scan across flights, hotels, distribution and discovery, with links to the leading stories. |
| **Top stories** | Four ranked, source-linked developments with a factual headline, what changed, a conditional OTA implication and expandable analysis. |
| **In brief** | Shorter developments grouped by flight, hotel, distribution and backdrop. |
| **Markets** | A dated, explicitly fictional FX, cost and travel-indicator strip. |
| **Ongoing situations** | Two continuing themes connecting recent evidence without treating a one-off event as a trend. |
| **Opportunity radar** | Three hypotheses, each with a factual event, falsifier and dated evidence. |
| **Source ledger** | Nine embedded fictional records so every sample claim can be traced without presenting invented sources as real publications. |

![Complete fictional Avenra Market Brief, from masthead through source ledger](assets/avenra-full-brief.png)

Open the [HTML edition](examples/interactive-demo.html) to use its story and source links and expand the analysis notes. The screenshot shows the entire brief, including the source ledger; all names, places, events, sources and figures are synthetic.

### Inspect the offline code slice

To inspect a small offline implementation of the source-to-brief flow, run:

```bash
python3 examples/build_demo.py
```

That standard-library script reads a synthetic fixture, validates it, ranks candidate signals and writes [a compact generated brief](examples/sample_brief.html). This generated file demonstrates the code path; the Avenra Market Brief is the portfolio's full reader sample. The script is deliberately a small illustration of the workflow, not a copy of the private production algorithm.

Read the [sample case](docs/sample-case.md) and [example guide](examples/README.md) for the signal logic and files.

## Repository map

```text
docs/       deep architecture, agent roster, workflow, OTA value and limits
examples/   synthetic input, small offline builder and sample HTML views
assets/     screenshot of the fictional reader brief
```

## What this demonstrates

This repo makes the system's reasoning and presentation inspectable: a compact cross-product brief, a source trail, a conditional implication and an explicit boundary between automation and human judgment. It claims no revenue lift, conversion gain, deployment at Avenra or verified market event in Caelora.
