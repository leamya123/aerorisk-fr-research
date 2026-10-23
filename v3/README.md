# AeroRisk-FR v3 展示页

## 在线与本地访问

- GitHub Pages 部署后：`https://leamya123.github.io/aerorisk-fr-research/v3/`
- 本地联网预览：在仓库根目录运行 `python -m http.server 8000`，打开 `http://localhost:8000/v3/`
- 断网答辩：直接双击 `v3/offline.html`。页面和证据快照已内嵌；官方来源链接需要网络。

## 重新生成

```bash
python studies/fifth_freedom_bj_sn/build.py
python v3/build.py
node scripts/validate_dashboard.js
python -m unittest discover -s tests -v
python -m unittest discover -s studies/fifth_freedom_bj_sn -p "test_*.py" -v
```

`v3/data/evidence.json` 是给页面和后续图表协作使用的稳定数据接口。上游唯一来源为 `studies/fifth_freedom_bj_sn/outputs/evidence.json`，请勿手改生成文件。

## 数据接口约定

- `counts`：六类研究材料计数。
- `data.sources`：来源登记，`document_id` 为主键，含 `official_url` 与 `verification_status`。
- `data.articles[*].source_id`：法律条文映射到来源。
- `data.routes[*].source_id`：航线审计映射到来源。
- `data.chains[*].source_ids`：分号分隔的证据链来源。
- 未取得的许可和当地商业载运证据必须保留字符串 `UNKNOWN`，不能转为 `true`、`0` 或“已批准”。

## 答辩操作

1. 首页先说明“区域开放承诺不等于个案许可”。
2. 在法律对照区点击贝宁或塞内加尔筛选，再点击卡片底部官方来源。
3. 在数据证据区解释 18 行是审计记录，不是 18 条已核实第五航权航线。
4. 在 Kenya Airways 案例区明确指出：开航陈述已交叉印证，但具体许可与当地付费载运仍为 `UNKNOWN`。
