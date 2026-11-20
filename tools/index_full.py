import json
import multiprocessing as mp
import os
import pickle
import re
import sys
from collections import Counter

SRC = sys.argv[1]
OUT = sys.argv[2]

KINDS = r'theorem|lemma|def|abbrev|structure|class|inductive|instance|opaque|axiom'
decl_re = re.compile(
    r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|nonrec|scoped|local)\s+)*'
    r'(' + KINDS + r')\b\s*([^\s:({\[]*)')
ns_re = re.compile(r'^namespace\s+(\S+)')
sec_re = re.compile(r'^(?:noncomputable\s+)?section\b\s*(\S*)')
end_re = re.compile(r'^end\b\s*(\S*)')
open_re = re.compile(r'^open\s+(?:scoped\s+)?([^\n(]+)')
imp_re = re.compile(r'^import\s+(\S+)')
tok_re = re.compile(r"[A-Za-z_Ͱ-Ͽᴀ-ᶿ℀-⅏][\w.'₀-ₜᵢ-ᵪ!?]*")
TACTICS = ['simp', 'simpa', 'rw', 'exact', 'apply', 'refine', 'intro', 'rintro', 'obtain', 'have', 'linarith', 'nlinarith',
           'positivity', 'omega', 'ring', 'ring_nf', 'field_simp', 'norm_num', 'decide', 'aesop', 'gcongr', 'calc', 'constructor',
           'ext', 'funext', 'induction', 'cases', 'rcases', 'by_contra', 'push_neg', 'filter_upwards', 'fun_prop', 'continuity',
           'measurability', 'tauto', 'exact_mod_cast', 'push_cast', 'norm_cast', 'unfold', 'subst', 'use', 'exists', 'trivial',
           'native_decide', 'sorry', 'polyrith', 'bound', 'interval_cases', 'fin_cases', 'congr', 'convert', 'specialize']
tac_res = {t: re.compile(r'(?<![\w.])' + re.escape(t) + r'(?![\w])') for t in TACTICS}


def files():
    for root, _, fs in os.walk(SRC):
        for fn in fs:
            if fn.endswith('.lean'):
                yield os.path.join(root, fn)


def parse(path):
    mod = os.path.relpath(path, SRC)[:-5].replace(os.sep, '.')
    with open(path, encoding='utf-8', errors='replace') as fh:
        text = fh.read()
    lines = text.split('\n')
    imports, opens, decls = [], [], []
    stack = []
    cur = None
    for i, raw in enumerate(lines):
        l = raw.rstrip()
        if not l or l[0] in ' \t':
            continue
        if m := imp_re.match(l):
            imports.append(m.group(1)); continue
        if m := ns_re.match(l):
            stack.append(('ns', m.group(1))); continue
        if m := sec_re.match(l):
            stack.append(('sec', m.group(1))); continue
        if end_re.match(l) and stack:
            stack.pop(); continue
        if m := open_re.match(l):
            opens.extend(x for x in m.group(1).split() if x[0].isalpha() or x[0] == '_'); continue
        if m := decl_re.match(l):
            kind, name = m.group(1), m.group(2)
            ns = '.'.join(x for k, x in stack if k == 'ns')
            if name.startswith('_root_.'):
                full = name[7:]
            elif name:
                full = (ns + '.' + name) if ns else name
            else:
                full = f'{mod}#anon{i}'
            if cur is not None:
                cur['end'] = i
            cur = {'name': full, 'kind': kind, 'start': i, 'end': len(lines), 'ns': ns}
            decls.append(cur)
    for d in decls:
        body = '\n'.join(lines[d['start']:d['end']])
        cut = body.find(':=')
        hdr = body if cut < 0 else body[:cut]
        d['stmt'] = ' '.join(hdr.split())[:700]
        d['plines'] = d['end'] - d['start']
        d['tokens'] = sorted(set(tok_re.findall(body)))
    tac = Counter()
    for t, r in tac_res.items():
        n = len(r.findall(text))
        if n:
            tac[t] = n
    return {'mod': mod, 'imports': imports, 'opens': sorted(set(opens)), 'lines': len(lines),
            'bytes': len(text.encode()), 'decls': decls, 'tac': dict(tac)}


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    paths = list(files())
    with mp.get_context('fork').Pool(16) as pool:
        recs = pool.map(parse, paths, chunksize=200)
    names = {}
    for fi, r in enumerate(recs):
        for di, d in enumerate(r['decls']):
            names.setdefault(d['name'], (fi, di))
    print('files', len(recs), 'decls', sum(len(r['decls']) for r in recs), 'unique names', len(names), flush=True)
    # resolve references
    nid = {n: k for k, n in enumerate(names)}
    edges = []
    for fi, r in enumerate(recs):
        opens = r['opens']
        for di, d in enumerate(r['decls']):
            me = nid.get(d['name'])
            if me is None or names[d['name']] != (fi, di):
                d.pop('tokens', None); continue
            parts = d['ns'].split('.') if d['ns'] else []
            prefixes = ['.'.join(parts[:k]) for k in range(len(parts), 0, -1)] + opens
            outs = set()
            for t in d.pop('tokens'):
                t = t.rstrip('.')
                cand = None
                if t in nid:
                    cand = t
                else:
                    for p in prefixes:
                        q = p + '.' + t
                        if q in nid:
                            cand = q; break
                if cand is not None and cand != d['name']:
                    outs.add(nid[cand])
            for o in outs:
                edges.append((me, o))
    print('edges', len(edges), flush=True)
    meta = []
    for n, (fi, di) in names.items():
        d = recs[fi]['decls'][di]
        meta.append((n, recs[fi]['mod'], d['kind'], d['plines'], d['stmt']))
    filemeta = [{k: r[k] for k in ('mod', 'imports', 'lines', 'bytes', 'tac')} | {'ndecl': len(r['decls'])} for r in recs]
    pickle.dump({'meta': meta, 'edges': edges, 'files': filemeta}, open(os.path.join(OUT, 'index.pkl'), 'wb'), protocol=5)
    print('saved', flush=True)
