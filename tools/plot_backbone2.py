import pickle
import sys
from collections import Counter, defaultdict, deque

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

idx = pickle.load(open(sys.argv[1], 'rb'))
OUT = sys.argv[2]
meta = idx['meta']
n2i = {m[0]: i for i, m in enumerate(meta)}
TOP_MODS = ('Main', 'Statements', 'Supplements')


def real(i):
    n, mod = meta[i][0], meta[i][1]
    return '.' in n or mod.split('.')[0] in TOP_MODS


adj = defaultdict(list)
for a, b in idx['edges']:
    if real(b):
        adj[a].append(b)
roots = ['riemannHypothesis', 'riemannZeta_eq_zero_re', 'LFunction_ne_zero_of_half_lt_re', 'LFunction_eq_zero_re',
         'LFunction_eq_zero_re_of_isPrimitive']
depth = {n2i[r]: 0 for r in roots}
q = deque(depth)
while q:
    x = q.popleft()
    for y in adj[x]:
        if y not in depth:
            depth[y] = depth[x] + 1
            q.append(y)

LANES = [
    ('Stated results', '#7a7974', lambda m: m.split('.')[0] in TOP_MODS),
    ('Analytic reduction\n(functional equation, Γ-factor)', '#2a78d6', lambda m: 'GammaFactorNonvanishing' in m),
    ('Selmer bound VWin\n→ nonvanishing', '#eb6834', lambda m: any(k in m for k in ('CharacterBoxes', 'ModularityArgument', 'ThirdPlaceSeries'))),
    ('Galois representations\n(Row0b, PropsB)', '#1baf7a', lambda m: 'GaloisRepresentations' in m and 'Theta' not in m),
    ('Theta lifts\n(TLiftK)', '#6250d6', lambda m: 'Theta' in m),
    ('Local Langlands\n(recT, LawsT)', '#eda100', lambda m: 'LocalLanglands' in m),
    ('Foundations: cusp forms, Weil–Deligne,\nCM fields, Arakelov positivity', '#a8a7a1', lambda m: True),
]


def lane(i):
    m = meta[i][1]
    for k, (_, _, f) in enumerate(LANES):
        if f(m):
            return k


MAXD = 5
nodes = [i for i, d in depth.items() if d <= MAXD and meta[i][2] in ('theorem', 'lemma', 'def', 'abbrev', 'structure')]
cell = defaultdict(list)
for i in nodes:
    cell[(depth[i], lane(i))].append(i)
nl = len(LANES)
lane_w = [1.0, 1.0, 1.25, 1.25, 1.0, 1.35, 1.6]
lx = np.concatenate([[0], np.cumsum(lane_w)])
pos = {}
for (d, k), ids in cell.items():
    ids.sort(key=lambda i: meta[i][0])
    n = len(ids)
    for j, i in enumerate(ids):
        pos[i] = (lx[k] + lane_w[k] * (j + 1) / (n + 1), -d + (0.18 if (n > 4 and j % 2) else 0))

fig = plt.figure(figsize=(30, 24), dpi=100)
ax = fig.add_axes([0.03, 0.30, 0.95, 0.66])
for k, (name, c, _) in enumerate(LANES):
    ax.add_patch(Rectangle((lx[k] + 0.01, -MAXD - 0.6), lane_w[k] - 0.02, MAXD + 1.15, color=c, alpha=0.07, lw=0))
    ax.text(lx[k] + lane_w[k] / 2, 0.75, name, ha='center', va='bottom', fontsize=14, fontweight='bold', color=c if k else '#52514e')
for d in range(MAXD + 1):
    ax.axhline(-d, color='#e4e3df', lw=0.8, zorder=0)
    ax.text(-0.04, -d, f'depth {d}', ha='right', va='center', fontsize=13, color='#52514e')
S = set(pos)
for a in S:
    for b in adj[a]:
        if b in S and depth[b] == depth[a] + 1:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=7, lw=0.6,
                                         color='#52514e', alpha=0.35, connectionstyle='arc3,rad=0.06', zorder=1))
for i, (x, y) in pos.items():
    k = lane(i)
    c = LANES[k][1]
    big = depth[i] <= 4
    ax.scatter([x], [y], s=110 if big else 45, color=c, edgecolors='white', linewidths=1.2, zorder=3,
               marker='s' if meta[i][2] in ('def', 'abbrev', 'structure') else 'o')
    short = meta[i][0].split('.')[-1]
    ax.text(x, y - 0.11, short, ha='center', va='top', fontsize=10.5 if big else 8, color='#0b0b0b', zorder=4,
            rotation=0 if big else 25)
ax.set_xlim(-0.5, lx[-1] + 0.05)
ax.set_ylim(-MAXD - 0.7, 1.25)
ax.axis('off')
ax.set_title('Top of the RH proof tree, laid out by depth (rows) and mathematical role (lanes).  ● theorem   ■ definition', loc='left', fontsize=18, pad=28)

ax2 = fig.add_axes([0.06, 0.04, 0.90, 0.21])


def lib(mod):
    p = mod.split('.')
    return p[0] + '.' + p[1] if p[0] in ('Development', 'Formalism', 'CompanionTheory') and len(p) > 1 else p[0]


libs = Counter(lib(meta[i][1]) for i in depth)
top = [l for l, _ in libs.most_common(7)]
PAL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6']
md = max(depth.values())
xs = np.arange(MAXD + 1, md + 1)
bottom = np.zeros(len(xs))
per = defaultdict(Counter)
for i, d in depth.items():
    per[d][lib(meta[i][1])] += 1
for l, c in list(zip(top, PAL)) + [('Other', '#c9c8c3')]:
    vals = np.array([per[d][l] if l != 'Other' else sum(v for kk, v in per[d].items() if kk not in top) for d in xs])
    ax2.bar(xs, vals, bottom=bottom, color=c, width=0.82, label=l, edgecolor='white', linewidth=0.6)
    bottom += vals
ax2.set_xlabel('depth below the RH theorem', fontsize=12)
ax2.set_ylabel('declarations', fontsize=12)
ax2.set_title(f'Below depth {MAXD}: {sum(1 for d in depth.values() if d > MAXD):,} more declarations down to depth {md}, by library '
              f'(cleaned walk, {len(depth):,} reached in total)', loc='left', fontsize=14)
ax2.legend(frameon=False, ncol=4, fontsize=10.5, loc='upper right')
for s in ('top', 'right'):
    ax2.spines[s].set_visible(False)
fig.savefig(f'{OUT}/graph_backbone_layered.png', bbox_inches='tight')
fig.savefig(f'{OUT}/graph_backbone_layered.pdf', bbox_inches='tight')
print('nodes shown', len(pos), 'reached', len(depth), 'max depth', md)
