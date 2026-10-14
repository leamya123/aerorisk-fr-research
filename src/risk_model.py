"""AeroRisk-FR v0.1: illustrative, source-traceable expected cash-flow model.

All defaults are HYPOTHETICAL scenarios, never observed lease quotes.
Returns use constant monthly default hazard, linear pre-default aircraft market
value and recovery after user-specified legal delay. The framework is meant for
sensitivity analysis, not regulatory risk capital or legal advice.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Scenario:
    purchase_price_usd: float = 50_000_000
    term_years: int = 8
    residual_percent: float = 45.0
    discount_rate_percent: float = 7.0
    annual_default_percent: float = 3.0
    recovery_haircut_percent: float = 25.0
    legal_delay_months: int = 12
    storage_cost_usd_month: float = 40_000
    grounded_value_decay_percent_year: float = 2.0


def evaluate(s: Scenario) -> dict:
    """Calculate illustrative break-even rent and present-value components."""
    if not (s.purchase_price_usd > 0 and 1 <= s.term_years <= 30):
        raise ValueError('Purchase price > 0 and term in [1,30] are required')
    for value, name in [(s.residual_percent,'residual'),
                        (s.annual_default_percent,'PD'),
                        (s.recovery_haircut_percent,'recovery haircut'),
                        (s.grounded_value_decay_percent_year,'grounded decay')]:
        if not (0 <= value <= 100):
            raise ValueError(f'{name} must be within [0,100] percent')
    if not (-99 < s.discount_rate_percent <= 100):
        raise ValueError('Discount rate must be greater than -99% and <= 100%')
    if not (0 <= s.legal_delay_months <= 120 and s.storage_cost_usd_month >= 0):
        raise ValueError('Delay must be [0,120] months; storage cost >= 0')

    months = s.term_years * 12
    q = 1 - (1 - s.annual_default_percent / 100) ** (1 / 12)
    monthly_discount = 1 + s.discount_rate_percent / 1200
    terminal_value = s.purchase_price_usd * s.residual_percent / 100
    cashflow_factor = 0.0
    recovery_pv = 0.0
    schedule = []
    for month in range(1, months + 1):
        survival = (1 - q) ** month
        default_mass = (1 - q) ** (month - 1) * q
        payment_factor = survival / monthly_discount ** month
        cashflow_factor += payment_factor
        remaining_value = s.purchase_price_usd + (terminal_value-s.purchase_price_usd)*month/months
        decay = (1 - s.grounded_value_decay_percent_year / 100) ** (s.legal_delay_months / 12)
        recoverable = max(0.0,remaining_value*(1-s.recovery_haircut_percent/100)*decay - s.storage_cost_usd_month*s.legal_delay_months)
        discounted_recovery = default_mass*recoverable/monthly_discount ** (month+s.legal_delay_months)
        recovery_pv += discounted_recovery
        schedule.append({'month': month,'survival_probability':survival,'default_probability_mass':default_mass,'payment_pv_factor':payment_factor,'default_recovery_pv_usd':discounted_recovery})
    residual_pv = (1-q)**months * terminal_value / monthly_discount**months
    required_rent_usd_month = (s.purchase_price_usd-residual_pv-recovery_pv)/cashflow_factor
    return {'required_rent_usd_month':required_rent_usd_month,
            'required_rent_usd_year':12*required_rent_usd_month,
            'lease_rate_factor_percent_month':100*required_rent_usd_month/s.purchase_price_usd,
            'rent_pv_usd':required_rent_usd_month*cashflow_factor,
            'residual_pv_usd':residual_pv,
            'default_recovery_pv_usd':recovery_pv,
            'total_pv_usd':required_rent_usd_month*cashflow_factor+residual_pv+recovery_pv,
            'prob_default_term':1-(1-q)**months,
            'schedule':schedule}


def stress(s: Scenario, rate_shock_bp: int=200, extra_delay_months: int=12):
    """Rate shocks are illustrative *discount-rate* shifts, not ECB forecasts."""
    scenario=replace(s,discount_rate_percent=s.discount_rate_percent+rate_shock_bp/100,
                     legal_delay_months=s.legal_delay_months+extra_delay_months)
    base=evaluate(s);shocked=evaluate(scenario)
    return {'baseline':base,'stress':shocked,'rent_difference_usd_month':shocked['required_rent_usd_month']-base['required_rent_usd_month'],
            'rent_difference_percent':100*(shocked['required_rent_usd_month']/base['required_rent_usd_month']-1)}
