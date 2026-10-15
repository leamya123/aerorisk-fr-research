# LEGAL 工作线 · OHADA 法语法律文本与航空器救济

**研究问题**：法定执行规则、航空器国际担保权的国别声明、司法实践三者如何区别？是否能识别与飞机租赁违约回收有关的有出处制度特征？

**先区分三个层级**
1. **OHADA 统一法（general enforcement law）**：债务追偿、强制执行等一般规则及2024年新旧版本的过渡。
2. **Cape Town Convention / Aircraft Protocol（aircraft-specific international instrument）**：加入/批准、适用范围、国别声明与国内实施。不能假设同一 OHADA 体系各国航空器救济时限完全相同。
3. **国别判例与实际执行（observed outcomes）**：只有原始案例明确写出实际流程日期、救济内容及飞机资产时，才可测量真实收回耗时。

### 重要原始法源（来源链接与法条摘要，非逐字全文）
- OHADA 2023 AUVE（新强制执行规则），2023-10-17 通过、2023-11-15 官方公报刊发、2024-02-16 生效：https://www.ohada.org/publication-au-j-o-ohada-de-lacte-uniforme-du-17-octobre-2023-portant-organisation-des-procedures-simplifiees-de-recouvrement-et-des-voies-dexecution-yaounde-le-15-novembre-2023/
- UNIDROIT Aircraft Protocol 各国加入状态及声明：https://www.unidroit.org/instruments/security-interests/aircraft-protocol/states-parties/
- UNIDROIT Article XXX(2) / Article X 临时救济各国声明：https://www.unidroit.org/instruments/security-interests/aircraft-protocol/depositary/declarations-deposited-under-the-protocol-to-the-cape-town-convention-on-international-interests-in-mobile-equipment-on-matters-specific-to-aircraft-equipment-arranged-by-article-2/

**值得重点研究：**塞内加尔依其国别声明在某些 Article 13(1)(a)–(c) 救济上写明不超过10个**日历日**、(d)–(e) 等上不超过30个**日历日**；科特迪瓦2019年通知、2020-01-01生效的后续声明则对后一类别写30个**工作日**。这些是法律文本规定，**不是**飞机所有权人实际收到飞机的平均周期，也不能与普通 OHADA 民商事追偿天数直接比较。待逐项核实适用对象、申请条件、当地执行/判例。

### 禁止性数据处理
- 不把关键词 `délai`、`contestation` 的频次无监督映射为“司法摩擦0–1”并认定其等于法律执行效率。
- 不以 WJP Civil Justice 分数直接推断资产收回时长。
- 不将“塞内加尔航司18个月”或“OHADA 必须12–18个月”等未核实口述变成观测记录。
- 不把法规规定的天数录入 `actual_repossession_days`。

### 本方向提交
`legal/evidence_registry_v1.csv`：官方法源可核对事实；`legal/case_coding_template_v1.csv`：判例采集模板（目前无已验证航空器判例）；`legal/research_log.md`：新增证据、检索策略与待核对问题。先建立样本框，再试验法语 NLP 分类、人工复核和编码一致性。
