> **当前全项目方向（2026-10-24）**：《云程有数：西非法语区航空业的制度开放与金融约束研究》，包含航空市场准入与法律、ECB/BCEAO 金融环境与航司盈利、尚待验证的综合机制。原立项题名及待审批状态保留；见[全项目概览](../v3/README.md)。 下文为历史阶段文档，保留原内容，不作为当前整体范围。

# AeroRisk-FR 研究设计 v0.1（2026-10-15）

> **定位**：这是基于 2026 年 4 月立项书重新整理的“可执行设计”，不是已完成的实证结果，不声称已获取交易级飞机租金/残值数据。

## 1. 总体问题与可检验的子问题

原题：货币互联、制度摩擦与跨境资产定价——欧央行利率冲击对法语区航空租赁的影响研究。

- **RQ1（可以先完成的实证）**：2020–2026 年 ECB 政策利率变动与 WAEMU/BCEAO、CEMAC/BEAC 货币政策之间存在何种方向、滞后期与非对称性？货币钉住不等于政策利率机械同步。
- **RQ2（法语法律文本与机构背景）**：不同国别在 OHADA 统一法、《开普敦公约》及其航空器议定书的适用、声明、执行实践上，能否找到可核验的差异？可否编码为一套有来源的制度机制表？
- **RQ3（仿真而非已识别事实）**：给定折现率、违约率、收回延迟、回收折价等显式假设，所需收支平衡月租金对风险参数有多敏感？
- **条件性 RQ4（仅拿到合规真实资产数据后）**：货币政策变动、本地利率、法律环境能否解释真实飞机租金、违约回收、资产价值的观测变化？缺乏真实观测值时不得把模拟输出当作因变量。

## 2. 两条研究线（不要混成一个“2SLS 因果结论”）

### A. 数据实证：ECB → BCEAO/BEAC 传导

- 数据单位：月；范围先定 2020-01 至可得最新完整月。存储真实日期、原始单位、政策生效日期、原始网址、下载日期。
- 因变量：BCEAO 最低投标利率、BEAC 主要政策利率；补充（若可得）货币市场、银行融资价格。
- 主要自变量：ECB deposit facility rate / MRO rate（分别定义）；不要把两种利率混在同一列。
- 方法递进：时序图→描述统计→滞后互相关（非因果）→考虑结构断点的分布滞后模型/事件分析（标注假设）→稳健性。
- 关键挑战：2024 年 ECB 已降息而 BCEAO 全年保持政策利率不变；观察其反应速度而非预设完全同步。
- 若检验 ECB 政策意外：须明确冲击识别来源与排除限制。ECB 可以直接影响全球租赁融资成本，不能因为其相对非洲单个企业“外生”就认定是有效 IV。
- 预先确定区分 WAEMU/BCEAO、CEMAC/BEAC；汇率均对欧元挂钩不意味着两央行政策相同。

### B. 法律参数 × 定价仿真

- 法源：OHADA 2023 revised uniform act on simplified recovery & enforcement（2024-02-16 生效），OHADA security interests act，UNIDROIT Aircraft Protocol 的批准和国别声明。
- 案例/判例：逐份整理案号、审级、作出日期、执行日期、涉及资产、适用规则、链接。只有判决文书里有明确日期和资产类别，才计算实际执行期限。
- WJP Civil Justice 可作**一般司法质量代理**；不能直接等同飞机收回耗时，也不能据此得出 12–18 个月。
- 建立 2 层变量：可验证的国别法律制度事实；待校准的收回延迟、维护/保险费、回收折价假设。不要用关键字频次“自动”生成可校准的金融损失率。
- 理论模型：固定条件月违约概率 q = 1 - (1-PD_annual)^(1/12)，每月存续租金用 S_m=(1-q)^m 加权。违约月份的预期回收按法律延迟、停场费用与折价估值，期末残值仅按存续概率计入。
- 收支平衡月租金 = (初始购价 - 期末存续残值现值 - 默认回收现值)/预期租金年金现值系数。实现于 `src/risk_model.py`。折现率为场景中输入的定价/资本机会成本，不直接等于 ECB 公开政策利率。
- 这是研究透明的简化模型，非市场报价模型、资本监管公式或商用估值意见。

## 3. 开题材料需修订的可证事实

1. “2024 年持续加息”不准确：ECB 2024-06 已开始降息。参考 ECB 官方利率序列。
2. “固定汇率→BCEAO 必须同步改政策利率”不成立；BCEAO 官方 2024 报告明确全年主要政策利率为 3.5%。
3. “12–18 月司法执行周期”“具体塞内加尔航司 18 个月收回案例”在提供的材料中没有足够来源证实：标记 **unverified**，仅可用于虚拟场景说明。
4. “ECB 作为 IV 可精准识别租金”需排除限制与真实资产级观测数据，否则不可宣称因果结论。
5. 要核对新修 OHADA 强制执行法（生效 2024-02-16），不得仅依赖 2010 年旧《担保法》概括所有收回程序。
6. 法国 DGAC 并非 WAEMU 国家飞机登记和司法程序的统一主管机关；应按国别核查航空主管部门与适用法律。

## 4. 研究进度建议

| 截止 | 产物 | 验收方式 |
|---|---|---|
| 2026-10 下旬 | 仓库可运行、变量字典、来源清单、宏观利率原始数据（先 ECB、BCEAO） | 数据行可追溯源链接；程序自动测试通过 |
| 2026-11 上旬 | ECB–BCEAO 首版传导图、滞后探索结果；BEAC 数据可行性报告 | 图由真实数据生成，清楚标识时滞/频率 |
| 2026-11 下旬 | OHADA 法条与 UNIDROIT 国别矩阵、10–20 份核验后的法律文本标注记录（目标，非已有） | 双语逐条出处/适用范围记录 |
| 2026-12 | 中期报告、误差分析与平台 v0.2 | 结果表可复算、不使用虚构“实证” |
| 2027-01–03 | 论文初稿、敏感度/稳健性分析和导师修改 | 原始数据/图/代码/附件同步 |
| 2027-04–05 | 投稿可行稿、结题答辩、可复现项目归档 | 不夸大投稿级别/发表状态 |

## 5. 是否能写成一篇论文的检验门槛

- 若仅有央行利率+法律背景+模拟定价：论文主张应是“金融传导的经验事实与制度风险定价的透明框架”，不是“真实飞机租金的因果效应”。
- 若获合规月度真实租金/价值数据：才讨论航空租赁定价的实证结果（优先考虑可比飞机型号、币种、租龄、时间、承租方风险等）。
- 若模型拟纳入机型比较：必须取得具可比性且来源合法的飞机购价、残值、维护成本等，不能把任意假设当作 C919/C909 对 A320/B737 的性能优劣。

## 6. 官方来源入口（访问、许可、版本需复核）

- ECB key rates https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html
- BCEAO 2024 annual report https://cofeb.bceao.int/sites/default/files/2025-07/BCEAO%20ANNUAL%20REPORT%202024%20%28Summarised%20Version%29.pdf
- BCEAO monthly statistics https://www.bceao.int/
- BEAC decisions https://www.beac.int/politique-monetaire/decisions-de-politique-monetaire/
- OHADA uniform acts https://www.ohada.org/actes-uniformes/
- OHADA revised enforcement act https://www.ohada.org/organisation-des-procedures-simplifiees-de-recouvrement-et-des-voies-dexecution/
- UNIDROIT Aircraft Protocol contracting states https://www.unidroit.org/instruments/security-interests/aircraft-protocol/states-parties/
- WJP Civil Justice methodology https://worldjusticeproject.org/rule-of-law-index/about
- SMBC Aviation Capital (2025) Push and pull factors on lease rates — for conceptual industry mechanism, NOT raw lease quotes.
