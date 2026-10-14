import unittest
from dataclasses import replace
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'src'))
from risk_model import Scenario,evaluate,stress

class TestRiskModel(unittest.TestCase):
    def test_break_even_identity(self):
        s=Scenario();r=evaluate(s)
        self.assertAlmostEqual(r['total_pv_usd'],s.purchase_price_usd,places=5)

    def test_no_default_and_no_discount(self):
        s=Scenario(purchase_price_usd=12_000_000,term_years=1,residual_percent=0,discount_rate_percent=0,annual_default_percent=0)
        self.assertAlmostEqual(evaluate(s)['required_rent_usd_month'],1_000_000,places=5)

    def test_interest_rate_shock_higher_rent(self):
        s=Scenario();self.assertGreater(evaluate(replace(s,discount_rate_percent=9))['required_rent_usd_month'],evaluate(s)['required_rent_usd_month'])

    def test_legal_delay_higher_rent(self):
        s=Scenario();self.assertGreater(evaluate(replace(s,legal_delay_months=30))['required_rent_usd_month'],evaluate(s)['required_rent_usd_month'])

    def test_higher_residual_reduces_rent(self):
        s=Scenario();self.assertLess(evaluate(replace(s,residual_percent=60))['required_rent_usd_month'],evaluate(s)['required_rent_usd_month'])

    def test_positive_stress(self):
        out=stress(Scenario());self.assertGreater(out['rent_difference_percent'],0)

    def test_invalid_scenarios(self):
        for bad in [Scenario(annual_default_percent=101),Scenario(legal_delay_months=-1),Scenario(purchase_price_usd=0)]:
            with self.assertRaises(ValueError):evaluate(bad)

if __name__=='__main__':unittest.main()
