# 中期研究增量：外国航空承运人准入制度比较

答辩日期：2026-10-28（按研究者提供的“下周三”）。证据核验截止2026-10-19；本次整理/代码验证日期2026-10-22。两日期不得混用。

当前结论：**CONDITIONAL GO**。工作范围B为贝宁与塞内加尔外国航空承运人准入制度及行政授权机制；并非已完成第五航权实际实施效果研究。学校最终题名与变更仍待导师/学校确认。

## 三分钟现场演示

1. 打开[逐条比较](outputs/legal_comparison.md)：选BJ224与SN231，说明一般许可规则不等于某条航线已经获批。
2. 打开[来源索引](outputs/source_index.md)：按BJ03找到官方URL和PDF页码，展示原文可追溯。
3. 打开[航线缺口](outputs/route_gaps.md)：KQ有协定及开航报告，但具体许可仍UNKNOWN。
4. 运行下面命令，展示自动生成表格和校验结果。

```bash
python studies/fifth_freedom_bj_sn/build.py
python -m unittest discover -s studies/fifth_freedom_bj_sn -p 'test_*.py' -v
```

Python 3.9+，无需购买数据或安装第三方依赖。断网也能生成表格；打开官方来源需网络。演示前保存合法原件到个人电脑，原件不纳入公开仓库。

## 交付与边界

25来源记录、11事件记录、18航线审计行、12文献记录、9核心法条、3候选证据链。不同单位不相加；18行不是18条核实航线。详见[审计输出](outputs/audit.json)。

- [法律分析](legal_findings_zh.md)：已核文本的初步解释，需独立复核。
- [编码手册](coding_manual.md)：缺失不填0，计划不当已实施。
- [文献审查](literature_reading_memo.md)：Shirichena2026全文仍未取得。
- [中期答辩讲稿及问答](../../docs/midterm_20261028.md)。

输入CSV是2026-10-19资料包的继承版本。输出可复算不表示法律现行效力或翻译已经获得独立认证。没有新增实证因果结论，没有把旧租赁情景模拟变为市场数据。
