# AeroRisk-FR | 法语区航空租赁风险定价研究

**研究原型 v0.1 · 2026-10-15 重新构建版。** 本仓库支撑“论文 + 可交互平台”两条工作线，基于华东师范大学本科创新训练项目研究目标，**不是旧聊天中无法取得的原始代码文件**。

- **论文线**：ECB→BCEAO/BEAC 的实际政策利率传导；OHADA / UNIDROIT 国别制度事实；有真实资产级数据后才研究实际飞机租金/估值。
- **平台线**：透明的现金流平衡租金、违约与收回延迟情景压力测试。

## 快速运行

浏览器打开 [`prototype/index.html`](prototype/index.html)，或用 GitHub Pages 打开根目录 `index.html`（设置 **Settings → Pages → Deploy from a branch → main / (root)**）。静态网页无需安装依赖。

```bash
python -m unittest discover -s tests -v
```

## 目录

- [`docs/research_design_v1.md`](docs/research_design_v1.md) — 可执行研究设计、论文的实证门槛、需修正的开题表述
- [`docs/variable_dictionary_v1.csv`](docs/variable_dictionary_v1.csv) — 真实变量与情景变量的分离
- [`docs/research_log.md`](docs/research_log.md) — 研究日志
- [`prototype/index.html`](prototype/index.html) — 单文件交互平台
- [`src/risk_model.py`](src/risk_model.py) — 与前端同一核心公式的 Python 计算器
- [`tests/test_risk_model.py`](tests/test_risk_model.py) — 自动单元测试
- [`data/README.md`](data/README.md) — 数据使用与来源管理
- [`paper/README.md`](paper/README.md) — 论文目录

## 严格的研究诚信约束

1. 网页的预设 **$50m 购置金额、7% 折现率、3% PD、12 个月法律延迟** 全部为 **演示性假设**，并非实际市场或司法统计。
2. 绝不将模拟输出当作真实交易数据，不称“实际租金”，不称“实证显著因果结果”。
3. 未验证 IV 排除限制前，不能将 ECB 利率作为已经证明有效的工具变量。
4. WJP 法治指数不是飞机收回执行周期数据。国别法律差异要结合 OHADA、UNIDROIT 与真实案例。
5. 2024 年 ECB 开始降息；BCEAO 2024 年主政策利率保持不变。本项目必须检验而非先验地宣称“镜像同步”。
6. 公共仓库不放 WRDS/Cirium 有授权限制的数据、个人联系方式、证书或未经允许公开的原始文件。

官方来源和问题修订列表见 [`docs/research_design_v1.md`](docs/research_design_v1.md)。
