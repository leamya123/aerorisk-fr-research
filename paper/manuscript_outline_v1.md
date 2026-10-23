> **当前全项目方向（2026-10-24）**：《云程有数：西非法语区航空业的制度开放与金融约束研究》，包含航空市场准入与法律、ECB/BCEAO 金融环境与航司盈利、尚待验证的综合机制。原立项题名及待审批状态保留；见[全项目概览](../v3/README.md)。 下文为历史阶段文档，保留原内容，不作为当前整体范围。

# Paper master outline v0.1 · 2026-10-15

**Working title (provisional):**
Monetary Policy Transmission, Legal Enforcement Frictions, and Aircraft Leasing Risk in Francophone West Africa: A Data-Driven and Scenario-Based Framework

**中文备选：**货币互联、法律执行差异与跨境航空租赁风险定价：西非法语区的金融证据和情景分析

## Academic positioning
研究论文+模型可复现应用。切勿声称目前已观察到飞机市场租金或航空器司法收回周期。首选清楚划分描述性银行利率证据、待核验法律机制、理论情景模拟。

## Draft sections and evidence requirements

1. **Introduction**：固定汇率安排是否意味着信贷成本同步？航空租赁资产为什么更受融资与收回风险影响？列明真正的 gap 和贡献边界，待补真实文献与可引用出版研究。
2. **Institutional setting**：ECB、BCEAO、XOF/欧元固定汇率、UEMOA 银行市场；OHADA 统一执行法与 2024 修订；Cape Town Convention Aircraft Protocol 国别声明（按国家和日期）。
3. **Conceptual framework**：资金成本→借款人融资条件→违约风险、残值/回收，制度摩擦可能影响损失率；识别额外的全球租赁融资直接路径。
4. **Data and validation**：ECB 与 BCEAO 官方政策利率；26 季度（2020Q1–2026Q2）UEMOA/科特迪瓦/塞内加尔平均银行贷款利率；混合 vintage 并标记 2025Q1 数据修订；以后增 CPI/银行间货币市场利率等。
5. **Empirical descriptive evidence**：时序图、政策/贷款利率变化、版本敏感性、时滞描述。只在完善控制变量和采样诊断后才做探索性简约回归，不预设因果。
6. **OHADA legal-text research**：法条与国际议定书/国别声明，制度编码的规则与有效性检验。不要把 Article X 中 10/30 天法定救济期限说成真实收回时长。
7. **Aircraft leasing scenario model**：公开假设的违约期望现金流、回收折价、法律延迟、压力测试，不把模拟场景当观测租金。
8. **Discussion and limitations**：真实飞机租金/残值资料与判例级观察的缺口；固定汇率不代表政策同步；小样本与版本修订；制约识别、法律适用差异。
9. **Conclusion**：只有在数据支撑的范围内总结，不用过大“打破英美法定价垄断”式政策结论。

### Papers & resources currently in repo
- `paper/quarterly_preanalysis_2026_10.md` — exploratory quarter-on-quarter lag correlations with n and vintage cautions.
- `docs/quarterly_lending_panel_audit_v1.md` — source/vintage tracking.
- `legal/evidence_registry_v1.csv` — official legal rule facts, not case outcomes.

**Next author decisions required before writing a full manuscript**：投向英文还是中文期刊？期刊学科定位（financial economics / aviation finance / law & economics / applied computational legal studies）？能否取得合规真实飞机租约与残值数据？如果没有，题目和论文声称范围必须收窄。

## Author integrity
- No invented references, p-values, coefficients, aircraft leasing contract records or successful submissions.
- Each figure/table must state data source, release vintage, observation period and code.
- Claims about legal deadlines must identify the relevant treaty/section, country, calendar vs working days, and distinction between legal rules and observed outcomes.
