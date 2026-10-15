# BCEAO 银行贷款利率：官方出版版本（vintage）与修订的审计记录

**日期：2026-10-15。** 实证表必须保存原始“发行版本”（publication vintage），不能将不同时间发布的数值混为同一无修订时间序列。

## 三个相互独立的统计出处

- 原有 `data/official/bceao_bank_lending_quarterly.csv`：BCEAO *Bulletin Trimestriel des Statistiques — 2026Q1*，印刷第 12 页表 3.1（`2026Q1 vintage`），2024Q4、2025Q1—Q4、2026Q1。
- 新增 `data/official/bceao_bank_lending_vintage_2026q2.csv`：BCEAO *Bulletin Trimestriel des Statistiques — 2026Q2*，2026-09-15，表 3.1 印刷第 12 页；时间点 **2024Q4、2025Q2、Q3、Q4、2026Q1、Q2**（2025Q1 在该表中未列示；绝对不能猜测/插值）。https://www.bceao.int/sites/default/files/2026-09/Bulletin%20Trimestriel%20des%20Statistiques%20-%20juin%202026.pdf
- 另一独立出版物 `data/official/bceao_annual_lending_2020_2025.csv`：BCEAO *Rapport annuel sur les conditions de banque – 2025*，2026-09-25 发布，地区年度报告，印刷第 23、34、46、62 页。报告回溯 2025 年区域年平均值为 **6.69%**，但 2026Q2 季度公报表 3.1 列 2025 年总体年均 **6.73%**。**尚未证实差异来源，不能默默合并这两份年均值。**

## 关键修订示例（两个季度公报）

| 指标季度 | 2026Q1 公报版本 | 2026Q2 公报版本 | 新-旧 |
|---|---:|---:|---:|
| 2026Q1 UEMOA 总体贷款利率 | 6.72% | 6.70% | −2bp |
| 2026Q1 科特迪瓦贷款利率 | 6.06% | 6.08% | +2bp |
| 2026Q1 塞内加尔贷款利率 | 6.32% | 6.24% | −8bp |
| 2025Q4 UEMOA 总体贷款利率 | 6.73% | 6.71% | −2bp |
| 2025Q3 UEMOA 总体贷款利率 | 6.67% | 6.63% | −4bp |

2026Q2 第一次发布的暂定值：UEMOA 总体 **6.67%**、科特迪瓦 **6.26%**、塞内加尔 **6.22%**。

## 论文处理方案

1. 先按报告发布日期留存 `source_vintage`，不能在原 CSV 上直接替换旧值。
2. 未来季度汇总表选择一个**可说明的主数据版本**（例如各期最新可得版本），并记录其选择规则、未修订例外及结构性定义差异。
3. 稳健性检验在 `first-release` 与 `latest-available` 版本间运行一致口径的描述性比较；出现变化时直接报告。
4. 年度平均与季度均值不保证等于季度简单算术平均，尤其是新发放银行贷款的加权平均利率。区分年度统计母体、加权方案和修订。
5. 仅将确认真实金融交易与合同数据的变量送入航空租赁资产定价实证。任何未知缺口一律标 `missing` 而非插值。

> Status: Vintage reconciliation **open**; annual report and quarterly bulletin 2025 annual aggregate mismatch **unresolved**. Further official clarification needed; do not claim a single canonical “2025 rate” across documents.
