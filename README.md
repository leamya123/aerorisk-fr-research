# AeroRisk-FR · 西非法语区航空公司财务盈利研究

**2026-10-16 · 研究范围调整 v2（经金融导师讨论，待确认学校的正式变更流程）**

**当前论文执行方案：仅更换被解释变量 Y**，从“飞机租赁价格／残值”改为“西非法语区航空公司净利润（résultat net）”；ECB 政策利率、BCEAO 金融传导、OHADA 法律政策和原研究地区均保留。使用净利润率作辅助规模标准化，不声称已获得可回归的完整企业面板。

**[必须先读：研究范围调整 v2](docs/research_scope_revision_v2_2026_10_16.md)** · [首批核验财务数据（Air Côte d'Ivoire 2019–2023）](data/official/airline_financials_candidate_v1.csv) · [财务变量字典](docs/airline_financial_variable_dictionary_v1.md)

原立项题目与租赁估值演示、旧版研究设计均保留为**历史材料/辅助演示**，不作为新论文的资产租金因果证据。

## 协作入口

**同一个 ChatGPT「航空大创」Project 分三条聊天工作线**：本聊天负责数据/计量/平台，OHADA 法律文本聊天专管 `legal/`，论文与投稿聊天专管 `paper/`。共同规则见 [跨聊天协作与交接](docs/WORKSTREAMS_AND_HANDOFF.md)。

- [法律来源登记（含 OHADA 2024 法版本与 UNIDROIT 国别声明）](legal/evidence_registry_v1.csv) — 有出处的**法定规则**，没有观测到的实际飞机收回天数
- [法律判例标注模板](legal/case_coding_template_v1.csv) — 暂无经过核验的航空器实际收回案例
- [旧版论文结构](paper/manuscript_outline_v1.md) — 2026-10-16 前的资产定价研究思路，**已被新 Y 方案取代**；最新研究范围见上方 v2 文件
- [下一步宏观控制变量采集规程](docs/ECON_next_sprint_2026_10.md) — 银行间利率、通胀、GDP 与信用流动性来源计划（尚未收集完整样本）

这个公开仓库用于完成本科创新训练项目《货币互联、制度摩擦与跨境资产定价：欧央行利率冲击对法语区航空租赁的影响研究》。

## 在线演示

- **[AeroRisk-FR 风险模拟器](https://leamya123.github.io/aerorisk-fr-research/prototype/)** — 假设情景的预期现金流、月租金与法律延迟压力测试，**不等于市场报价**
- **[2020Q1—2026Q2 连续季度实证数据库](https://leamya123.github.io/aerorisk-fr-research/quarterly/)** — UEMOA/塞内加尔/科特迪瓦 26 季银行贷款成本，附所选公报版本、季末 ECB/BCEAO 及第一差分
- **[2020–2025 年度信贷数据](https://leamya123.github.io/aerorisk-fr-research/annual/)** — 6 年 × 7 组 BCEAO 官方银行信贷成本系列（UEMOA、科特迪瓦、塞内加尔、贷款用途）
- **[真实融资传导观察](https://leamya123.github.io/aerorisk-fr-research/transmission/)** — 官方 BCEAO 一周流动性招标利率与 UEMOA / 塞内加尔 / 科特迪瓦银行贷款利率（分别展示月度、季度数据）
- **[真实宏观利率观察](https://leamya123.github.io/aerorisk-fr-research/macro/)** — ECB 与 BCEAO 官方利率生效日期整理、月末对比图和可下载的可复现 CSV

## 研究状态（仅描述已完成成果）

| 模块 | 进展 | 数据类型 |
|---|---|---|
| ECB DFR/MRO | ✅ 官方政策利率事件 21 条 | 真实官方公布值、手动转录 |
| BCEAO TMS/边际贷款 | ✅ 官方政策利率事件 10 条 | 真实官方公布值、手动转录 |
| 月末央行政策利率面板 | ✅ 2020-01 至 2026-09，81 个月 | 由上两份事件 CSV 按生效日生成 |
| CPI / 银行间资金利率控制变量 | 🗂️ 官方入口与采集方案已登记 | 2020—2026 连续数据未收集，不宣称已进入回归 |
| BEAC 历史政策利率 | ⏳ 官方入口已定位，未加入时间序列 | 尚未核验完整历史表 |
| OHADA 执行制度 | 🔎 已登记 2024 生效法与两国航空器议定书声明，判例待查 | 法定临时救济时限不等于实际飞机收回天数 |
| 航司净利润与营业收入（新 Y） | 🔎 已核验 Air Côte d'Ivoire 2019–2023 报告图表及 2022–2023 叙述数字 | 仅 1 家航司 × 5 年，未达到可靠计量回归所需的样本覆盖 |
| 飞机租金/残值（旧 Y） | 🗄️ 仅保留旧项目的演示模型，不再是主论文 Y | 不把租金情景模拟误当利润实测 |
| 风险模拟 | ✅ 可交互、可导出、可单元测试 | 假设情景，非观测数据 |

## 项目目录

- `docs/research_scope_revision_v2_2026_10_16.md`：**当前优先生效的研究设计**；新 Y = 航司财务净利润
- `data/official/airline_financials_candidate_v1.csv`：科特迪瓦官方报告中 2019–2023 年航司净利润和营收（带精度标签）
- `prototype/index.html`：原租赁风险情景模型（辅助演示，非新 Y）
- `macro/index.html`：官方宏观数据走势图（非因果结论）
- `data/official/ecb_policy_events.csv`：ECB 日期生效数据与官网链接
- `data/official/bceao_policy_events.csv`：BCEAO 日期生效数据与官网链接
- `data/official/README.md`：数据转录来源、口径、待核查项
- `data/processed/central_bank_policy_monthly_v1.csv`：加工后的月末值
- `data/official/bceao_lending_quarterly_2020q1_2026q2_selected_vintages.csv`：26 季度连续贷款利率（来源版本可追溯）
- `data/processed/quarterly_policy_lending_panel_v1.csv`：贷款利率与 ECB/BCEAO 季末政策利率合并数据
- `src/build_quarterly_panel.py`：季度面板重建；`src/explore_quarterly_lags.py`：非因果相关诊断
- `docs/quarterly_lending_panel_audit_v1.md`：不同公报数字冲突与修订清单
- `data/official/bceao_annual_lending_2020_2025.csv`：BCEAO 2025 年年度报告的 2020—2025 回溯加权贷款利率
- `src/build_annual_lending_summary.py`：自动计算国别、贷款类型 2024—2025 变化量
- `data/official/bceao_weekly_auction_monthly.csv`：BCEAO 一周流动性招标利率，2024-07 至 2026-03
- `data/official/bceao_bank_lending_quarterly.csv`：UEMOA 银行贷款利率（及塞内加尔/科特迪瓦），2024Q4 至 2026Q1
- `src/build_financing_summary.py`：可复算 BCEAO 融资指标描述统计
- `src/build_macro_panel.py`：只用 Python 标准库重建 81 个月数据
- `src/risk_model.py`：飞机租赁模拟模型
- `tests/`：模型与官方利率数据自动校验
- `docs/research_design_v1.md`：论文研究问题与识别边界
- `docs/variable_dictionary_v1.csv`：数据字典
- `docs/research_log.md`：研究日志
- `paper/`：论文工作区

## 本地复现

需要 Python 3.9+，不要求任何第三方 Python 依赖：

```bash
python src/build_quarterly_panel.py
python src/explore_quarterly_lags.py
python src/build_annual_lending_summary.py
python src/build_macro_panel.py
python src/build_financing_summary.py
python -m unittest discover -s tests -v
```

`src/build_macro_panel.py` 将从两份官方政策事件 CSV 重建月末政策面板；提交的面板文件必须与再生成输出逐字节一致。

## 科研边界

1. ECB 与 BCEAO 数据是**官方政策利率水平**的人工转录，不是政策意外冲击的识别结果；月末值不是月平均值。
2. 固定汇率制度不必然导致 BCEAO 或 BEAC 与 ECB 同步调整政策利率。
3. 不能仅因“ECB 对航司外生”便称其为有效 IV；净利润由汇率、航油、客流、政策、补贴、疫情等共同决定；当前 1 家公司 5 年观察不足以开展可信因果回归。
4. WJP 的 Civil Justice 分数 ≠ 飞机司法收回延迟，12/18/36 个月等暂仅为假设情景。
5. 严禁将 WRDS、Cirium 等受许可的数据，个人信息或未公开采访材料上传公共仓库。
6. 论文证据与平台情景模拟始终分开展示，引用时注明出处、查询日期及处理脚本。

**下一步（按 2026-10-16 调整）：**优先完成西非航空公司逐年净利润和收入可获得性矩阵，将净利润 Y 与财务口径核对；同时保留 ECB/BCEAO 金融和 OHADA 法律研究。只有获得足够可比公司年样本，才讨论相应回归。