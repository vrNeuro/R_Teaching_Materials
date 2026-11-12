#!/usr/bin/env python3
"""Generate the outcome-first 'Choosing a statistical test' flowchart (self-contained HTML + SVG).

Decision order:  0) is there one clear outcome? (No -> separate "summarising relationships" path)
                 1) outcome type (and number of outcomes)
                 2) number and type of predictors
                 3) design: independent observations vs repeated / clustered
Usage: python3 make_flowchart_v3_with_summary_path.py out.html
"""
import sys
from html import escape

BASE = "https://vrneuro.github.io/R_Teaching_Materials/"
def lab(n, anchor=""): return f"{BASE}PS71020_Unit{n}_Lab.html" + (f"#{anchor}" if anchor else "")
def hw(n): return f"{BASE}PS71020_Unit{n}_Homework.html"

NAVY, TEAL, TEAL_S = "#1f2a6b", "#dff5f3", "#2ad1c0"
BLUE, BLUE_S = "#e6f1fb", "#1f6fe0"
PINK, PINK_S = "#f8e5f6", "#c25bb8"
GREY, GREY_S = "#f1f2f6", "#9aa0b8"
AMBER, AMBER_S = "#fff0d9", "#e8962a"      # "not taught in this course"
PILL_S = "#7a82a6"
BAND, BAND_S = "#fafbff", "#e3e6f2"

out = []
def add(s): out.append(s)

def multiline(cx, y, h, lines, cls="q", fill=None, lh=22):
    y0 = y + h/2 - (len(lines)-1)*lh/2 + 6
    f = f' fill="{fill}"' if fill else ''
    for i, l in enumerate(lines):
        add(f'<text x="{cx}" y="{y0+i*lh}" text-anchor="middle" class="{cls}"{f}>{escape(l)}</text>')

def question(x, y, w, h, text, kind="teal"):
    fill, stroke = (TEAL, TEAL_S) if kind == "teal" else (BLUE, BLUE_S)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    multiline(x+w/2, y, h, text.split("\n"))

def pill(cx, cy, text):
    w = 14 + len(text)*7.6
    add(f'<rect x="{cx-w/2}" y="{cy-14}" width="{w}" height="28" rx="5" fill="#fff" stroke="{PILL_S}" stroke-width="1.5"/>')
    add(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" class="pill">{escape(text)}</text>')

def edge(d, arrow=True):
    m = ' marker-end="url(#arr)"' if arrow else ''
    add(f'<path d="{d}" fill="none" stroke="{PILL_S}" stroke-width="1.8" stroke-dasharray="5 4"{m}/>')

def soon(x, y, w, h, title, note="Worksheet coming soon"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GREY}" stroke="{GREY_S}" stroke-width="2" stroke-dasharray="6 4"/>')
    add(f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" class="rt" fill="#6b7190">{escape(title)}</text>')
    add(f'<text x="{x+w/2}" y="{y+68}" text-anchor="middle" class="soon">{escape(note)}</text>')

def notcovered(x, y, w, h, title, note="Not covered in this course"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{AMBER}" stroke="{AMBER_S}" stroke-width="2" stroke-dasharray="2 4"/>')
    add(f'<text x="{x+w/2}" y="{y+37}" text-anchor="middle" class="rt" fill="#8a5410">{escape(title)}</text>')
    add(f'<text x="{x+w/2}" y="{y+62}" text-anchor="middle" class="soon" fill="#9a6a2a">{escape(note)}</text>')

def chip(x, y, w, text, href, tip, h=26):
    arrow = f'<text x="{x+w-10}" y="{y+h/2+4.5}" text-anchor="end" class="ca">↗</text>' if w >= 150 else ''
    tx = x+10 if w >= 150 else x+w/2
    anchor = 'start' if w >= 150 else 'middle'
    add(f'<a href="{href}" target="_blank" rel="noopener"><title>{escape(tip)}</title>'
        f'<g class="chip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
        f'<text x="{tx}" y="{y+h/2+4.5}" text-anchor="{anchor}" class="ct">{escape(text)}</text>'
        f'{arrow}</g></a>')

def box_h(rows, hws, desc=()):
    return 46 + len(desc)*18 + (6 if desc else 0) + len(rows)*32 + (32 if hws else 0) + 4

def test_box(x, y, w, title, rows, hws, fill=PINK, stroke=PINK_S, h=None, desc=()):
    """rows/hws: [(label, href, tooltip)]; desc: grey explanatory lines under the title."""
    h = h or box_h(rows, hws, desc)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    add(f'<text x="{x+w/2}" y="{y+29}" text-anchor="middle" class="rt">{escape(title)}</text>')
    cy = y + 42
    for line in desc:
        add(f'<text x="{x+w/2}" y="{cy+12}" text-anchor="middle" class="desc">{escape(line)}</text>'); cy += 18
    if desc: cy += 6
    for label, href, tip in rows:
        chip(x+10, cy, w-20, label, href, tip); cy += 32
    if hws:
        n = len(hws); gap = 6
        cw = (w-20-gap*(n-1))/n
        for i, (label, href, tip) in enumerate(hws):
            chip(x+10+i*(cw+gap), cy, cw, label, href, tip)
    return h

# ---------------- worksheet link shortcuts ----------------
L_TTEST   = ("Wk 3 · Independent t-test", lab(3, "section-b.-t-tests"), "Week 3 lab, Section B: t-tests")
L_WELCH   = ("Wk 6 · Welch t-test", lab(6), "Week 6 lab: Welch t-test (completers vs dropouts)")
L_PAIRED  = ("Wk 3 · Paired t-test", lab(3, "section-c.-paired-samples-t-test-and-correlation"), "Week 3 lab, Section C: paired samples t-test")
L_ANOVA   = ("Wk 3 · ANOVAs", lab(3, "sec-ANOVAs"), "Week 3 lab, Section D: ANOVAs")
L_ANOVA2  = ("Wk 3 · Two-way ANOVA", lab(3, "sec-ANOVAs"), "Week 3 lab, Section D: two-way between-subjects ANOVA")
L_RM      = ("Wk 6 · Repeated-measures ANOVA", lab(6, "section-b.-various-approaches-to-modelling"), "Week 6 lab, Section B: repeated-measures (mixed) ANOVA")
L_MIXANOVA= ("Wk 6 · Mixed ANOVA", lab(6, "section-b.-various-approaches-to-modelling"), "Week 6 lab, Section B: between + within factors")
L_LMM     = ("Wk 6 · Linear mixed model", lab(6, "section-b.-various-approaches-to-modelling"), "Week 6 lab, Section B: mixed models approach")
L_LMM_ALT = ("or Wk 6 · Linear mixed model", lab(6, "section-b.-various-approaches-to-modelling"), "Week 6 lab, Section B: mixed models approach")
L_MISSING = ("Wk 6 · Missing data", lab(6, "section-c.-a-note-on-missing-data"), "Week 6 lab, Section C: a note on missing data")
L_REG1    = ("Wk 4 · Regression 1", lab(4, "section-c.-regression"), "Week 4 lab, Section C: regression")
L_CORR    = ("Wk 3 · Correlation", lab(3, "section-c.-paired-samples-t-test-and-correlation"), "Week 3 lab, Section C: Pearson correlation")
L_MREG    = ("Wk 4 · Multiple regression", lab(4, "section-c.-regression"), "Week 4 lab, Section C")
L_SEMI    = ("Wk 4 · Semi-partial correlations", lab(4, "section-d.-semi-partial-correlations"), "Week 4 lab, Section D")
L_CATREG  = ("Wk 5 · Categorical predictors", lab(5, "section-c.-regression-with-categorical-variables"), "Week 5 lab: regression with categorical variables")
L_MOD     = ("Wk 5 · Moderation", lab(5, "section-c.-moderation-analysis"), "Week 5 lab: moderation analysis")
L_HIER    = ("Wk 5 · Hierarchical regression", lab(5, "section-d.-hierarchical-regression"), "Week 5 lab: hierarchical regression")
def HW(n): return (f"Wk {n} HW", hw(n), f"Week {n} homework")
def HWL(n): return (f"Week {n} homework", hw(n), f"Week {n} homework")

# ---------------- layout ----------------
W = 1220
DY = 150   # existing tree is shifted down to make room for the new first question

add(f'<g transform="translate(0,{DY})">')
# Level 1: outcome type
question(330, 30, 540, 84, "Outcome variable:\ncategorical or quantitative?")
edge("M330,72 H170 V190");  pill(250, 72, "Quantitative")
edge("M870,72 H960 V190");  pill(946, 72, "Categorical")   # 27px gap to the box, matching the "Quantitative" pill

# Level 1b: how many outcomes (quantitative branch)
question(40, 190, 260, 84, "How many outcome\nvariables?", "blue")
edge("M300,232 H450"); pill(375, 232, "More than one")
notcovered(450, 190, 220, 84, "MANOVA")

# Categorical-outcome branch (not yet covered)
question(780, 190, 360, 84, "What type of predictor?", "blue")
edge("M810,274 V380"); pill(810, 327, "Categorical")
edge("M1050,274 V380"); pill(1050, 327, "Quantitative / several")
soon(700, 380, 220, 100, "Chi-square", "Non-parametric · coming soon")
soon(940, 380, 220, 100, "Logistic regression", "Worksheet coming soon")

# Level 2: predictors
edge("M170,274 V380"); pill(170, 327, "One")
question(40, 380, 260, 100, "How many predictors,\nand of what type?")

# Level 3 header (design)
question(340, 540, 820, 56, "Then ask: are the observations independent?")
add(f'<rect x="340" y="640" width="400" height="52" rx="6" fill="#fff" stroke="{TEAL_S}" stroke-width="2"/>')
add('<text x="540" y="662" text-anchor="middle" class="q">Independent</text>')
add('<text x="540" y="681" text-anchor="middle" class="desc">each participant measured once (between-subjects)</text>')
add(f'<rect x="780" y="640" width="380" height="52" rx="6" fill="#fff" stroke="{TEAL_S}" stroke-width="2"/>')
add('<text x="970" y="662" text-anchor="middle" class="q">Repeated or clustered</text>')
add('<text x="970" y="681" text-anchor="middle" class="desc">same people repeatedly, or nested data</text>')
edge("M540,596 V640"); edge("M970,596 V640")

# Rows: (label lines, independent box spec, repeated box spec)
IND_X, IND_W, REP_X, REP_W = 340, 400, 780, 380
rows = [
    (("One categorical predictor", "2 groups / conditions"),
     dict(title="Independent-samples t-test", rows=[L_TTEST, L_WELCH], hws=[HWL(3)]),
     dict(title="Paired-samples t-test", rows=[L_PAIRED, L_LMM_ALT], hws=[HWL(3)])),
    (("One categorical predictor", "3+ groups / conditions"),
     dict(title="One-way ANOVA", rows=[L_ANOVA], hws=[HWL(3)]),
     dict(title="Repeated-measures ANOVA", rows=[L_RM, L_LMM_ALT], hws=[HWL(6)])),
    (("Two or more categorical", "predictors (factorial)"),
     dict(title="Factorial ANOVA", rows=[L_ANOVA2], hws=[HWL(3)]),
     dict(title="Mixed (split-plot) ANOVA", rows=[L_MIXANOVA, L_LMM_ALT], hws=[HWL(6)])),
    (("One quantitative predictor",),
     dict(title="Simple regression", rows=[L_REG1], hws=[HWL(4)]),
     None),
    (("Two or more predictors", "(quantitative or mixed types)"),
     dict(title="Multiple regression", rows=[L_MREG, L_CATREG, L_MOD, L_HIER], hws=[HW(4), HW(5)]),
     None),
]

def spec_h(s): return box_h(s["rows"], s["hws"], s.get("desc", ())) if s else 0
y = 712
GAP = 16
row_geo = []
for lbl, ind, rep in rows:
    h = max(spec_h(ind), spec_h(rep), 110) + 16
    row_geo.append((y, h)); y += h + GAP
last_bottom = y - GAP

# trunk from Level 2 question down the left margin
cys = [ry + rh/2 for ry, rh in row_geo]
edge(f"M170,480 V515 H26 V{cys[-1]}", arrow=False)

for (lbl, ind, rep), (ry, rh), cy in zip(rows, row_geo, cys):
    add(f'<rect x="40" y="{ry}" width="1130" height="{rh}" rx="8" fill="{BAND}" stroke="{BAND_S}" stroke-width="1.5"/>')
    edge(f"M26,{cy} H54")
    add(f'<rect x="56" y="{cy-34}" width="240" height="68" rx="6" fill="#fff" stroke="{BLUE_S}" stroke-width="2"/>')
    if len(lbl) == 2:
        add(f'<text x="176" y="{cy-6}" text-anchor="middle" class="lab1">{escape(lbl[0])}</text>')
        add(f'<text x="176" y="{cy+15}" text-anchor="middle" class="lab2">{escape(lbl[1])}</text>')
    else:
        add(f'<text x="176" y="{cy+5}" text-anchor="middle" class="lab1">{escape(lbl[0])}</text>')
    test_box(IND_X, ry+(rh-spec_h(ind))/2 if False else ry+8, IND_W, ind["title"], ind["rows"], ind["hws"], desc=ind.get("desc", ()))
    if rep:
        test_box(REP_X, ry+8, REP_W, rep["title"], rep["rows"], rep["hws"], desc=rep.get("desc", ()))

# Merged repeated/clustered box beside the two regression rows
(y4, h4), (y5, h5) = row_geo[3], row_geo[4]
top = y4 + 8
tall = (y5 + h5) - top - 8
add(f'<rect x="{REP_X}" y="{top}" width="{REP_W}" height="{tall}" rx="6" fill="{BLUE}" stroke="{BLUE_S}" stroke-width="2"/>')
add(f'<text x="{REP_X+REP_W/2}" y="{top+29}" text-anchor="middle" class="rt">Linear mixed-effects model</text>')
cy = top + 42
chip(REP_X+10, cy, REP_W-20, *L_LMM); cy += 32
chip(REP_X+10, cy, REP_W-20, *L_MISSING); cy += 32
chip(REP_X+10, cy, REP_W-20, *HWL(6)); cy += 46
add(f'<text x="{REP_X+16}" y="{cy}" class="when">Use a mixed model when:</text>'); cy += 24
for line in ["• the same people are measured repeatedly",
             "• data are nested (e.g. students in classes)",
             "• some time points are missing",
             "• you have continuous predictors, or several",
             "   predictors, in a repeated or clustered design"]:
    add(f'<text x="{REP_X+16}" y="{cy}" class="when2">{escape(line)}</text>'); cy += 21
cy += 6
add(f'<text x="{REP_X+16}" y="{cy}" class="when2" font-style="italic">It also works for every row above, so it is the</text>'); cy += 21
add(f'<text x="{REP_X+16}" y="{cy}" class="when2" font-style="italic">general-purpose option for repeated designs.</text>')

add('</g>')
tree_bottom = last_bottom + DY

# ---------------- Level 0 + "no clear outcome" path ----------------
question(330, 30, 540, 84, "Is there one clear outcome\n(dependent) variable?")
edge(f"M600,114 V{DY+30}"); pill(600, 147, "Yes")
B = tree_bottom + 80                       # top of the summarising panel
edge(f"M870,72 H1200 V{B-34} H170 V{B}"); pill(1035, 72, "No: just summarising relationships")

add(f'<text x="40" y="{B-46}" class="sect">No single outcome: summarising relationships between variables</text>')
question(40, B, 260, 84, "How many variables,\nand what is the aim?")

def soon_box(x, y, w, h, title, desc, note):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GREY}" stroke="{GREY_S}" stroke-width="2" stroke-dasharray="6 4"/>')
    add(f'<text x="{x+w/2}" y="{y+29}" text-anchor="middle" class="rt" fill="#6b7190">{escape(title)}</text>')
    for i, d in enumerate(desc):
        add(f'<text x="{x+w/2}" y="{y+52+i*18}" text-anchor="middle" class="desc">{escape(d)}</text>')
    add(f'<text x="{x+w/2}" y="{y+h-14}" text-anchor="middle" class="soon">{escape(note)}</text>')

L_PEARSON = ("Wk 3 · Pearson correlation", lab(3, "section-c.-paired-samples-t-test-and-correlation"), "Week 3 lab, Section C: Pearson correlation")
sumrows = [
    (("Two variables", "how strongly are they related?"),
     lambda ry, rh: test_box(IND_X, ry+8, IND_W, "Correlation", [L_PEARSON], [HWL(3)]),
     ["Use when neither variable is an outcome and you",
      "want to describe how two variables relate."]),
    (("Two variables, controlling", "for one or more others"),
     lambda ry, rh: test_box(IND_X, ry+8, IND_W, "Partial / semi-partial correlation", [L_SEMI], [HWL(4)]),
     ["Partial: the others are removed from both variables.",
      "Semi-partial: removed from one variable only."]),
    (("Three or more variables", "(no outcome)"), None, None),
]
sum_geo = []
y = B + 128
for lbl, fn, txt in sumrows:
    h = 130 if fn else 150
    sum_geo.append((y, h)); y += h + GAP
panel_bottom = y - GAP
scys = [ry + rh/2 for ry, rh in sum_geo]
edge(f"M170,{B+84} V{B+108} H26 V{scys[-1]}", arrow=False)

for (lbl, fn, txt), (ry, rh), cy in zip(sumrows, sum_geo, scys):
    add(f'<rect x="40" y="{ry}" width="1130" height="{rh}" rx="8" fill="{BAND}" stroke="{BAND_S}" stroke-width="1.5"/>')
    edge(f"M26,{cy} H54")
    add(f'<rect x="56" y="{cy-34}" width="240" height="68" rx="6" fill="#fff" stroke="{BLUE_S}" stroke-width="2"/>')
    add(f'<text x="176" y="{cy-6}" text-anchor="middle" class="lab1">{escape(lbl[0])}</text>')
    add(f'<text x="176" y="{cy+15}" text-anchor="middle" class="lab2">{escape(lbl[1])}</text>')
    if fn:
        fn(ry, rh)
        for i, t in enumerate(txt):
            add(f'<text x="{REP_X+16}" y="{cy-6+i*22}" class="when2">{escape(t)}</text>')

# PCA / EFA row
ry, rh = sum_geo[2]
soon_box(IND_X, ry+8, IND_W, rh-16, "Principal component analysis (PCA)",
         ["Aim: reduce many variables to fewer", "components that retain most of the variance"], "Wk 9 · worksheet coming soon")
soon_box(REP_X, ry+8, REP_W, rh-16, "Exploratory factor analysis (EFA)",
         ["Aim: find the latent factors that", "explain the correlations between variables"], "Wk 9 · worksheet coming soon")
add(f'<text x="{(IND_X+REP_X+REP_W)/2}" y="{ry-3}" text-anchor="middle" class="desc"> </text>')

last_bottom = panel_bottom - 44 + 44   # legend sits below the new panel

# Legend
ly = last_bottom + 44
add(f'<rect x="60" y="{ly}" width="22" height="16" rx="3" fill="{PINK}" stroke="{PINK_S}" stroke-width="2"/>')
add(f'<text x="92" y="{ly+13}" class="leg">Click a test to open the worksheet (new tab)</text>')
add(f'<rect x="440" y="{ly}" width="22" height="16" rx="3" fill="{GREY}" stroke="{GREY_S}" stroke-width="2" stroke-dasharray="4 3"/>')
add(f'<text x="472" y="{ly+13}" class="leg">Worksheet coming soon</text>')
add(f'<rect x="700" y="{ly}" width="22" height="16" rx="3" fill="{AMBER}" stroke="{AMBER_S}" stroke-width="2" stroke-dasharray="2 3"/>')
add(f'<text x="732" y="{ly+13}" class="leg">Not covered in this course</text>')
H = ly + 40

svg_body = "\n".join(out)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Choosing a statistical test in R (outcome first) – PS71020 worksheets</title>
<style>
  body {{ margin:0; background:#fff; color:{NAVY}; font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }}
  .wrap {{ max-width:1200px; margin:0 auto; padding:24px 16px 32px; }}
  h1 {{ text-align:center; font-size:clamp(26px,4.6vw,46px); margin:8px 0 6px; letter-spacing:-.5px; }}
  p.sub {{ text-align:center; font-size:clamp(14px,1.9vw,19px); margin:0 0 18px; font-weight:600; }}
  svg {{ width:100%; height:auto; display:block; }}
  .q {{ font-size:18px; font-weight:600; fill:{NAVY}; }}
  .rt {{ font-size:19px; font-weight:700; fill:{NAVY}; }}
  .pill {{ font-size:15px; fill:{PILL_S}; }}
  .soon {{ font-size:14px; fill:#7d839f; font-style:italic; }}
  .desc {{ font-size:13px; fill:#5b6285; }}
  .lab1 {{ font-size:16px; font-weight:700; fill:{NAVY}; }}
  .lab2 {{ font-size:14px; fill:#4a5280; }}
  .when {{ font-size:14px; font-weight:700; fill:{NAVY}; }}
  .when2 {{ font-size:13.5px; fill:#3a4275; }}
  .sect {{ font-size:15px; font-weight:700; fill:{BLUE_S}; letter-spacing:.3px; }}
  .leg {{ font-size:14px; fill:{NAVY}; }}
  .chip rect {{ fill:#fff; stroke:{PINK_S}; stroke-width:1.2; }}
  .chip .ct {{ font-size:13.5px; fill:{NAVY}; font-weight:600; }}
  .chip .ca {{ font-size:13px; fill:{PINK_S}; }}
  a {{ cursor:pointer; }}
  a:hover .chip rect, a:focus .chip rect {{ fill:{NAVY}; stroke:{NAVY}; }}
  a:hover .chip .ct, a:focus .chip .ct, a:hover .chip .ca, a:focus .chip .ca {{ fill:#fff; }}
  a:focus {{ outline:none; }}
  a:focus-visible .chip rect {{ stroke-width:3; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Choosing a statistical test</h1>
  <p class="sub">Start by asking whether you have one clear outcome variable, then click a test to open the matching R worksheet</p>
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Outcome-first flowchart with a summarising path for choosing a statistical test, with links to the R worksheets">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="{PILL_S}"/>
      </marker>
    </defs>
{svg_body}
  </svg>
</div>
</body>
</html>
"""
open(sys.argv[1], "w", encoding="utf-8").write(html)
print("wrote", sys.argv[1], len(html), "bytes", "H=", H)
