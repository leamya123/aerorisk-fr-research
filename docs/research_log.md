# Research log

## 2026-10-15: 重新整理原型和识别边界
- 审核立项书、答辩 PPT、SMBC 2025 报告。
- 仓库起点原先为空；旧版 `prototype/index.html` 的源代码未随上传材料提供，因此本版从头重建，不能声称与旧版相同。
- **Confirmed by official sources**: ECB 2024 年 6 月已转向降息；BCEAO 2024 年维持主要政策利率 3.5%。
- **Corrections pending in proposal/slides**: ECB 工具变量排除限制、法律执行时间未经证实、OHADA 新执行法、归口国家的民航监管部门。
- 已创建简化预期现金流 + 法律延迟压力模型与测试。模型参数全部为标明的虚拟情景，没有真实交易输入。
- 下一步：下载 ECB/BCEAO 官方政策利率的日期—利率原始文件，在 source registry 补充文件哈希、发布日期与访问许可；撰写数据抓取与校验脚本。暂不做 2SLS 因果断言。
