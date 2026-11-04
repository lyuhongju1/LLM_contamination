#!/usr/bin/env python3
"""Score Amendment 7 (paraphrase families P1, P2 and the extended-thinking arm T) against the frozen
criteria R1-R4. Usage: python score_amend7.py <repo_root> <out_md>"""
import json, re, math, sys, os
from collections import defaultdict

ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
out = []; w = lambda s="": out.append(s)
MS = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6'}

def final(fn, keyf):
    best = {}
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l); k = keyf(r)
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    return list(best.values())

orig = final('raw_v2.jsonl', lambda r: (r['pair'], r['condition'], r['model'], r['sample']))
para = final('raw_paraphrase.jsonl', lambda r: (r['template'], r['pair'], r['condition'], r['model'], r['sample']))
cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]

cells = defaultdict(list)   # (template, pair, cond, model) -> records
for r in orig: cells[('O', r['pair'], r['condition'], MS[r['model']])].append(r)
for r in para: cells[(r['template'], r['pair'], r['condition'], MS[r['model']])].append(r)

def hit(pn, item, t): return t is not None and re.search(pairs[pn]['items'][item]['regex'], t, re.I) is not None
def kn(tpl, pn, item, c, m, field='response'):
    rs = cells.get((tpl, pn, c, m), []); return sum(hit(pn, item, r.get(field)) for r in rs), len(rs)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return p, max(0, c-h), min(1, c+h)
def newcombe(k1, n1, k2, n2):
    p1, l1, u1 = wilson(k1, n1); p2, l2, u2 = wilson(k2, n2); d = p1 - p2
    return d, d - math.sqrt((p1-l1)**2 + (u2-p2)**2), d + math.sqrt((u1-p1)**2 + (p2-l2)**2)
def pc(k, n): return f"{100*k/n:.0f}" if n else "--"

n_check = {k: len(v) for k, v in cells.items() if k[0] in ('P1', 'P2', 'T')}
w(f"Records: paraphrase final {len(para)}; cells P1/P2 sizes {sorted({v for k,v in n_check.items() if k[0]!='T'})}; T sizes {sorted({v for k,v in n_check.items() if k[0]=='T'})}\n")

# ---------------- R1
w("## R1 Saturation (items >= 90% in D on the original template must stay >= 75% in D under P1 and P2)\n")
w("| item | model | O | P1 | P2 | pass |"); w("|---|---|---|---|---|---|")
r1 = []
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        k, n = kn('O', pn, item, 'D', m)
        if k / n >= 0.9:
            v = [kn(t, pn, item, 'D', m) for t in ('P1', 'P2')]
            ok = all(a / b >= 0.75 for a, b in v); r1.append(ok)
            w(f"| {pn}.{item} | {m} | {pc(k,n)} | {pc(*v[0])} | {pc(*v[1])} | {'yes' if ok else 'NO'} |")
w(f"\nR1: {sum(r1)} of {len(r1)} pass\n")

# ---------------- R2
w("## R2 VeloPix on Sonnet 4.5: A - D >= 50 points under each family\n")
for t in ('O', 'P1', 'P2'):
    a = kn(t, 'lhcb', 'velopix', 'A', 'S4.5'); d = kn(t, 'lhcb', 'velopix', 'D', 'S4.5')
    dd, lo, hi = newcombe(*a, *d)
    w(f"- {t}: A {pc(*a)}, D {pc(*d)}, A-D {100*dd:+.0f} [{100*lo:+.0f}, {100*hi:+.0f}] -> {'pass' if dd >= 0.5 else 'FAIL'}" if t != 'O' else f"- {t}: A {pc(*a)}, D {pc(*d)}, A-D {100*dd:+.0f}")
w()

# ---------------- R3
w("## R3 Cutoff suppression on Sonnet 4.6 (A -> B, Newcombe interval excludes zero under each family)\n")
w("| item | O A->B | P1 A->B [CI] | P2 A->B [CI] | pass |"); w("|---|---|---|---|---|")
for pn, item in [('darkside', 'successor_named'), ('gerda', 'inverted_coaxial'), ('lhcb', 'velopix'), ('sno', 'successor_named')]:
    row = [f"{pn}.{item}"]; oks = []
    for t in ('O', 'P1', 'P2'):
        a = kn(t, pn, item, 'A', 'S4.6'); b = kn(t, pn, item, 'B', 'S4.6'); dd, lo, hi = newcombe(*a, *b)
        if t == 'O': row.append(f"{pc(*a)} -> {pc(*b)}")
        else: row.append(f"{pc(*a)} -> {pc(*b)} [{100*lo:+.0f}, {100*hi:+.0f}]"); oks.append(lo > 0)
    row.append('yes' if all(oks) else 'NO'); w('| ' + ' | '.join(row) + ' |')
w()

# ---------------- R4
w("## R4 Anchoring: originally significant negative A - D cells keep a negative point estimate\n")
w("| item | model | O A-D | P1 A-D | P2 A-D | pass |"); w("|---|---|---|---|---|---|")
r4 = []
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        a = kn('O', pn, item, 'A', m); d = kn('O', pn, item, 'D', m); dd, lo, hi = newcombe(*a, *d)
        if hi < 0:
            v = []
            for t in ('P1', 'P2'):
                a2 = kn(t, pn, item, 'A', m); d2 = kn(t, pn, item, 'D', m); v.append(a2[0]/a2[1] - d2[0]/d2[1])
            ok = all(x < 0 for x in v); r4.append(ok)
            w(f"| {pn}.{item} | {m} | {100*dd:+.0f} | {100*v[0]:+.0f} | {100*v[1]:+.0f} | {'yes' if ok else 'NO'} |")
w(f"\nR4: {sum(r4)} of {len(r4)} pass\n")

# ---------------- full per-item table + max shift
w("## All items, all templates (rate %; O = original template)\n")
w("| item | model | A O/P1/P2 | B O/P1/P2 | D O/P1/P2 | max shift |"); w("|---|---|---|---|---|---|")
shifts = []
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        row = [f"{pn}.{item}", m]; ms = 0
        for c in 'ABD':
            v = [kn(t, pn, item, c, m) for t in ('O', 'P1', 'P2')]; r = [a/b for a, b in v]
            ms = max(ms, max(r) - min(r)); row.append('/'.join(f"{100*x:.0f}" for x in r))
        shifts.append(ms); row.append(f"{100*ms:.0f}"); w('| ' + ' | '.join(row) + ' |')
shifts.sort()
w(f"\nMax across-template shift per item-model (over A, B, D): median {100*shifts[len(shifts)//2]:.0f}, "
  f"75th pct {100*shifts[int(.75*len(shifts))]:.0f}, max {100*shifts[-1]:.0f} points; "
  f"{sum(s > .3 for s in shifts)} of {len(shifts)} exceed 30 points\n")

# ---------------- thinking arm
w("## Extended-thinking arm (original templates, N=20) vs original no-thinking (N=50)\n")
w("Rates %. 'think-only' = share of samples where the item appears in the thinking text but not in the final answer.\n")
w("| item | model | A no-think / think | B no-think / think | D no-think / think | think-only A/B/D |"); w("|---|---|---|---|---|---|")
tdiff = defaultdict(list)
for pn, item in ITEMS:
    if not cells.get(('T', pn, 'A', 'S4.5')): continue
    for m in ['S4.5', 'S4.6']:
        row = [f"{pn}.{item}", m]; to = []
        for c in 'ABD':
            o = kn('O', pn, item, c, m); t = kn('T', pn, item, c, m)
            row.append(f"{pc(*o)} / {pc(*t)}"); tdiff[(m, c)].append(t[0]/t[1] - o[0]/o[1])
            rs = cells[('T', pn, c, m)]
            to.append(sum(hit(pn, item, r.get('thinking')) and not hit(pn, item, r['response']) for r in rs) / len(rs))
        row.append('/'.join(f"{100*x:.0f}" for x in to)); w('| ' + ' | '.join(row) + ' |')
w()
for k, v in sorted(tdiff.items()):
    w(f"- {k[0]} {k[1]}: mean change with thinking {100*sum(v)/len(v):+.1f} points over {len(v)} items; "
      f"items moving >= 20 points: {sum(abs(x) >= .2 for x in v)}")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out)); print('wrote', OUT)
