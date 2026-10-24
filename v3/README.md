# 云程有数：西非法语区航空业的制度开放与金融约束研究

中期答辩：2026-10-28。当前项目范围包含三个模块：

完整文字资料：[进展报告、12页PPT内容、讲稿及22个问答](../docs/midterm_20261028/content.md) · [可离线打开的答辩网页](../docs/midterm_20261028/index.html)。本目录提供交互展示，文字包提供汇报内容与来源，不把HTML文件已提交等同于已经公网部署。

1. **制度开放**：贝宁—塞内加尔准入制度、一般规则与个案授权的区别、KQ 候选案例；保留来源与 UNKNOWN。
2. **金融约束**：ECB/BCEAO 利率与银行贷款条件、Air Côte d'Ivoire 2019–2023 营收与净利润；沿用已有真实数据和金融页面。
3. **交叉整合**：制度与融资条件可能共同影响经营的机制假说，尚无因果识别或可用的联结面板。

原立项／历史正式题名：《货币互联、制度摩擦与跨境资产定价：欧央行利率冲击对法语区航空租赁的影响研究》。题名变更待学校批准。法律子研究的 CONDITIONAL GO 不替代全项目范围。

## 研究递进与截图视图

- `v3/index.html#top`：完整项目与三模块范围，适合开场截图。
- `#legal`、`#evidence`、`#case`：法律对照、证据统计、KQ UNKNOWN 边界；既有证据保持原分类。
- `#finance`：ECB/BCEAO、贷款条件入口及一幅公司财务图；图内标签保留两位小数，表格保留 CSV 原值与逐行精度。
- `#progression`：已完成金融基础、已完成法律证据基础、未来整合假说；附六个原有演示入口。

金融已完成数据与描述性计算；法律已完成证据基础设施与初步文本比较。许可、实际载运、公司借款成本、更多同口径财报及控制变量仍待补证，不能以缺失填 0、据条文打开放评分，或把利率变化当作利润原因。


## 在线与本地访问

- GitHub Pages 在明确部署本分支后（当前不保证已部署）：`https://leamya123.github.io/aerorisk-fr-research/v3/`
- 本地联网预览：在仓库根目录运行 `python -m http.server 8000`，打开 `http://localhost:8000/v3/`
- 断网答辩：直接双击 `v3/offline.html`。页面、法律证据、财务快照和 SVG 图均已内嵌，不使用 CDN 或联网 fetch。官方来源链接仍需网络；相对路径的原有金融演示需保留完整仓库目录，并用本地 HTTP 服务查看。单独复制 offline.html 不包含其他演示页面。

## 重新生成

```bash
python studies/fifth_freedom_bj_sn/build.py
python v3/build.py
node scripts/validate_dashboard.js
python -m unittest discover -s tests -v
python -m unittest discover -s studies/fifth_freedom_bj_sn -p "test_*.py" -v
```

最新本地复验：30 项仓库测试、6 项法律证据测试及前端 9 个 HTML 页面校验均通过；v3 展示测试现为 6 项（新增 Git 换行检出测试）。最新远端 CI 结果需按 PR 最新提交核验，不能沿用旧交付记录。Windows 双击 `offline.html` 仍需在最终答辩电脑断网复核。

`v3/data/evidence.json` 是给页面和后续图表协作使用的稳定数据接口。上游唯一来源为 `studies/fifth_freedom_bj_sn/outputs/evidence.json`，请勿手改生成文件。

## 数据接口约定

- `counts`：六类研究材料计数。
- `data.sources`：来源登记，`document_id` 为主键，含 `official_url` 与 `verification_status`。
- `data.articles[*].source_id`：法律条文映射到来源。
- `data.routes[*].source_id`：航线审计映射到来源。
- `data.chains[*].source_ids`：分号分隔的证据链来源。
- 未取得的许可和当地商业载运证据必须保留字符串 `UNKNOWN`，不能转为 `true`、`0` 或“已批准”。

## 答辩操作

1. 首页先说明完整项目的制度、金融与交叉研究三模块，再说明“区域开放承诺不等于个案许可”。
2. 在法律对照区点击贝宁或塞内加尔筛选，再点击卡片底部官方来源。
3. 在数据证据区解释 18 行是审计记录，不是 18 条已核实第五航权航线。
4. 在 Kenya Airways 案例区明确指出：开航陈述已交叉印证，但具体许可与当地付费载运仍为 `UNKNOWN`。

5. 金融区说明五个年度公司观测与银行宏观面板不能混为企业样本。
6. 研究递进区区分已完成基础与尚待检验的机制。

## DS 协作接口（本次不改变法律 schema）

既有 `data/evidence.json` 与 `window.AERORISK_EVIDENCE` 的六类对象、字段、计数单位和 UNKNOWN 语义保持不变。财务独立使用 `window.AERORISK_FINANCE = {source, rows}`（`data/finance.js`），`rows` 按原 CSV 逐列逐字符串保留，包括 `measurement_precision`、`financial_statement_audit_status`、`notes` 和来源页码；不写入法律计数。`data/airline-financials.svg` 也由同一 CSV 构建；构建审计记录其输入 SHA-256。不要手改生成快照。

本说明为 DS 交接记录，尚未获得 DS 团队确认；本会话未向团队发送消息。未来更改年份覆盖、字段、连接键或分类前，由 DS 团队确认 schema 与观测粒度；不可静默合并季度与年度数据。

## 分支发布与安全访问

答辩前最稳妥的备份是下载本分支的完整 ZIP、解压并打开 `v3/offline.html`，所有法律和金融新内容均可断网展示。六个原始演示保留在原路径；完整交互请在根目录启动 Python HTTP 服务。GitHub 文件预览不是网页部署。

不更改 main 或现有 Pages 设置。若确需在线分支预览，优先独立的临时预览部署，需明确授权与可用部署环境；若要更改现有 Pages 发布源或合并至 main，应先征得许可。任何 PR 保持 draft，不合并。当前未声称已完成公网部署。

实际验证、限制与结果见 [2026-10-24 验证记录](../docs/verification_20261024_v3.md)；六幅截图在 [screenshots/](screenshots/)。

## PR #1 合并前修复（2026-10-24）

离线版提供“下载证据 JSON”与“返回页首”两个实际可用操作。操作说明保留在本 README 和交接包中，不在展示页内展开；展示页不放内部操作说明按钮。原始财务表独立内嵌，不混入法律 schema。

根首页现为完整课题导航；原首页所跳转的租赁原型仍在 `prototype/`，五个独立金融／情景演示目录保持不变。当前 PR 保持 Draft，等待研究者最终确认；[合并前检查与发布方案](../docs/premerge_review_pr1_20261024.md)记录远端 CI、资产保留、公开资料审查和部署边界。

## 金融源字节跨平台一致性

`financial_source_sha256` 继续使用源 CSV 的原始字节 SHA-256，不做忽略差异的哈希处理。`.gitattributes` 将 `data/official/airline_financials_candidate_v1.csv` 固定为 `text eol=lf`，确保 Git 在 Windows 与 Linux 检出相同字节；请勿用编辑器将该文件另存为 CRLF 后提交旧审计。修改后须先重建，再检查产物差异。

[本次故障与最终验收记录](../docs/v3_line_endings_acceptance_20261024.md)说明根因、36项测试与旧交付的对应关系。原金融数值、法律证据、截图、离线页面不因换行修复而改写。
