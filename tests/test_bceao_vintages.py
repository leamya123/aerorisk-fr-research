"""Guard against silently overwriting or merging BCEAO publication vintages."""
import csv
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"data/official/bceao_bank_lending_quarterly.csv"
NEW=ROOT/"data/official/bceao_bank_lending_vintage_2026q2.csv"
ANNUAL=ROOT/"data/official/bceao_annual_lending_2020_2025.csv"
def read(filename,key):
    with filename.open(encoding="utf-8-sig",newline="") as f:
        return {row[key]:row for row in csv.DictReader(f)}
class BCEAOVintageTests(unittest.TestCase):
    def test_two_distinct_releases(self):
        first=read(OLD,"quarter");revised=read(NEW,"quarter")
        self.assertIn("2025-Q1",first)
        self.assertNotIn("2025-Q1",revised) # absent in newest publication, NOT missing observation inferred zero
        self.assertEqual(revised["2026-Q2"]["provisional"],"true")
        self.assertEqual(revised["2026-Q2"]["publication_date"],"2026-09-15")
        self.assertTrue(all(r["source_url"].startswith("https://www.bceao.int/") for r in revised.values()))

    def test_revisions_preserved_and_not_replaced(self):
        a=read(OLD,"quarter");b=read(NEW,"quarter")
        def v(x,q,col):return float(x[q][col])
        col="uemoa_avg_bank_lending_pct"
        self.assertAlmostEqual(v(a,"2026-Q1",col)-v(b,"2026-Q1",col),0.02)
        self.assertAlmostEqual(v(a,"2025-Q4",col)-v(b,"2025-Q4",col),0.02)
        self.assertAlmostEqual(v(a,"2025-Q3",col)-v(b,"2025-Q3",col),0.04)
        self.assertAlmostEqual(v(a,"2026-Q1","senegal_avg_bank_lending_pct")-v(b,"2026-Q1","senegal_avg_bank_lending_pct"),0.08)

    def test_annual_and_quarterly_2025_vintage_discrepancy(self):
        y=read(ANNUAL,"year")["2025"]
        self.assertEqual(float(y["uemoa_all_loans_pct"]),6.69)
        # BCEAO Q2 bulletin has separate 2025 ANNUAL row 6.73;
        # source difference documented in docs/bceao_vintage_revisions_2026q2.md
        self.assertNotEqual(float(y["uemoa_all_loans_pct"]),6.73)
if __name__=="__main__":unittest.main()
