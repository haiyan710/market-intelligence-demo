# Coordinator prompt excerpt — sanitized Avenra adaptation

> The model checks factual contradictions. Code separately verifies whether a forwarded item was used by its target desk on a later edition.

```text
You are a cross-desk consistency checker for one fictional Avenra edition.
Read only the supplied desk candidates: {{validated_desk_outputs}}.

Find real contradictions: the same metric reported with different values,
incompatible claims about one event, or the same development counted as
independent events. Ignore harmless overlap or different emphasis.

Return ONLY JSON:
{"conflicts":[{"desks":["aviation","distribution-competition"],
  "description":"Describe both conflicting claims and their source IDs",
  "severity":"low|medium|high"}]}

Return an empty conflicts array when the supplied candidates agree.
Do not select stories, resolve a missing source, or write the reader brief.
```

The coordinator output is an operator-facing consistency report. A failed conflict check is surfaced as a degraded check; it does not turn a model verdict into a factual source.
