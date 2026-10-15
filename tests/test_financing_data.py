import unittest
import sys
from pathlib import Path
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from build_financing_summary import build, OUT, AUCTIONS, BANKS, _read

class TestOfficialFinancing(unittest.TestCase):
    def test_complete_official_frequencies(self):
        auctions=_read(AUCTIONS)
        lending=_read(BANKS)
        self.assertEqual(len(auctions),21)
        self.assertEqual(auctions[0]["month"],"2024-07")
        self.assertEqual(auctions[-1]["month"],"2026-03")
        self.assertEqual(len(lending),6)
        self.assertEqual(lending[-1]["quarter"],"2026-Q1")

    def test_transcription_crosschecks(self):
        auction={x["month"]:x for x in _read(AUCTIONS)}
        bank={x["quarter"]:x for x in _read(BANKS)}
        self.assertEqual(float(auction["2025-02"]["one_week_auction_weighted_average_pct"]),5.48)
        self.assertEqual(float(auction["2026-03"]["one_week_auction_marginal_average_pct"]),3.10)
        self.assertEqual(float(bank["2025-Q4"]["senegal_avg_bank_lending_pct"]),6.45)
        self.assertEqual(float(bank["2026-Q1"]["cote_divoire_avg_bank_lending_pct"]),6.06)

    def test_deterministic_financing_summary(self):
        with tempfile.TemporaryDirectory() as d:
            generated=Path(d)/"summary.json"
            result=build(out=generated)
            self.assertEqual(result["auction_change_2024_07_to_2026_03_bp"],-192.3)
            self.assertEqual(result["bank_uemoa_change_2024q4_to_2026q1_bp"],-25)
            self.assertEqual(result["auction_minus_policy_spread_2026_03_bp"],57.7)
            self.assertEqual(generated.read_bytes(),OUT.read_bytes())

if __name__=="__main__":unittest.main()
