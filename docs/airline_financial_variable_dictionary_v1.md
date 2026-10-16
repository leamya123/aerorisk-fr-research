# Airline Profitability Variable Dictionary v1

| Variable | Unit | Source and validation rule |
|---|---|---|
| `airline_id` | string | stable company identifier; do not merge distinct subsidiaries |
| `fiscal_year` | calendar/fiscal year | original company reporting year, not automatically calendar year |
| `fiscal_year_end` | YYYY-MM-DD | confirm accounting-period year end |
| `net_income_billion_xof` | billion XOF | official reported *résultat net*, may be negative; check consolidated vs entity-only |
| `revenue_billion_xof` | billion XOF | *chiffre d'affaires*, same accounting scope and reporting period |
| `net_profit_margin` | net_income/revenue | compute only if both compatible and revenue>0; derived sensitivity outcome, not replacement of original net income |
| `operating_income` | billion XOF | *résultat d'exploitation*, distinct from net profit |
| `financial_expenses` | billion XOF | *charges financières* if separately disclosed, subject to reporting conventions |
| `government_operating_subsidy` | billion XOF | operating grants recognized in earnings; distinguish from equity contributions |
| `government_equity_injection` | billion XOF | capital transaction, NOT automatically profit |
| `fleet_size` | aircraft | dated official fleet count, not a proxy for EBITDA |
| `passenger_traffic` | annual passengers | ensure comparable flown / carried definition |
| `fuel_cost` | billion XOF | company fuel expenses if disclosed, else don't impute from spot prices as if actual cash cost |
| `legal_policy` | dated evidence-coded categorical | define specific national/airline rule event, verified enforcement/applicability; shared OHADA membership has no cross-country variation in UEMOA |
| `ecb_dfr`, `bceao_tms` | annual % | aggregate official rate to fiscal year with explicit date weights; do not substitute quarterly observations for annual earnings |
| `report_status` | audited/unaudited/chart | distinguish audited figures from rounded chart labels |

### Data integrity
- Every company-year data row needs a stable official document, cited page and revision/version.
- Missing cells stay blank; no fabricated filling or synthetic firm data.
- Policy/firm profit correlations are not proof of ECB causality.
- The initial 2019–2023 Air Côte d'Ivoire rows were transcribed from graphs in an official DGPE report, **not independently verified against separate audited company statements**.
