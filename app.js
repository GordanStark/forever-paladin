const SPN=Object.keys(window.SPELLS||{}).filter(k=>SPELLS[k].u).sort((a,b)=>b.length-a.length);
const SPRX=new RegExp("(?<![\\w'])("+SPN.map(n=>n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+")(?![\\w'])","g");
function spLink(n){const v=SPELLS[n];return `<a class="sp" href="${v.u}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/${v.i}.jpg" alt="">${n}</a>`}
function linkHTML(h){return h.split(/(<[^>]+>)/).map(p=>p.startsWith('<')?p:p.replace(SPRX,m=>spLink(m))).join('')}
const S={get:(k,d)=>{try{return JSON.parse(localStorage.getItem('pal:'+k))??d}catch(e){return d}},set:(k,v)=>localStorage.setItem('pal:'+k,JSON.stringify(v))};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
// tabs
function showTab(){const id=(location.hash||'#guide').slice(1);const t=$('#t-'+id)?id:'guide';
$$('.tab').forEach(x=>x.classList.toggle('on',x.id==='t-'+t));$$('.tabs a').forEach(a=>a.classList.toggle('on',a.hash==='#'+t));window.scrollTo(0,0)}
addEventListener('hashchange',showTab);showTab();
// level picker
const sel=$('#lvSel');for(let i=1;i<=60;i++)sel.add(new Option(i,i));
function rotFor(l){const a=[];
 a.push(l<20?'<b>Seal of Righteousness</b> up':'<b>Seal of Command</b> (slow 2H) — or SoR if fast weapon / high Spell Power');
 a.push('<b>Judgement</b> on CD (keeps your seal)');
 if(l>=6)a.push('<b>Holy Strike</b> on CD');
 if(l>=20)a.push('<b>Consecration</b> on 3+ mobs (mana-heavy)');
 a.push('Exorcism on Undead/Demons · Hammer of Justice to stun');
 a.push('Low HP: Holy Light · Panic: Divine Protection → Lay on Hands');
 a.push('Buffs: Blessing of Might/Kings + Retribution Aura');
 return `<ol>${a.map(x=>'<li>'+x+'</li>').join('')}</ol><span class="src">Icy Veins Forever Ret · spell levels other than Holy Strike (6) & Consecration (20) not verified</span>`}
function setLv(l){l=Math.max(1,Math.min(60,l));S.set('lv',l);sel.value=l;$('#curLv').textContent=l;$('#rotTag').textContent='· Lv '+l;$('#rot').innerHTML=linkHTML(rotFor(l));
 $$('.row').forEach(r=>{const c=+r.dataset.lv===l;r.classList.toggle('cur',c);r.classList.toggle('open',c)})}
sel.onchange=()=>setLv(+sel.value);$('#lvUp').onclick=()=>setLv(+sel.value+1);$('#lvDown').onclick=()=>setLv(+sel.value-1);
$('#rotBtn').onclick=e=>{const r=$('#rot');r.hidden=!r.hidden;e.currentTarget.setAttribute('aria-expanded',!r.hidden)};
// rows
const done=S.get('done',{});
$$('.row').forEach(r=>{const k=r.id;if(done[k])r.classList.add('done');
 r.querySelector('.row-head').onclick=e=>{if(e.target.classList.contains('chk')){r.classList.toggle('done');done[k]=r.classList.contains('done');S.set('done',done);
   if(done[k]&&+r.dataset.lv===+sel.value)setLv(+sel.value+1);return}r.classList.toggle('open')}});
const hd=$('#hideDone');hd.checked=S.get('hideDone',false);document.body.classList.toggle('hidedone',hd.checked);hd.onchange=()=>{S.set('hideDone',hd.checked);document.body.classList.toggle('hidedone',hd.checked)};
// checkboxes
const cb=S.get('cb',{});function wire(i){if(!i.dataset.k)return;i.checked=!!cb[i.dataset.k];i.onchange=()=>{cb[i.dataset.k]=i.checked;S.set('cb',cb)}}
// custom bags
function renderBags(){const list=S.get('bags',[]);$('#customBags').innerHTML=list.map((t,i)=>`<label class="ci"><input type="checkbox" data-k="cb${i}_${t}"><span>${t.replace(/</g,'&lt;')}</span></label>`).join('');$$('input[type=checkbox][data-k]').forEach(wire)}
$('#bagAdd').onclick=()=>{const v=$('#bagNew').value.trim();if(!v)return;const l=S.get('bags',[]);l.push(v);S.set('bags',l);$('#bagNew').value='';renderBags()};
$('#resetBags').onclick=()=>{Object.keys(cb).filter(k=>/^b|^cb/.test(k)).forEach(k=>delete cb[k]);S.set('cb',cb);renderBags()};
renderBags();
const n=$('#notes');n.value=S.get('notes','');n.oninput=()=>S.set('notes',n.value);
setLv(S.get('lv',1));
// my character
fetch('data.json',{cache:'no-cache'}).then(r=>r.json()).then(d=>{const esc=s=>String(s).replace(/</g,'&lt;');
 const g=d.gold||{};const tbl=(o)=>'<table>'+Object.entries(o).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')+'</table>';
 $('#meBox').innerHTML=(d.example?'<div class="example">⚠ EXAMPLE DATA — not your real character. This fills in once the addon sync is set up.</div>':'')+
 `<div class="card"><h3>${esc(d.name)} · Lv ${d.level}</h3><p>${esc(d.race)} ${esc(d.class)} · ${g.g||0}g ${g.s||0}s ${g.c||0}c<br><span class="src">Last synced: ${esc(d.lastSynced)}</span></p></div>`+
 `<div class="card"><h3>Gear</h3>${tbl(Object.fromEntries(d.gear.map(x=>[x.slot,x.item+(x.ilvl?' (ilvl '+x.ilvl+')':'')])))}</div>`+
 `<div class="card"><h3>Professions</h3>${tbl(Object.fromEntries(d.professions.map(p=>[p.name,p.skill+'/'+p.max])))}</div>`+
 `<div class="card"><h3>Bags</h3>${tbl(Object.fromEntries(d.bags.map(b=>[b.item,'×'+b.count])))}</div>`+
 `<div class="card"><h3>Mounts</h3>${d.mounts.length?d.mounts.map(esc).join('<br>'):'None yet'}<span class="src">Mount lookup in Forever's addon API not yet confirmed.</span></div>`
}).catch(()=>{$('#meBox').textContent='No synced data yet.'});
if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(r=>r.update());let rl=0;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!rl){rl=1;location.reload()}})}
(()=>{const q=new URLSearchParams(location.search);if(q.get('lv'))setLv(+q.get('lv'));if(q.get('rot'))$('#rotBtn').click()})();

setTimeout(()=>{if(!location.search.includes('noscroll')&&(location.hash||'#guide')==='#guide'){const r=$('.row.cur');if(r)window.scrollTo(0,r.offsetTop-$('.bar').offsetHeight-8)}},50);
const SH={'Hammer of Justice':'Hammer of Justice','Blessing of Protection':'Bless. of Protect','Divine Protection':'Divine Protect','Seal of the Crusader':'Seal of Crusader','Seal of Righteousness':'Seal of Right.','Seal of Command':'Seal of Command','Judgement':'Judge-ment','Consecration':'Consec-ration','Exorcism':'Exor-cism','Flash of Light':'Flash of Light','Blessing of Might':'Bless. of Might','Blessing of Kings':'Bless. of Kings','Redemption':'Redemp-tion','Hearthstone':'Hearth-stone','Blessing of Freedom':'Bless. of Freedom','Hammer of Wrath':'Hammer of Wrath','Divine Shield':'Divine Shield','Bow & Buff':'Bow & Buff','Holy Strike':'Holy Strike'};
function renderBars(l){const b=window.BARS[l],p=window.BARS[l-1];const lab={top:['Top','click · combat cooldowns'],mid:['Middle','keys 1-6 · pressed constantly'],bot:['Bottom','long CDs · out of combat']};
 $('#barLv').textContent=l;
 $('#barsBox').innerHTML=['top','mid','bot'].map(r=>`<div class="brow"><div class="blab"><b>${lab[r][0]}</b> ${lab[r][1]}</div><div class="bslots">`+b[r].map((s,i)=>{if(!s)return`<div class="bs empty">${r==='mid'?i+1:''}</div>`;
  const nw=!p||JSON.stringify(p[r][i])!==JSON.stringify(s);const v=s.n==='Bow & Buff'?{i:SPELLS['Blessing of Might'].i}:(SPELLS[s.n]||{});const tag=v.u?'a':'div';return`<${tag} class="bs${nw?' new':''}${s.u?' unc':''}"${v.u?` href="${v.u}" target="_blank" rel="noopener"`:''} title="${s.n}">${v.i?`<img src="icons/spells/${v.i}.jpg" alt="">`:''}${r==='mid'?`<i>${i+1}</i>`:''}<span>${SH[s.n]||s.n}</span>${nw?'<em>NEW</em>':''}</${tag}>`}).join('')+'</div></div>').join('')}
const _setLv=setLv;setLv=function(l){_setLv(l);renderBars(+sel.value)};renderBars(+sel.value);

$('#copyMacro')&&($('#copyMacro').onclick=async e=>{const t=$('#macroTxt').textContent;try{await navigator.clipboard.writeText(t)}catch(_){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}e.target.textContent='Copied ✓';setTimeout(()=>e.target.textContent='Copy macro',1500)});
(()=>{const o=new URLSearchParams(location.search).get('only');if(o)$$('.row').forEach(r=>{if(r.dataset.lv!==o)r.style.display='none'})})();
