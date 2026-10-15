# BCEAO: 真实货币市场成本与客户贷款利率数据（2026-10-15）

**来源（官方 PDF）**：[BCEAO Bulletin Trimestriel des Statistiques — Premier trimestre 2026](https://www.bceao.int/sites/default/files/2026-06/Bulletin-Trimestriel-des-Statistiques-mars-2026.pdf)

| 表格 | 官方印刷页码 | 数据窗口 | 指标定义 |
|---|---|---|---|
| Tableau 1.2 Taux du marché monétaire | 第 4 页（PDF p.5） | 2024-07—2026-03，21 个**月度**记录 | 一周流动性注入操作的加权平均利率（Taux moyen pondéré du marché monétaire）与边际平均利率；是 BCEAO 银行流动性**招标成交**条件，不是商业银行间拆借利率，也不是航空公司融资成本 |
| Tableau 3.1 Taux d'intérêt débiteurs des crédits bancaires | 第 12 页（PDF p.13） | 2024Q4、2025Q1—Q4、2026Q1，6 个**季度**记录 | 银行向客户发放贷款的期间平均利率：UEMOA 全区、科特迪瓦、塞内加尔；UEMOA 总体平均未必是两个国家的简单均值 |

**重要差异**：政策利率（TMS）、一周流动性注入中标加权平均利率、银行间一周利率、商业银行实际贷款利率，是四种**不同**的时间序列。前两者分别在 `data/processed/central_bank_policy_monthly_v1.csv` 与 `data/official/bceao_weekly_auction_monthly.csv`；第四者在 `data/official/bceao_bank_lending_quarterly.csv`。

**核查记录**：数据为人工逐行转录自官方 PDF 的表 1.2 和表 3.1；逐项按印刷页码核对。所有百分率均以年化利率％计；变动由百分点换算为基点（1 pp = 100 bp）。表 3.1 的 2026Q1 在官方原表带星号，是**暂定数据**。

**不得推断**：从两条不同频率时间序列的端点差异不能推出同一单位货币政策冲击的银行传导系数；也不能把 UEMOA 平均银行贷款利率当作航空公司真实租赁费率。

**更严谨的后续研究**：扩展样本、加入银行间 1 周拆借实际利率、按季度匹配各央行月末或季度均值（两种口径稳健性）、加入国家层面通胀、增长、银行信贷供给与政府债务融资控制变量后再讨论传导模型。最终仍需真实航空租赁资产级数据才能声称微观资产定价效应。
