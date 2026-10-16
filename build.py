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

# Protection plan 10-30: order matches classicwowforever (Oct 14) + Mobalytics (Oct 15). Beyond 30: Mobalytics only, unconfirmed.
TALP = {}
def _run(lv0, name, n, d):
    for i in range(n): TALP[lv0 + i] = (name, f"{i+1}/{n}", d)
_run(10, "Redoubt", 5, "Hits on you can give extra block chance for a short time")
_run(15, "Precision", 3, "+3% hit with all spells and attacks at 3/3")
TALP[18] = ("Anticipation", "1/5", "+Defense (8 at 2 points)"); TALP[19] = ("Anticipation", "2/5", "+Defense (8 at 2 points)")
TALP[20] = ("Improved Seal of Fury", "1/1", "Mana back each time Seal of Fury's absorb is used up")
for _i, _lv in enumerate(range(21, 24)): TALP[_lv] = ("Shield Specialization", f"{_i+1}/3", "Shield blocks 30% more; a block gives back 4% Mana at 3/3 (3 sec limit)")
TALP[24] = ("Improved Righteous Fury", "1/3", "2% less damage taken while Righteous Fury is on")
TALP[25] = ("Swift Judgement", "1/1", "Resets Judgement and makes the next one free (1 min cooldown)")
for _i, _lv in enumerate(range(26, 29)): TALP[_lv] = ("One-Handed Weapon Specialization", f"{_i+1}/3", "+10% damage with your one-hander at 3/3")
TALP[29] = ("Improved Righteous Fury", "2/3", "4% less damage taken while Righteous Fury is on")
TALP[30] = ("Templar's Bulwark", "1/1", "Absorb equal to your full health for 8 sec (5 min cooldown)")
for _i, _lv in enumerate(range(31, 36)): TALP[_lv] = ("Reckoning", f"{_i+1}/5", "Extra attacks after a block or a crit on you")
TALP[36] = ("Improved Righteous Fury", "3/3", "6% less damage taken while Righteous Fury is on")
for _i, _lv in enumerate(range(37, 40)): TALP[_lv] = ("Iron Creed", f"{_i+1}/5", "Holy Strike gives a short damage cut with Righteous Fury on")
TALP[40] = ("Holy Shield", "1/1", "+30% block for 10 sec (needs Templar's Bulwark)")
PROT_ORDER = [(lv, TALP[lv][0], TALP[lv][1]) for lv in range(10, 31)]

MS_C = {
 1: ["Start in Northshire Abbey, Elwynn Forest. Seal of Righteousness + auto-attack."],
 5: ["Pick up Mining at a trainer; Blacksmithing in Goldshire/Stormwind. Cooking + First Aid too."],
 6: ["Holy Strike unlocked: press it on cooldown when you have mana. [Icy Veins]"],
 10: ["Talents open. Head toward Westfall / Loch Modan."],
 30: ["Beta cap. Check Merchant's Favor Blacksmithing recipes (Crusader's set). [Icy Veins]"],
 40: ["Dual Specialization opens (Blizzard Paladin deep dive). Cost not published. See Off spec tab."],
 60: ["Max level. Endgame gear/talents not published yet."],
}
MS_P = {
 10: ["Seal of Fury learned. Wear a one-hander and a shield now: its absorb only works with a shield."],
 16: ["Righteous Fury learned. Keep it on (Aura bar 7); Improved Righteous Fury only works while it is up."],
 20: ["Consecration learned: full damage on the first 4 enemies only (Blizzard). Oct 15 build cut its Spell Power scaling."],
 30: ["Beta cap. Templar's Bulwark shares Forbearance with Divine Protection: use one or the other."],
}
ZONES = [(1,"Northshire / Elwynn Forest"),(10,"Westfall / Loch Modan"),(18,"Redridge Mountains"),(20,"Duskwood / Wetlands"),(25,"Ashenvale / Wetlands"),(30,"Hillsbrad / Alterac & beyond"),(40,"Stranglethorn / Arathi / Desolace"),(45,"Tanaris / Feralas / Hinterlands"),(50,"Un'Goro / Felwood / Searing Gorge"),(55,"Winterspring / Plaguelands")]
SPELLS = json.load(open("spells.json"))
from dungeons_data import DUNGEONS, IVD, WHQ
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
ITEM = {"Mount": 1, "Food": 1, "Water": 1, "Hearthstone": 1, "Bow & Buff": 4}
# each slot: candidates in order (name, unconfirmed_placement); latest learned wins
BARS = {
 "top": [[("Divine Protection",0),("Divine Shield",1)], [("Holy Light",0)], [("Blessing of Protection",0)],
         [("Blessing of Freedom",0)], [("Purify",0),("Cleanse",1)], [("Hammer of Wrath",1)], [("Lay on Hands",0)]],
 "mid": [[("Seal of Righteousness",0),("Holy Strike",0)], [("Judgement",0)], [("Seal of Righteousness@6",0),("Seal of Command",0)],
         [("Consecration",0)], [("Hammer of Justice",0)], [("Flash of Light",0)], [("Divine Intervention",0)]],
 "bot": [[("Food",0)], [("Water",0)], [("Bow & Buff",0)], [("Exorcism",0)],
         [("Redemption",0)], [("Hearthstone",0)], [("Mount",0),("Summon Warhorse",1)]],
 "aur": [[("Devotion Aura",0)], [("Retribution Aura",0)], [("Concentration Aura",0)], [("Shadow Resistance Aura",0)],
         [("Frost Resistance Aura",0)], [("Fire Resistance Aura",0)], [("Righteous Fury",0)]],
}
import copy
BARS_P = copy.deepcopy(BARS)
BARS_P["top"][0] = [("Divine Protection",0),("Templar's Bulwark",0)]
BARS_P["mid"][2] = [("Seal of Righteousness@6",0),("Seal of Fury",0)]
BARS_P["mid"][6] = [("Swift Judgement",0)]
def bars_at(lv, BARS=BARS):
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
BARDATA = {lv: bars_at(lv, BARS_P) for lv in range(1, 61)}
def bar_changes(lv, BARDATA=BARDATA):
    a, b = BARDATA[lv], BARDATA.get(lv-1, {"top":[None]*7,"mid":[None]*7,"bot":[None]*7,"aur":[None]*7})
    ch = []
    for r, lab in (("top","Top"),("mid","Middle"),("bot","Bottom"),("aur","Aura")):
        for i in range(7):
            if a[r][i] != b[r][i] and a[r][i]:
                ch.append(f'{lab} {i+1 if r=="mid" else i+1}: {a[r][i]["n"]}' + (" (unconfirmed)" if a[r][i]["u"] else ""))
    return ch
def icon_of(n, lv=1):
    if n == "Bow & Buff": return SPELLS["Blessing of Kings" if lv >= 20 else "Blessing of Might"]["i"]
    v = SPELLS.get(n); return v["i"] if v else None
def mini_bars(lv):
    a, b = BARDATA[lv], BARDATA.get(lv-1)
    h = '<div class="mini">'
    for r in ("top","mid","bot"):
        for i, x in enumerate(a[r]):
            if not x: h += '<span class="mb e"></span>'; continue
            nw = (b is None) or b[r][i] != x
            ic = icon_of(x["n"], lv)
            h += f'<span class="mb{" n" if nw else ""}{" u" if x["u"] else ""}" title="{E(x["n"])}">' + (f'<img src="icons/spells/{ic}.jpg" alt="" loading="lazy">' if ic else E(x["n"][:3])) + '</span>'
    return h + '</div>'
SIDE={"A":"Alliance","S":"Shared","H":"Horde-side quests"}
def dline(lv):
    ds=[d for d in DUNGEONS if d[1]==lv]
    if not ds: return ""
    return '<div class="dline"><b>🏰 Dungeon opens</b> ' + " · ".join(f'<a href="#dungeons">{E(d[0])}</a> ({d[1]}-{d[2]}{", new" if d[4] else ""}{", Horde-side" if d[3]=="H" else ""})' for d in ds) + ' <span class="src">Icy Veins ranges</span></div>'
def dcard(d):
    n,lo,hi,side,new,where,qs,note=d
    q="".join(f'<li><b>{E(a)}</b> · {E(b)}</li>' for a,b in qs) or '<li>Not known yet.</li>'
    return f'<div class="card dcard" data-lo="{lo}"><h3>{E(n)} <span class="rank">{lo}-{hi}</span>{' <span class="tb">New</span>' if new else ''} <span class="src">{SIDE[side]}</span></h3><p><b>Where:</b> {E(where)}</p><p><b>Quests to grab first</b></p><ul>{q}</ul><p class="note">{E(note)}</p><p><b>Prot loot:</b> Not listed here. See the Gear tab for level-30 picks.</p></div>'
rows = []
def barch(lv):
    p = bar_changes(lv, BARDATA)
    return '<div class="barch"><b>Bars</b> ' + " · ".join(E(c) for c in p) + '</div>' if p else ""
for lv in range(1, 61):
    items = MS_C.get(lv, []) + MS_P.get(lv, [])
    tal = ""
    if lv in TALP:
        n, r, d = TALP[lv]
        if lv <= 30:
            tal = f'<div class="tal"><b>{E(n)}</b> <span class="rank">{r}</span><div class="eff">{E(d)}</div><span class="src">Protection · order: classicwowforever + Mobalytics</span></div>'
        else:
            tal = f'<div class="tal unk"><b>{E(n)}</b> <span class="rank">{r}</span><div class="eff">{E(d)}</div><span class="src warn">Unconfirmed: one source (Mobalytics); the beta stops at 30</span></div>'
    elif lv > 30:
        tal = '<div class="tal unk"><b>Talent point</b><div class="eff">41-60 builds not published (beta cap 30). Will fill in at launch.</div><span class="src warn">Unannounced</span></div>'
    lis = "".join(f'<li>{E(x)}</li>' for x in items)
    summ = TALP[lv][0] if lv in TALP else ((items[0][:48] + ("…" if len(items[0]) > 48 else "")) if items else (f"Trainer: {len(TR[lv])} new" if lv in TR else "No new spells"))
    rows.append(f'''<div class="row" data-lv="{lv}" id="lv{lv}">
 <div class="row-head"><button class="chk" aria-label="Mark level {lv} done" data-k="lv{lv}"></button>
  <span class="lv">{lv}</span><span class="sum">{'<span class="tb">Trainer</span> ' if lv in TR else ''}{E(summ)}</span><span class="zone">{E(zone(lv))}</span></div>
 <div class="row-body">{barch(lv)}{trainer_html(lv)}{tal}{dline(lv)}<ul>{lis}</ul><div class="zline">{zicon(zone(lv))}Zone: {E(zone(lv))} <span class="src">(general Alliance path; Forever quest XP may differ)</span></div></div>
</div>''')

def ck(key, text, sub=""):
    s = f'<small>{sub}</small>' if sub else ""
    return f'<label class="ci"><input type="checkbox" data-k="{key}"><span>{text}{s}</span></label>'

talent_list = "".join(ck(f"t{lv}", f"<b>{lv}</b> · {E(TAL[lv][0])} {TAL[lv][1]}") for lv in range(10, 31))
talent_list_p = "".join(ck(f"pt{lv}", f"<b>{lv}</b> · {E(n)} {r}") for lv, n, r in PROT_ORDER)

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Gordan Stark · Prot Paladin</title>
<meta name="theme-color" content="#0b1526">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Gordan Stark">
<link rel="apple-touch-icon" href="icons/icon-180.png"><link rel="icon" href="icons/icon-192.png">
<link rel="manifest" href="manifest.webmanifest"><link rel="stylesheet" href="style.css">
</head><body>
<header class="bar">
 <div class="bar-top"><div class="who"><span class="crest">{icimg("_human","ci1")}{icimg("_paladin","ci1")}<img class="ci1" src="icons/spells/{SPELLS["_prot"]["i"]}.jpg" alt=""></span><b>Gordan Stark</b><span>Human Prot Paladin · Lv <span id="curLv">1</span></span></div>
  <div class="lvpick"><button id="lvDown" aria-label="Level down">−</button><select id="lvSel" aria-label="Current level"></select><button id="lvUp" aria-label="Level up">+</button></div></div>
 <button id="rotBtn" class="rotbtn" aria-expanded="false">⚔ Rotation <span id="rotTag"></span></button>
 <div id="rot" class="rot" hidden></div>
 <nav class="tabs"><a href="#guide">1-60</a><a href="#bars">Bars</a><a href="#prot">Prot</a><a href="#dungeons">Dungeons</a><a href="#gear">Gear</a><a href="#prof">Profs</a><a href="#offspec">Off spec</a><a href="#back">Break</a><a href="#me">Me</a></nav>
</header>
<main>
<section id="t-guide" class="tab"><h2>Leveling 1-60</h2>
 <p class="note">Tap a level to open it. Check it off and it collapses. Levels 1-30 match the beta; 31-60 is mostly unannounced.</p>
 <label class="ci inline"><input type="checkbox" id="hideDone"> <span>Hide finished levels</span></label>
 {''.join(rows)}
</section>

<section id="t-offspec" class="tab"><h2>{icimg("_ret","hic")}Off spec: Retribution</h2>
 <p class="note">Your main spec is Protection. This tab is only for a Ret swap.</p>
 <div class="card"><h3>Dual spec</h3><p><b>Level 40</b>, from a class trainer in a capital city (Blizzard's Paladin deep dive). Price isn't published. That's how you'd add Ret as a second spec.</p></div>
 <div class="card"><h3>Spare gear (keep in bags)</h3>
  {ck("o1","A slow two-hander (3.0+ speed) for Seal of Command")}
  {ck("o2","A fast weapon, only if its DPS is clearly higher")}
  {ck("o3","Pieces with both Strength and Spell Power")}
  <ul><li><b>Slow 2H:</b> Seal of Righteousness until 20, then Seal of Command (talent). Judge after a Hammer of Justice stun for burst. Slower two-handers make Holy Strike hit harder.</li>
  <li><b>Fast weapon or high Spell Power:</b> Seal of Righteousness at every level.</li>
  <li>Any weapon type gets Human Ruthless (+2% crit).</li></ul>
  <p>Level-30 options: Manual Crowd Pummeler (Gnomeregan), Strike of the Hydra (BFD, Aku'mai), Boneslicer (Stockades, Dextren Ward), Corpsemaker (RFK, Overlord Ramtusk), Rock Pulverizer (Badlands, Alliance quest).</p>
  <details><summary>Ret stats (Icy Veins, beta Lv30)</summary><ol>
  <li><b>Weapon DPS</b>: your #1 upgrade. Slow is a bit better for Holy Strike.</li>
  <li>Hit / Expertise (rare before 30)</li><li>Crit</li><li><b>Spell Power</b>: scales Judgement, Holy Strike, Consecration</li>
  <li>Strength</li><li>Intellect</li><li>Agility (fine if it's there, don't chase it)</li><li>Stamina</li><li>Spirit</li></ol>
  <p>Items with <b>both Strength and Spell Power</b> beat items with only one. Greens "of Holy Wrath" can be great.</p>
  <p class="src warn">This is different from the earlier shorthand (Str &gt; Crit &gt; Stam &gt; Int, skip Agi/Spirit). On Icy Veins, Spell Power ranks above Strength and Stamina sits low. Stamina still keeps you safer solo. <a href="{IV}">Icy Veins</a></p></details></div>
 <div class="card"><h3>Ret bars vs Prot bars</h3><ul>
  <li><b>Middle 3:</b> Seal of Righteousness, then Seal of Command from 20 with a slow 2H (talent). Prot has Seal of Fury.</li>
  <li><b>Middle 7:</b> Divine Intervention at 30. Prot has Swift Judgement.</li>
  <li><b>Top 1:</b> Divine Protection. Prot swaps in Templar's Bulwark at 30.</li>
  <li>Everything else is the same.</li></ul></div>
 <div class="card"><h3>Talents to 30</h3>{talent_list}
 <p class="src">Talent names match the Icy Veins "Retribution Focused" build (Benediction, Sanctified Judgement, Pursuit of Justice, Sacred Arbiter, Seal of Command, Vengeance). Icy Veins also highlights <b>Holy Conduit</b> and <b>Improved Judgement</b>, which aren't in this plan. Icy Veins doesn't print a level-by-level order, so double-check it in their calculator. <a href="{IV}">Icy Veins</a></p></div>
 <div class="card"><h3>Rotation</h3><ol>
  <li>Always keep a Seal up. <b>Before 20:</b> Seal of Righteousness. <b>20+:</b> Seal of Command with a slow two-hander and no on-hit effect. SoR is still better with high Spell Power, a fast weapon, or "Strike of the Hydra" gear.<span class="src warn">Oct 15 build: Seal of Righteousness got about half as much from Spell Damage as before (a bug fix), so the Spell Power advice may be out of date.</span></li>
  <li><b>Judgement</b> on cooldown. It does <b>not</b> use up your Seal in Forever.</li>
  <li><b>Holy Strike</b> on cooldown (from level 6).</li>
  <li>Long fights: Seal of the Crusader, then Judgement (debuff), then switch back to SoR/SoC.</li>
  <li>With SoC: Hammer of Justice stun, then Judgement for burst.</li>
  <li>Exorcism on Undead and Demons.</li>
  <li><b>Consecration</b> (20+) for groups of up to about 4. It costs a lot of mana.</li>
 </ol><p>Buffs: Blessing of Might or Kings on yourself, plus Retribution Aura.</p>
 <p class="src">Source: <a href="{IV}">Icy Veins Ret</a>. Blessing duration: 60 min in Forever (from earlier research, not on the Icy Veins page).</p></div>
 <div class="card"><h3>Ret notes by level</h3><ul>
  <li><b>10:</b> Equip the slowest two-hander you can find.</li>
  <li><b>20:</b> Consecration is your first AoE. Mana-hungry: 2-3 mobs max solo. Take the Seal of Command talent (best with a slow 2H). <span class="src">Icy Veins</span></li>
  <li><b>30:</b> Shockadin (Holy Shock) build becomes possible. Not our plan.</li></ul></div>
 <details class="card"><summary><b>More Ret notes</b></summary><div class="card" style="margin-top:8px"><h3>Staying alive solo</h3><ul>
  <li>Mana is extra health. Holy Light yourself and keep going instead of sitting to eat (Icy Veins).</li>
  <li>No AoE before 20, so pull one mob at a time.</li>
  <li>Emergencies: Divine Protection, Lay on Hands, Hammer of Justice. Human <b>Will to Survive</b> breaks stuns.</li>
  <li>Bandages and potions for when you're out of mana.</li></ul></div><div class="card"><h3>Helping strangers</h3><ul>
  <li><b>Blessings:</b> Might for melee, Wisdom for casters, Kings if you're not sure.</li>
  <li><b>Heals:</b> Holy Light on anyone who's struggling.</li>
  <li><b>Blessing of Protection:</b> makes a caster or healer immune to physical damage, but they can't attack while it's on.</li>
  <li><b>Blessing of Freedom:</b> breaks roots and slows.</li>
  <li><b>Purify:</b> removes poison and disease.</li>
  <li><b>Lay on Hands:</b> full heal, uses all your mana.</li>
  <li><b>Redemption:</b> brings back dead players out of combat.</li>
 </ul><p class="src">Source: <a href="{IVP}">Icy Veins Prot</a> utility section.</p></div></details>
 <div class="card big"><h3>{icimg("_paladin","ic")}Paladin weapon quest (Lv 20)</h3>
 <p><b>The Tome of Valor</b> (starts in Stormwind, defend Daphne Stilwell in Westfall) leads to <b>The Test of Righteousness</b> from <b>Jordan Stilwell</b> just outside the Ironforge gates. He needs 4 materials: Whitestone Oak Lumber (Deadmines), Jordan's Refined Ore Shipment (Mo'grosh Stronghold elites, Loch Modan, via Bailor Stonehand in Thelsamar), Jordan's Smithing Hammer (Shadowfang Keep), and Purified Kor Gem (Blackfathom Deeps).</p>
 <p><b>Reward: Verigan's Fist</b>, a 2H mace, 65-99 damage, 3.20 speed, +5 Sta +10 Spi +6 Int, with a chance on hit for 39-59 Holyfire damage (3x vs Fire and Earth elementals). That's a slow 2H, so it suits Seal of Command.</p>
 <p class="src">Sources: <a href="https://forg.gg/en/forever/tips/verigans-fist">ForG</a>, <a href="https://endgametools.com/en/wow-forever/news/wow-forever-wolfsbane">Endgame Tools</a> (beta build 70291), <a href="https://theforeverera.com/en/quests/1806/">The Forever Era</a>. Stats are beta and may change by launch. Not on Icy Veins yet.</p></div>
 
</section>

<section id="t-gear" class="tab"><h2>Gear & Stats</h2>
 <div class="card"><h3>Prot gear (1H + shield)</h3>
 <p><b>Stats:</b> Stamina, Armor, Defense first. Intellect and Strength come next (sources swap those two).</p>
 <p><b>Weapon:</b> a one-hander plus a shield. Seal of Fury adds the same Holy damage every swing, so Blizzard says a faster weapon is better for tanking.</p>
 <p>Level-30 picks: Pronged Reaver (main hand, Charlga Razorflank, Razorfen Kraul), Bonepile Gaze (off hand, Lyn the Ignored, City of Dalaran), Tusken Helm (head, Overlord Ramtusk, Razorfen Kraul), Ironspine's Ribcage (chest, Ironspine, Scarlet Monastery), Supple Bellyskin Leggings (legs, Saltspine, Excavation Site: Wetlands).</p>
 <p class="src">Stats: <a href="https://classicwowforever.com/class-guides/paladin/protection/">classicwowforever</a> and <a href="https://leprestore.com/guides/world-of-warcraft-forever/wow-forever-protection-paladin-guide-best-builds-race-professions/">Leprestore</a> put Stamina, Armor, Defense first and differ on Intellect vs Strength. <a href="https://mobalytics.gg/wow-forever/classes/protection-paladin-guide">Mobalytics</a> puts Strength first for leveling. Gear: classicwowforever's list. Wowhead also lists Painwalker Buckler, Blade of Silverlaine and Skullbreaker.</p></div>
 <div class="card"><h3>Blacksmithing pieces (Merchant's Favor recipes)</h3><ul>
  <li>Crusader's Chain Helm</li><li>Crusader's Silvered Chain Shirt</li><li>Justicar's Belt / Crusader's Chain Belt</li><li>Crusader's Silvered Chain Leggings</li><li>Crusader's Boots</li></ul>
  <p>Also: Cloak of the Divine Storm (Alliance Paladin quest chain), Libram: Tenets of the Silver Hand (Enchanting).</p>
  <p class="src">Source: <a href="{IV}">Icy Veins Lv30 gear table</a>. Exact recipe levels (20 vs 30) aren't listed.</p></div>
 <div class="card"><h3>{icimg("_human","ic")}Human racials</h3><ul>
  <li><b>Ruthless</b> (passive): +2% critical strike chance with all spells and attacks. Any weapon, no sword needed.</li>
  <li><b>Will to Survive</b> (active): removes stuns.</li>
  <li><b>Perception</b> (active): better stealth detection for 20 sec.</li>
  <li><b>The Human Spirit</b> (passive): +5% Spirit.</li></ul>
  <p class="src">Ruthless replaced Sword Specialization in the Oct 15 build (1.60.1.70425). The other three aren't in that build's racial changes. Diplomacy is now a Legacy talent, not a racial. <a href="https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/">Warcraft Tavern</a>, <a href="https://talentsforever.com/builds">Talents Forever</a>, <a href="https://wowdb.wiki/forever/spells/racials/human">WoWDB wiki</a>.</p></div>
</section>

<section id="t-prof" class="tab"><h2>Professions</h2>
 <div class="card"><h3>{icimg("_mining")}Mining + {icimg("_bs")}Blacksmithing ✔</h3><p>Icy Veins' top leveling combo for Ret. You craft your own mail and weapons, and Forever's Merchant's Favor recipes are some of the best gear at 30.</p>
 <p>Bonus: sharpening stones and weightstones for your weapon.</p></div>
 <div class="card"><h3>Secondary</h3><ul><li><b>Cooking:</b> Well Fed buff food gives stats and <b>+5% XP from kills</b> in Forever. Cooking also makes Campfires.</li><li><b>First Aid:</b> bandages, and in Forever it can make healing potions. It also adds a Stamina First Aid Kit to Campfires.</li></ul>
 <p class="src"><a href="{IV}">Icy Veins Ret</a>, <a href="{IVP}">Icy Veins Prot</a></p></div>
</section>

<section id="t-prot" class="tab"><h2>{icimg("_prot","hic")}Protection (main path)</h2>
 <div class="card"><h3>Talents to 30</h3>
  <p><b>Protection (21 points)</b></p>
  <ul>
   <li>Redoubt 5/5</li><li>Precision 3/3</li><li>Anticipation 2/5</li><li>Improved Seal of Fury 1/1</li><li>Shield Specialization 3/3</li><li>Improved Righteous Fury 2/3</li><li>Swift Judgement 1/1</li><li>One-Handed Weapon Specialization 3/3</li><li>Templar's Bulwark 1/1</li></ul>
  <p><b>Holy:</b> none. <b>Retribution:</b> none.</p>
  <p class="src">Consecration is a trainer spell at 20 now, so you don't need Holy talents. Levels 10-30 only; the beta stops at 30. <a href="https://classicwowforever.com/class-guides/paladin/protection/">classicwowforever</a> (Oct 14) and <a href="https://mobalytics.gg/wow-forever/classes/protection-paladin-guide">Mobalytics</a> (Oct 15) give this exact order. Both were written before the Oct 15 build.</p>
  <h3 style="margin-top:12px">Order by level</h3>{talent_list_p}
  <details><summary>Where sources differ, and after 30 (unconfirmed)</summary>
   <ul>
    <li><a href="https://topbuilds.gg/wow-forever/paladin/protection/">TopBuilds</a> (Oct 9) takes Shield Specialization at 20 and Improved Seal of Fury at 26, and has no Templar's Bulwark.</li>
    <li><a href="https://leprestore.com/guides/world-of-warcraft-forever/wow-forever-protection-paladin-guide-best-builds-race-professions/">Leprestore</a> (Oct 3) lists the same 21 points with Anticipation 5/5, Improved Righteous Fury 3/3 and Sacred Duty 2/2, no Precision and no order.</li>
    <li><a href="https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview">Wowhead</a> (Oct 6) agrees on Improved Seal of Fury, Shield Specialization and Templar's Bulwark, then 3 points in either One-Handed Weapon Specialization or Improved Righteous Fury.</li>
    <li>Swift Judgement can wait: Mobalytics says to take it after One-Handed Weapon Specialization if you aren't running dungeons.</li>
    <li class="warn">After 30, one source (Mobalytics): Reckoning 5/5 (31-35), Improved Righteous Fury 3/3 (36), Iron Creed 3/5 (37-39), Holy Shield (40). Nobody has tested this.</li>
    <li class="warn">Holy Shield needs Templar's Bulwark first (Blizzard). Sources disagree on when it comes: classicwowforever says level 40, Leprestore calls it a deeper capstone. It isn't in the 30-level beta.</li>
    <li>Legacy perk Talented can move your first talent point to level 9 (classicwowforever). The order stays the same.</li></ul></details></div>
 <div class="card"><h3>Solo priority</h3><ol>
  <li>Before the pull: shield on, <b>Righteous Fury</b> (16+), <b>Seal of Fury</b> (10+).</li>
  <li><b>Judgement</b> on cooldown. With Seal of Fury it taunts for 4 sec and keeps your Seal.</li>
  <li><b>Exorcism</b> on Undead and Demons (20+).</li>
  <li><b>Holy Strike</b> on cooldown.</li>
  <li><b>Consecration</b> for 3 or more mobs (20+). Only the first 4 take full damage.</li>
  <li><b>Swift Judgement</b> (25+) is a free extra Judgement every minute. Mobalytics calls it your damage button when soloing.</li>
  <li>Hammer of Justice on a caster. Low health: Templar's Bulwark (30), then Holy Light. Lay on Hands last.</li></ol>
  <p class="src"><a href="https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview">Wowhead</a>, <a href="https://classicwowforever.com/class-guides/paladin/protection/">classicwowforever</a>, <a href="https://mobalytics.gg/wow-forever/classes/protection-paladin-guide">Mobalytics</a>. Wowhead says a two-hander kills faster in the open world before about level 20, and sword and board gets better at 20, 26 and 30.</p></div>
 <div class="card"><h3>Staying alive solo</h3><ul>
  <li><b>Keep the shield on.</b> Seal of Fury's absorb, Redoubt and Shield Specialization all need it.</li>
  <li>Seal of Fury adds an absorb on every swing. classicwowforever says that saves on food.</li>
  <li>Blocks give Mana back from 21 (Shield Specialization), so long fights cost less water.</li>
  <li>Righteous Fury has to be up for Improved Righteous Fury's damage cut.</li>
  <li>Aura: sources split. Wowhead and Mobalytics like Retribution Aura for threat. classicwowforever calls Devotion Aura the tanking aura. Mobalytics says Devotion is better against slow, hard physical hitters.</li></ul>
  <p class="src">Which wanted mobs a Prot Paladin can solo: not known, no Forever source says. The only hint is <a href="https://games.gg/world-of-warcraft/guides/wow-forever-elwynn-forest/">Games.gg's Elwynn guide</a>: do Wanted: Hogger (level 11 elite) at 10 with 2-3 players, or at 12 solo on classes with a pet or self-heals. It doesn't name Paladin.</p></div>
 <div class="card"><h3>Gear to carry</h3>
  {ck("p1","A one-handed weapon and a shield on by level 10")}
  {ck("p2","Stamina, Armor and Defense gear first")}
  {ck("p3","Water, plenty of it")}
  {ck("p4","Mana potions for after Lay on Hands")}
  {ck("p5","Keybind Seal of Fury and Righteous Fury")}
 </div>
 <details class="card"><summary><b>Oct 15 build: Paladin changes (1.60.1.70425)</b></summary><ul>
  <li><b>Human:</b> Ruthless (+2% crit, any weapon) replaces Sword Specialization.</li>
  <li><b>Righteous Fury:</b> Holy threat 60% to 90%.</li>
  <li><b>Shield Specialization:</b> block Mana 6% to 4% (3 sec limit).</li>
  <li><b>Reckoning:</b> now stores up to 4 charges and fires on your next swing. Not in your 30-level plan.</li>
  <li><b>Seal of Fury:</b> rank 3 moved from level 25 to 26. It is no longer overwritten by Power Word: Shield.</li>
  <li><b>Salvation</b> is no longer a Blessing, so it stacks with one. Mass Salvation replaces the Greater Blessing. You also learn Revoke at 26.</li>
  <li><b>Consecration:</b> Spell Power scaling per tick cut from 0.095 to 0.042. Seal of Righteousness got about half as much from Spell Damage (a fix), and Judgement of Righteousness and Fury coefficients were corrected.</li>
  <li><b>Ret:</b> Champion of the Light is now 10/20/30% of Intellect (was 20/40/60%). Sanctified Judgement's Mana no longer adds threat.</li></ul>
  <p class="src">The notes list no other Protection talent changes. <a href="https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/">Warcraft Tavern's copy of the notes</a>, <a href="https://talentsforever.com/builds">Talents Forever</a>, <a href="https://news.blizzard.com/en-us/article/24302099/world-of-warcraft-forever-class-deep-dives-paladin">Blizzard's Paladin deep dive</a> (Oct 15).</p></details>
</section>

<section id="t-bars" class="tab"><h2>My Bars · Lv <span id="barLv"></span></h2>
 <p class="note">Change the level in the top bar. Gold outline = new at this level. Dashed = placement for 31-60 not confirmed.</p>
 <div id="barsBox"></div>
 <div class="card"><h3><img id="macroIc" class="ic" src="icons/spells/{SPELLS["Blessing of Might"]["i"]}.jpg" alt="">Bow &amp; Buff macro (Bottom 3, from Lv 4)</h3>
 <pre id="macroTxt">#showtooltip Blessing of Might
/cast Blessing of Might
/bow</pre><button id="copyMacro" class="ghost">Copy macro</button>
 <p class="src">Make it in-game with /macro, then New. It casts Blessing of Might before Lv 20 and Blessing of Kings from Lv 20 (the text above follows your level). Character macros hold 255 characters, and this one is far under. That limit is from standard WoW and wasn't checked against Forever.</p></div>
 <div class="card"><h3>Not on bars</h3><p class="note">Seal of the Crusader, Blessing of Might/Kings (cast by Bow &amp; Buff), Blessing of Wisdom, Salvation, Light, Sacrifice, Turn Undead, Sense Undead, Holy Wrath (50), Summon Charger (60, talent mount), Greater Blessings. Drag them from your spellbook if you want them. Divine Intervention (30) is off the bars too.</p></div>
 <p class="src">Learn levels from <a href="{TFE}">The Forever Era</a> beta client data. Swift Judgement is a talent (taken at 25 in the plan). Spells after 30 can't be tested in the beta.</p>
</section>
<section id="t-dungeons" class="tab"><h2>Dungeons</h2>
 <p class="note">35 dungeons, Lv 13-60. Level ranges from Icy Veins Forever. Alliance and shared ones shown; Ragefire Chasm (Horde) left out. ⚠️ = Wowhead says it couldn't test that dungeon in the beta and used Classic data.</p>
 {''.join(dcard(d) for d in DUNGEONS)}
 <p class="src">Ranges: <a href="{IVD}">Icy Veins Forever</a>. Quests: <a href="{WHQ}">Wowhead Forever dungeon quests</a> (beta, updated Oct 11). Locations are the usual entrances; new Forever dungeons without a published location say Not known yet.</p>
</section>
<section id="t-back" class="tab"><h2>Back from a break</h2>
 <div class="card big"><h3>30-second rotation</h3><ol>
  <li>Shield on. Righteous Fury (Aura bar 7), then Seal of Fury.</li><li>Judgement on CD.</li><li>Holy Strike on CD.</li><li>Exorcism on Undead and Demons. Consecration if 3+ mobs.</li><li>Low health: Templar's Bulwark (30+) or Divine Protection, then Holy Light. Last resort: Lay on Hands.</li><li>Bad pull: Blessing of Protection on yourself and run.</li><li>Buffs: Bow &amp; Buff (Might, Kings from 20) + an Aura.</li></ol></div>
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
sw = _re.sub(r"const C='pal-v\d+',F=\[[^\]]*\]", "const C='pal-v17',F=" + json.dumps(['./','index.html','style.css','app.js','data.json','manifest.webmanifest','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png'] + [f"icons/spells/{i}.jpg" for i in icons]), sw)
open("sw.js","w").write(sw)
print("built", len(PAGE))
