#!/usr/bin/env python3
"""Tiny offline simulation of fixture collection, prioritization, and brief rendering.

All input is fictional. This is teaching/demo code, not the private project's pipeline.
"""

from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path


HERE = Path(__file__).resolve().parent


def collect_fixture(path: Path) -> dict:
    """Load the local synthetic source records; perform no network request."""
    scenario = json.loads(path.read_text(encoding="utf-8"))
    if not scenario.get("scenario", "").startswith("Fictional"):
        raise ValueError("fixture must declare itself fictional")
    records = scenario.get("records", [])
    if not records:
        raise ValueError("fixture has no records")
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("source ids must be unique")
    for record in records:
        if record["line"] not in {"flight", "hotel"}:
            raise ValueError(f"unsupported product line: {record['line']}")
        date.fromisoformat(record["published"])
        for key in ("source", "headline", "fact", "hypothesis"):
            if not record[key].strip():
                raise ValueError(f"{record['id']} has an empty {key}")
        reasoning = record.get("reasoning")
        if not isinstance(reasoning, dict):
            raise ValueError(f"{record['id']} needs a structured reasoning trace")
        for key in ("first_mover", "channel", "exposure", "evidence_gap", "falsifier"):
            if not isinstance(reasoning.get(key), str) or not reasoning[key].strip():
                raise ValueError(f"{record['id']} has no reasoning.{key}")
    return scenario


def prioritize(records: list[dict], edition_date: str) -> list[dict]:
    """Rank toy records with explicit weights and preserve air/stay representation."""
    end = date.fromisoformat(edition_date)
    ranked = []
    for record in records:
        age = (end - date.fromisoformat(record["published"])).days
        if age < 0:
            raise ValueError(f"{record['id']} is dated after the edition")
        freshness = 2 if age <= 2 else 1 if age <= 4 else 0
        scored = dict(record)
        scored["score"] = 2 * record["relevance"] + record["evidence"] + freshness
        ranked.append(scored)
    ranked.sort(key=lambda item: (-item["score"], item["published"], item["id"]))
    if not {"flight", "hotel"}.issubset({record["line"] for record in ranked}):
        raise ValueError("edition requires both flight and hotel records")
    return ranked


def render(scenario: dict, records: list[dict]) -> str:
    """Render a self-contained reader sample with an embedded source ledger."""
    esc = html.escape
    cards = []
    sources = []
    for record in records:
        source_id = esc(record["id"], quote=True)
        line = esc(record["line"])
        reasoning = record["reasoning"]
        cards.append(f"""
        <article class="card {line}">
          <div class="meta"><span class="tag">{line}</span><span>Scenario signal · {source_id}</span></div>
          <h2>{esc(record['headline'])}</h2>
          <h3>What changed</h3><p>{esc(record['fact'])}</p>
          <h3>Conditional implication</h3><p class="hypothesis">{esc(record['hypothesis'])}</p>
          <details><summary>Reasoning and falsifier</summary><div class="reasoning">
            <p><b>First mover:</b> {esc(reasoning['first_mover'])}</p>
            <p><b>Transmission:</b> {esc(reasoning['channel'])}</p>
            <p><b>Assumed OTA exposure:</b> {esc(reasoning['exposure'])}</p>
            <p><b>Evidence still needed:</b> {esc(reasoning['evidence_gap'])}</p>
            <p><b>Falsifier:</b> {esc(reasoning['falsifier'])}</p>
          </div></details>
          <footer><a href="#source-{source_id}">{esc(record['source'])}</a> · published {esc(record['published'])} · as of {esc(scenario['edition_date'])} · synthetic</footer>
        </article>""")
        sources.append(f"""
        <article id="source-{source_id}" class="source">
          <span class="tag">Fictional source {source_id}</span>
          <h3>{esc(record['source'])}</h3><p>{esc(record['fact'])}</p>
          <small>Scenario record · published {esc(record['published'])} · as of {esc(scenario['edition_date'])} · not a real publication</small>
        </article>""")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(scenario['company'])} · sample intelligence brief</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f8f7;color:#172b3e;font:15px/1.6 system-ui,-apple-system,sans-serif}}a{{color:#087d79}}header.hero{{background:#112338;color:#fff;padding:52px max(24px,calc((100vw - 1050px)/2)) 48px}}.eyebrow{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8cd4bf;font-weight:800}}h1{{font-size:clamp(32px,5vw,52px);line-height:1.08;letter-spacing:-.05em;margin:9px 0}}.hero p{{color:#c6d7dd;max-width:650px}}main{{max-width:1100px;margin:0 auto;padding:32px 24px 65px}}.warning{{border:1px solid #e7cb99;background:#fff6e5;color:#6e542b;padding:12px 16px;border-radius:9px;font-size:12px;font-weight:700}}.summary{{display:flex;gap:16px;flex-wrap:wrap;margin:28px 0}}.summary span{{background:#e0f1ea;border-radius:7px;padding:9px 13px;font-size:12px;font-weight:700;color:#12635c}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:17px}}.card,.source{{background:#fff;border:1px solid #dce6e7;border-radius:12px;padding:24px}}.card{{display:flex;flex-direction:column}}.card.flight{{border-top:4px solid #087d79}}.card.hotel{{border-top:4px solid #d97860}}.meta{{display:flex;justify-content:space-between;color:#7b8995;font-size:11px;gap:10px}}.tag{{font-size:10px;text-transform:uppercase;letter-spacing:.1em;font-weight:800;color:#087d79}}.hotel .tag{{color:#b45d49}}h2{{font-size:21px;line-height:1.25;letter-spacing:-.03em;margin:18px 0}}.card h3{{font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:#81919f;margin:8px 0 3px}}p{{margin:0 0 10px}}.card p{{font-size:13px}}.hypothesis{{border-left:2px solid #a7d7ca;padding-left:11px}}.card details{{font-size:12px;margin:0 0 12px}}.card summary{{cursor:pointer;color:#087d79;font-weight:700}}.reasoning{{background:#f5f8f7;border-left:2px solid #a7d7ca;padding:10px 12px;margin-top:8px}}.reasoning p{{margin:0 0 6px}}.card footer{{border-top:1px solid #e3ebec;margin-top:auto;padding-top:14px;font-size:11px;color:#687b8c}}.section-title{{font-size:24px;letter-spacing:-.04em;margin:45px 0 15px}}.source{{margin-bottom:12px;scroll-margin-top:15px}}.source:target{{outline:3px solid #9ad8c8}}.source h3{{font-size:16px;margin:7px 0}}.source p,.source small{{font-size:12px}}.source small{{color:#728391}}@media(max-width:720px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
<header class="hero"><span class="eyebrow">{esc(scenario['company'])} / reader edition</span><h1>Travel market signals</h1><p>{esc(scenario['window'])} · {esc(scenario['continent'])} · A fictional OTA portfolio spanning flights, hotels, experiences and partner distribution.</p></header>
<main><div class="warning">FICTIONAL SIMULATION · All companies, places, figures, dates and sources are invented for this portfolio example. No real market claim or business result is represented.</div>
<div class="summary"><span>{len(records)} signals</span><span>{sum(item['line']=='flight' for item in records)} flight</span><span>{sum(item['line']=='hotel' for item in records)} hotel</span><span>Human decision owner</span></div>
<div class="grid">{''.join(cards)}</div>
<h2 class="section-title">Embedded fictional source ledger</h2><p>Each record repeats the invented input supporting the corresponding headline. Links stay within this file.</p>
{''.join(sources)}
</main></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=HERE / "fixture.json")
    parser.add_argument("--output", type=Path, default=HERE / "sample_brief.html")
    args = parser.parse_args()
    scenario = collect_fixture(args.fixture)
    records = prioritize(scenario["records"], scenario["edition_date"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(scenario, records), encoding="utf-8")
    print(f"Rendered {len(records)} synthetic signals to {args.output}")


if __name__ == "__main__":
    main()
