# Opportunity matcher prompt excerpt — sanitized Avenra adaptation

> This excerpt represents the **ambiguous-match** step of the private event → thread → revision ledger. Code handles clear cases before invoking a model. The public reference pipeline groups same-edition developments but does not run this cross-edition matcher.

```text
You maintain a fictional Avenra ledger of causal threads.
A THREAD is one stable driver → mechanism → target-outcome hypothesis.
For each NEW EVENT, compare its dated claim and source origin with the
OLD thread, its last revision, known claims and candidate threads.

EVENTS AND CANDIDATES: {{bounded_ambiguous_pairs_with_old_and_new_evidence}}

Choose one decision for each event:
- same_thread: the same causal root and analytical lens.
- same_thread_new_facet: the same root with a genuinely new allowed lens.
- related_but_distinct: shared topic or actor, different causal root.
- new_thread: no supported match.
- ambiguous: evidence is insufficient; do not guess.

For a same-thread event, classify the change as unchanged, strengthened,
weakened or resolved. A new URL, article ID or source count alone is NOT
a material change. Strengthened needs a concrete new milestone, magnitude,
independent reporting with its own facts, or a removed uncertainty.
Weakened needs a contradicting fact. Resolved needs evidence that settles
the falsifier. Copy only candidate thread IDs and facet labels supplied
for this event; never invent either.

Return ONLY JSON keyed by event index:
{"0":{"decision":"same_thread","candidate_thread_id":"thr-kivora-bundles",
  "candidate_hint_thread_id":null,"facet_kind":null,
  "change":"unchanged","materiality_code":null,
  "reason":"F-01B repeats the previously recorded bundle listing without a new term or rollout milestone."}}
```

**Code boundary.** The private resolver uses one bounded batch call for uncertain events, validates each response against an exact decision matrix and known thread IDs, then records event/revision state. A malformed or missing judgment becomes **ambiguous** for QC; it does not silently strengthen a thread. The Kivora example is illustrative, not a captured ledger judgment.
