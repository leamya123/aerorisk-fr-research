# 数据字典与编码手册 v3.2
单位：一条可定位的事实主张/政策事件；来源、事件、航线分表，使用source_id关联。来源的权威性与主张得到证实的程度是两条轴，不合成分数。

## 五层状态
A 政策承诺；B 法律/协定授权；C 国内实施机制；D 具体监管批准；E 实际运营。现有events字段legal_commitment须配合event_type区分A和B；后续正式版增设layer=A/B/C/D/E与claim_id，禁止只用一个“开放=1”字段。
每层分别使用DIRECT（原文直接证实该限定事实）、REPORTED（官方声称）、SECONDARY（二手报道）、PLANNED（计划）、UNKNOWN（不足）、EXPLICIT_NOT_IMPLEMENTED（有明确、带日期的未实施证据）、NA（本记录不涉及）。未检索到不能编码0或EXPLICIT_NOT_IMPLEMENTED。
DIRECT仅相对于该主张：法律存在不等于法律已经落实；机构职责网页不等于机构实际履职。

## 日期
publication_date为明确网页/文书刊载日，effective_date只在有法律依据时填。event_date必须由正文明确；不能把回顾2022的无日期采访写成2022-01-01事件。年级信息放date_anchor。
adoption、signature、promulgation、provisional_application、entry_into_force分别记录，草签不等于签署，临时适用不等于最终生效。继承记录保留原检索日；本轮最后复核为2026-10-19 UTC。URL路径、版权页脚、PDF创建日期不是法律生效日。
BJ03司法部目录01-01-0001无效；SGG的2024-07-22只作网站刊载日期。

## 第五航权个案
逐项核对：真实承运人及注册/许可本国；完整航程与本国连接；两个外国国家；当地有偿上下客/货权；明确许可及期间；日期明确的实际执行。
经营承运人与营销代码共享方不同。机场起降或经停不能证明当地商业承运；售票页只能证明提供销售，不能单独证明实际执行。
D需要个案授权文书；E如仅AFCAC报告则REPORTED。没有许可文书不必断言未运行，但不得把来源缺失“补齐”为DIRECT。
Transair Senegal境外Abidjan–Bamako段不衡量塞内加尔向外国航司开放。Nouakchott–Conakry不经过塞内加尔。Dakar/Diass的别名与方向去重须保留原文和处理日志；LVB不擅自改LBV。

## 复核
每个关键结论保存source_id、文章/段落/页码、短原文、保守英译。译文保留shall/may、subject to、provisional等限定。
第二编码者复核全部A–E关键主张及全部候选航线；分歧记入日志，不能把同一模型再问一次算独立编码。小样本先报告具体分歧和修订，不强行给不稳定一致性系数。
来源复制、双语转载、同一访谈不算多个独立事件。2022工作论文与2025正式版为同一研究族。源PDF仅用于合法研究访问，公开仓库默认放元数据与短引文，不批量复制版权全文。
空字符串表示未填/未知，具体原因在missing_information/coding_caution说明；NA为不适用，二者不得混淆。

## v3.2修正与计数
来源记录数、政策事件数、航线审计行数、文献数是四个不同单位。航线表18行包含别名、待核、排除对象，不等于18条第五航权航线。11事件含历史法律与报告主张，不等于11次开放改革。
E06/E07的证据级别改为OFFICIAL_ASSERTION，与其PLANNED状态一致。不新增无确切日期的“改革事件”来放大样本。
legal_article_matrix：9行对应4+5个核心条文；effective_date空白均为未核实，不是无法律效力。french_anchor是定位短语，英文为转述。
evidence_chain_and_gaps：3行候选链；UNKNOWN严格保留，非否定事实。
新增网页入口BJ10/BJ11不等于取得其目标程序全文。
