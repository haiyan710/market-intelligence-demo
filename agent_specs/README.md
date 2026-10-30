# Sanitized agent configuration and prompt excerpts

These files are **public-safe adaptations of prompt contracts used in the implemented private system**, rewritten for fictional Avenra Travel. They preserve the roles, handoffs, evidence rules and output shapes that explain the design. They are **not** verbatim production prompts, a copy of the private configuration, or a runnable AI pipeline. The [offline reference pipeline](../reference_pipeline/README.md) makes zero model calls.

| File | What it shows | Private-system relationship |
| --- | --- | --- |
| [`agent-config.example.yaml`](agent-config.example.yaml) | Four role switches, bounded inputs, call order and release boundary | Adapted from typed desk flags and edition orchestration; all company context is fictional. |
| [`classifier.prompt.md`](classifier.prompt.md) | Public article → desk routing and confidence | Adapted from the classifier's JSON and known-source-ID contract. |
| [`desk.prompt.md`](desk.prompt.md) | Common desk instructions, four role overlays and opportunity output | Adapted from desk briefs, market-map reasoning and typed desk handoffs. |
| [`coordinator.prompt.md`](coordinator.prompt.md) | Cross-desk contradiction check | Adapted from the coordinator's narrow conflict task. |
| [`opportunity-matcher.prompt.md`](opportunity-matcher.prompt.md) | Ambiguous event-to-thread decision matrix | Adapted from the ledger's bounded match judgment and fail-closed outcome. |
| [`editor.prompt.md`](editor.prompt.md) | One editorial selection pass and materiality decisions | Adapted from the editor's source, implication, novelty and product-line rules. |

The implemented runner invokes enabled desks **sequentially**. Each receives a bounded source pack and returns structured candidates; a disabled desk emits a typed disabled record without a model call. The coordinator checks contradictions after the desks, while code checks whether cross-desk forwards were consumed in a later edition. An opportunity matcher applies model judgment only to ambiguous matches. The editor receives validated candidates and makes one selection pass. Code then validates the edition and renders the reader and QC views. [The full architecture map](../docs/ai-workflow.md) covers supporting model stages and state.

The examples intentionally omit real company context, actual source lists and URLs, operational paths, credentials, delivery settings, live rollout flags and historical prompt examples. The Avenra facts used in examples come only from the [invented fixture](../reference_pipeline/fixtures/sources.json). Any `{{placeholder}}` represents a bounded input supplied by orchestration code, not permission for the model to fetch its own evidence.

For provenance of the adaptation, the private implementation keeps these responsibilities in modules named `classify`, `desk_agent`, `coordinator`, `insight_ledger` and `run_builder`, with typed handoffs under `schemas`. The examples preserve their **behavioral contracts**, while shortening wording and replacing all organization-specific context. They should be read as design evidence, not copied into an operational run.
