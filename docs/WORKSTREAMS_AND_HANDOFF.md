# AeroRisk-FR 工作流与跨聊天交接规程

**2026-10-15 | 本仓库是唯一权威科研资料库。** ChatGPT 聊天是处理工作区，不是数据版本存储。

## 三条工作线及所有权

| Stream | ChatGPT 会话 | 负责目录 | 不应做 |
|---|---|---|---|
| ECON | 当前数据/计量/网站聊天 | `data/`, `src/`, `tests/`, `macro/`, `quarterly/`, `annual/`, `transmission/`, `prototype/` | 无理由覆盖 `legal/` 或作者已核对的论文正文 |
| LEGAL | 新建 OHADA 法语法律研究聊天 | `legal/` | 不把法定救济时限冒充飞机实际收回耗时；不直接覆写模拟模型 |
| PAPER | 新建论文与投稿聊天 | `paper/` | 不编造回归、判例、估值结论；不静默改动原始/处理数据 |

共享的 `README.md`、`docs/research_design_v1.md`、`docs/variable_dictionary_v1.csv` 由 ECON 主聊天统一维护，其他线程提出更新建议/新建各自文档，不要同时覆写。科研日志按目录独立维护：`docs/research_log.md`（ECON）、`legal/research_log.md`（LEGAL）、`paper/research_log.md`（PAPER）。

### 每次新聊天先做

1. 用 GitHub 连接读取 `README.md`、`docs/WORKSTREAMS_AND_HANDOFF.md`、`docs/research_design_v1.md` 和本方向对应文件，确认仓库最新状态。不要假设读得到另一个聊天的历史。
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
- 市场租金、飞机残值、实际收回成本仍**未取得**交易/案例级直接观测；模拟器默认参数是场景假设。

## 阶段交付定义

- ECON：官方控制变量来源+连续 26 季度数据验证、完整模型假设及敏感性分析。
- LEGAL：官方法条与 UNIDROIT 国别声明核验、法语法律文档元数据、严格编码手册、判例检索可行性。
- PAPER：可追溯文献矩阵、摘要/研究问题/章节骨架，直到可核验的真实实证输出出现后再写最终 results/conclusion。

GitHub: https://github.com/leamya123/aerorisk-fr-research
