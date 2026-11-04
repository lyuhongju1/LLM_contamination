#!/usr/bin/env python3
"""Score Amendment 8 (and, when present, Amendment 9 part c) model runs against frozen expectations.
Usage: python score_models.py <repo_root> <out_md> [--newest]"""
import json, re, math, sys, os, statistics
from collections import defaultdict

ROOT, OUT = sys.argv[1], sys.argv[2]; NEWEST = '--newest' in sys.argv
P = lambda *a: os.path.join(ROOT, *a)
out = []; w = lambda s="": out.append(s)
SHORT = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6', 'claude-sonnet-5': 'S5',
         'claude-haiku-4-5-20251001': 'H4.5', 'claude-opus-4-5-20251101': 'O4.5',
         'claude-haiku-5-5': 'H5.5', 'claude-sonnet-5-5': 'S5.5', 'claude-opus-5-5': 'O5.5', 'claude-fable-5-1': 'F5.1'}

def load(fn, only_template=None):
    best = {}
    if not os.path.exists(P('data', fn)): return []
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l)
        if only_template and r.get('template', 'O') != only_template: continue
        k = (r['pair'], r['condition'], r['model'], r['sample'])
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    return list(best.values())

recs = load('raw_v2.jsonl') + load('raw_dprime.jsonl') + load('raw_models.jsonl') + load('raw_amend10.jsonl')
cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
cells = defaultdict(list)
for r in recs:
    m = SHORT.get(r['model'], r['model'])
    cells[(r['pair'], r['condition'], m)].append(r['response'])
models = [m for m in ['H4.5', 'S4.5', 'O4.5', 'S4.6', 'S5', 'H5.5', 'S5.5', 'O5.5', 'F5.1'] if any(k[2] == m for k in cells)]

def kn(pn, item, c, m):
    rs = cells.get((pn, c, m), []); rx = pairs[pn]['items'][item]['regex']
    return sum(re.search(rx, t, re.I) is not None for t in rs), len(rs)
def rate(*a):
    k, n = kn(*a); return k / n if n else float('nan')
def wilson(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return p, max(0, c-h), min(1, c+h)
def newcombe(a, b):
    p1, l1, u1 = wilson(*a); p2, l2, u2 = wilson(*b); d = p1-p2
    return d, d-math.sqrt((p1-l1)**2+(u2-p2)**2), d+math.sqrt((u1-p1)**2+(p2-l2)**2)

w(f"Models present: {models}; cell sizes: {sorted({len(v) for v in cells.values()})}\n")
w("## Per-item rates (%), all models, conditions A / B / C / D / D'\n")
w("| item | " + " | ".join(models) + " |"); w("|---|" + "---|" * len(models))
for pn, item in ITEMS:
    w(f"| {pn}.{item} | " + " | ".join('/'.join(f"{100*rate(pn,item,c,m):.0f}" for c in ['A','B','C','D','Dp']) for m in models) + " |")
w()
w("## Distribution over the 26 items (count at >=90% / median %)\n")
w("| model | " + " | ".join(['A', 'B', 'C', 'D', "D'"]) + " |"); w("|---|---|---|---|---|---|")
for m in models:
    row = []
    for c in ['A', 'B', 'C', 'D', 'Dp']:
        rs = [rate(pn, it, c, m) for pn, it in ITEMS]
        row.append(f"{sum(x >= .9 for x in rs)} / {100*statistics.median(rs):.0f}")
    w(f"| {m} | " + " | ".join(row) + " |")
w()

def generation(newest_sonnet, ref='S4.6'):
    w(f"### G1 cutoff, {newest_sonnet} vs {ref} (A -> B; suppression at least as strong; pre-cutoff technologies retained)\n")
    for pn, item in [('darkside','successor_named'), ('lux','successor_named'), ('lhcb','velopix'), ('sno','successor_named')]:
        for m in [ref, newest_sonnet]:
            d, lo, hi = newcombe(kn(pn, item, 'A', m), kn(pn, item, 'B', m))
            w(f"- {pn}.{item} {m}: A {100*rate(pn,item,'A',m):.0f} -> B {100*rate(pn,item,'B',m):.0f}, drop {100*d:+.0f} [{100*lo:+.0f}, {100*hi:+.0f}]")
    for pn, item in [('darkside','sipm_adoption'), ('exo200','sipm_adoption'), ('protodune','xarapuca'), ('lhcb','scifi')]:
        w(f"- retained {pn}.{item} {newest_sonnet}: A {100*rate(pn,item,'A',newest_sonnet):.0f} -> B {100*rate(pn,item,'B',newest_sonnet):.0f}")
    w(f"\n### G2 identity in D: successor naming {newest_sonnet} >= {ref}, pair by pair\n")
    ge = 0; tot = 0
    for pn in pairs:
        if 'successor_named' not in pairs[pn]['items']: continue
        a, b = rate(pn, 'successor_named', 'D', ref), rate(pn, 'successor_named', 'D', newest_sonnet); tot += 1; ge += b >= a
        w(f"- {pn}: {ref} {100*a:.0f}, {newest_sonnet} {100*b:.0f}")
    w(f"\nG2: {ge} of {tot} pairs at least as high -> {'holds (majority)' if ge > tot/2 else 'does NOT hold'}\n")

def scale(h, s, o):
    sat = [(pn, it) for pn, it in ITEMS if pairs[pn]['items'][it]['class'] == 'technology_recall' and rate(pn, it, 'D', s) >= .9]
    w(f"### S1 defaults: technology items >= 90% in D on {s} reach >= 50% on {h}\n")
    ok = 0
    for pn, it in sat:
        x = rate(pn, it, 'D', h); ok += x >= .5; w(f"- {pn}.{it}: {s} {100*rate(pn,it,'D',s):.0f}, {h} {100*x:.0f}")
    w(f"\nS1: {ok} of {len(sat)}\n")
    tech = [(pn, it) for pn, it in ITEMS if pairs[pn]['items'][it]['class'] == 'technology_recall']
    iden = [(pn, 'successor_named') for pn in pairs if 'successor_named' in pairs[pn]['items']]  # D: leakage irrelevant
    rt = statistics.mean(rate(*x, 'D', h) for x in tech) / statistics.mean(rate(*x, 'D', s) for x in tech)
    ri = statistics.mean(rate(*x, 'D', h) for x in iden) / statistics.mean(rate(*x, 'D', s) for x in iden)
    w(f"### S2 dissociation: fraction of {s}'s condition-D rate retained by {h}\n\n- technology items: {100*rt:.0f}%\n- identity items: {100*ri:.0f}%\n- S2 {'holds' if rt > ri else 'does NOT hold'}\n")
    io = statistics.mean(rate(*x, 'D', o) for x in iden); isn = statistics.mean(rate(*x, 'D', s) for x in iden)
    w(f"### S3 upward: mean identity rate in D, {o} {100*io:.0f}% vs {s} {100*isn:.0f}% -> {'holds' if io >= isn else 'does NOT hold'}\n")

w("## Amendment 8 expectations\n")
generation('S5'); scale('H4.5', 'S4.5', 'O4.5')
if NEWEST and 'S5.5' in models:
    w("## Amendment 9 (c) re-tests\n"); generation('S5.5'); scale('H5.5', 'S5.5', 'O5.5')

w("## Response length (median output tokens, all conditions)\n")
for fn in ['raw_v2.jsonl', 'raw_models.jsonl', 'raw_amend10.jsonl']:
    toks = defaultdict(list)
    for r in load(fn):
        toks[SHORT.get(r['model'], r['model'])].append((r.get('usage') or {}).get('output_tokens', 0))
    for m, v in toks.items(): w(f"- {m}: {statistics.median(v):.0f}")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out)); print('wrote', OUT)
