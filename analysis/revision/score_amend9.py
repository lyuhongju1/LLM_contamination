#!/usr/bin/env python3
"""Score Amendment 9 parts (a) template spread and (b) length control (regex, primary measure).
Usage: python score_amend9.py <repo_root> <out_md>"""
import json, re, math, sys, os, statistics as st
from collections import defaultdict

ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
out = []; w = lambda s="": out.append(s)
MS = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6'}

def final(fn, keyf, keep=lambda r: True):
    best = {}
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l)
        if not keep(r): continue
        k = keyf(r)
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    return list(best.values())

cells = defaultdict(list)
for r in final('raw_v2.jsonl', lambda r: (r['pair'], r['condition'], r['model'], r['sample'])):
    cells[('O', r['pair'], r['condition'], MS[r['model']])].append(r['response'])
for fn in ['raw_paraphrase.jsonl', 'raw_amend9_ab.jsonl']:
    for r in final(fn, lambda r: (r['template'], r['pair'], r['condition'], r['model'], r['sample']),
                   keep=lambda r: r.get('template') not in ('O', 'T')):
        cells[(r['template'], r['pair'], r['condition'], MS[r['model']])].append(r['response'])

cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
def kn(t, pn, item, c, m):
    rs = cells.get((t, pn, c, m), []); rx = pairs[pn]['items'][item]['regex']
    return sum(re.search(rx, x, re.I) is not None for x in rs), len(rs)
def r_(t, pn, item, c, m):
    k, n = kn(t, pn, item, c, m); return 100 * k / n
def wilson(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return p, max(0, c-h), min(1, c+h)
def newcombe(a, b):
    p1, l1, u1 = wilson(*a); p2, l2, u2 = wilson(*b); d = p1-p2
    return d, d-math.sqrt((p1-l1)**2+(u2-p2)**2), d+math.sqrt((u1-p1)**2+(p2-l2)**2)

T5 = ['O', 'P1', 'P2', 'P3', 'P4']
w(f"Cell sizes: {sorted({len(v) for v in cells.values()})}\n")
w("## (a) Five-template spread (regex rates %, templates O/P1/P2/P3/P4)\n")
w("| item | model | cond | O/P1/P2/P3/P4 | mean | SD | range | robust (range<=30) |"); w("|---|---|---|---|---|---|---|---|")
summ = defaultdict(list)
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        for c in 'ABD':
            v = [r_(t, pn, item, c, m) for t in T5]
            rg = max(v) - min(v); summ[(m, c)].append((rg, st.mean(v)))
            w(f"| {pn}.{item} | {m} | {c} | {'/'.join(f'{x:.0f}' for x in v)} | {st.mean(v):.0f} | {st.pstdev(v):.0f} | {rg:.0f} | {'yes' if rg <= 30 else 'no'} |")
w()
w("Summary: wording-robust items (range <= 30 points across five templates)\n")
for (m, c), v in sorted(summ.items()):
    sat = [x for x in v if x[1] >= 90]; low = [x for x in v if x[1] <= 10]; mid = [x for x in v if 10 < x[1] < 90]
    w(f"- {m} {c}: {sum(x[0] <= 30 for x in v)} of {len(v)} robust; median range {st.median(x[0] for x in v):.0f}; "
      f"by template-mean: saturated (>=90) {sum(x[0]<=30 for x in sat)}/{len(sat)}, low (<=10) {sum(x[0]<=30 for x in low)}/{len(low)}, mid {sum(x[0]<=30 for x in mid)}/{len(mid)}")
w()
w("## (b) Length control: K15 - K5 (regex rates %), Newcombe 95% CI\n")
w("| item | model | cond | K5 | K15 | K15-K5 [CI] | class |"); w("|---|---|---|---|---|---|---|")
bs = defaultdict(list)
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        for c in 'AD':
            a, b = kn('K15', pn, item, c, m), kn('K5', pn, item, c, m); d, lo, hi = newcombe(a, b)
            cls = 'breadth-sensitive' if d >= .30 else 'breadth-robust'; bs[(m, c)].append((d, pn, item))
            w(f"| {pn}.{item} | {m} | {c} | {100*b[0]/b[1]:.0f} | {100*a[0]/a[1]:.0f} | {100*d:+.0f} [{100*lo:+.0f}, {100*hi:+.0f}] | {cls} |")
w()
for (m, c), v in sorted(bs.items()):
    w(f"- {m} {c}: breadth-sensitive {sum(d >= .3 for d, _, _ in v)} of {len(v)}; mean K15-K5 {100*st.mean(d for d, _, _ in v):+.0f}; "
      f"items: {[f'{p}.{i}' for d, p, i in v if d >= .3]}")
w()
w("### Frozen expectations\n")
sat_items = [(pn, it, m) for pn, it in ITEMS for m in ['S4.5', 'S4.6'] if r_('O', pn, it, 'D', m) >= 90]
ok = [(pn, it, m) for pn, it, m in sat_items if newcombe(kn('K15', pn, it, 'D', m), kn('K5', pn, it, 'D', m))[0] < .3]
w(f"- Saturated items (>=90% in D, original template) breadth-robust in D: {len(ok)} of {len(sat_items)}; "
  f"exceptions: {[f'{p}.{i} {m}' for p, i, m in sat_items if (p, i, m) not in ok]}")
for m in ['S4.5', 'S4.6']:
    for c in 'AD':
        d, lo, hi = newcombe(kn('K15', 'lhcb', 'velopix', c, m), kn('K5', 'lhcb', 'velopix', c, m))
        w(f"- VeloPix {m} {c}: K5 {r_('K5','lhcb','velopix',c,m):.0f}, K15 {r_('K15','lhcb','velopix',c,m):.0f}, diff {100*d:+.0f} -> {'breadth-sensitive' if d >= .3 else 'breadth-robust'}")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out)); print('wrote', OUT)
