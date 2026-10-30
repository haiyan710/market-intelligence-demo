# Runnable reference pipeline

This is a **small, offline data-engineering reference slice** for fictional Avenra Travel. It uses invented external-source fixtures and Python's standard library. It is independent of the private system's code, data, source registry, model calls, scheduler, delivery and application.

From the portfolio repository root:

```bash
python3 reference_pipeline/run.py --output reference_pipeline/output
python3 -m unittest discover -s reference_pipeline/tests -v
```

The command loads [synthetic source records](fixtures/sources.json) and a [small registry](fixtures/source_registry.csv) that declares each fictional publisher's input role. It validates provenance and dates, inserts records idempotently into SQLite, groups the same canonical development, excludes out-of-window sources, checks that both flight and hotel have a central story, and writes:

- `output/edition.json` — canonical, inspectable edition with source IDs and score components;
- `output/reader.html` — a **simpler generated projection** than the hand-designed [portfolio brief](../examples/interactive-demo.html);
- `output/qc.html` — operator view of included, duplicate and excluded records;
- `output/sources.sqlite` — local normalized source store.

The output directory is ignored by Git. Run the command again with the same inputs: the SQLite row count and the three rendered artifact bytes stay the same. `--fixture`, `--registry` and `--output` can point to other local files/directories. No network request, account, LLM or email is used.

The fixture represents four developments already shown in the portfolio brief: Kivora, Selune, Orivo and Teralis. A second fictional Kivora report covers the **same** development and is kept as an additional source, not a fifth signal. An older Lumen report is retained in SQLite but excluded from this edition window. Every publisher, place, figure and event is fictional; the source IDs are embedded scenario provenance, not real external citations.

The scoring and release logic here are intentionally much smaller than the implemented private system. This reference slice demonstrates data contracts and reproducible rendering, not its editorial judgement or complete safeguards.
