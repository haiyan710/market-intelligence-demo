# Case study: why the largest number was not the lead story

**Fictional Avenra Travel scenario.** Every company, source, route, date, figure and event below was invented for this portfolio. The [fixture](../reference_pipeline/fixtures/sources.json), [pipeline](../reference_pipeline/run.py) and [tests](../reference_pipeline/tests/test_reference_pipeline.py) let a reviewer inspect the reference output. This is an editorial and system-design example, not a claim about a real OTA or a measured commercial result.

## The question

Avenra is assumed to compare flights and sell hotels. The edition window is **26–29 October 2026**, as of 30 October. The source set contains a carrier's new bundle offer, a larger-sounding capacity increase and two hotel developments. Which facts deserve a reader's limited attention, and what can be said without access to Avenra's bookings or private inventory?

| Candidate | Fictional public record | Possible OTA exposure | What remains unknown |
| --- | --- | --- | --- |
| **Kivora bundles** | `F-01` (27 Oct) and `F-01B` (28 Oct) both describe **three** direct-connect bundles on Lyria–Mora; two include baggage. | Channel-specific flight offer content could change what a comparison displays. | Whether equivalent bundles already appear in Avenra's public offers. |
| **Orivo capacity** | `F-02` (26 Oct) reports **14%** more scheduled seats on Vela–Iskar for six weeks. | More operated seats could affect itinerary choice or fares. | Whether the seats operate and whether demand absorbs them. |
| **Selune wellness stays** | `H-01` (28 Oct) lists **18** Solenne properties; 11 show package inclusions. | Premium stay choice could differ by catalogue. | Whether comparable bookable inventory and terms are already available. |

The 14% figure is more visually striking than “three bundles.” It is not automatically more relevant to an OTA. Kivora's development has a shorter **possible** path to a product-display difference; Orivo's fare effect needs at least two additional conditions. That is an analytical priority judgment, not proof of an offer gap or a recommendation to change distribution.

## The source-to-brief decision

1. **Keep source identity.** `F-01` and `F-01B` remain two dated source records in SQLite. They share `development_id: kivora-bundles`, so the edition emits **one** Kivora Signal with both source references. A second report does not manufacture a second market event.
2. **Separate fact from interpretation.** The Kivora headline reports the bundle announcement. The conditional `so_what` says Avenra's flight comparisons *could* differ by channel **if** equivalent bundles are absent from its public offers. The brief does not claim that absence was observed.
3. **Make the hypothesis defeasible.** A dated, same-route and same-conditions public offer comparison showing equivalent bundles, or withdrawal of Kivora's bundles, would weaken or falsify the proposed content-gap reading.
4. **Preserve the hotel line.** Selune is a central hotel development, not a tag on a cross-product technology story. A multi-product OTA brief should not let louder aviation news erase hotel coverage.
5. **Respect the window.** `B-OLD`, a fictional hotel record dated 20 October, remains in the source store but is excluded as a *new* development for this edition.

The reference runner uses an **illustrative**, hand-specified score: `2 × relevance + evidence depth + freshness + source breadth`. It gives Kivora **12** (rank 1), Selune **11** (rank 2), Teralis **9** (rank 3) and Orivo **8** (rank 4). These weights demonstrate inspectable ordering; they are not the private editor's scoring method, learned model weights or validated business impact.

## What the system design contributes

| Design choice | Failure it prevents | Observable reference evidence |
| --- | --- | --- |
| Source IDs plus canonical development ID | Two articles about one event become two Signals | Kivora has one Signal with `F-01` and `F-01B`; the duplicate group appears in QC. |
| Distinct `what_changed`, `so_what`, `falsifier` fields | A possible OTA effect reads as a sourced fact | The canonical `edition.json` stores each separately. |
| Date-window check before edition construction | An older item is presented as fresh news | `B-OLD` appears in QC exclusions, not reader Signals. |
| Central flight and hotel release condition | A single product line silently dominates the edition | A flight-only fixture raises before reader HTML is written. |
| Canonical JSON feeding reader and QC | Reader and operator pages disagree about the edition | Replaying the same input yields byte-identical artifacts in the included test. |

In the **private multi-agent system**, specialist desks propose candidate interpretations, an editor makes one selection pass, and code applies stronger source, novelty, headline and line-balance checks. This public pipeline covers only the smaller deterministic controls listed above. The richer [AI workflow trace](ai-workflow.md#fictional-handoff-trace-kivora-bundles) illustrates the agent handoffs without presenting them as executed model output.

## Business value and limit

The outcome shown here is a **more inspectable question for an OTA reader**: “Is there a public offer-content difference on Lyria–Mora, and what evidence would disprove it?” The system makes that question easier to notice while keeping a hotel development visible. It does not know Avenra's sales, conversion, customer mix or private supplier terms, so it cannot quantify revenue impact or prescribe an action.
