import json
import pickle
import re
import sys
from collections import Counter, defaultdict, deque

import networkx as nx
import numpy as np

sys.path.insert(0, sys.argv[4])
from notes import GLOSSARY, NOTES

idx = pickle.load(open(sys.argv[1], 'rb'))
OUT = sys.argv[2]
TEMPLATE = sys.argv[3]
meta = idx['meta']
n2i = {m[0]: i for i, m in enumerate(meta)}
TOP_MODS = ('Main', 'Statements', 'Supplements')


def real(i):
    return '.' in meta[i][0] or meta[i][1].split('.')[0] in TOP_MODS


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
    ('Stated results', '#6f6e69', lambda m: m.split('.')[0] in TOP_MODS, 'Main.lean, Statements.lean'),
    ('Analytic reduction', '#2a78d6', lambda m: 'GammaFactorNonvanishing' in m, 'functional equation, Γ-factor'),
    ('Selmer bound ⟹ nonvanishing', '#e0602c', lambda m: any(k in m for k in ('CharacterBoxes', 'ModularityArgument', 'ThirdPlaceSeries')), 'VWin, Green, theta integrals'),
    ('Galois representations', '#1a9e6f', lambda m: 'GaloisRepresentations' in m and 'Theta' not in m, 'Row0b, PropsB'),
    ('Theta lifts', '#6250d6', lambda m: 'Theta' in m, 'TLiftK'),
    ('Local Langlands', '#b87900', lambda m: any(k in m for k in ('LocalLanglands', 'NonGaloisDescent.Langlands', 'LanglandsExtension')), 'recT, LawsT, segments'),
    ('Representation-theoretic foundations', '#8f8e88', lambda m: True, 'cusp forms, Weil–Deligne, CM fields, Arakelov'),
]


def lane(i):
    for k, (_, _, f, _) in enumerate(LANES):
        if f(meta[i][1]):
            return k


def group(mod):
    return '.'.join(mod.split('.')[:3])


def lib(mod):
    p = mod.split('.')
    return p[0] + '.' + p[1] if p[0] in ('Development', 'Formalism', 'CompanionTheory') and len(p) > 1 else p[0]


MAXD = 6
KINDS = ('theorem', 'lemma', 'def', 'abbrev', 'structure')
nodes = [i for i, d in depth.items() if d <= MAXD and meta[i][2] in KINDS and not meta[i][0].split('.')[-1].startswith('_')]
S = set(nodes)
lane_w = [1.6, 1.15, 1.3, 1.2, 0.85, 1.45, 2.1]
lx = [0]
for w in lane_w:
    lx.append(lx[-1] + w)
W = 1560
LM = 70
TM = 96
sx = (W - LM - 10) / lx[-1]
SLOT = 92
ROWH = 54
cell = defaultdict(list)
for i in nodes:
    cell[(depth[i], lane(i))].append(i)
layout, rows_needed = {}, defaultdict(int)
for (d, k), ids in cell.items():
    ids.sort(key=lambda i: (meta[i][2] not in ('def', 'abbrev', 'structure'), meta[i][0].split('.')[-1].lower()))
    cap = max(1, int(sx * lane_w[k] // (SLOT if d < 6 else 30)))
    nr = -(-len(ids) // cap)
    layout[(d, k)] = (cap, nr)
    rows_needed[d] = max(rows_needed[d], nr)
ytop, y = {}, TM
for d in range(MAXD + 1):
    ytop[d] = y
    y += max(1, rows_needed[d]) * (ROWH if d < 6 else 24) + 72
HH = y
pos, colof = {}, {}
for (d, k), ids in cell.items():
    cap, nr = layout[(d, k)]
    for j, i in enumerate(ids):
        r, c = divmod(j, cap)
        inrow = min(cap, len(ids) - r * cap)
        pos[i] = (LM + sx * (lx[k] + lane_w[k] * (c + 1) / (inrow + 1)), ytop[d] + r * (ROWH if d < 6 else 24))
        colof[i] = c

gloss_re = [(re.compile(r'(?<![\w.])(?:[\w.]*\.)?' + re.escape(k) + r'(?![\w])'), k, t, dfn) for k, t, dfn in GLOSSARY]


def terms_for(i):
    s = meta[i][4]
    out = []
    for r, k, t, dfn in gloss_re:
        if k == meta[i][0].split('.')[-1]:
            continue
        if r.search(s):
            out.append([t, dfn])
    seen, res = set(), []
    for t, dfn in out:
        if t not in seen:
            seen.add(t)
            res.append([t, dfn])
    return res


nid = {i: f'n{k}' for k, i in enumerate(nodes)}
node_js = []
for i in nodes:
    short = meta[i][0].split('.')[-1]
    node_js.append({'id': nid[i], 'x': round(pos[i][0], 1), 'y': round(pos[i][1], 1), 'lane': lane(i), 'd': depth[i],
                    'col': colof[i], 'name': meta[i][0], 'short': short, 'kind': meta[i][2], 'mod': meta[i][1],
                    'lines': meta[i][3], 'stmt': meta[i][4], 'note': NOTES.get(short, ''), 'terms': terms_for(i),
                    'grp': group(meta[i][1])})
edge_js = [[nid[a], nid[b]] for a in nodes for b in set(adj[a]) if b in S and depth[b] == depth[a] + 1]

# whole-proof module-group graph
gcount = Counter(group(meta[i][1]) for i in depth)
gmin = {}
for i, d in depth.items():
    g = group(meta[i][1])
    gmin[g] = min(gmin.get(g, 99), d)
gedge = Counter()
indeg = Counter()
for a in depth:
    ga = group(meta[a][1])
    for b in adj[a]:
        if b in depth:
            indeg[b] += 1
            gb = group(meta[b][1])
            if ga != gb:
                gedge[(ga, gb)] += 1
G = nx.Graph()
for g in gcount:
    G.add_node(g)
for (a, b), w in gedge.items():
    if G.has_edge(a, b):
        G[a][b]['w'] += w
    else:
        G.add_edge(a, b, w=w)
P = nx.spring_layout(G, k=1.5 / np.sqrt(G.number_of_nodes()), iterations=250, seed=11)
GW, GH = 1500, 1250
names_ = list(P)
xy = np.array([P[g] for g in names_], dtype=float)
xy = (xy - xy.min(0)) / (xy.max(0) - xy.min(0))
xy = np.column_stack([60 + xy[:, 0] * (GW - 120), 60 + xy[:, 1] * (GH - 120)])
rad = np.array([2.5 + np.sqrt(gcount[g]) * 0.30 for g in names_])
home = xy.copy()
for it in range(600):
    d = xy[:, None, :] - xy[None, :, :]
    dist = np.sqrt((d ** 2).sum(-1)) + 1e-9
    need = rad[:, None] + rad[None, :] + 3.0
    ov = np.clip(need - dist, 0, None)
    np.fill_diagonal(ov, 0)
    if ov.max() < 0.05:
        break
    push = (d / dist[..., None]) * (ov[..., None] * 0.5)
    w = rad[None, :] / (rad[:, None] + rad[None, :])
    xy += (push * w[..., None]).sum(1)
    xy += (home - xy) * 0.004
    xy[:, 0] = np.clip(xy[:, 0], rad + 8, GW - rad - 8)
    xy[:, 1] = np.clip(xy[:, 1], rad + 8, GH - rad - 8)
print('collision iterations', it, 'max overlap', round(float(ov.max()), 3))
POS = {g: [round(float(xy[k, 0]), 1), round(float(xy[k, 1]), 1)] for k, g in enumerate(names_)}
RAD = {g: round(float(rad[k]), 2) for k, g in enumerate(names_)}


def sc(p):
    return p


bygroup = defaultdict(list)
for i in depth:
    bygroup[group(meta[i][1])].append(i)
libs = Counter(lib(meta[i][1]) for i in depth)
top_libs = [l for l, _ in libs.most_common(7)]
glist = sorted(gcount, key=lambda g: -gcount[g])
gid = {g: k for k, g in enumerate(glist)}
groups_js = []
for g in glist:
    best = sorted(bygroup[g], key=lambda i: (-indeg[i], depth[i]))[:8]
    l = lib(g)
    groups_js.append({'g': g, 'n': gcount[g], 'd': gmin[g], 'lib': top_libs.index(l) if l in top_libs else 7,
                      'xy': POS[g], 'r': RAD[g], 'top': [[meta[i][0], meta[i][2], depth[i], meta[i][4][:240]] for i in best]})
gedges_js = [[gid[a], gid[b], d['w']] for a, b, d in G.edges(data=True)]

per = defaultdict(Counter)
for i, d in depth.items():
    l = lib(meta[i][1])
    per[d][l if l in top_libs else 'Other'] += 1
md = max(depth.values())
bars = {'libs': top_libs + ['Other'], 'depths': list(range(MAXD + 1, md + 1)),
        'counts': [[per[d][l] for l in top_libs + ['Other']] for d in range(MAXD + 1, md + 1)]}
kinds_r = Counter(meta[i][2] for i in depth)
stats = {'reached': len(depth), 'maxd': md, 'below': sum(1 for d in depth.values() if d > MAXD), 'files': len(idx['files']),
         'decls': len(meta), 'groups': len(gcount), 'gedges': len(gedges_js),
         'lines': sum(f['lines'] for f in idx['files']), 'thm': kinds_r['theorem'] + kinds_r['lemma'], 'defs': kinds_r['def'] + kinds_r['abbrev'] + kinds_r['structure']}
lanes_js = [{'name': L[0], 'sub': L[3], 'color': L[1], 'x0': LM + sx * lx[k], 'w': sx * lane_w[k]} for k, L in enumerate(LANES)]
data = {'nodes': node_js, 'edges': edge_js, 'lanes': lanes_js, 'bars': bars, 'stats': stats, 'W': W, 'H': HH, 'TM': TM,
        'MAXD': MAXD, 'ytop': [ytop[d] for d in range(MAXD + 1)], 'groups': groups_js, 'gedges': gedges_js, 'GW': GW, 'GH': GH}
page = open(TEMPLATE).read().replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
open(OUT, 'w').write(page)
print('nodes', len(nodes), 'edges', len(edge_js), 'groups', len(groups_js), 'gedges', len(gedges_js), 'bytes', len(page))
