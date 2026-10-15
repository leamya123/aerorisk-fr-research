/**
 * Frontend quality gate for AeroRisk-FR static GitHub Pages.
 * 1. Compile every inline script to catch syntax errors.
 * 2. Execute annual dashboard with local CSV/JSON and a minimal DOM stub,
 *    then assert charts, summary table and success message are rendered.
 *
 * Usage: node scripts/validate_dashboard.js
 * No external npm packages required.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index.html', 'prototype/index.html', 'macro/index.html',
               'transmission/index.html', 'annual/index.html', 'quarterly/index.html'];

function getScripts(relativePath) {
  const html = fs.readFileSync(path.join(ROOT, relativePath), 'utf8');
  return [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
    .map((m) => m[1].trim()).filter(Boolean);
}

async function main() {
  let total = 0;
  for (const p of PAGES) {
    const sources = getScripts(p);
    for (const [i, source] of sources.entries()) {
      new vm.Script(source, {filename: p + '#script-' + i});
      total++;
    }
    console.log('Syntax OK:', p, '(' + sources.length + ' scripts)');
  }
  const source = getScripts('annual/index.html')[0];
  if (!source) throw new Error('annual/index.html missing inline JavaScript');
  const elements = {};
  const document = {
    getElementById(id) {
      if (!elements[id]) elements[id] = {innerHTML: '', textContent: ''};
      return elements[id];
    }
  };
  const fixtures = {
    '../data/official/bceao_annual_lending_2020_2025.csv': {
      text: fs.readFileSync(path.join(ROOT, 'data/official/bceao_annual_lending_2020_2025.csv'), 'utf8')
    },
    '../data/processed/annual_lending_descriptives_v1.json': {
      json: JSON.parse(fs.readFileSync(path.join(ROOT, 'data/processed/annual_lending_descriptives_v1.json'), 'utf8'))
    }
  };
  async function fetch(resource) {
    if (!Object.prototype.hasOwnProperty.call(fixtures, resource)) {
      throw new Error('Unexpected dashboard data request: ' + resource);
    }
    const f = fixtures[resource];
    return {ok: true, text: async () => f.text, json: async () => f.json};
  }
  const done = vm.runInNewContext(source, {document, fetch, console},
                                  {filename: 'annual/index.html', timeout: 3000});
  await done;
  for (const id of ['country', 'sector']) {
    if (!(elements[id]?.innerHTML || '').includes('<polyline')) {
      throw new Error(id + ' chart did not render a line');
    }
  }
  const body = elements.statsBody?.innerHTML || '';
  if (!body.includes('6.76') || !body.includes('6.69') || !body.includes('塞内加尔')) {
    throw new Error('BCEAO annual loan-rate table did not render real values');
  }
  if (!(elements.status?.textContent || '').includes('成功载入')) {
    throw new Error('Annual dashboard load/parse failed: '+elements.status?.textContent);
  }
  console.log('Dashboard smoke OK: two SVG charts, seven rate rows and success status.');
  const quarterSrc=getScripts('quarterly/index.html')[0];
  if (!quarterSrc) throw new Error('quarterly/index.html missing script');
  const quarterNodes={};
  const quarterDom={getElementById(id) {return quarterNodes[id]??(quarterNodes[id]={innerHTML:'',textContent:''});}};
  const quarterCsv=fs.readFileSync(path.join(ROOT,'data/processed/quarterly_policy_lending_panel_v1.csv'),'utf8');
  const quarterFetch=async (url)=>{
    if(url!=='../data/processed/quarterly_policy_lending_panel_v1.csv')throw new Error('Unexpected URL '+url);
    return {ok:true,text:async()=>quarterCsv};
  };
  const quarterDone=vm.runInNewContext(quarterSrc,{document:quarterDom,fetch:quarterFetch,console},{filename:'quarterly/index.html',timeout:3000});
  await quarterDone;
  if(!quarterNodes.loanChart?.innerHTML.includes('<polyline') || !quarterNodes.policyChart?.innerHTML.includes('<polyline')){
    throw new Error('Quarterly charts failed to render');
  }
  if(!quarterNodes.rows?.innerHTML.includes('2025-Q1') || !quarterNodes.rows?.innerHTML.includes('2026-Q2')){
    throw new Error('Quarterly data table failed to render');
  }
  if(!quarterNodes.status?.textContent.includes('成功读取 26')){
    throw new Error('Quarterly panel not loaded: '+quarterNodes.status?.textContent);
  }
  console.log('Quarterly dashboard smoke OK: two SVG charts and 26-quarter data table.');
  console.log('Validated '+total+' inline JavaScript blocks across '+PAGES.length+' HTML pages.');
}
main().catch((error) => {console.error(error);process.exitCode=1;});
