"""Regression tests for verified (transcribed) official ECB/BCEAO rate events."""
import csv
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "src"))
from build_macro_panel import build, read_events, ECB, BCEAO

ROOT=Path(__file__).resolve().parents[1]
COMMITTED=ROOT/"data/processed/central_bank_policy_monthly_v1.csv"

class TestMacroPanel(unittest.TestCase):
    def test_event_files_ordered_and_sourced(self):
        self.assertEqual(len(read_events(ECB,["deposit_facility_rate_pct","main_refinancing_rate_pct"])),21)
        self.assertEqual(len(read_events(BCEAO,["minimum_bid_rate_pct","marginal_lending_rate_pct"])),10)

    def test_monthly_reproducibility(self):
        with tempfile.TemporaryDirectory() as td:
            outfile=Path(td)/"panel.csv"
            self.assertEqual(build(output=outfile),81)
            self.assertEqual(outfile.read_bytes(),COMMITTED.read_bytes())

    def test_effective_dates_and_levels(self):
        with COMMITTED.open(encoding="utf-8",newline="") as f:
            rows={r["month_end"]:r for r in csv.DictReader(f)}
        self.assertEqual(rows["2024-05-31"]["ecb_deposit_facility_pct"],"4.00")
        self.assertEqual(rows["2024-06-30"]["ecb_deposit_facility_pct"],"3.75")
        self.assertEqual(rows["2024-12-31"]["bceao_minimum_bid_pct"],"3.50")
        self.assertEqual(rows["2025-05-31"]["bceao_minimum_bid_pct"],"3.50")
        self.assertEqual(rows["2025-06-30"]["bceao_minimum_bid_pct"],"3.25")
        self.assertEqual(rows["2026-09-30"]["ecb_deposit_facility_pct"],"2.50")
        self.assertEqual(rows["2026-09-30"]["bceao_minimum_bid_pct"],"3.00")

if __name__=="__main__":
    unittest.main()
