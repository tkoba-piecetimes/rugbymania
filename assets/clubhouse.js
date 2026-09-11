(() => {
 'use strict';
 const script=document.currentScript, root=new URL('../',script.src);
 const out=document.getElementById('match-results'); if(!out)return;
 const $=id=>document.getElementById(id);
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const link=p=>new URL(p,root).href;
 const ids=['year','league','team','opponent','view']; let data,limit=12;
 const card=m=>`<article class="match-card"><div class="match-meta">${esc(m.date||'日程未確認')} / ${esc(m.label)}</div><h3><span>${esc(m.home)}</span><b>${m.status==='played'?esc(m.home_score)+' − '+esc(m.away_score):'VS'}</b><span>${esc(m.away)}</span></h3><p>${esc(m.status==='played'?'試合終了':m.status==='scheduled'?m.time||'時間未定':'公式発表あり')} · ${esc(m.venue||'会場未定')}</p>${m.note?`<p>${esc(m.note)}</p>`:''}${m.url?`<a href="${esc(link(m.url))}">試合詳細・過去の対戦 →</a>`:`<a href="${esc(m.source)}" target="_blank" rel="noopener">協会の公式情報 ↗</a>`}</article>`;
 function teams(){
  const league=$('league').value,year=Number($('year').value);
  const names=[...new Set(data.matches.filter(m=>(!year||m.year===year)&&(!league||m.league===league)).flatMap(m=>[m.home,m.away]))].sort((a,b)=>a.localeCompare(b,'ja'));
  ['team','opponent'].forEach(id=>{const v=$(id).value;$(id).innerHTML=`<option value="">${id==='team'?'すべての大学':'指定なし'}</option>`+names.map(n=>`<option value="${esc(n)}">${esc(n)}</option>`).join('');if(names.includes(v))$(id).value=v;});
 }
 function render(){
  const year=Number($('year').value),league=$('league').value,team=$('team').value,opponent=$('opponent').value,view=$('view').value;
  const params=new URLSearchParams();ids.forEach(id=>{if($(id).value)params.set(id,$(id).value);});history.replaceState(null,'',`${location.pathname}?${params}${location.hash}`);
  $('opponent').disabled=view==='standings';
  if(view==='standings'){
   const seasons=data.seasons.filter(s=>(!year||s.year===year)&&(!league||s.league===league));
   const blocks=seasons.flatMap(s=>Object.entries(s.standings).filter(([,entries])=>entries.length&&(!team||entries.some(t=>t.team===team))).map(([block,entries])=>`<section><h3>${s.year}年 / ${esc(s.label)} / ${esc(block)}</h3><p>スコアのある収録試合を合算した参考集計です。リーグの複数ステージを合算する場合があります。不戦勝や公式のボーナスポイントは含めておらず、公式最終順位ではありません。</p><div class="archive-table"><table><thead><tr><th scope="col">参考順位</th><th scope="col">大学</th><th scope="col">勝</th><th scope="col">分</th><th scope="col">敗</th><th scope="col">得点</th><th scope="col">失点</th><th scope="col">得失点差</th><th scope="col">参考勝ち点</th></tr></thead><tbody>${entries.map(t=>`<tr ${t.team===team?'style="font-weight:800"':''}><td>${esc(t.rank)}</td><th scope="row">${esc(t.team)}</th><td>${esc(t.wins)}</td><td>${esc(t.draws)}</td><td>${esc(t.losses)}</td><td>${esc(t.gf)}</td><td>${esc(t.ga)}</td><td>${esc(t.goal_diff)}</td><td>${esc(t.points)}</td></tr>`).join('')}</tbody></table></div><a href="${esc(s.source)}" target="_blank" rel="noopener">協会の公式情報 ↗</a></section>`));
   out.innerHTML=blocks.join('')||'<p>この条件の順位表は未収録です。年度・リーグを変更してください。</p>';return;
  }
  let ms=data.matches.filter(m=>(!year||m.year===year)&&(!league||m.league===league)&&(!team||[m.home,m.away].includes(team))&&(!opponent||[m.home,m.away].includes(opponent))&&(view==='all'?true:view==='unscored'?['unscored','cancelled'].includes(m.status):m.status===view));
  if(team&&team===opponent){out.innerHTML='<p>対戦相手には別の大学を選んでください。</p>';return;}
  ms.sort((a,b)=>view==='played'?(b.date||'').localeCompare(a.date||''):(a.date||'9999').localeCompare(b.date||'9999'));
  const today=new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Tokyo'}).format(new Date());
  if(view==='scheduled')ms=ms.filter(m=>!m.date||m.date>=today);
  let summary=`${ms.length}試合 / ${year?year+'年':'全年度'}の収録データ`;
  if(team&&view==='played'){
   let w=0,d=0,l=0;ms.forEach(m=>{const delta=(m.home===team?1:-1)*(m.home_score-m.away_score);delta>0?w++:delta<0?l++:d++;});summary+=` · ${esc(team)} ${w}勝 ${d}分 ${l}敗`;
  }
  out.innerHTML=`<p class="result-summary">${summary}</p><div class="match-grid">${ms.slice(0,limit).map(card).join('')}</div>${ms.length? '':'<p>この条件の試合はありません（未収録の場合を含みます）。別の年度・リーグ・表示に切り替えてください。</p>'}${ms.length>limit?'<p><button type="button" id="load-more">さらに12試合を表示</button></p>':''}`;
  if($('load-more'))$('load-more').onclick=()=>{limit+=12;render();};
 }
 function favorite(){
  const select=$('favorite-team');if(!select)return;
  const teams=[...new Set(data.leagues.filter(l=>!l.archived).flatMap(l=>Object.keys(l.teams)).filter(t=>!t.includes('の勝者')&&!t.includes('の敗者')))].sort((a,b)=>a.localeCompare(b,'ja'));
  select.innerHTML+=[...teams].map(t=>`<option value="${esc(t)}">${esc(t)}</option>`).join('');
  const show=()=>{const t=select.value;try{localStorage.setItem('rugbymania-team',t);}catch{}if(!t){$('favorite-result').innerHTML='';return;}
   const leagues=data.leagues.filter(l=>!l.archived&&l.teams[t]);
   $('favorite-result').innerHTML=leagues.map(l=>`<p><a href="${esc(link(`${l.code}/clubs/${l.teams[t].slug}/index.html`))}">${esc(t)} / ${esc(l.label)} の日程・戦績を見る →</a></p>`).join('')+`<a href="${esc(link('archive/index.html'))}?team=${encodeURIComponent(t)}">過去の記録を調べる →</a>`;
  };try{const stored=localStorage.getItem('rugbymania-team');if(teams.includes(stored))select.value=stored;}catch{}
  select.onchange=show;show();
 }
 fetch(new URL('assets/rugby-data.json',root)).then(r=>{if(!r.ok)throw Error('fetch');return r.json();}).then(d=>{
  data=d;const p=new URLSearchParams(location.search);['year','league','view'].forEach(id=>{if([...$(id).options].some(o=>o.value===p.get(id)))$(id).value=p.get(id);});teams();['team','opponent'].forEach(id=>{if([...$(id).options].some(o=>o.value===p.get(id)))$(id).value=p.get(id);});
  ids.forEach(id=>$(id).addEventListener('change',()=>{limit=12;if(['year','league'].includes(id))teams();render();}));
  $('reset-filters').onclick=()=>{ids.forEach(id=>$(id).selectedIndex=0);teams();limit=12;render();};render();favorite();
 }).catch(()=>{out.innerHTML='<p>試合データを読み込めませんでした。再読み込みするか、リーグ別の日程・順位表をご覧ください。</p>';});
})();
