# v3 金融源字节一致性修复与合并前验收

2026-10-24 · `research/fifth-freedom-bj-sn-v3` · PR #1 保持 Draft，不合并 main。

## 故障证据

上游最新交付 `4487235` 的 [GitHub Actions #68](https://github.com/leamya123/aerorisk-fr-research/actions/runs/40058680563) 显示 Failure；失败位于 `Verify v3 artifacts reproduce exactly`。本地同步了贺俊豪后续交付记录与移除展示页内部操作说明的改动后再修复，没有回退他的改动。

对 `data/official/airline_financials_candidate_v1.csv` 检查工作目录、分支 Git blob 和 main Git blob：三者均为2261字节，6个LF、0个CRLF，无UTF-8 BOM；字节完全相同。

|源CSV换行|原始字节SHA-256|
|---|---|
|LF（Git blob / CI检出）|`87375f09866bd83be2aefd173c721a784e5f687d9a029785c94f75f1f5493d93`|
|仅将LF转为CRLF|`3bdd5ed72e6775603e7f543e9550a5adbfbe47c2161208133dbe795a9b9395d9`|

两个值分别精确复现CI值和旧提交值，说明同一内容在不同检出换行下被计算原始字节哈希，导致审计漂移。不是财务数值、来源或法律证据改变。

## 修复与校验原则

- `.gitattributes` 仅为该金融源CSV增加 `text eol=lf`，使Git在 `core.autocrlf=true` 和 `false` 时检出相同LF字节。
- 不修改金融源CSV；不对金融数字或精度标签做格式化；不改变 `v3/build.py` 中原始字节 SHA-256 算法。
- 实际运行 `python v3/build.py` 重建审计。预期仅 `v3/build-audit.json` 的 `financial_source_sha256` 从CRLF哈希更新为LF哈希，其余v3产物不变。
- 保留原有测试、CI的 `git diff --exit-code` 与哈希断言；新增真实Git索引检出测试，分别在 autocrlf true / false 下检查CSV字节与审计哈希一致，禁止用测试内的哈希规范化掩盖差异。

## 最新本地验证与交付对应

- 仓库Python测试30项通过（原29项全部保留，增加1项；v3测试由5项增为6项）。
- 法律证据Python测试6项通过，无失败或跳过；Python合计36项。
- Node校验覆盖9个HTML、外部脚本以及年度、季度、v3在线／离线功能。
- 法律与四项金融构建及非因果滞后诊断执行完成；旧金融数据和法律快照重建无差异。
- 原金融演示、法律CSV及生成输出、六幅PNG截图、离线HTML和金融JS／SVG保持 `4487235` 的内容，特别保留“下载证据JSON”和“返回页首”两个操作；不重新加入已移除的内部说明。
- 交付记录原“最终本地1015197”已改为明确的历史交付；保留当时29＋6测试记录，并补入最新30＋6计数与本次故障说明，避免历史成功被误读为最新远端CI成功。

修复提交推送后，必须从PR Checks核对最新提交的真实远端结果；最终提交与CI链接在本次会话最终验收回复中列出。不能用本地36项通过或历史CI代替该确认。

## 保留与人工验收边界

main核查基线为 `a5af45deba195e53debdefd74ee12de6fe3f21b2`；本次只在研究分支提交、普通推送，不修改main、Pages配置或PR Draft状态，不删分支、不强推、不重写历史。合并仍须研究者最终批准。

Windows／Edge／Chrome原生双击与答辩投影不在本机能力范围；管理型浏览器禁止 `file://` 导航，不能把内嵌HTML禁网渲染称作Windows实机验收。DS接口确认、法律现行性与人工来源复核保持原有待办，不因技术修复扩大研究结论。
