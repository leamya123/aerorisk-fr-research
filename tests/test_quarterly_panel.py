"""Test sourcing, full quarter coverage and rate matching; no causal estimates."""
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from build_quarterly_panel import build,OUTPUT,LOANS,_load

class QuarterlyPanelTests(unittest.TestCase):
    def test_all_26_quarters_and_historical_spot_checks(self):
        x=_load(LOANS)
        self.assertEqual(len(x),26)
        self.assertEqual(x[0]["quarter"],"2020-Q1")
        self.assertEqual(x[-1]["quarter"],"2026-Q2")
        d={r["quarter"]:r for r in x}
        self.assertEqual(float(d["2020-Q1"]["uemoa_lending_pct"]),6.63)
        self.assertEqual(float(d["2021-Q2"]["senegal_lending_pct"]),5.84)
        self.assertEqual(float(d["2022-Q3"]["uemoa_lending_pct"]),6.54)
        self.assertEqual(float(d["2024-Q3"]["uemoa_lending_pct"]),7.07)
        self.assertEqual(float(d["2025-Q1"]["senegal_lending_pct"]),5.93)
        self.assertIn("large_", d["2025-Q1"]["quality_flag"])
        self.assertEqual(d["2026-Q2"]["quality_flag"],"provisional")

    def test_full_policy_join_and_first_differences(self):
        x=build(output=Path(tempfile.gettempdir())/"ar_test_quarter_panel.csv")
        self.assertEqual(len(x),26)
        d={r["quarter"]:r for r in x}
        self.assertEqual(d["2020-Q1"]["delta_uemoa_lending_pp"],"")
        self.assertEqual(d["2024-Q3"]["uemoa_lending_pct"],"7.07")
        self.assertEqual(d["2024-Q3"]["bceao_tms_quarter_end_pct"],"3.50")
        self.assertEqual(d["2024-Q4"]["delta_uemoa_lending_pp"],"-0.10")
        self.assertEqual(d["2025-Q2"]["bceao_tms_quarter_end_pct"],"3.25")
        self.assertEqual(d["2026-Q2"]["ecb_dfr_quarter_end_pct"],"2.25")
        self.assertEqual(d["2026-Q2"]["bceao_tms_quarter_end_pct"],"3.00")

    def test_panel_reproducible_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            temp=Path(d)/"quarterly.csv"
            build(output=temp)
            self.assertEqual(temp.read_bytes(),OUTPUT.read_bytes())

if __name__=="__main__":unittest.main()
