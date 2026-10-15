# AeroRisk-FR · 法语区航空租赁风险研究

**2026-10-15 · Open research prototype v0.4 (央行政策 + 资金成本传导 + 风险模拟器)**

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
| BEAC 历史政策利率 | ⏳ 官方入口已定位，未加入时间序列 | 尚未核验完整历史表 |
| OHADA 执行制度 | ⏳ 待法律条文逐条标注 | 2024 年生效的新执行法已确认为基本资料 |
| 飞机真实租金/残值 | ❌ 暂无合法可公开的交易级数据库 | 不得假装已有数据 |
| 风险模拟 | ✅ 可交互、可导出、可单元测试 | 假设情景，非观测数据 |

## 项目目录

- `prototype/index.html`：租赁风险交互网页（假设参数）
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
3. 不能只因“欧央行相对非洲航司外生”就将其视为满足排除限制的工具变量；真实市场租金因变量尚未获取。
4. WJP 的 Civil Justice 分数 ≠ 飞机司法收回延迟，12/18/36 个月等暂仅为假设情景。
5. 严禁将 WRDS、Cirium 等受许可的数据，个人信息或未公开采访材料上传公共仓库。
6. 论文证据与平台情景模拟始终分开展示，引用时注明出处、查询日期及处理脚本。

**下一步：**核验 BEAC 政策决议序列；加入 BCEAO 实际市场融资成本、欧元区宏观控制变量；严格区分政策利率共同变化与因果冲击传导。