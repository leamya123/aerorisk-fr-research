# BCEAO Continuous Quarterly Bank Lending Panel — Source & Revision Audit v1

**Status 2026-10-15:** 26 quarterly observations, 2020Q1–2026Q2, for UEMOA aggregate, Côte d'Ivoire and Senegal. Source = official BCEAO `Tableau 3.1, Taux d'intérêt débiteurs des crédits bancaires (valeur moyenne sur la période, en pourcentage)`. These are the average interest rates on bank customer lending in the referenced period, **not** lease rates or aircraft operator borrowing rates.

This panel is a deliberately **mixed-vintage compilation**: each period records the exact publication vintage selected, the source URL and the printed page. We never silently replace original editions in `data/official/`; do not interpret this table as an unambiguously final unrevised history.

| Selected vintage key | Periods used | Printed page | Source |
|---|---|---:|---|
| `q2021` | 2020Q1–2021Q1 | 11 | https://www.bceao.int/sites/default/files/2021-07/Bulletin%20trimestriel%20des%20statistiques%20premier%20trimestre%202021.pdf |
| `q2021_2` | 2021Q2 | 11 | https://www.bceao.int/sites/default/files/2021-10/Bulletin%20Trimestriel%20des%20Statistiques%20-%20Juin%202021.pdf |
| `q2022` | 2021Q3–2022Q2 | 11 | https://www.bceao.int/sites/default/files/2023-01/Bulletin%20Trimestriel%20des%20Statistiques%20-%203T_2022.pdf |
| `q2023` | 2022Q3–2023Q3 | 11 | https://www.bceao.int/sites/default/files/2023-12/Bulletin%20Trimestriel%20des%20Statistiques%203T2023.pdf |
| `q2024` | 2023Q4–2024Q3 | 12 | https://www.bceao.int/sites/default/files/2025-03/Bulletin%20Trimestriel%20des%20Statistiques_4%20T2024.pdf |
| `q2025` | 2025Q1 | 12 | https://www.bceao.int/sites/default/files/2026-06/Bulletin-Trimestriel-des-Statistiques-mars-2026.pdf |
| `q2026` | 2024Q4 and 2025Q2–2026Q2 | 12 | https://www.bceao.int/sites/default/files/2026-09/Bulletin%20Trimestriel%20des%20Statistiques%20-%20juin%202026.pdf |

## Known revision checks

- **2020Q1**: the 2020Q1 first-release official report lists UEMOA **6.68%**, while the 2021Q1 bulletin's historic table gives **6.63%**. The selected mixed panel uses 6.63%, with the revision documented. First-release archive: https://www.bceao.int/sites/default/files/2020-06/Bulletin%20Trimestriel%20des%20Statistiques%20-%20Premier%20trimestre%202020.pdf
- **2022Q3**: 2022Q3 bulletin lists 6.51% (UEMOA), 6.06% (Côte d'Ivoire), 5.70% (Senegal); 2023Q3 vintage lists **6.54%, 6.08%, 5.79%**. The selected mixed panel uses the 2023Q3 vintage.
- **2025Q1: unresolved *large cross-vintage differences*.** The 2025Q3 bulletin table 3.1 gives UEMOA 6.80%, Côte d'Ivoire **6.78%**, Senegal **7.07%** whereas 2026Q1 vintage table 3.1 gives UEMOA 6.80%, Côte d'Ivoire **6.34%**, Senegal **5.93%**. For an internally coherent latest-available panel, this version selects 2026Q1 values **but flags that quarter**. The cause of 44bp/114bp differences is **unverified**; no imputation. Older bulletin: https://downloads.bceao.int/sites/default/files/2026-02/Bulletin-Trimestriel-des-Statistiques_3T2025_VF.pdf; newer: https://www.bceao.int/sites/default/files/2026-06/Bulletin-Trimestriel-des-Statistiques-mars-2026.pdf. **Any regression involving country heterogeneity must run a sensitivity analysis excluding 2025Q1**.
- **2025Q2–2026Q1**: 2026Q2 vintage contains known revisions from 2026Q1 vintage; preserve both original CSVs separately.
- **2026Q2** is marked provisional (`provisional`), not necessarily final.
- Do not compare the average annual levels from a report with the arithmetic mean of quarterly averages, because period loan origination volumes differ.

## Controls, identification and aggregation

- ECB Deposit Facility / BCEAO TMS at **calendar-quarter-end** are joined strictly from the existing end-of-month policy panel: March, June, September, December. This is a stock level, **not** quarterly average of effective daily rates. Only research as association, not automatic IV validity.
- Derive `delta_*` by simple quarter-over-quarter change, measured in **percentage points** (not basis points). A separate reported 100× multiplier expresses basis points.
- Sample size: 26 quarterly levels; 25 first differences; fewer for leads/lags; insufficient basis for a flexible country FE IV with many controls or claims of policy causality.
- Pooled region+two-country values aren't three independent units because UEMOA aggregate includes its member countries. **Do not use them as independent cross-sectional panel observations.**
- Before academic submission: (1) confirm cross-vintage changes with BCEAO; (2) secure CPI, exchange-rate regime, bank liquidity, sovereign spread/country macro controls; (3) pre-register time-series and sample splits; (4) obtain real aircraft lease transaction outcomes or keep conclusions limited to bank credit conditions.
