// Paladin class hooks for the shared Forever guide app.js
(function(){
const WN={slow:'Retribution',fast:'Protection'};
function sealAt(l,W){if(W==='slow')return l>=20?'Seal of Command':'Seal of Righteousness';return l>=10?'Seal of Fury':'Seal of Righteousness'}
function sealWhy(l,W){if(W==='slow')return l<20?'Slow 2H: Seal of Righteousness until 20, then Seal of Command (talent).':'Slow 2H: Seal of Command (talent). Judge after a Hammer of Justice stun for burst.';
 return l<10?'Prot: Seal of Righteousness until Seal of Fury at 10.':'Prot (1H + shield): Seal of Fury. Its absorb needs a shield; faster weapons get more from its flat Holy damage. Judging it taunts.'}
function rotFor(l,W){const a=[];
 a.push('<b>'+sealAt(l,W)+'</b> up <span class="src">'+WN[W]+'</span>');
 a.push('<b>Judgement</b> on CD (keeps your seal)');
 if(l>=6)a.push('<b>Holy Strike</b> on CD');
 if(l>=20)a.push('<b>Consecration</b> on 3+ mobs (mana-heavy)');
 if(l>=8)a.push('<b>Hammer of Justice</b> (key 5) to stun or interrupt');
 if(l>=20)a.push('Exorcism (Bottom 4) on Undead/Demons');
 a.push((l>=20?'Top-up: Flash of Light (key 6) · ':'')+'Low HP: Divine Protection → Holy Light (Top 1-2)'+(l>=10?' · Last resort: Lay on Hands (Top 7)':''));
 if(l>=44)a.push('Hammer of Wrath (Top 6) on targets below 20% HP');
 if(l>=10)a.push('Bad pull: Blessing of Protection on yourself and run'+(l>=18?' · Rooted: Blessing of Freedom':''));
 a.push('Buffs: Bow & Buff ('+(l>=20?'Kings':'Might')+') + Retribution Aura');
 return `<ol>${a.map(x=>'<li>'+x+'</li>').join('')}</ol><span class="src">Icy Veins Forever Ret</span>`}
const SH={'Hammer of Justice':'Hammer of Justice','Blessing of Protection':'Bless. of Protect','Divine Protection':'Divine Protect','Seal of the Crusader':'Seal of Crusader','Seal of Righteousness':'Seal of Right.','Seal of Command':'Seal of Command','Judgement':'Judge-ment','Consecration':'Consec-ration','Exorcism':'Exor-cism','Flash of Light':'Flash of Light','Blessing of Might':'Bless. of Might','Blessing of Kings':'Bless. of Kings','Redemption':'Redemp-tion','Hearthstone':'Hearth-stone','Blessing of Freedom':'Bless. of Freedom','Hammer of Wrath':'Hammer of Wrath','Divine Shield':'Divine Shield','Bow & Buff':'Bow & Buff','Holy Strike':'Holy Strike','Divine Intervention':'Divine Interv.','Summon Warhorse':'Warhorse','Devotion Aura':'Devotion','Retribution Aura':'Retri-bution','Concentration Aura':'Concen-tration','Shadow Resistance Aura':'Shadow Res.','Frost Resistance Aura':'Frost Res.','Fire Resistance Aura':'Fire Res.'};
function wfix(x){if(!x)return x;const c=JSON.parse(JSON.stringify(x));if(W!=='slow'&&c.mid[2]&&/^Seal of (Command|Righteousness)$/.test(c.mid[2].n)&&window.__L>=10)c.mid[2].n='Seal of Fury';return c}
function macroUpd(l){const n=l>=20?'Blessing of Kings':'Blessing of Might';const t=$('#macroTxt');if(t)t.textContent='#showtooltip '+n+'\n/cast '+n+'\n/bow';const ic=$('#macroIc');if(ic)ic.src='icons/spells/'+SPELLS[n].i+'.jpg'}

window.K={prefix:'pal',modeKey:'wpn2',modes:['fast','slow'],rotFor,advice:sealWhy,SH,
 wfix:(c,l,W)=>{if(W!=='slow'&&c.mid[2]&&/^Seal of (Command|Righteousness)$/.test(c.mid[2].n)&&l>=10)c.mid[2].n='Seal of Fury';return c},
 barLab:{top:['Top','click · combat cooldowns'],mid:['Middle','keys 1-7 · pressed constantly'],bot:['Bottom','long CDs · out of combat'],aur:['Aura Bar','auras + Righteous Fury']},
 iconAlias:(n,l)=>n==='Bow & Buff'?(l>=20?'Blessing of Kings':'Blessing of Might'):null,
 label:n=>n==='Righteous Fury'?'Prot: R. Fury':null,macroUpd,
 wnote:{slow:'Ret alt spec (dual spec from 40): slowest two-hander, Seal of Command once you have the talent.',fast:'Prot main: one-hander + shield, Seal of Fury from 10 (WoW Forever DB / Blizzard deep dive).'}};
})();
