import html
import json
import sys
from collections import Counter, defaultdict

data = json.load(open(sys.argv[1]))
outdir = sys.argv[2]
mods = data['modules']

CSS = """
@page { size: Letter; margin: 0.6in 0.6in 0.7in 0.6in; }
body { font-family: -apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #0b0b0b; font-size: 10.5pt; line-height: 1.45; }
h1 { font-size: 20pt; margin: 0 0 4pt 0; }
h2 { font-size: 13.5pt; margin: 18pt 0 6pt 0; border-bottom: 1px solid #d9d8d4; padding-bottom: 3pt; }
h3 { font-size: 11pt; margin: 12pt 0 4pt 0; }
p { margin: 5pt 0; }
.sub { color: #52514e; font-size: 10pt; }
.caveat { background: #f4f3ef; border-left: 4px solid #eda100; padding: 7pt 10pt; margin: 10pt 0; font-size: 9.8pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 6pt 0; }
th, td { border-bottom: 1px solid #e4e3df; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { color: #52514e; font-weight: 600; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
code, .mono { font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 8.4pt; }
.fig { page-break-inside: avoid; margin: 8pt 0 4pt 0; }
.figcap { color: #52514e; font-size: 9pt; margin-top: 2pt; }
.mod { font-family: 'SF Mono', Menlo, monospace; font-size: 8.6pt; font-weight: 700; margin: 9pt 0 2pt 0; color: #2a78d6; page-break-after: avoid; }
.st { font-family: 'SF Mono', Menlo, monospace; font-size: 7.4pt; margin: 0 0 3pt 10pt; white-space: pre-wrap; word-break: break-word; }
.st b { color: #0b0b0b; }
.toc { columns: 2; font-size: 8.6pt; }
"""

C = {'galois': '#2a78d6', 'auto': '#eb6834', 'geom': '#1baf7a', 'rep': '#eda100', 'miss': '#9a9993'}


def box(x, y, w, h, title, lines, color, dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ''
    fill = '#ffffff' if not dashed else '#f7f7f5'
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="2"{dash}/>',
         f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{color}"/>',
         f'<text x="{x + 16}" y="{y + 20}" font-size="13" font-weight="700" fill="#0b0b0b">{html.escape(title)}</text>']
    for i, ln in enumerate(lines):
        s.append(f'<text x="{x + 16}" y="{y + 38 + 15 * i}" font-size="10.5" fill="#52514e">{html.escape(ln)}</text>')
    return '\n'.join(s)


def arrow(x1, y1, x2, y2, label=None, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ''
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#52514e" stroke-width="1.6" marker-end="url(#ah)"{dash}/>'
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s += f'<text x="{mx + 6}" y="{my - 4}" font-size="9.5" fill="#52514e">{html.escape(label)}</text>'
    return s


DEFS = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#52514e"/></marker></defs>'


def fig_architecture():
    W, H = 760, 560
    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, Helvetica, Arial">', DEFS]
    p.append(box(20, 10, 720, 62, 'Foundations (not in part 1)', ['Mathlib  ·  Formalism (the "MainNotions" being proved)  ·  GroundTheory (local/global fields, adeles, Galois cohomology)'], C['miss'], True))
    p.append(box(20, 110, 350, 150, 'A. Abelian varieties & theta functions', ['Development.AbelianVarietyTheory (~58k results)', 'divisors, cubical line bundles, coherent cohomology,', 'integral theta generators with small sup-norm,', 'Hermitian / CM lattices, cusp-form evaluations,', 'CM periods via L′/L(χ,1), covolume bounds'], C['geom']))
    p.append(box(390, 110, 350, 150, 'B. Galois side: twisted Selmer groups', ['Development: NonGaloisDescent, TorsionBlocks,', 'BlochKatoReduction  ·  auxiliary split primes and', 'l-power twists ψ; "TwistKillsSelmer": some twist', 'bounds the Selmer length, which is read off a', 'determinant (ThmS, ThmC, SelmerLengthsByDeterminant)'], C['galois']))
    p.append(box(20, 310, 350, 140, 'C. Real groups & representations', ['CompanionTheory.RealGroups, .HarishChandraModules,', '.ThickeningEstimates  (~1.7k results)', 'discrete series of U(p,q), K-types, formal degrees,', 'Whittaker models, smooth / K-finite vectors'], C['rep']))
    p.append(box(390, 310, 350, 140, 'D. Automorphic theory (local analysis)', ['CompanionTheory.AutomorphicTheory (~2.5k results)', 'Bessel models: uniqueness, orbit bounds, wave grids,', 'theta lifts, Siegel–Weil finiteness, Zuckerman', 'functors, Pieri rules, rank-one tori, spectral geometry'], C['auto']))
    p.append(box(20, 488, 720, 62, 'Top: Statements / Main  (not in part 1)  +  ReciprocityTheory, PositivityTheory, Lemmata', ['The final theorem lives here and combines all four areas; part 1 already imports ReciprocityTheory ~2,000 times.'], C['miss'], True))
    p.append(arrow(195, 72, 195, 108))
    p.append(arrow(565, 72, 565, 108))
    p.append(arrow(372, 185, 388, 185))
    p.append(arrow(195, 260, 195, 308, 'imported by'))
    p.append(arrow(565, 260, 565, 308, 'imported by'))
    p.append(arrow(330, 260, 430, 308))
    p.append(arrow(372, 380, 388, 380))
    p.append(arrow(195, 450, 195, 486, '', True))
    p.append(arrow(565, 450, 565, 486, '', True))
    p.append('</svg>')
    return '\n'.join(p)


def fig_chain():
    W, H = 760, 330
    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, Helvetica, Arial">', DEFS]
    p.append(box(10, 10, 230, 70, 'Zuckerman ingredients', ['zuckerman_ingredients', 'zuckerman_library_bounds'], C['rep']))
    p.append(box(270, 10, 220, 70, 'Small Zuckerman gap', ['zuckerman_gap_small : ZuckSm thr', 'zuckerman_gap : ZuckG'], C['rep']))
    p.append(box(520, 10, 230, 70, 'Pieri hypotheses', ['PieriExpansion.hypsG_of_zuck', '→ BranchingSupport.HypsG'], C['auto']))
    p.append(box(520, 125, 230, 70, 'Wave inputs', ['WEnd.wave_inputs_of_', 'hypotheses_global'], C['auto']))
    p.append(box(270, 125, 220, 70, 'Rank-one torus bound', ['MainStatements.RankOne.', 'one_bessel_torus_bound (≤ 100)'], C['miss'], True))
    p.append(box(270, 240, 480, 78, 'Theorem B: weighted bound, rotated, uniform', ['uniform_bessel_rank_three_of_inputs  ⇒', 'Formalism.MainNotions.RotatedPoints.WeightedBoundRotatedUniform', '(file ThmBFinal.lean)'], C['auto']))
    p.append(box(10, 240, 230, 78, 'Read as', ['a uniform bound for Bessel', 'functions of rank-three unitary', 'groups on rotated grids'], C['miss'], True))
    p.append(arrow(240, 45, 268, 45))
    p.append(arrow(490, 45, 518, 45))
    p.append(arrow(635, 80, 635, 123))
    p.append(arrow(635, 195, 635, 238))
    p.append(arrow(380, 195, 440, 238))
    p.append('</svg>')
    return '\n'.join(p)


def area(m):
    p = m.split('.')
    return '.'.join(p[:3])


astats = defaultdict(lambda: [0, 0])
for m, v in mods.items():
    astats[area(m)][0] += 1
    astats[area(m)][1] += len(v['decls'])

discharged = []
for m, v in mods.items():
    for x in v['decls']:
        s = x['stmt']
        if ': Formalism.MainNotions.' in s and len(s) < 260:
            tgt = s.split(': Formalism.MainNotions.', 1)[1].split()[0].rstrip('})],;')
            discharged.append((tgt, x['name'], m))
tc = Counter(t for t, _, _ in discharged)

ov = [f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>']
ov.append('<h1>lean.tar.gz, part 1: what it is and how the proof is organised</h1>')
ov.append('<p class="sub">Read-only analysis of the 10,334 Lean 4 source files in part 1 (Mathlib-based, toolchain v4.33.1). Nothing was compiled or executed.</p>')
ov.append('<div class="caveat"><b>What is verified and what is inferred.</b> Verified from the text: the file layout, the import graph, 68,703 theorem/lemma declarations, zero occurrences of <code>sorry</code> and no <code>axiom</code> declarations in part 1, and the exact chain of lemmas behind the "Theorem B" file shown in Figure 2. Not verifiable from part 1: the final statement (it lives in the <code>Statements</code>/<code>Main</code> library, which is in a later part), whether the project actually compiles, and the mathematical reading in the next section, which is inferred from names and statement shapes. The archive is about 861 MB uncompressed, so part 1 (73 MB of source) is a small fraction of it.</div>')
ov.append('<h2>The approach, in plain terms</h2>')
ov.append('<p>The project has the architecture of a large arithmetic theorem proved in the style of modern Euler system and automorphic arguments over CM fields. On the <b>Galois side</b> it studies Selmer groups of twisted Galois representations. The strategy visible in the definitions is to choose auxiliary split primes together with characters of l-power order, show that a suitable twist exists (<code>TwistExists</code>, <code>TwistKillsSelmer</code>), and then read off the length of the Selmer group from the determinant of an explicit matrix over the coefficient ring (<code>SelmerLengthsByDeterminant</code>), whose entries are shown to be non-units (<code>ThmS</code>) with a controlled valuation (<code>ThmC</code>). The names <code>BlochKatoReduction</code> and <code>finiteSelmer</code> suggest that the target is a Bloch–Kato type bound.</p>')
ov.append('<p>Such Galois arguments need <b>automorphic input</b>, and <code>CompanionTheory</code> supplies it, building on top of the Development definitions (Figure 1). It develops the representation theory of real unitary groups (discrete series, K-type multiplicity one, formal degrees), local uniqueness of Bessel models, theta lifts and Siegel–Weil finiteness, and a sequence of analytic estimates culminating in uniform bounds for Bessel functions (Figure 2). The <b>arithmetic geometry</b> in <code>Development.AbelianVarietyTheory</code>, by far the largest part, builds abelian varieties and Shimura-type moduli with theta functions: it constructs integral theta generators with small sup-norm and no common zeros (the 50 results proving <code>ModuliIntegralCharts.H</code>), works with Hermitian and CM lattices, and computes CM periods through the logarithmic derivative L′/L(χ,1) of a Kronecker character. A separate <code>ReciprocityTheory</code> library, which part 1 imports about 2,000 times but does not contain, is where the automorphic and Galois sides are presumably tied together by reciprocity laws. A <code>Counterexamples</code> folder records examples showing that the hypotheses cannot be dropped.</p>')
ov.append('<div class="fig">' + fig_architecture() + '<div class="figcap"><b>Figure 1.</b> How the libraries in part 1 depend on one another. Every arrow points from a library to the libraries that import it, as measured from the import graph (for example, CompanionTheory.AutomorphicTheory imports Development 176 times; nothing in Development imports CompanionTheory). Dashed boxes are libraries that part 1 imports but does not contain.</div></div>')
ov.append('<h2>One complete chain: "Theorem B"</h2>')
ov.append('<p>The file <code>BesselWaveGrids/ThmBFinal.lean</code> shows the project\'s pattern clearly. Each headline result is a named proposition in <code>Formalism.MainNotions</code>, and a short top-level file discharges it by composing intermediate theorems. Here a small spectral gap for Zuckerman functors yields the hypotheses of a Pieri-type expansion, those yield the inputs to a wave-grid estimate, and together with a rank-one torus bound they give a weighted bound for Bessel functions that is uniform over rotated grids. That chain alone pulls in 422 modules of part 1.</p>')
ov.append('<div class="fig">' + fig_chain() + '<div class="figcap"><b>Figure 2.</b> The lemma chain behind Theorem B, read directly from the source. The rank-one torus bound is stated in <code>Formalism.MainStatements</code>, which is in a later part.</div></div>')
ov.append('<h2>Headline propositions discharged in part 1</h2>')
ov.append('<table><tr><th>Proposition in Formalism.MainNotions</th><th class="num">theorems proving it</th><th>example</th></tr>')
for t, n in tc.most_common():
    ex = next(nm for tt, nm, _ in discharged if tt == t)
    ov.append(f'<tr><td><code>{html.escape(t)}</code></td><td class="num">{n}</td><td><code>{html.escape(ex)}</code></td></tr>')
ov.append('</table>')
ov.append('<h2>Size of each area in part 1</h2><table><tr><th>area</th><th class="num">files</th><th class="num">theorems + lemmas</th></tr>')
for a, (f, dcount) in sorted(astats.items(), key=lambda x: -x[1][1]):
    if dcount >= 30:
        ov.append(f'<tr><td><code>{html.escape(a)}</code></td><td class="num">{f:,}</td><td class="num">{dcount:,}</td></tr>')
ov.append('</table><p class="sub">The two statement PDFs list every theorem and lemma statement (proof bodies omitted), grouped by file.</p>')
ov.append('</body></html>')
open(f'{outdir}/overview.html', 'w').write('\n'.join(ov))


def statements(prefix, title, fname):
    ms = sorted(m for m in mods if m.startswith(prefix) and mods[m]['decls'])
    n = sum(len(mods[m]['decls']) for m in ms)
    o = [f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>']
    o.append(f'<h1>{html.escape(title)}</h1><p class="sub">{n:,} statements from {len(ms):,} files in part 1, proofs omitted, grouped by module.</p>')
    for m in ms:
        o.append(f'<div class="mod">{html.escape(m)}</div>')
        for x in mods[m]['decls']:
            s = html.escape(x['stmt'])
            nm = html.escape(x['name'])
            s = s.replace(nm, f'<b>{nm}</b>', 1)
            o.append(f'<div class="st">{s}</div>')
    o.append('</body></html>')
    open(f'{outdir}/{fname}', 'w').write('\n'.join(o))
    return n


print(statements('CompanionTheory', 'Statements: CompanionTheory (automorphic and representation theory)', 'statements_companion.html'))
print(statements('Development', 'Statements: Development.AbelianVarietyTheory (arithmetic geometry and Galois side)', 'statements_development.html'))
print(len(discharged), 'discharges')
