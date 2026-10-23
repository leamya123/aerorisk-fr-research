'use strict';
(function(){
  const evidence=window.AERORISK_EVIDENCE;
  if(!evidence||!evidence.data)throw new Error('Evidence snapshot is missing. Run python v3/build.py.');
  const data=evidence.data;
  const sources=Object.fromEntries(data.sources.map(row=>[row.document_id,row]));
  const byId=(id)=>document.getElementById(id);
  const esc=(value)=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const officialLink=(id,label)=>{
    const source=sources[id];
    if(!source)return '<span>来源待补</span>';
    return '<a class="source-link" href="'+esc(source.official_url)+'" target="_blank" rel="noopener"><span>'+esc(label||source.institution)+' ↗</span><span class="verify-label">'+esc(statusLabel(source.verification_status))+'</span></a>';
  };
  function statusLabel(status){
    const labels={
      text_checked:'正文已核',relevant_text_checked:'相关文本已核',relevant_articles_checked:'相关条文已核',
      'key_articles_OCR_and_image_checked_2026-10-19':'关键条文双重核对',text_checked_official_assertion:'官方陈述已核',
      selected_pages_visually_checked:'选定页视觉核对',relevant_sections_checked:'相关章节已核',relevant_paragraph_checked:'相关段落已核',
      page_checked:'页面已核','official_index_link_checked_target_unavailable_2026-10-19':'入口已核 / 文件不可得',
      text_checked_route_anomalies:'文本已核 / 航线异常'
    };
    return labels[status]||String(status).replaceAll('_',' ');
  }
  byId('cutoff').textContent=evidence.evidence_cutoff;
  byId('packaging').textContent=evidence.packaging_date;

  const legalGrid=byId('legalGrid');
  legalGrid.innerHTML=data.articles.map(row=>{
    const country=row.country==='BJ'?'贝宁 BENIN':'塞内加尔 SENEGAL';
    const source=sources[row.source_id];
    return '<article class="legal-card" data-country="'+esc(row.country)+'">'+
      '<div class="legal-card-head"><span class="country-mark">'+country+'</span><span class="article-mark">ART. '+esc(row.article)+' · 对照 '+esc(row.paired_article)+'</span></div>'+
      '<h3>'+esc(row.comparative_finding)+'</h3><p>'+esc(row.english_analytical_paraphrase)+'</p>'+
      '<p class="boundary">'+esc(row.interpretation_boundary)+'</p>'+
      officialLink(row.source_id,(source?.institution||row.source_id)+' · '+row.source_locator)+'</article>';
  }).join('');
  document.querySelectorAll('.tab').forEach(button=>button.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(tab=>{tab.classList.remove('active');tab.setAttribute('aria-selected','false');});
    button.classList.add('active');button.setAttribute('aria-selected','true');
    const filter=button.dataset.filter;
    document.querySelectorAll('.legal-card').forEach(card=>card.classList.toggle('hidden',filter!=='all'&&card.dataset.country!==filter));
  }));

  const statNames={sources:'官方/一手来源',events:'政策与制度事件',routes:'航线审计行',literature:'文献记录',articles:'核心法条',chains:'候选证据链'};
  byId('statsGrid').innerHTML=Object.entries(evidence.counts).map(([key,value])=>'<article class="stat-card"><b>'+esc(value)+'</b><span>'+esc(statNames[key]||key)+'</span></article>').join('');

  const statusCounts={};
  data.sources.forEach(row=>{statusCounts[statusLabel(row.verification_status)]=(statusCounts[statusLabel(row.verification_status)]||0)+1;});
  const grouped=Object.entries(statusCounts).sort((a,b)=>b[1]-a[1]);
  byId('verificationBars').innerHTML=grouped.map(([label,count])=>'<div class="bar-row"><span class="bar-label" title="'+esc(label)+'">'+esc(label)+'</span><span class="bar-track"><i class="bar-fill" style="width:'+Math.round(count/data.sources.length*100)+'%"></i></span><span class="bar-count">'+count+'</span></div>').join('');

  function cell(value,type){
    const upper=String(value||'').toUpperCase();
    const cls=upper==='UNKNOWN'?'no':upper.includes('PARTIAL')||upper.includes('REPORTED')?'partial':'yes';
    const label=upper==='UNKNOWN'?'未知':upper.includes('PARTIAL')?'部分':upper.includes('REPORTED')?'报告':'已见材料';
    const prefix=type?type+': ':'';
    return '<span class="matrix-cell '+cls+'" title="'+esc(value)+'">'+esc(prefix+label)+'</span>';
  }
  byId('chainMatrix').innerHTML='<div class="matrix-row"><span></span><span class="matrix-cell">协定</span><span class="matrix-cell">许可</span><span class="matrix-cell">运营</span></div>'+data.chains.map(row=>'<div class="matrix-row"><span>'+esc(row.carrier.split(' [')[0])+'</span>'+cell(row.specific_ASA_terms,'')+cell(row.specific_permit,'')+cell(row.operation,'')+'</div>').join('');

  const coreIds=['YD01','UE01','BJ03','SN01','AF01','KQ01','KG01','BJ02'];
  byId('sourceList').innerHTML=coreIds.map(id=>{
    const source=sources[id];
    return '<a class="source-pill" href="'+esc(source.official_url)+'" target="_blank" rel="noopener"><b>'+esc(id+' · '+source.institution)+'</b><span>'+esc(statusLabel(source.verification_status))+' ↗</span></a>';
  }).join('');

  const kq=data.chains.find(row=>row.chain_id==='CH01');
  const kqRoute=data.routes.find(row=>row.route_id==='R03');
  if(!kq||!kqRoute||kq.specific_permit!=='UNKNOWN')throw new Error('KQ guardrail failed: permit must remain UNKNOWN.');
  byId('caseFacts').innerHTML=[
    ['候选航段',kq.candidate_foreign_segment],['航司报告开航','2022-12-11 · 每周 2 班'],['许可结论','未取得具体文件']
  ].map(([label,value])=>'<div class="fact"><span>'+esc(label)+'</span><b>'+esc(value)+'</b></div>').join('');
  byId('caseTimeline').innerHTML=[
    ['2014-12-13','肯尼亚—加纳协定签署','协定文本含第五航权及指定授权条款；最终外交通知与当前连续性未核。'],
    ['2022-12-11','航司回顾称 Accra–Dakar 开航','Kenya Airways 年报列为每周两班；这是航司一手回顾，不是政府许可。'],
    ['2023 报告期','AFCAC 列出完整航程','监管侧材料与航司报告相互印证，但具体许可、当地载运与逐班执行仍缺。']
  ].map(([date,title,text])=>'<article class="timeline-item"><time>'+esc(date)+'</time><h4>'+esc(title)+'</h4><p>'+esc(text)+'</p></article>').join('');
  byId('caseSources').innerHTML=kq.source_ids.split(';').map(id=>{
    const source=sources[id];
    return '<a class="case-source" href="'+esc(source.official_url)+'" target="_blank" rel="noopener">'+esc(id+' · '+source.institution)+' ↗</a>';
  }).join('');
})();
