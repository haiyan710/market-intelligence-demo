# Offline sample

This directory contains two independent, fully synthetic examples:

- [`interactive-demo.html`](interactive-demo.html): a standalone reader mockup with a summary, four ranked stories, expandable analysis notes, grouped In brief items, a synthetic Markets strip, ongoing situations, opportunity-radar hypotheses, and an embedded fictional source ledger. Its document hierarchy and density are inspired by the parent project's current brief design; all content is newly written and synthetic.
- [`build_demo.py`](build_demo.py): a small Python standard-library simulation that loads [`fixture.json`](fixture.json), validates it, ranks its records, and renders [`sample_brief.html`](sample_brief.html). Run `python3 build_demo.py` from any directory to regenerate the sample.

The scoring in `build_demo.py` is intentionally simple and **illustrative**: `2 × relevance + evidence + freshness`, with a check that both flight and hotel appear. The numeric inputs are synthetic. This is not the private project's algorithm, code, source registry, production data or measured performance. The example makes the flow inspectable without a network request, LLM call, account, database or email send.

All organizations, geography, figures, dates and source records are invented. Source links point to records embedded in each HTML file. The conditional implications are hypotheses, not recommendations.
