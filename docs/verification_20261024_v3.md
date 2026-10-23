# 2026-10-24 中期展示验证记录

工作分支：`research/fifth-freedom-bj-sn-v3`。在已有代码与证据上增量修改；不合并或推送 main，不修改 Pages 设置，未创建 PR。当前项目为《云程有数：西非法语区航空业的制度开放与金融约束研究》，原立项正式题名与待审批状态保留。

## 实际执行结果

环境：Python 3.12.14、Node.js 24.19.0、系统 Chromium（Playwright 驱动）。无需新增第三方应用依赖。

|检查|结果及范围|
|---|---|
|`python studies/fifth_freedom_bj_sn/build.py`|通过；25来源、11事件、18审计行、12文献、9核心法条、3候选证据链；原法律生成输出逐字节不变|
|`python v3/build.py`|通过；重建法律快照、独立财务 JS、财务 SVG、离线 HTML 与输入／产物 SHA-256 审计|
|`python -m unittest discover -s tests -v`|29项通过，无失败、跳过或预期失败；含原金融／模型24项与v3五项（来源原值／精度／审计字段保持、图形金额、UNKNOWN、快照可复现与离线内嵌）|
|`python -m unittest discover -s studies/fifth_freedom_bj_sn -p 'test_*.py' -v`|6项通过，无失败、跳过或预期失败；来源引用、UNKNOWN、审计哈希和证据输出可复现|
|`node scripts/validate_dashboard.js`|通过；8个HTML页面及外部脚本语法；年度／季度图表功能；v3在线与离线法律、KQ与五年财务表渲染|
|Chromium原有六入口|首页重定向原型与原型计算正常，调整折现率改变模拟租金；宏观图两条路径且DFR→MRO选择器生效；融资传导两幅图有2／3条线；年度图和7行表；季度图和26行表均正常，无页面脚本错误|
|Chromium v3桌面 1440px|9张法条卡、5行财务数据、贝宁筛选与恢复并列对照通过；截图见 `v3/screenshots/`|
|Chromium v3窄屏 390px|页面无整体水平溢出；财务图与表在自身容器内滚动，避免缩小标签|
|断网HTML渲染|网络禁用的独立浏览器上下文中，直接注入生成HTML后9张法条卡、5行财务表和内嵌SVG均渲染，无脚本错误|
|差异检查|原六入口及金融资产、原CSV、法律分类、法律JSON schema、法律生成快照未改；仅新增独立展示财务快照，未改变来源或分类以补齐UI|

初次浏览器检查脚本误按 `polyline` 查找宏观阶梯图；阅读实现确认其使用 `path`，校正检查后通过，未改宏观代码。窄屏初次截图显示图中文字过小，已改为图表容器内滚动。

## 验证边界与待办

- 管理型 Chromium 明确禁止直接 `file://` 导航（`ERR_BLOCKED_BY_ADMINISTRATOR`）；未绕过该策略。上述断网渲染通过不等同于在答辩电脑上双击测试。请用实际答辩浏览器复核 `v3/offline.html`。
- 未测试 Safari、Firefox、Windows、投影仪及所有下载操作。未重新联网核验外部法律／财务报告URL、文本现行效力、翻译或财报审计状态；沿用仓库出处与限制。
- 法律数据接口未改变；财务字段逐字符串继承CSV，独立输出 `{source, rows}`。DS 交接约定在 `v3/README.md`；尚无 DS 团队确认或直接团队通信。
- 不声称已部署本分支到 Pages；默认 Pages 可能仍指向 main。现有工作流只在 main push 或 PR 上触发，本分支直接 push 不证明远端 CI 已运行。上述为当前机器实际检查结果。
- 最安全的答辩备份为本分支完整ZIP和单文件离线页。公网预览若确需发布，应另行授权独立预览部署；不为展示擅改 main 或 Pages 发布源。

## 截图和离线使用

`v3/screenshots/` 含开场、法律、证据、KQ、金融、研究递进六幅实际 Chromium 截图，供答辩排版使用，不作为新研究证据。

下载本分支完整ZIP并解压，双击 `v3/offline.html` 展示新法律和金融内容。仅此单文件即可展示内嵌图表；官方URL需网络。原有六个演示的相对链接需完整目录，并在根目录运行 `python -m http.server 8000` 后使用浏览器打开相应路径。`v3/README.md` 列出每个截图锚点及完整复算命令。

发布后截图字节检查发现既有 `.gitattributes` 的 `v3/** text eol=lf` 会改写 PNG 字节。已增加 `v3/screenshots/*.png binary` 覆盖规则并重新保存全部截图；逐文件验证 Git 对象与实际 PNG 字节、PNG 签名完全一致。未修改原有金融资产规则或内容。
