import copy
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run import run  # noqa: E402


FIXTURE = ROOT / "fixtures" / "sources.json"
REGISTRY = ROOT / "fixtures" / "source_registry.csv"


class ReferencePipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "output"
        self.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def fixture_with(self, payload):
        path = self.root / "fixture.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_offline_replay_is_idempotent_and_byte_reproducible(self):
        fixture = self.fixture_with(self.payload)
        run(fixture, REGISTRY, self.output)
        first = {
            name: (self.output / name).read_bytes()
            for name in ("edition.json", "reader.html", "qc.html")
        }
        run(fixture, REGISTRY, self.output)
        second = {
            name: (self.output / name).read_bytes()
            for name in first
        }
        self.assertEqual(first, second)
        with sqlite3.connect(self.output / "sources.sqlite") as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0], 6)

    def test_duplicate_development_retains_both_source_references(self):
        canonical, qc = run(self.fixture_with(self.payload), REGISTRY, self.output)
        self.assertEqual(len(canonical["signals"]), 4)
        kivora = next(signal for signal in canonical["signals"]
                      if signal["development_id"] == "kivora-bundles")
        self.assertEqual([ref["source_id"] for ref in kivora["source_refs"]],
                         ["F-01", "F-01B"])
        self.assertEqual(len(qc["duplicate_developments"]), 1)

    def test_provenance_and_future_date_are_rejected_before_ingest(self):
        for change in (
            {"publisher": "Unregistered scenario publisher"},
            {"source_kind": "internal_booking_data"},
            {"published": "2026-10-31"},
        ):
            with self.subTest(change=change):
                payload = copy.deepcopy(self.payload)
                payload["sources"][0].update(change)
                with self.assertRaises(ValueError):
                    run(self.fixture_with(payload), REGISTRY, self.output)
                self.assertFalse((self.output / "sources.sqlite").exists())

    def test_release_requires_both_flight_and_hotel(self):
        payload = copy.deepcopy(self.payload)
        payload["sources"] = [row for row in payload["sources"] if row["line"] == "flight"]
        with self.assertRaisesRegex(ValueError, "flight and hotel"):
            run(self.fixture_with(payload), REGISTRY, self.output)
        self.assertFalse((self.output / "reader.html").exists())

    def test_generated_artifacts_show_dates_provenance_and_exclusion(self):
        canonical, qc = run(self.fixture_with(self.payload), REGISTRY, self.output)
        self.assertEqual(qc["excluded"][0]["source_id"], "B-OLD")
        self.assertEqual(qc["release_rule"], "pass")
        reader = (self.output / "reader.html").read_text(encoding="utf-8")
        operator = (self.output / "qc.html").read_text(encoding="utf-8")
        self.assertIn("FICTIONAL SIMULATION", reader)
        self.assertIn('href="#source-F-01"', reader)
        self.assertIn('id="source-F-01"', reader)
        self.assertIn("as of 2026-10-30", reader)
        self.assertIn("B-OLD", operator)
        self.assertEqual({row["line"] for row in canonical["signals"]},
                         {"flight", "hotel"})


if __name__ == "__main__":
    unittest.main()
