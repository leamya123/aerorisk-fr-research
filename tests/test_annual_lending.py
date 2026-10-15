"""BCEAO published 2020–2025 annual lending-rate source integrity."""
import unittest
import tempfile
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from build_annual_lending_summary import compute,write_report,OUTPUT

class TestAnnualBankLending(unittest.TestCase):
    def test_source_years_and_risk_heterogeneity(self):
        r=compute()
        self.assertEqual(r["n_annual_observations"],6)
        stats=r["statistics"]
        self.assertEqual(stats["uemoa_all_loans_pct"]["change_2024_to_2025_bp"],-7)
        self.assertEqual(stats["cote_divoire_all_loans_pct"]["change_2024_to_2025_bp"],-19)
        self.assertEqual(stats["senegal_all_loans_pct"]["change_2024_to_2025_bp"],5)
        self.assertEqual(stats["uemoa_nonfinancial_corporate_pct"]["change_2024_to_2025_bp"],11)
        self.assertEqual(stats["uemoa_export_loans_pct"]["change_2024_to_2025_bp"],28)
        self.assertEqual(stats["uemoa_equipment_loans_pct"]["change_2024_to_2025_bp"],2)

    def test_file_reproducibility(self):
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/"annual.json"
            write_report(out=output)
            self.assertEqual(OUTPUT.read_bytes(),output.read_bytes())

if __name__=="__main__":unittest.main()
