import json
import os
import re
import sys
from collections import Counter, defaultdict

src = sys.argv[1]
out = sys.argv[2]

decl_re = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private |protected |noncomputable )*(theorem|lemma)\s+(\S+)')
imp_re = re.compile(r'^import\s+(\S+)')


def group_of(mod, depth=3):
    return '.'.join(mod.split('.')[:depth])


modules = {}
for root, _, files in os.walk(src):
    for fn in files:
        if not fn.endswith('.lean'):
            continue
        path = os.path.join(root, fn)
        mod = os.path.relpath(path, src)[:-5].replace(os.sep, '.')
        with open(path, encoding='utf-8', errors='replace') as fh:
            lines = fh.read().split('\n')
        imports = [m.group(1) for l in lines if (m := imp_re.match(l))]
        decls = []
        i = 0
        while i < len(lines):
            m = decl_re.match(lines[i])
            if m:
                buf = [lines[i].strip()]
                j = i
                while ':=' not in lines[j] and not lines[j].rstrip().endswith(' where') and j - i < 25 and j + 1 < len(lines):
                    j += 1
                    buf.append(lines[j].strip())
                text = ' '.join(buf)
                cut = text.find(':=')
                if cut >= 0:
                    text = text[:cut].rstrip()
                decls.append({'kind': m.group(1), 'name': m.group(2), 'stmt': text[:900]})
                i = j + 1
            else:
                i += 1
        modules[mod] = {'imports': imports, 'decls': decls, 'lines': len(lines)}

internal = set(modules)
gstats = defaultdict(lambda: {'files': 0, 'decls': 0, 'lines': 0})
gedges = Counter()
ext = Counter()
for mod, d in modules.items():
    g = group_of(mod)
    gstats[g]['files'] += 1
    gstats[g]['decls'] += len(d['decls'])
    gstats[g]['lines'] += d['lines']
    for imp in d['imports']:
        if imp in internal:
            h = group_of(imp)
            if h != g:
                gedges[(g, h)] += 1
        else:
            ext[(g, imp.split('.')[0])] += 1

json.dump({
    'modules': modules,
    'groups': gstats,
    'edges': [[a, b, n] for (a, b), n in gedges.items()],
    'external': [[a, b, n] for (a, b), n in ext.items()],
}, open(out, 'w'))
print(len(modules), 'modules', sum(len(d['decls']) for d in modules.values()), 'decls', len(gstats), 'groups')
