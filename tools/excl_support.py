import json
import pickle
import sys
from collections import Counter, defaultdict, deque

idx = pickle.load(open(sys.argv[1], 'rb'))
OUT = sys.argv[2]
meta = idx['meta']
n2i = {m[0]: i for i, m in enumerate(meta)}
TOP = ('Main', 'Statements', 'Supplements')


def real(i):
    return '.' in meta[i][0] or meta[i][1].split('.')[0] in TOP


adj = defaultdict(set)
for a, b in idx['edges']:
    if real(b):
        adj[a].add(b)


def reach(starts):
    seen = set(starts)
    q = deque(starts)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


roots = ['riemannHypothesis', 'riemannZeta_eq_zero_re', 'LFunction_ne_zero_of_half_lt_re', 'LFunction_eq_zero_re',
         'LFunction_eq_zero_re_of_isPrimitive']
R = reach([n2i[r] for r in roots])

PILLARS = [
    ('Analytic reduction', '#2a78d6', ['Formalism.VW.rh_of_every', 'Formalism.VW.critLine'],
     'RH and the critical line from nonvanishing right of ½ (functional equation, Γ-factor).'),
    ('Galois representations', '#1a9e6f', ['UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift'],
     'Row0b: l-adic Galois representations for polarized cuspidal π over CM fields.'),
    ('Theta lifts', '#6250d6', ['UpperTheory.TP.K.tLiftK'], 'TLiftK: theta lifting from U(n) to U(d) for all large d.'),
    ('Local Langlands', '#b87900', ['UpperTheory.Zero.LLC.recTExists'], 'RecTExists: the local Langlands correspondence for GL_n.'),
    ('Selmer bound', '#e0602c', ['UpperTheory.One.vwin_of_row'], 'VWin: the uniform Selmer/Ш-length bound, from Row0b.'),
    ('Nonvanishing bridge', '#c2410c', ['UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin'],
     'From VWin and the literature bundle to L(s, χ) ≠ 0 (theta integrals, Green, covolume bound).'),
]
D = []
for name, col, starts, desc in PILLARS:
    D.append(reach([n2i[s] for s in starts]) & R)
cnt = Counter()
for s in D:
    for x in s:
        cnt[x] += 1
E = [{x for x in s if cnt[x] == 1} for s in D]
union = set().union(*D)
shared = {x for x in union if cnt[x] >= 2}
none = R - union


def grp(mod, k=4):
    return '.'.join(mod.split('.')[:k])


def lib(mod):
    p = mod.split('.')
    return p[0] + '.' + p[1] if p[0] in ('Development', 'Formalism', 'CompanionTheory') and len(p) > 1 else p[0]


def summarize(S):
    ind = Counter()
    for a in S:
        for b in adj[a]:
            if b in S:
                ind[b] += 1
    kinds = Counter(meta[i][2] for i in S)
    return {
        'n': len(S), 'lines': int(sum(meta[i][3] for i in S)),
        'thm': kinds['theorem'] + kinds['lemma'], 'defs': kinds['def'] + kinds['abbrev'] + kinds['structure'],
        'libs': Counter(lib(meta[i][1]) for i in S).most_common(5),
        'mods': Counter(grp(meta[i][1]) for i in S).most_common(8),
        'top': [[meta[i][0], meta[i][2], ind[i], meta[i][4][:260]] for i, _ in
                sorted(((i, ind[i]) for i in S if '.' in meta[i][0]), key=lambda t: -t[1])[:8]],
    }


pillars = []
for k, (name, col, starts, desc) in enumerate(PILLARS):
    pillars.append({'name': name, 'color': col, 'roots': starts, 'desc': desc, 'support': len(D[k]),
                    'excl': summarize(E[k]), 'share': round(len(E[k]) / len(R), 4)})
overlap = [[len(D[a] & D[b]) for b in range(len(D))] for a in range(len(D))]
res = {'reached': len(R), 'union': len(union), 'shared': summarize(shared), 'none': len(none), 'pillars': pillars,
       'overlap': overlap}
json.dump(res, open(OUT, 'w'), ensure_ascii=False)
print('reached', len(R), 'union', len(union), 'shared', len(shared), 'outside', len(none))
for p in pillars:
    e = p['excl']
    print(f"{p['name']:24s} support {p['support']:7d} exclusive {e['n']:7d} ({100*p['share']:.1f}%) lines {e['lines']:8d}  top mods {[m for m,_ in e['mods'][:3]]}")
print('shared top mods', [m for m, _ in res['shared']['mods'][:5]])
for r in overlap:
    print(r)
