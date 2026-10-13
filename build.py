#!/usr/bin/env python3
"""Build Gordan Stark (Human Ret Paladin) PWA guide. Structure mirrors gordan-hunter v4."""
import json, html
E = html.escape
IV = "https://www.icy-veins.com/wow-forever/retribution-paladin-melee-dps-pve-guide"
IVP = "https://www.icy-veins.com/wow-forever/protection-paladin-tank-pve-guide"

# Talent plan 10-30 (user-supplied ExpCarry order; talent NAMES match Icy Veins key talents, exact point order NOT verified)
TAL = {}
for i, lv in enumerate(range(10, 15)): TAL[lv] = ("Benediction", f"{i+1}/5", "Holy · cheaper spells (mana)")
for i, lv in enumerate(range(15, 20)): TAL[lv] = ("Conviction", f"{i+1}/5", "Ret · more crit")
TAL[20] = ("Seal of Command", "1/1", "Ret · seal for slow two-handers")
for i, lv in enumerate(range(21, 24)): TAL[lv] = ("Sanctified Judgement", f"{i+1}/3", "Ret · Judgement mana return")
for i, lv in enumerate(range(24, 26)): TAL[lv] = ("Pursuit of Justice", f"{i+1}/2", "Ret · run speed (your only one)")
TAL[26] = ("Sacred Arbiter", "1/1", "Ret · more Judgement / Holy Strike damage")
for i, lv in enumerate(range(27, 30)): TAL[lv] = ("Vindication", f"{i+1}/3", "Ret · weakens what you hit")
TAL[30] = ("Vengeance", "1/3", "Ret · damage after crits")

MILESTONE = {
 1: ["Start in Northshire Abbey, Elwynn Forest. Seal of Righteousness + auto-attack."],
 5: ["Pick up Mining at a trainer; Blacksmithing in Goldshire/Stormwind. Cooking + First Aid too."],
 6: ["Holy Strike unlocked — press it on cooldown when you have mana. [Icy Veins]"],
 10: ["Talents open. Head toward Westfall / Loch Modan.", "Equip the slowest two-hander you can find (sword ideal)."],
 20: ["Consecration — your first AoE. Mana-hungry: 2-3 mobs max solo. [Icy Veins]", "Seal of Command talent — swap from SoR if your 2H is slow."],
 30: ["Beta cap. Check Merchant's Favor Blacksmithing recipes (Crusader's set). [Icy Veins]", "Shockadin (Holy Shock) build becomes possible — not our plan."],
 40: ["Dual Specialization reportedly opens (Ret + Prot). See Prot tab. [unconfirmed cost]"],
 60: ["Max level. Endgame gear/talents not published yet."],
}
ZONES = [(1,"Northshire / Elwynn Forest"),(10,"Westfall / Loch Modan"),(18,"Redridge Mountains"),(20,"Duskwood / Wetlands"),(25,"Ashenvale / Wetlands"),(30,"Hillsbrad / Alterac & beyond"),(40,"Stranglethorn / Arathi / Desolace"),(45,"Tanaris / Feralas / Hinterlands"),(50,"Un'Goro / Felwood / Searing Gorge"),(55,"Winterspring / Plaguelands")]
SPELLS = json.load(open("spells.json"))
ZICON = {"Northshire":"_elwynn","Westfall":"_westfall","Redridge":"_redridge","Duskwood":"_duskwood","Ashenvale":"_ashenvale","Hillsbrad":"_hillsbrad","Stranglethorn":"_stv","Tanaris":"_tanaris","Un'Goro":"_ungoro","Winterspring":"_winterspring"}
def icimg(key, cls="ic"):
    v = SPELLS.get(key)
    return f'<img class="{cls}" src="icons/spells/{v["i"]}.jpg" alt="" loading="lazy">' if v else ""
def zicon(z):
    for k, v in ZICON.items():
        if z.startswith(k): return icimg(v, "ic zi")
    return ""
def zone(lv):
    z = ZONES[0][1]
    for a, n in ZONES:
        if lv >= a: z = n
    return z

TR = {int(k): v for k, v in json.load(open("trainer.json")).items()}
TFE = "https://theforeverera.com/en/spells/paladin/levels/"
def trainer_html(lv):
    sp = TR.get(lv)
    if not sp: return ""
    li = []
    for x in sp:
        kind = "New" if x["kind"] == "New ability" else x["kind"].replace("Rank ", "R")
        tags = ""
        if x.get("forever"): tags += ' <span class="tg fv">New in Forever</span>'
        if x.get("talent"): tags += f' <span class="tg tl">{E("talent spell" if x["talent"].startswith("Talent") else "needs talent")}</span>'
        li.append(f'<li><span class="k {"new" if kind=="New" else ""}">{kind}</span> {E(x["name"])}{tags}</li>')
    note = "Beta client data, Lv 1-30 playable in the beta" if lv <= 30 else "Beta client data, not reachable in the beta (cap 30) and may change at launch"
    cls = "" if lv <= 30 else " warn"
    return f'<div class="trn"><b>Trainer</b><ul>{"".join(li)}</ul><span class="src{cls}">{note}. <a href="{TFE}">The Forever Era</a></span></div>'
LEARN = {}
for _lv in sorted(TR):
    for _x in TR[_lv]:
        if _x["kind"] == "New ability": LEARN.setdefault(_x["name"], _lv)
ITEM = {"Food": 1, "Water": 1, "Hearthstone": 1, "Bow & Buff": 4}
# each slot: candidates in order (name, unconfirmed_placement); latest learned wins
BARS = {
 "top": [[("Hammer of Justice",0)], [("Blessing of Protection",0)], [("Lay on Hands",0)],
         [("Divine Protection",0),("Divine Shield",1)], [("Bow & Buff",0)],
         [("Purify",0),("Cleanse",1)]],
 "mid": [[("Seal of Righteousness",0),("Holy Strike",0)], [("Judgement",0)], [("Seal of Righteousness@6",0),("Seal of Command",0)],
         [("Consecration",0)], [("Exorcism",0),("Hammer of Wrath",1)], [("Holy Light@1",0),("Flash of Light",0)]],
 "bot": [[("Food",0)], [("Water",0)], [("Holy Light@20",0)], [("Blessing of Might",0),("Blessing of Kings",0)],
         [("Redemption",0)], [("Hearthstone",0)]],
}
def bars_at(lv):
    out = {}
    for r, slots in BARS.items():
        row = []
        for cands in slots:
            pick = None
            for nm, unc in cands:
                base, _, at = nm.partition("@")
                L = int(at) if at else ITEM.get(base, LEARN.get(base, 99))
                if L <= lv: pick = {"n": base, "u": unc}
            row.append(pick)
        out[r] = row
    return out
BARDATA = {lv: bars_at(lv) for lv in range(1, 61)}
def bar_changes(lv):
    a, b = BARDATA[lv], BARDATA.get(lv-1, {"top":[None]*6,"mid":[None]*6,"bot":[None]*6})
    ch = []
    for r, lab in (("top","Top"),("mid","Middle"),("bot","Bottom")):
        for i in range(6):
            if a[r][i] != b[r][i] and a[r][i]:
                ch.append(f'{lab} {i+1 if r=="mid" else i+1}: {a[r][i]["n"]}' + (" (unconfirmed)" if a[r][i]["u"] else ""))
    return ch
def icon_of(n):
    if n == "Bow & Buff": return SPELLS["Blessing of Might"]["i"]
    v = SPELLS.get(n); return v["i"] if v else None
def mini_bars(lv):
    a, b = BARDATA[lv], BARDATA.get(lv-1)
    h = '<div class="mini">'
    for r in ("top","mid","bot"):
        for i, x in enumerate(a[r]):
            if not x: h += '<span class="mb e"></span>'; continue
            nw = (b is None) or b[r][i] != x
            ic = icon_of(x["n"])
            h += f'<span class="mb{" n" if nw else ""}{" u" if x["u"] else ""}" title="{E(x["n"])}">' + (f'<img src="icons/spells/{ic}.jpg" alt="" loading="lazy">' if ic else E(x["n"][:3])) + '</span>'
    return h + '</div>'
rows = []
for lv in range(1, 61):
    items = list(MILESTONE.get(lv, []))
    if lv in TAL:
        n, r, d = TAL[lv]
        tal = f'<div class="tal"><b>{E(n)}</b> <span class="rank">{r}</span><div class="eff">{E(d)}</div><span class="src">Icy Veins key talent · order: your plan</span></div>'
    elif lv > 30:
        tal = '<div class="tal unk"><b>Talent point</b><div class="eff">31-60 builds not published (beta cap 30). Will fill in at launch.</div><span class="src warn">Unannounced</span></div>'
    else:
        tal = ""
    lis = "".join(f'<li>{E(x)}</li>' for x in items)
    summ = TAL[lv][0] if lv in TAL else (items[0][:48] + ("…" if items and len(items[0])>48 else "") if items else (f"Trainer: {len(TR[lv])} new" if lv in TR else "No new spells"))
    rows.append(f'''<div class="row" data-lv="{lv}" id="lv{lv}">
 <div class="row-head"><button class="chk" aria-label="Mark level {lv} done" data-k="lv{lv}"></button>
  <span class="lv">{lv}</span><span class="sum">{'<span class="tb">Trainer</span> ' if lv in TR else ''}{E(summ)}</span><span class="zone">{E(zone(lv))}</span></div>
 <div class="row-body">{mini_bars(lv)}{("<div class=\"barch\"><b>Bars</b> " + " · ".join(E(c) for c in bar_changes(lv)) + "</div>") if bar_changes(lv) else ""}{trainer_html(lv)}{tal}<ul>{lis}</ul><div class="zline">{zicon(zone(lv))}Zone: {E(zone(lv))} <span class="src">(general Alliance path; Forever quest XP may differ)</span></div></div>
</div>''')

def ck(key, text, sub=""):
    s = f'<small>{sub}</small>' if sub else ""
    return f'<label class="ci"><input type="checkbox" data-k="{key}"><span>{text}{s}</span></label>'

talent_list = "".join(ck(f"t{lv}", f"<b>{lv}</b> · {E(TAL[lv][0])} {TAL[lv][1]}") for lv in range(10, 31))

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Gordan Stark · Ret Paladin</title>
<meta name="theme-color" content="#0b1526">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Gordan Stark">
<link rel="apple-touch-icon" href="icons/icon-180.png"><link rel="icon" href="icons/icon-192.png">
<link rel="manifest" href="manifest.webmanifest"><link rel="stylesheet" href="style.css">
</head><body>
<header class="bar">
 <div class="bar-top"><div class="who"><span class="crest">{icimg("_human","ci1")}{icimg("_paladin","ci1")}{icimg("_ret","ci1")}</span><b>Gordan Stark</b><span>Human Ret Paladin · Lv <span id="curLv">1</span></span></div>
  <div class="lvpick"><button id="lvDown" aria-label="Level down">−</button><select id="lvSel" aria-label="Current level"></select><button id="lvUp" aria-label="Level up">+</button></div></div>
 <button id="rotBtn" class="rotbtn" aria-expanded="false">⚔ Rotation <span id="rotTag"></span></button>
 <div id="rot" class="rot" hidden></div>
 <nav class="tabs"><a href="#guide">1-60</a><a href="#ret">Ret</a><a href="#gear">Gear</a><a href="#prof">Profs</a><a href="#prot">Prot</a><a href="#bars">Bars</a><a href="#back">Break</a><a href="#me">Me</a></nav>
</header>
<main>
<section id="t-guide" class="tab"><h2>Leveling 1-60</h2>
 <p class="note">Tap a level to open it. Check it off and it collapses. Levels 1-30 match the beta; 31-60 is mostly unannounced.</p>
 <label class="ci inline"><input type="checkbox" id="hideDone"> <span>Hide finished levels</span></label>
 {''.join(rows)}
</section>

<section id="t-ret" class="tab"><h2>{icimg("_ret","hic")}Retribution</h2>
 <div class="card"><h3>Talents to 30</h3>{talent_list}
 <p class="src">Talent names match the Icy Veins "Retribution Focused" build (Benediction, Sanctified Judgement, Pursuit of Justice, Sacred Arbiter, Seal of Command, Vengeance). Icy Veins also highlights <b>Holy Conduit</b> and <b>Improved Judgement</b>, which aren't in this plan. Icy Veins doesn't print a level-by-level order, so double-check it in their calculator. <a href="{IV}">Icy Veins</a></p></div>
 <div class="card"><h3>Rotation</h3><ol>
  <li>Always keep a Seal up. <b>Before 20:</b> Seal of Righteousness. <b>20+:</b> Seal of Command with a slow two-hander and no on-hit effect. SoR is still better with high Spell Power, a fast weapon, or "Strike of the Hydra" gear.</li>
  <li><b>Judgement</b> on cooldown. It does <b>not</b> use up your Seal in Forever.</li>
  <li><b>Holy Strike</b> on cooldown (from level 6).</li>
  <li>Long fights: Seal of the Crusader, then Judgement (debuff), then switch back to SoR/SoC.</li>
  <li>With SoC: Hammer of Justice stun, then Judgement for burst.</li>
  <li>Exorcism on Undead and Demons.</li>
  <li><b>Consecration</b> (20+) for groups of up to about 4. It costs a lot of mana.</li>
 </ol><p>Buffs: Blessing of Might or Kings on yourself, plus Retribution Aura.</p>
 <p class="src">Source: <a href="{IV}">Icy Veins Ret</a>. Blessing duration: 60 min in Forever (from earlier research, not on the Icy Veins page).</p></div>
 <div class="card"><h3>Staying alive solo</h3><ul>
  <li>Mana is extra health. Holy Light yourself and keep going instead of sitting to eat (Icy Veins).</li>
  <li>No AoE before 20, so pull one mob at a time.</li>
  <li>Emergencies: Divine Protection, Lay on Hands, Hammer of Justice. Human <b>Will to Survive</b> breaks stuns.</li>
  <li>Bandages and potions for when you're out of mana.</li></ul></div>
 <div class="card"><h3>Helping strangers</h3><ul>
  <li><b>Blessings:</b> Might for melee, Wisdom for casters, Kings if you're not sure.</li>
  <li><b>Heals:</b> Holy Light on anyone who's struggling.</li>
  <li><b>Blessing of Protection:</b> makes a caster or healer immune to physical damage, but they can't attack while it's on.</li>
  <li><b>Blessing of Freedom:</b> breaks roots and slows.</li>
  <li><b>Purify:</b> removes poison and disease.</li>
  <li><b>Lay on Hands:</b> full heal, uses all your mana.</li>
  <li><b>Redemption:</b> brings back dead players out of combat.</li>
 </ul><p class="src">Source: <a href="{IVP}">Icy Veins Prot</a> utility section.</p></div>
</section>

<section id="t-gear" class="tab"><h2>Gear & Stats</h2>
 <div class="card"><h3>Stat priority (Icy Veins, beta Lv30)</h3><ol>
  <li><b>Weapon DPS</b>: your #1 upgrade. Slow is a bit better for Holy Strike.</li>
  <li>Hit / Expertise (rare before 30)</li><li>Crit</li><li><b>Spell Power</b>: scales Judgement, Holy Strike, Consecration</li>
  <li>Strength</li><li>Intellect</li><li>Agility (fine if it's there, don't chase it)</li><li>Stamina</li><li>Spirit</li></ol>
  <p>Items with <b>both Strength and Spell Power</b> beat items with only one. Greens "of Holy Wrath" can be great.</p>
  <p class="src warn">This is different from the earlier shorthand (Str &gt; Crit &gt; Stam &gt; Int, skip Agi/Spirit). On Icy Veins, Spell Power ranks above Strength and Stamina sits low. Stamina still keeps you safer solo. <a href="{IV}">Icy Veins</a></p></div>
 <div class="card"><h3>Weapon</h3><p>Two-hander. A <b>sword</b> gets Human Sword Specialization (+2% crit). Maces and axes are fine if they hit harder.</p>
 <p>Level-30 options: Manual Crowd Pummeler (Gnomeregan), Strike of the Hydra (BFD, Aku'mai), Boneslicer (Stockades, Dextren Ward), Corpsemaker (RFK, Overlord Ramtusk), Rock Pulverizer (Badlands, Alliance quest).</p></div>
 <div class="card"><h3>Blacksmithing pieces (Merchant's Favor recipes)</h3><ul>
  <li>Crusader's Chain Helm</li><li>Crusader's Silvered Chain Shirt</li><li>Justicar's Belt / Crusader's Chain Belt</li><li>Crusader's Silvered Chain Leggings</li><li>Crusader's Boots</li></ul>
  <p>Also: Cloak of the Divine Storm (Alliance Paladin quest chain), Libram: Tenets of the Silver Hand (Enchanting).</p>
  <p class="src">Source: <a href="{IV}">Icy Veins Lv30 gear table</a>. Exact recipe levels (20 vs 30) aren't listed.</p></div>
</section>

<section id="t-prof" class="tab"><h2>Professions</h2>
 <div class="card"><h3>{icimg("_mining")}Mining + {icimg("_bs")}Blacksmithing ✔</h3><p>Icy Veins' top leveling combo for Ret. You craft your own mail and weapons, and Forever's Merchant's Favor recipes are some of the best gear at 30.</p>
 <p>Bonus: sharpening stones and weightstones for your weapon.</p></div>
 <div class="card"><h3>Secondary</h3><ul><li><b>Cooking:</b> Well Fed buff food gives stats and <b>+5% XP from kills</b> in Forever. Cooking also makes Campfires.</li><li><b>First Aid:</b> bandages, and in Forever it can make healing potions. It also adds a Stamina First Aid Kit to Campfires.</li></ul>
 <p class="src"><a href="{IV}">Icy Veins Ret</a>, <a href="{IVP}">Icy Veins Prot</a></p></div>
</section>

<section id="t-prot" class="tab"><h2>{icimg("_prot","hic")}Protection (alt spec)</h2>
 <div class="card"><h3>Dual spec</h3><p><b>Level 40</b>, bought from your class trainer in a capital city. Several sites cite Blizzard's 30 Sep class deep dive for this.</p>
 <p class="src warn">Cost isn't confirmed. One site says 50g, but Blizzard hasn't given a price. The beta caps at 30, so nobody has tested it yet.</p></div>
 <div class="card"><h3>Prep before 40 (bank it)</h3>
  {ck("p1","A one-handed weapon and a shield (upgrade the shield as you level)")}
  {ck("p2","Tank pieces: Stamina, Defense, Armor, Block, plus Spell Power")}
  {ck("p3","Water, plenty of it. Mana is your limit when tanking.")}
  {ck("p4","Mana potions for after Lay on Hands")}
  {ck("p5","Keybind Seal of Fury and Righteous Fury now so they're ready")}
 </div>
 <div class="card"><h3>How to tank</h3><ol>
  <li><b>Righteous Fury</b> up at all times (threat).</li>
  <li><b>Seal of Fury</b>: when you Judge with it, it taunts for 4 seconds. That's new in Forever.</li>
  <li><b>Consecration</b> for AoE threat, when your mana allows.</li>
  <li>Save <b>Judgement</b> for taunting back mobs that get loose.</li>
  <li>Holy Strike on cooldown. Exorcism on Undead and Demons.</li></ol>
  <p>Talents (Lv30 plan): Redoubt, Precision, Anticipation, Shield Specialization, Improved Seal of Fury, then Holy Conduit in Ret.</p>
  <p>Stats: Spell Power &gt; Hit &gt; Stamina &gt; Defense &gt; Armor &gt; Block &gt; Int &gt; Str &gt; Agi.</p>
  <p class="src">Source: <a href="{IVP}">Icy Veins Prot</a>. Note that Icy Veins picks Dwarf for Prot (Stoneform), but Human works.</p></div>
</section>

<section id="t-bars" class="tab"><h2>My Bars · Lv <span id="barLv"></span></h2>
 <p class="note">Change the level in the top bar. Gold outline = new at this level. Dashed = placement for 31-60 not confirmed.</p>
 <div id="barsBox"></div>
 <div class="card"><h3><img class="ic" src="icons/spells/{SPELLS["Blessing of Might"]["i"]}.jpg" alt="">Bow &amp; Buff macro (Top 5, from Lv 4)</h3>
 <pre id="macroTxt">#showtooltip Blessing of Might
/cast Blessing of Might
/bow</pre><button id="copyMacro" class="ghost">Copy macro</button>
 <p class="src">Make it in-game with /macro, then New. Character macros hold 255 characters, and this one is far under. That limit is from standard WoW and wasn't checked against Forever.</p></div>
 <p class="src">Learn levels from <a href="{TFE}">The Forever Era</a> beta client data. Seal of Command needs the talent (taken at 20 in your plan). Spells after 30 can't be tested in the beta.</p>
</section>
<section id="t-back" class="tab"><h2>Back from a break</h2>
 <div class="card big"><h3>30-second rotation</h3><ol>
  <li>Seal up (SoR before 20, SoC with a slow 2H).</li><li>Judgement on CD (keeps your seal).</li><li>Holy Strike on CD.</li><li>Consecration if 3+ mobs.</li><li>Low health: Holy Light. Panic: Divine Protection, then Lay on Hands.</li><li>Buffs: Might/Kings + Ret Aura.</li></ol></div>
 <div class="card"><h3>Bag check</h3>
  {ck("b1","Water (lots)")}{ck("b2","Well Fed food (+5% XP)")}{ck("b3","Bandages / healing potions")}{ck("b4","Mana potions")}{ck("b5","Mining pick + blacksmith hammer")}{ck("b6","Sharpening stone / weightstone")}{ck("b7","Hearthstone")}
  <div id="customBags"></div>
  <div class="addrow"><input id="bagNew" placeholder="Add an item…"><button id="bagAdd">Add</button></div>
  <button id="resetBags" class="ghost">Uncheck all</button></div>
 <div class="card"><h3>Notes</h3><textarea id="notes" rows="5" placeholder="Where I left off…"></textarea></div>
</section>

<section id="t-me" class="tab"><h2>{icimg("_human","hic")}My Character</h2><div id="meBox">Loading…</div>
<div class="card credits"><h3>Credits</h3><p>Spell, item, class, race and zone icons © Blizzard Entertainment, downloaded once from Wowhead's public icon CDN (wow.zamimg.com) and bundled in this app. Icon choices and spell/talent links: <a href="https://theforeverera.com/en/spells/paladin/levels/" target="_blank" rel="noopener">The Forever Era</a>. Personal, non-commercial fan page; not affiliated with Blizzard.</p></div></section>
</main>
<script>window.SPELLS={json.dumps({k:v for k,v in SPELLS.items() if not k.startswith("_")})};window.BARS={json.dumps(BARDATA)};</script><script src="app.js"></script></body></html>'''
import re as _re
NAMES = sorted([k for k in SPELLS if not k.startswith("_") and SPELLS[k]["u"]], key=len, reverse=True)
NRX = _re.compile(r"(?<![\w'])(" + "|".join(_re.escape(n) for n in NAMES) + r")(?![\w'])")
def link(n):
    v = SPELLS[n]
    return f'<a class="sp" href="{v["u"]}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/{v["i"]}.jpg" alt="" loading="lazy">{E(n)}</a>'
def linkify(doc):
    body_start = doc.index("<main>"); body_end = doc.index("</main>")
    head, body, tail = doc[:body_start], doc[body_start:body_end], doc[body_end:]
    out = []; st = []
    VOID = ("img","input","br","meta","link","hr")
    for part in _re.split(r"(<[^>]+>)", body):
        if part.startswith("<"):
            m = _re.match(r"<(/?)([a-z0-9]+)", part.lower())
            if m:
                tag = m.group(2)
                if m.group(1):
                    while st:
                        t2, _ = st.pop()
                        if t2 == tag: break
                elif tag not in VOID and not part.endswith("/>"):
                    t = part.lower()
                    st.append((tag, tag in ("a","textarea","option","script","button","pre") or 'class="sum"' in t or 'class="row-head"' in t))
            out.append(part)
        else:
            out.append(part if any(f for _, f in st) else NRX.sub(lambda m: link(m.group(1)), part))
    return head + "".join(out) + tail
PAGE = linkify(PAGE)
open("index.html", "w").write(PAGE)
icons = sorted({v["i"] for v in SPELLS.values()})
sw = open("sw.js").read()
sw = _re.sub(r"const C='pal-v\d+',F=\[[^\]]*\]", "const C='pal-v7',F=" + json.dumps(['./','index.html','style.css','app.js','data.json','manifest.webmanifest','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png'] + [f"icons/spells/{i}.jpg" for i in icons]), sw)
open("sw.js","w").write(sw)
print("built", len(PAGE))
