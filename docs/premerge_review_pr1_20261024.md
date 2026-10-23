# PR #1 合并前检查 · 2026-10-24

项目：《云程有数：西非法语区航空业的制度开放与金融约束研究》。制度开放与法律、金融环境与盈利、待验证的综合机制三个模块全部保留。原立项／历史正式题名及学校题名变更待审批状态不变。

检查对象：[Draft PR #1](https://github.com/leamya123/aerorisk-fr-research/pull/1)，基线 main `a5af45deba195e53debdefd74ee12de6fe3f21b2`。本次先同步研究者新增的完整中期包提交 `28f66fd`，再增量修复。未合并 main、未强推、未删分支、未将 PR 转为 Ready，也未更改 Pages 设置。

## 远端 GitHub Actions 与本地验证分开报告

开始检查时，PR 提交 `28f66fd` 的 [Research validation #65](https://github.com/leamya123/aerorisk-fr-research/actions/runs/40011682355) 中 [verify](https://github.com/leamya123/aerorisk-fr-research/actions/runs/40011682355/job/120613372516) 明确显示 succeeded（11 秒）。没有发现该次 CI 失败。公开页面提示 Actions Node 20 运行时弃用／强制迁移 Node 24，以及 ubuntu-latest 镜像迁移；这是提示，未当作测试失败。项目被测 Node 版本仍由 setup-node 设置为 22，不与 Actions 自身运行时混淆。

GitHub API 请求被当前云环境网络策略拒绝（CONNECT 403），因此改用可访问的 GitHub 公开 PR Checks 和 Actions 页面核验真实远端状态；没有据本地测试宣称远端成功，也没有绕过网络策略。修复推送后会再次检查 PR 最新 SHA 对应的实际结果；最终结论以该 SHA 的 Checks 为准，旧提交成功不覆盖新提交。

本次实际本地通过：

- 法律证据重建、v3 在线／离线快照与审计重建。
- 四个原金融构建脚本输出与 main CSV／JSON 一致；非因果季度滞后诊断执行完成。
- `python -m unittest discover -s tests -v`：29 项通过（含 5 项 v3 测试），无失败或跳过。
- `python -m unittest discover -s studies/fifth_freedom_bj_sn -p 'test_*.py' -v`：6 项通过，无失败或跳过。合计 35 项 Python 测试。
- `node scripts/validate_dashboard.js`：年度／季度功能、v3 在线与离线渲染通过；所有列入的 HTML 和外部脚本语法通过，包括完整中期报告页。
- Chromium 在 `/aerorisk-fr-research/` 项目子路径下验证：首页导航、租赁原型参数响应、宏观 DFR/MRO 切换、传导图、年度7行表、季度26行表、v3法条筛选、5年财务表和完整中期包。
- Chromium 禁网上下文直接加载自包含 HTML：实际点击下载，文件名为 `evidence.json`，解析内容与法律来源快照完全相同；点击“返回页首”和“查看离线说明”分别到 `#top`、`#offline-help`。无页面脚本错误。
- 390px 页面无整体横向溢出；财务图、表在自身容器内滚动。

管理型 Chromium 仍禁止 `file://` 导航；禁网加载HTML的验证不替代答辩电脑 Windows / Edge / Chrome 双击与投影实测。

## 具体修复与资产保留

1. **离线三个按钮**：下载证据 JSON 由原来的统计区锚点改为内嵌 data URL 下载；原“下载离线单页”在离线页改名“返回页首”；原“查看操作说明”改为“查看离线说明”，指向新增页内说明。在线页仍保留原下载离线 HTML／操作 README 功能。生成器与产物一起更新，并加入回归断言。
2. **测试数量与范围**：旧中期提纲“4项v3”修正为5项，完整命令与29＋6总数明确。paper README 移除把历史 v2 当当前整体方向的声明；其他 README 和历史研究设计／阶段报告增加当前三模块范围及历史文件标识，不覆盖原研究发现。
3. **首页**：原根首页只是租赁原型跳转，本次有意更新为完整项目导航；`/prototype/` 仍是原原型，不改其文件、逻辑和历史身份。首页、原型、宏观、融资传导、年度信贷、季度面板六个原访问路径均存在且验证可用。
4. **金融资产**：main 的 `data/official/*.csv`、可获得性矩阵、`data/processed/`、`prototype/`、`macro/`、`transmission/`、`annual/`、`quarterly/` 与分支逐字节相同。data目录只给 README 增加方向说明，不改数值与来源。
5. **法律资产**：原法律 CSV、分类、来源、法律JSON和输出快照不变；KQ具体许可与当地付费载运均 UNKNOWN。财务快照独立，不改变 DS 法律 schema，也不把不同频率数据拼作回归样本。
6. **历史**：main 是研究分支祖先，未发现 main 文件删除。原滞后诊断脚本在早期分支中仅增加 stdout UTF-8 初始化，不改计算。最终合并若获批准，应使用 **Create a merge commit**，避免 squash／rebase 丢失原提交结构；当前不执行合并。

## 公开资料与敏感内容审查

检查当前跟踪文件、相对 main 的新增文件、文本内容以及截图：未发现凭据、私钥、个人联系方式、证件信息或未授权的原始附件。库中没有 Word、PDF、PPT、Excel、ZIP、密钥或数据库附件；法语组材料是已授权整理的短篇Markdown／CSV，非原Word，完整原件由研究者另行保管。截图是仓库展示页，不含桌面或账户后台。

对私钥头、GitHub/API/AWS密钥特征、邮箱、手机号和证件号特征进行了扫描。长数字误报逐项确认来自 World Bank 公开文献URL的文档编号，并未改写原始来源。现有公共Git作者署名／提交邮箱属于历史元数据，未为本次审查重写Git历史。

这是有限内容审查，不构成自动证明全部版权或转载授权。法语组整理稿和引用使用权、署名方式仍由负责人确认；后续禁止提交受许可数据库、完整版权PDF、内部申报原件、私聊／采访原件或密钥。若历史中发现真正敏感值，应另行评估撤销凭据及历史清理，不能以本次安全合并名义静默重写历史。

## Pages 方案与合并后路径

[既有 Pages #83](https://github.com/leamya123/aerorisk-fr-research/actions/runs/38897360828) 的公开记录显示：main `a5af45d`，Status Success，部署地址为 `https://leamya123.github.io/aerorisk-fr-research/`。这是现有 main 的部署证据，不表示 PR 分支已上线。

最安全方案：保留现有 Pages 发布方式，**不把发布目录切成 `/v3` 或 `/docs`**，不另造覆盖既有站点的发布流程。负责人应在 Settings → Pages 确认发布源仍为 main 的仓库根目录（`/(root)`）；管理员设置本会话无法读取。若现有配置不同，先确认实际发布方式再调整，不能静默修改。

待研究者最终确认、以 merge commit 合并且 Pages 部署成功后，预计访问：

|内容|地址后缀（均接在上述站点根地址后）|
|---|---|
|全项目首页|`/`（根地址本身）|
|综合研究v3|`v3/`|
|自包含离线页|`v3/offline.html`|
|完整中期报告|`docs/midterm_20261028/`|
|原租赁情景原型|`prototype/`|
|宏观政策|`macro/`|
|融资传导|`transmission/`|
|年度信贷|`annual/`|
|季度面板|`quarterly/`|

本地已用项目子路径验证相对资源，不替代合并后的真实 Pages 验收。届时需查看 main 的 Research validation 和 Pages 部署结果，并对上述路径逐个实际打开；现阶段不把预期地址声称为新内容已上线。

## 人工确认清单

- 研究者最终批准合并，并选择 merge commit 保留完整提交历史；此批准尚未给出。
- 答辩电脑断网双击、JSON下载、Edge/Chrome和PPT投影实测。
- Settings → Pages 发布源／根目录确认及合并后的线上验收。
- 法语译文、法律现行性、原报告精度／审计限制和整理稿授权／署名复核。
- DS 团队确认未来跨模块观测单位、schema和连接键；本次不改变现有法律接口。
