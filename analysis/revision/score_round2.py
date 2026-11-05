#!/usr/bin/env python3
"""Second-round reanalysis (internal review): per-template saturation counts, binomial null for the
five-template spread, content-leakage sensitivity, post-baseline items by pair, nine-model counts.
Exploratory (not pre-registered). Usage: python score_round2.py <repo_root> <out_md>"""
import json, re, math, sys, os, random, statistics as st
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
out = []; w = lambda s="": out.append(s)
SHORT = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6', 'claude-sonnet-5': 'S5',
         'claude-haiku-4-5-20251001': 'H4.5', 'claude-opus-4-5-20251101': 'O4.5',
         'claude-haiku-5-5': 'H5.5', 'claude-sonnet-5-5': 'S5.5', 'claude-opus-5-5': 'O5.5', 'claude-fable-5-1': 'F5.1'}
ORDER = ['H4.5', 'S4.5', 'O4.5', 'S4.6', 'S5', 'H5.5', 'S5.5', 'O5.5', 'F5.1']

cells = defaultdict(list)  # (template, pair, cond, model) -> responses
def load(fn, default_t='O', skip=()):
    best = {}
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l); t = r.get('template', default_t)
        if t in skip: continue
        k = (t, r['pair'], r['condition'], r['model'], r['sample'])
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    for (t, pn, c, m, s), r in best.items(): cells[(t, pn, c, SHORT.get(m, m))].append(r['response'])
load('raw_v2.jsonl'); load('raw_dprime.jsonl'); load('raw_models.jsonl'); load('raw_amend10.jsonl')
load('raw_paraphrase.jsonl', skip=('O', 'T')); load('raw_amend9_ab.jsonl', skip=('O', 'T'))

cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
assert len(ITEMS) == 26, len(ITEMS)
CONTENT_LEAK = {('gerda', 'argon_instrumentation'), ('lhcb', 'velopix')}
POST = [('darkside', 'veto_upgrade_gd'), ('lux', 'xenon_skin'), ('gerda', 'successor_named'), ('gerda', 'inverted_coaxial'),
        ('exo200', 'sipm_adoption'), ('sno', 'successor_named'), ('sno', 'scintillator_fill'), ('sno', 'tellurium')]
_cache = {}
def kn(t, pn, item, c, m):
    key = (t, pn, item, c, m)
    if key not in _cache:
        rs = cells.get((t, pn, c, m), []); rx = pairs[pn]['items'][item]['regex']
        _cache[key] = (sum(re.search(rx, x, re.I) is not None for x in rs), len(rs))
    return _cache[key]
def rate(*a):
    k, n = kn(*a); return 100 * k / n if n else float('nan')
def wilson(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return p, max(0, c-h), min(1, c+h)
def newcombe(a, b):
    p1, l1, u1 = wilson(*a); p2, l2, u2 = wilson(*b); d = p1-p2
    return d, d-math.sqrt((p1-l1)**2+(u2-p2)**2), d+math.sqrt((u1-p1)**2+(p2-l2)**2)

T5 = ['O', 'P1', 'P2', 'P3', 'P4']
# ---- (1) per-template saturation counts
w("# Round-2 reanalysis (exploratory)\n")
w("## 1. Per-template saturation: number of the five templates in which an item is >=90% (or <=10%)\n")
w("| model | cond | items >=90 in all 5 | in >=4 | in >=1 | items <=10 in all 5 | in >=4 | in >=1 |"); w("|---|---|---|---|---|---|---|---|")
per_t = {}
for m in ['S4.5', 'S4.6']:
    for c in 'ABD':
        hi = [sum(rate(t, pn, it, c, m) >= 90 for t in T5) for pn, it in ITEMS]
        lo = [sum(rate(t, pn, it, c, m) <= 10 for t in T5) for pn, it in ITEMS]
        per_t[(m, c)] = (hi, lo)
        w(f"| {m} | {c} | {sum(x == 5 for x in hi)} | {sum(x >= 4 for x in hi)} | {sum(x >= 1 for x in hi)} | {sum(x == 5 for x in lo)} | {sum(x >= 4 for x in lo)} | {sum(x >= 1 for x in lo)} |")
w()
w("Items >=90 under the original template but not under all five (model, cond: item [templates >=90 of 5]):\n")
for m in ['S4.5', 'S4.6']:
    for c in 'AD':
        lst = [f"{pn}.{it} [{sum(rate(t, pn, it, c, m) >= 90 for t in T5)}]" for pn, it in ITEMS
               if rate('O', pn, it, c, m) >= 90 and not all(rate(t, pn, it, c, m) >= 90 for t in T5)]
        w(f"- {m} {c}: {', '.join(lst) or 'none'}")
w()
# ---- (2) binomial null for the five-template range
w("## 2. Binomial null for the five-template range\n")
w("Null: the five templates share the cell's pooled rate; each template is Binomial(n_t, p_pooled). 20,000 draws per cell. p = P(null range >= observed).\n")
rng = random.Random(2026)
def null_ranges(p, ns, B=20000):
    out_ = []
    for _ in range(B):
        v = [sum(rng.random() < p for _ in range(n)) / n for n in ns]
        out_.append(100 * (max(v) - min(v)))
    return out_
# speed: binomial via normal approx is not acceptable at extremes; use exact sampling with cached CDFs
def binom_sampler(n, p):
    cdf = []; acc = 0.0
    for k in range(n + 1):
        acc += math.comb(n, k) * p**k * (1-p)**(n-k); cdf.append(acc)
    def draw():
        u = rng.random()
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if cdf[mid] < u: lo = mid + 1
            else: hi = mid
        return lo
    return draw
w("| model | cond | cells | median obs. range | median null range | cells p<0.05 | expected by chance | cells range>30 | of which p<0.05 |"); w("|---|---|---|---|---|---|---|---|---|")
allp = []
for m in ['S4.5', 'S4.6']:
    for c in 'ABD':
        obs, nullmed, ps, big, bigsig = [], [], [], 0, 0
        for pn, it in ITEMS:
            kns = [kn(t, pn, it, c, m) for t in T5]
            ks = sum(k for k, n in kns); ns = [n for k, n in kns]; p = ks / sum(ns)
            v = [100 * k / n for k, n in kns]; r = max(v) - min(v)
            draws = [binom_sampler(n, p) for n in ns]
            B = 20000; ge = 0; nr = []
            for _ in range(B):
                vv = [100 * d() / n for d, n in zip(draws, ns)]; rr = max(vv) - min(vv); nr.append(rr)
                if rr >= r - 1e-9: ge += 1
            pv = ge / B; obs.append(r); nullmed.append(st.median(nr)); ps.append(pv); allp.append((pv, m, c, pn, it, r))
            if r > 30: big += 1; bigsig += pv < 0.05
        w(f"| {m} | {c} | {len(ITEMS)} | {st.median(obs):.0f} | {st.median(nullmed):.0f} | {sum(x < 0.05 for x in ps)} | {0.05*len(ps):.1f} | {big} | {bigsig} |")
w()
# BH over all 156 cells
allp.sort(); M = len(allp); bh = 0
for i, (pv, *_ ) in enumerate(allp, 1):
    if pv <= 0.05 * i / M: bh = i
w(f"Benjamini-Hochberg at FDR 5% over all {M} cells: {bh} cells show template dependence beyond binomial noise.\n")
w("Mid-range cells only (pooled rate 10-90%):\n")
for m in ['S4.5', 'S4.6']:
    for c in 'ABD':
        mids = [x for x in allp if x[1] == m and x[2] == c]
        mids = [x for x in mids if 10 < 100 * sum(kn(t, x[3], x[4], c, m)[0] for t in T5) / sum(kn(t, x[3], x[4], c, m)[1] for t in T5) < 90]
        w(f"- {m} {c}: {len(mids)} mid-range cells, {sum(x[0] < 0.05 for x in mids)} with p<0.05, median obs range {st.median(x[5] for x in mids):.0f}")
w()
# ---- (3) content-level leakage sensitivity
w("## 3. Content-level leakage sensitivity (exclude GERDA argon instrumentation and LHCb VeloPix)\n")
def dist(items, m, c, t='O'):
    v = [rate(t, pn, it, c, m) for pn, it in items]
    return sum(x >= 90 for x in v), sum(x <= 10 for x in v), st.median(v)
ITEMS24 = [x for x in ITEMS if x not in CONTENT_LEAK]
w("| model | cond | 26 items: >=90 / <=10 / median | 24 items: >=90 / <=10 / median |"); w("|---|---|---|---|")
for m in ORDER:
    for c in 'AD':
        a = dist(ITEMS, m, c); b = dist(ITEMS24, m, c)
        w(f"| {m} | {c} | {a[0]} / {a[1]} / {a[2]:.0f} | {b[0]} / {b[1]} / {b[2]:.0f} |")
w()
for label, its in [('26 items', ITEMS), ('24 items', ITEMS24)]:
    pos = neg = nul = 0
    for pn, it in its:
        for m in ['S4.5', 'S4.6']:
            d, lo, hi = newcombe(kn('O', pn, it, 'A', m), kn('O', pn, it, 'D', m))
            if lo > 0: pos += 1
            elif hi < 0: neg += 1
            else: nul += 1
    w(f"- A-D Newcombe, {label}: {pos} positive, {neg} negative, {nul} null")
w(f"- Content-leak items, rates A/B/C/D: " + "; ".join(f"{pn}.{it} {m}: " + '/'.join(f"{rate('O', pn, it, c, m):.0f}" for c in 'ABCD') for pn, it in CONTENT_LEAK for m in ['S4.5', 'S4.6']))
w()
# ---- (4) post-baseline items by pair
w("## 4. Post-baseline items, by pair (rates %, A / D)\n")
w("| pair | item | " + " | ".join(ORDER) + " |"); w("|---|---|" + "---|" * len(ORDER))
for pn, it in POST:
    w(f"| {pn} | {it} | " + " | ".join(f"{rate('O', pn, it, 'A', m):.0f}/{rate('O', pn, it, 'D', m):.0f}" for m in ORDER) + " |")
w()
w("| model | cond | items >=90 (of 8) | pairs with any item >=90 (of 5) | items <=10 | pairs with all items <=10 |"); w("|---|---|---|---|---|---|")
PP = sorted({pn for pn, _ in POST})
for m in ORDER:
    for c in 'AD':
        v = {(pn, it): rate('O', pn, it, c, m) for pn, it in POST}
        w(f"| {m} | {c} | {sum(x >= 90 for x in v.values())} | {sum(any(v[(pn, it)] >= 90 for p2, it in POST if p2 == pn) for pn in PP)} | "
          f"{sum(x <= 10 for x in v.values())} | {sum(all(v[(pn, it)] <= 10 for p2, it in POST if p2 == pn) for pn in PP)} |")
w()
# ---- (5) nine models: saturated and absent counts, D'
w("## 5. Nine models: items >=90 and <=10 (of 26), median, conditions A / D / D'\n")
w("| model | A >=90 | A <=10 | A med | D >=90 | D <=10 | D med | D' >=90 | D' med |"); w("|---|---|---|---|---|---|---|---|---|")
for m in ORDER:
    a, d = dist(ITEMS, m, 'A'), dist(ITEMS, m, 'D')
    dp = dist(ITEMS, m, 'Dp') if cells.get(('O', 'lux', 'Dp', m)) else None
    w(f"| {m} | {a[0]} | {a[1]} | {a[2]:.0f} | {d[0]} | {d[1]} | {d[2]:.0f} | " + (f"{dp[0]} | {dp[2]:.0f} |" if dp else "- | - |"))
w()
w("## 6. Absence items on all nine models (A/B/C/D/D')\n")
for pn, it in [('sno', 'tellurium'), ('exo200', 'tonne_scale')]:
    w(f"- {pn}.{it}: " + "; ".join(f"{m} " + '/'.join(f"{rate('O', pn, it, c, m):.0f}" if kn('O', pn, it, c, m)[1] else '-' for c in ['A', 'B', 'C', 'D', 'Dp']) for m in ORDER))
w()
w("## 7. Sample counts\n")
for fn in ['raw_v2.jsonl', 'raw_dprime.jsonl', 'raw_local.jsonl', 'raw_v1_superseded.jsonl']:
    keys = set()
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l); keys.add((r.get('template', 'O'), r['pair'], r['condition'], r['model'], r['sample']))
    w(f"- {fn}: {len(keys)} distinct samples")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out)); print('wrote', OUT)
