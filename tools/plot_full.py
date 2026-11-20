import json
import os
import pickle
import sys
from collections import Counter, defaultdict, deque

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

idx = pickle.load(open(sys.argv[1], 'rb'))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
meta, edges, files = idx['meta'], idx['edges'], idx['files']
N = len(meta)
name2id = {m[0]: i for i, m in enumerate(meta)}
adj = defaultdict(list)
for a, b in edges:
    adj[a].append(b)

ROOTS = [n for n in ['riemannHypothesis', 'riemannZeta_eq_zero_re', 'LFunction_ne_zero_of_half_lt_re',
                     'LFunction_eq_zero_re', 'LFunction_eq_zero_re_of_isPrimitive'] if n in name2id]
depth = {}
q = deque()
for r in ROOTS:
    depth[name2id[r]] = 0
    q.append(name2id[r])
while q:
    x = q.popleft()
    for y in adj[x]:
        if y not in depth:
            depth[y] = depth[x] + 1
            q.append(y)


def lib(mod):
    p = mod.split('.')
    if p[0] in ('Development', 'CompanionTheory', 'Formalism') and len(p) > 1:
        return p[0] + '.' + p[1]
    return p[0]


def group(mod):
    return '.'.join(mod.split('.')[:3])


libs_all = Counter(lib(m[1]) for m in meta)
libs_reach = Counter(lib(meta[i][1]) for i in depth)
top_libs = [l for l, _ in libs_reach.most_common(7)]
PAL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6']
OTHER = '#a8a7a1'
col = {l: PAL[i] for i, l in enumerate(top_libs)}


def color(mod):
    return col.get(lib(mod), OTHER)


plt.rcParams.update({'font.family': 'Helvetica', 'font.size': 9, 'axes.edgecolor': '#c9c8c3', 'axes.labelcolor': '#52514e',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e', 'axes.spines.top': False, 'axes.spines.right': False})


def legend_handles():
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], marker='o', color='w', markerfacecolor=col[l], markersize=8, label=l) for l in top_libs]
    h.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=OTHER, markersize=8, label='Other'))
    return h


# 1. area-level graph of everything the proof reaches
gcount = Counter(group(meta[i][1]) for i in depth)
gdepth = defaultdict(lambda: 99)
for i, dd in depth.items():
    g = group(meta[i][1])
    gdepth[g] = min(gdepth[g], dd)
gedge = Counter()
for a in depth:
    ga = group(meta[a][1])
    for b in adj[a]:
        if b in depth:
            gb = group(meta[b][1])
            if ga != gb:
                gedge[(ga, gb)] += 1
G = nx.DiGraph()
for g, c in gcount.items():
    G.add_node(g, w=c)
for (a, b), w in gedge.items():
    G.add_edge(a, b, w=w)
pos = nx.spring_layout(G.to_undirected(), k=1.6 / np.sqrt(max(1, G.number_of_nodes())), iterations=200, seed=7, weight=None)
fig, ax = plt.subplots(figsize=(22, 22), dpi=110)
ew = np.array([G[u][v]['w'] for u, v in G.edges()]) if G.number_of_edges() else np.array([1])
nx.draw_networkx_edges(G, pos, ax=ax, width=0.25 + 1.2 * np.log10(ew) / max(1, np.log10(ew.max())), alpha=0.18,
                       edge_color='#52514e', arrows=False)
sizes = [12 + 2.2 * np.sqrt(G.nodes[g]['w']) * 6 for g in G]
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=[color(g) for g in G], linewidths=0.6, edgecolors='white')
lab = sorted(G, key=lambda g: -G.nodes[g]['w'])[:45] + [g for g in G if gdepth[g] <= 2]
for g in set(lab):
    x, y = pos[g]
    ax.text(x, y, g.split('.', 1)[-1] if '.' in g else g, fontsize=7.5, color='#0b0b0b', ha='center', va='bottom')
ax.legend(handles=legend_handles(), loc='upper left', frameon=False, fontsize=11, title='library', title_fontsize=11)
ax.set_title(f'Everything the RH proof reaches: {len(depth):,} declarations in {G.number_of_nodes():,} module groups, '
             f'{G.number_of_edges():,} group-to-group dependencies\n(node size ~ sqrt(declarations reached); edges = references between groups)',
             fontsize=15, loc='left')
ax.axis('off')
fig.savefig(f'{OUT}/graph_areas.png', bbox_inches='tight'); fig.savefig(f'{OUT}/graph_areas.pdf', bbox_inches='tight')
plt.close(fig)

# 2. declaration-level backbone: top layers of the proof
LIMIT = 1800
keep = [i for i, dd in sorted(depth.items(), key=lambda x: x[1])]
keep = [i for i in keep if meta[i][2] in ('theorem', 'lemma', 'def', 'abbrev', 'structure')]
maxd = 0
sel = []
for i in keep:
    if len(sel) >= LIMIT:
        break
    sel.append(i)
    maxd = depth[i]
sel = set(sel)
B = nx.DiGraph()
for i in sel:
    B.add_node(i)
for a in sel:
    for b in adj[a]:
        if b in sel:
            B.add_edge(a, b)
layers = defaultdict(list)
for i in sel:
    layers[depth[i]].append(i)
posb = {}
for dd, nodes in layers.items():
    nodes.sort(key=lambda i: (lib(meta[i][1]), meta[i][1]))
    n = len(nodes)
    for k, i in enumerate(nodes):
        posb[i] = ((k + 0.5) / n, -dd)
pos2 = nx.spring_layout(B.to_undirected(), pos=posb, fixed=None, iterations=40, seed=3, k=0.02)
for i in pos2:
    pos2[i] = (pos2[i][0], posb[i][1] * 0.15 + pos2[i][1] * 0.0)
fig, ax = plt.subplots(figsize=(26, 16), dpi=110)
nx.draw_networkx_edges(B, posb, ax=ax, width=0.2, alpha=0.12, edge_color='#52514e', arrows=False)
nx.draw_networkx_nodes(B, posb, ax=ax, node_size=[60 if depth[i] <= 2 else 12 for i in B],
                       node_color=[color(meta[i][1]) for i in B], linewidths=0.3, edgecolors='white')
for i in B:
    if depth[i] <= 2:
        x, y = posb[i]
        ax.text(x, y + 0.12, meta[i][0].split('.')[-1], fontsize=7, rotation=30, ha='left', va='bottom', color='#0b0b0b')
for dd in layers:
    ax.text(-0.02, -dd, f'depth {dd}  ({len(layers[dd])})', ha='right', va='center', fontsize=9, color='#52514e')
ax.legend(handles=legend_handles(), loc='lower right', frameon=False, fontsize=10)
ax.set_title(f'Top of the proof tree: the first {len(sel):,} declarations below the RH theorem, by distance from it '
             f'(depth 0 = Main.lean)', fontsize=15, loc='left')
ax.axis('off')
fig.savefig(f'{OUT}/graph_backbone.png', bbox_inches='tight'); fig.savefig(f'{OUT}/graph_backbone.pdf', bbox_inches='tight')
plt.close(fig)

# 3. metadata dashboard
fig, axs = plt.subplots(3, 2, figsize=(16, 17), dpi=110)
ax = axs[0, 0]
L = [l for l, _ in libs_all.most_common(14)]
ya = np.arange(len(L))
ax.barh(ya, [libs_all[l] for l in L], color='#d9d8d4', height=0.7, label='all declarations')
ax.barh(ya, [libs_reach[l] for l in L], color=[col.get(l, OTHER) for l in L], height=0.7, label='reached by the RH proof')
ax.set_yticks(ya, L); ax.invert_yaxis(); ax.set_xscale('log'); ax.set_xlabel('declarations (log scale)')
ax.set_title('Where the declarations live, and how many the proof uses', loc='left'); ax.legend(frameon=False)
ax = axs[0, 1]
dc = Counter(depth.values())
xs = sorted(dc)
ax.bar(xs, [dc[x] for x in xs], color='#2a78d6', width=0.8)
ax.set_yscale('log'); ax.set_xlabel('distance from the RH theorem (references)'); ax.set_ylabel('declarations (log)')
ax.set_title(f'Depth profile of the proof: {len(depth):,} reachable, max depth {max(xs)}', loc='left')
ax = axs[1, 0]
kinds = Counter(m[2] for m in meta)
kr = Counter(meta[i][2] for i in depth)
K = [k for k, _ in kinds.most_common(10)]
xk = np.arange(len(K))
ax.bar(xk - 0.2, [kinds[k] for k in K], 0.4, color='#d9d8d4', label='all')
ax.bar(xk + 0.2, [kr[k] for k in K], 0.4, color='#eb6834', label='reached')
ax.set_xticks(xk, K, rotation=30); ax.set_yscale('log'); ax.legend(frameon=False)
ax.set_title('Kinds of declaration', loc='left')
ax = axs[1, 1]
pl_all = np.array([m[3] for m in meta if m[2] in ('theorem', 'lemma')])
pl_r = np.array([meta[i][3] for i in depth if meta[i][2] in ('theorem', 'lemma')])
bins = np.logspace(0, np.log10(max(2, pl_all.max())), 50)
ax.hist(pl_all, bins=bins, color='#d9d8d4', label=f'all theorems (median {int(np.median(pl_all))} lines)')
ax.hist(pl_r, bins=bins, color='#1baf7a', label=f'reached (median {int(np.median(pl_r)) if len(pl_r) else 0} lines)')
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('lines per theorem (statement + proof)'); ax.legend(frameon=False)
ax.set_title('How long the proofs are', loc='left')
ax = axs[2, 0]
tac = Counter()
for f in files:
    tac.update(f['tac'])
T = [t for t, _ in tac.most_common(22)]
ax.barh(np.arange(len(T)), [tac[t] for t in T], color='#6250d6', height=0.7)
ax.set_yticks(np.arange(len(T)), T); ax.invert_yaxis(); ax.set_xscale('log'); ax.set_xlabel('occurrences (log)')
ax.set_title('Tactic and keyword usage across all files', loc='left')
ax = axs[2, 1]
indeg = Counter(b for a, b in edges if a in depth and b in depth)
topn = [(i, c) for i, c in indeg.most_common(400) if '.' in meta[i][0] and len(meta[i][0].split('.')[-1]) > 3][:18]
ax.barh(np.arange(len(topn)), [c for _, c in topn], color=[color(meta[i][1]) for i, _ in topn], height=0.7)
ax.set_yticks(np.arange(len(topn)), [meta[i][0][-48:] for i, _ in topn], fontsize=7.5); ax.invert_yaxis()
ax.set_xlabel('declarations in the proof that cite it')
ax.set_title('Most-cited named results inside the proof (qualified names only)', loc='left')
fig.suptitle('lean.tar.gz: metadata of the formal RH development', fontsize=17, x=0.02, ha='left')
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(f'{OUT}/metadata.png', bbox_inches='tight'); fig.savefig(f'{OUT}/metadata.pdf', bbox_inches='tight')
plt.close(fig)

# 4. text outputs: the first layers of the proof tree with statements
with open(f'{OUT}/proof_top_layers.md', 'w') as fh:
    fh.write('# Top of the proof tree (from Main.lean)\n\n')
    for dd in range(0, 5):
        ids = sorted([i for i, x in depth.items() if x == dd and meta[i][2] in ('theorem', 'lemma', 'def', 'abbrev')],
                     key=lambda i: meta[i][0])
        fh.write(f'## depth {dd} ({len(ids)} declarations)\n\n')
        for i in ids[:150]:
            fh.write(f'- **{meta[i][0]}** ({meta[i][2]}, `{meta[i][1]}`, {meta[i][3]} lines)\n  `{meta[i][4][:500]}`\n')
        fh.write('\n')
summary = {'declarations': N, 'files': len(files), 'lines': sum(f['lines'] for f in files), 'edges': len(edges),
           'reachable_from_RH': len(depth), 'max_depth': max(depth.values()) if depth else 0,
           'reachable_by_lib': libs_reach.most_common(), 'all_by_lib': libs_all.most_common(),
           'kinds_all': kinds.most_common(), 'kinds_reached': kr.most_common(), 'roots': ROOTS,
           'top_cited': [(meta[i][0], c) for i, c in topn]}
json.dump(summary, open(f'{OUT}/summary.json', 'w'), indent=1)
print(json.dumps({k: summary[k] for k in ('declarations', 'files', 'lines', 'edges', 'reachable_from_RH', 'max_depth')}))
print(summary['reachable_by_lib'][:10]); print(summary['kinds_reached'])
