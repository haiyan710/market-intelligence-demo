#!/usr/bin/env python3
"""Offline, deterministic source-to-edition reference slice using fictional data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import sqlite3
from collections import defaultdict
from datetime import date
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIELDS = (
    "source_id", "publisher", "source_title", "source_kind", "published",
    "development_id", "line", "headline", "fact", "hypothesis", "falsifier",
    "relevance", "evidence_depth",
)
TEXT_FIELDS = FIELDS[:11]
SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    publisher TEXT NOT NULL,
    source_title TEXT NOT NULL,
    input_role TEXT NOT NULL,
    published TEXT NOT NULL,
    development_id TEXT NOT NULL,
    line TEXT NOT NULL,
    headline TEXT NOT NULL,
    fact TEXT NOT NULL,
    hypothesis TEXT NOT NULL,
    falsifier TEXT NOT NULL,
    relevance INTEGER NOT NULL,
    evidence_depth INTEGER NOT NULL,
    content_hash TEXT NOT NULL
);
"""


def load_registry(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or set(rows[0]) != {"publisher", "input_role"}:
        raise ValueError("registry must have publisher,input_role columns")
    registry = {}
    for row in rows:
        publisher, role = row["publisher"].strip(), row["input_role"].strip()
        if not publisher or not role or publisher in registry:
            raise ValueError("registry has blank or duplicate publisher")
        registry[publisher] = role
    return registry


def load_fixture(path: Path, registry: dict[str, str]) -> tuple[dict, list[dict]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not str(payload.get("scenario", "")).startswith("FICTIONAL EXTERNAL SOURCES"):
        raise ValueError("fixture must be explicitly fictional")
    edition = payload["edition"]
    for key in ("id", "company", "window_start", "window_end", "as_of"):
        if not str(edition.get(key, "")).strip():
            raise ValueError(f"edition missing {key}")
    start, end, as_of = (date.fromisoformat(edition[key]) for key in
                         ("window_start", "window_end", "as_of"))
    if not start <= end < as_of:
        raise ValueError("edition dates must satisfy start <= end < as_of")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("fixture requires source records")
    seen = set()
    for record in sources:
        if not isinstance(record, dict) or any(key not in record for key in FIELDS):
            raise ValueError("source record missing required fields")
        if any(not isinstance(record[key], str) or not record[key].strip()
               for key in TEXT_FIELDS):
            raise ValueError("source text and provenance fields must be nonempty")
        sid = record["source_id"]
        if sid in seen:
            raise ValueError(f"duplicate source id in fixture: {sid}")
        seen.add(sid)
        if record["source_kind"] != "fictional_external":
            raise ValueError(f"{sid}: only fictional external source records are allowed")
        if record["publisher"] not in registry:
            raise ValueError(f"{sid}: publisher is absent from source registry")
        if record["line"] not in {"flight", "hotel"}:
            raise ValueError(f"{sid}: unsupported product line")
        if not isinstance(record["relevance"], int) or not 0 <= record["relevance"] <= 3:
            raise ValueError(f"{sid}: relevance must be 0..3")
        if not isinstance(record["evidence_depth"], int) or not 0 <= record["evidence_depth"] <= 3:
            raise ValueError(f"{sid}: evidence_depth must be 0..3")
        published = date.fromisoformat(record["published"])
        if published > as_of:
            raise ValueError(f"{sid}: source date is after edition as_of")
    return edition, sources


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def ingest(conn: sqlite3.Connection, sources: list[dict], registry: dict[str, str]) -> int:
    """Insert once; refuse changed content under an existing source id."""
    inserted = 0
    with conn:
        for record in sources:
            canonical = json.dumps(record, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"))
            digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            prior = conn.execute(
                "SELECT content_hash FROM sources WHERE source_id=?", (record["source_id"],)
            ).fetchone()
            if prior:
                if prior["content_hash"] != digest:
                    raise ValueError(f"{record['source_id']}: changed fixture under stable source id")
                continue
            conn.execute(
                "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    record["source_id"], record["publisher"], record["source_title"],
                    registry[record["publisher"]], record["published"],
                    record["development_id"], record["line"], record["headline"],
                    record["fact"], record["hypothesis"], record["falsifier"],
                    record["relevance"], record["evidence_depth"], digest,
                ),
            )
            inserted += 1
    return inserted


def build_edition(conn: sqlite3.Connection, edition: dict, source_ids: set[str]) -> tuple[dict, dict]:
    """Deduplicate by canonical development and retain every in-window source."""
    rows = [
        dict(row) for row in conn.execute(
            "SELECT * FROM sources ORDER BY published, source_id"
        ).fetchall() if row["source_id"] in source_ids
    ]
    start, end = edition["window_start"], edition["window_end"]
    excluded = [
        {"source_id": row["source_id"], "published": row["published"],
         "reason": "outside edition window"}
        for row in rows if not start <= row["published"] <= end
    ]
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if start <= row["published"] <= end:
            groups[row["development_id"]].append(row)
    signals = []
    duplicate_groups = []
    for dev_id, group in sorted(groups.items()):
        if len({row["line"] for row in group}) != 1 or len({row["headline"] for row in group}) != 1:
            raise ValueError(f"{dev_id}: conflicting product line or headline")
        primary = sorted(group, key=lambda row: (-row["evidence_depth"], row["published"],
                                                  row["source_id"]))[0]
        age = (date.fromisoformat(edition["as_of"]) -
               max(date.fromisoformat(row["published"]) for row in group)).days
        freshness = 2 if age <= 2 else 1 if age <= 4 else 0
        breadth = min(len(group), 2)
        score = 2 * primary["relevance"] + primary["evidence_depth"] + freshness + breadth
        refs = [
            {"source_id": row["source_id"], "publisher": row["publisher"],
             "source_title": row["source_title"], "input_role": row["input_role"],
             "published": row["published"]}
            for row in sorted(group, key=lambda row: row["source_id"])
        ]
        signals.append({
            "development_id": dev_id, "line": primary["line"],
            "headline": primary["headline"], "what_changed": primary["fact"],
            "so_what": primary["hypothesis"], "falsifier": primary["falsifier"],
            "source_refs": refs,
            "score": score,
            "score_components": {
                "relevance_x2": 2 * primary["relevance"],
                "evidence_depth": primary["evidence_depth"],
                "freshness": freshness, "source_breadth": breadth,
            },
        })
        if len(group) > 1:
            duplicate_groups.append({
                "development_id": dev_id,
                "source_ids": sorted(row["source_id"] for row in group),
                "result": "one signal with all source references",
            })
    signals.sort(key=lambda item: (-item["score"], item["development_id"]))
    lines = {signal["line"] for signal in signals}
    if not {"flight", "hotel"} <= lines:
        raise ValueError("release rule: edition needs central flight and hotel signals")
    canonical = {
        "scenario": "FICTIONAL / OFFLINE REFERENCE ONLY",
        "run": dict(edition),
        "signals": [{"rank": index, **signal} for index, signal in enumerate(signals, 1)],
    }
    qc = {
        "scenario": canonical["scenario"],
        "run_id": edition["id"],
        "source_records": len(rows),
        "in_window_sources": sum(len(group) for group in groups.values()),
        "excluded": excluded,
        "duplicate_developments": duplicate_groups,
        "signal_count": len(signals),
        "flight_signals": sum(signal["line"] == "flight" for signal in signals),
        "hotel_signals": sum(signal["line"] == "hotel" for signal in signals),
        "release_rule": "pass",
    }
    return canonical, qc


def reader_html(canonical: dict) -> str:
    esc = html.escape
    run = canonical["run"]
    stories, records = [], []
    for signal in canonical["signals"]:
        links = []
        for ref in signal["source_refs"]:
            sid = esc(ref["source_id"], quote=True)
            links.append(f'<a href="#source-{sid}">{esc(ref["publisher"])} · {esc(ref["published"])}</a>')
            records.append(
                f'<article id="source-{sid}"><h3>{sid} · {esc(ref["source_title"])}</h3>'
                f'<p>{esc(ref["publisher"])} · {esc(ref["input_role"])} · '
                f'published {esc(ref["published"])} · as of {esc(run["as_of"])}</p></article>'
            )
        stories.append(
            f'<article class="story"><p class="label">{signal["rank"]}. {esc(signal["line"])}</p>'
            f'<h2>{esc(signal["headline"])}</h2>'
            f'<p>{esc(signal["what_changed"])}</p>'
            f'<p><strong>Why it may matter.</strong> {esc(signal["so_what"])}</p>'
            f'<p class="source">Source: {"; ".join(links)} · as of {esc(run["as_of"])}</p>'
            f'</article>'
        )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(run["company"])} · fictional generated brief</title>
<style>body{{max-width:760px;margin:35px auto;padding:0 20px;color:#17283b;font:18px/1.5 Georgia,serif}}a{{color:#174d83}}h1{{font-size:42px;text-align:center}}h2{{line-height:1.2}}.banner{{background:#fff4dd;border:1px solid #d6b678;padding:10px;font:700 12px Arial,sans-serif}}.sub,.label,.source{{font:14px/1.5 Arial,sans-serif;color:#365471}}.sub{{text-align:center}}.story{{border-top:1px solid #ccd8e3;padding:18px 0}}.label{{font-weight:700;color:#174d83}}section{{border-top:3px solid #17283b;margin-top:25px}}section article{{border-bottom:1px solid #ddd;padding:7px 0}}section article h3{{font-size:16px;margin:5px 0}}section article p{{font:13px Arial,sans-serif}}:target{{background:#eef6fb}}</style></head>
<body><div class="banner">FICTIONAL SIMULATION · All organizations, events, sources and figures are invented.</div>
<h1>Market Brief</h1><p class="sub">{esc(run["company"])} · {esc(run["window_start"])} to {esc(run["window_end"])} · as of {esc(run["as_of"])}</p>
{''.join(stories)}<section><h2>Embedded fictional source ledger</h2>{''.join(records)}</section>
</body></html>
'''


def qc_html(qc: dict) -> str:
    esc = html.escape
    rows = [
        f"<li>{esc(item['source_id'])} ({esc(item['published'])}): {esc(item['reason'])}</li>"
        for item in qc["excluded"]
    ]
    duplicates = [
        f"<li>{esc(item['development_id'])}: {esc(', '.join(item['source_ids']))} → {esc(item['result'])}</li>"
        for item in qc["duplicate_developments"]
    ]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Fictional edition QC</title>
<style>body{{max-width:760px;margin:40px auto;padding:0 20px;font:15px/1.5 Arial,sans-serif;color:#17283b}}h1{{border-bottom:2px solid #174d83}}.banner{{background:#fff4dd;padding:10px}}</style></head><body>
<p class="banner">FICTIONAL OFFLINE REFERENCE · operator view</p><h1>Edition QC</h1>
<p>Run: {esc(qc['run_id'])} · release rule: {esc(qc['release_rule'])}</p>
<p>{qc['source_records']} source records · {qc['in_window_sources']} in-window · {qc['signal_count']} signals
({qc['flight_signals']} flight, {qc['hotel_signals']} hotel)</p>
<h2>Out-of-window sources</h2><ul>{''.join(rows) or '<li>None</li>'}</ul>
<h2>Duplicate developments</h2><ul>{''.join(duplicates) or '<li>None</li>'}</ul>
</body></html>
'''


def write_artifacts(output: Path, canonical: dict, qc: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "edition.json").write_text(
        json.dumps(canonical, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "reader.html").write_text(reader_html(canonical), encoding="utf-8")
    (output / "qc.html").write_text(qc_html(qc), encoding="utf-8")


def run(fixture: Path, registry_path: Path, output: Path) -> tuple[dict, dict]:
    registry = load_registry(registry_path)
    edition, sources = load_fixture(fixture, registry)
    with connect(output / "sources.sqlite") as conn:
        ingest(conn, sources, registry)
        canonical, qc = build_edition(
            conn, edition, {source["source_id"] for source in sources}
        )
    write_artifacts(output, canonical, qc)
    return canonical, qc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=HERE / "fixtures" / "sources.json")
    parser.add_argument("--registry", type=Path, default=HERE / "fixtures" / "source_registry.csv")
    parser.add_argument("--output", type=Path, default=HERE / "output")
    args = parser.parse_args()
    canonical, qc = run(args.fixture, args.registry, args.output)
    print(f"{canonical['run']['id']}: {qc['signal_count']} signals, "
          f"{qc['in_window_sources']} in-window sources, "
          f"{len(qc['excluded'])} excluded; wrote {args.output}")


if __name__ == "__main__":
    main()
