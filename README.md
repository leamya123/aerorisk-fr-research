# AeroRisk-FR | 法语区航空租赁风险定价研究

**研究原型 v0.1 · 2026-10-15 重新构建版。**

本仓库对应华东师范大学本科生创新训练项目《货币互联、制度摩擦与跨境资产定价：欧央行利率冲击对法语区航空租赁的影响研究》，分为两条研究线：

- **论文线**：检验 ECB 对 BCEAO/BEAC 货币政策及融资环境的实际传导；系统核查 OHADA / UNIDROIT 制度差异；只有取得真实且有授权的航空资产级数据后才研究市场租金和残值的实证效应。
- **平台线**：构建透明的现金流折现、违约回收与法律延迟情景压力测试工具，明确标注所有假设。

## 接下来要上传的文件

完整初版请保留以下结构：
- `prototype/index.html`：交互式网页原型
- `index.html`：GitHub Pages 的跳转首页
- `src/risk_model.py`：Python 风险定价模型
- `tests/test_risk_model.py`：7 项单元测试
- `docs/research_design_v1.md`：论文研究设计
- `docs/variable_dictionary_v1.csv`：变量字典
- `docs/research_log.md`：研究日志
- `data/README.md`、`paper/README.md`：数据及论文管理

**注意：当前 GitHub 仓库尚未上传上述源码。** 请从聊天中下载 `AeroRisk-FR_rebuilt_v0.1.zip`，解压后将 `aerorisk-fr-research/` 文件夹里的内容（而非外层文件夹）上传到仓库根目录，覆盖此 README。

## 科研诚信边界

1. 平台默认购价、折现率、违约概率和法律延迟均为**情景假设**，不是市场报价或司法实测。
2. 未通过有效的识别策略检验时，不得将 ECB 利率简单称作有效工具变量，或将相关性称作因果。
3. WJP Civil Justice 指数不等于飞机收回时长。
4. 2024 年 ECB 开始降息，而 BCEAO 主要政策利率未同步下降；传导关系需要实证检验。
5. 不向公共仓库上传 WRDS/Cirium 许可限制的数据、个人隐私或机密材料。

## 本地运行

直接打开 `prototype/index.html`；模型测试：

```bash
python -m unittest discover -s tests -v
```

平台只用于研究和演示，不构成实际金融报价。
