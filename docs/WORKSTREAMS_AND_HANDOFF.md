# AeroRisk-FR 工作流与跨聊天交接规程

**2026-10-16 最新决定：被解释变量 Y 改为西非法语区航空公司净利润（résultat net），旧飞机租金/残值 Y 不再是主论文目标。研究地区、ECB—BCEAO 金融主线、OHADA 法律政策不变。** 新的统一研究设计：[research_scope_revision_v2_2026_10_16.md](research_scope_revision_v2_2026_10_16.md)。如果旧版论文/法律/原型文档与 v2 冲突，优先以 v2 执行方案为准，原材料保留历史版本。

**2026-10-15 | 本仓库是唯一权威科研资料库。** ChatGPT 聊天是处理工作区，不是数据版本存储。

## 三条工作线及所有权

| Stream | ChatGPT 会话 | 负责目录 | 不应做 |
|---|---|---|---|
| ECON | 当前数据/计量/网站聊天 | `data/`, `src/`, `tests/`, `macro/`, `quarterly/`, `annual/`, `transmission/`, `prototype/` | 无理由覆盖 `legal/` 或作者已核对的论文正文 |
| LEGAL | 新建 OHADA 法语法律研究聊天 | `legal/` | 不把法定救济时限冒充飞机实际收回耗时；不直接覆写模拟模型 |
| PAPER | 新建论文与投稿聊天 | `paper/` | 不编造回归、判例、估值结论；不静默改动原始/处理数据 |

共享的 `README.md`、`docs/research_design_v1.md`、`docs/variable_dictionary_v1.csv` 由 ECON 主聊天统一维护，其他线程提出更新建议/新建各自文档，不要同时覆写。科研日志按目录独立维护：`docs/research_log.md`（ECON）、`legal/research_log.md`（LEGAL）、`paper/research_log.md`（PAPER）。

### 每次新聊天先做

1. 用 GitHub 连接读取 `README.md`、`docs/WORKSTREAMS_AND_HANDOFF.md`、**`docs/research_scope_revision_v2_2026_10_16.md`**（优先于旧版 v1）及必要时 `docs/research_design_v1.md` 和本方向对应文件，确认仓库最新状态。不要假设读得到另一个聊天的历史。
2. 检查来源公开、合法、许可，保留来源 URL、国家/发布日期、条款或表格编号、原始内容版本。
3. 改动前检查路径是否属于自己负责目录；跨目录需求先提建议，避免未经协调的同时编辑。
4. 每份“结果”说明哪些来自实测，哪些属于文本编码，哪些是假设与模拟；证据不足明确说未核实。
5. 提交后检查 GitHub Actions（Research validation）以及公开网页发布是否成功。编写大型功能或协同编辑时优先使用 branch/PR 并在合并前 review；如果直接提交 main，尤其注意别覆盖别人新提交的修改。
6. 文本判例与法条采集不能把版权不明的整份来源复制进公开仓库；记录链接、页码、标签、少量引用及授权信息即可。

### 关键学术边界

- ECB 与 BCEAO 的政策利率共同变化 ≠ ECB 货币冲击的可信因果识别。
- 26 个季度混合出版版本银行融资数据仍有修订，尤其 2025Q1；回归/图表必须标注。
- OHADA 2023 修订执行法在 2024-02-16 生效；其适用仍受过渡规则和实际程序日期制约。
- 《开普敦公约》航空器议定书下的**声明法定时限** ≠ 实际飞机收回周期。
- 新 Y = 航司年度净利润（net income / résultat net）；辅助标准化指标 = 净利润率。Air Côte d'Ivoire 政府报告目前仅核验 2019–2023 一家公司财务记录；不能把 26 个 BCEAO 季度观测冒充 26 个利润观测。
- 市场租金、飞机残值、实际收回成本仍**未取得**交易/案例级直接观测；原模拟器仅作为附属旧项目演示，不再是主论文结果。

## 阶段交付定义

- ECON：官方控制变量来源+连续 26 季度数据验证、完整模型假设及敏感性分析。
- LEGAL：官方法条与 UNIDROIT 国别声明核验、法语法律文档元数据、严格编码手册、判例检索可行性。
- PAPER：按 v2 航司净利润 Y 修改论文标题和章节方案；任何旧稿的租赁定价主线应归档，直至真实航司财务数据足以支撑比较或计量后再写最终 results/conclusion。

GitHub: https://github.com/leamya123/aerorisk-fr-research
