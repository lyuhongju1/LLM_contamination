#!/usr/bin/env python3
"""Revision reanalyses (referee report 1, points 2, 3, 4, 6) on the released data.
Usage: python reanalysis.py <repo_root> <out_md>
No new sampling. Uses the same final-record rule and frozen keys as analysis/analyze.py."""
import json, re, math, sys, os, statistics
from collections import defaultdict, Counter

ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
out = []
def w(s=""): out.append(s)

def load(fn):
    recs = [json.loads(l) for l in open(P('data', fn), encoding='utf-8')]
    final = {}
    for r in recs:
        k = (r['pair'], r['condition'], r['model'], r['sample'])
        if k not in final or r.get('max_tokens', 0) > final[k].get('max_tokens', 0):
            final[k] = r
    return list(final.values())

claude = load('raw_v2.jsonl') + load('raw_dprime.jsonl')
qwen = load('raw_local.jsonl')
cfg = json.load(open(P('keys.json'), encoding='utf-8'))
pairs = {p['name']: p for p in cfg['pairs']}
MS = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6',
      'qwen2.5:32b-instruct': 'Q32', 'qwen2.5:72b-instruct': 'Q72'}

# leakage audit, identical rule to analyze.py
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I):
            leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
assert len(ITEMS) == 26, len(ITEMS)

def hit(pn, item, text):
    return re.search(pairs[pn]['items'][item]['regex'], text, re.I) is not None

# identity regexes: successor (frozen key, used even where leakage-excluded) and baseline name
SUCC = {pn: p['items']['successor_named']['regex'] for pn, p in pairs.items()
        if 'successor_named' in p['items']}
SUCC['lhcb'] = r'upgrade\s?(i|1)\b|run\s?3'   # no frozen successor key for lhcb; added here, flagged in text
BASE = {pn: '|'.join(p['redact_patterns']) for pn, p in pairs.items()}

def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 3
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)

def newcombe(k1, n1, k2, n2):
    p1, l1, u1 = wilson(k1, n1); p2, l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)

cells = defaultdict(list)
for r in claude + qwen:
    cells[(r['pair'], r['condition'], MS[r['model']])].append(r)

def rate(pn, item, cond, m, filt=None, trunc=None):
    rs = cells.get((pn, cond, m), [])
    if filt: rs = [r for r in rs if not filt(r)]
    k = sum(hit(pn, item, (r['response'][:trunc[(pn, cond)]] if trunc else r['response'])) for r in rs)
    return k, len(rs)

def pct(k, n):
    if n == 0: return '--'
    p, lo, hi = wilson(k, n)
    return f"{100*p:.0f} [{100*lo:.0f}, {100*hi:.0f}]"

# ------------------------------------------------------------------ R2
w("## R2. Conditions D and D' restricted to samples that do not identify the experiment\n")
w("Identity rates first: share of D / D' samples naming the successor (frozen successor key, "
  "applied even where the key was leakage-excluded for A-C) or the baseline experiment itself "
  "(the redaction patterns). LHCb has no frozen successor key; an ad hoc 'Upgrade I / Run 3' "
  "expression is used here and flagged.\n")
w("| pair | model | D succ. | D succ. or baseline | D' succ. | D' succ. or baseline |")
w("|---|---|---|---|---|---|")
for pn in pairs:
    for m in ['S4.5', 'S4.6']:
        row = [pn, m]
        for c in ['D', 'Dp']:
            rs = cells[(pn, c, m)]
            s = sum(bool(re.search(SUCC[pn], r['response'], re.I)) for r in rs)
            sb = sum(bool(re.search(SUCC[pn] + '|' + BASE[pn], r['response'], re.I)) for r in rs)
            row += [pct(s, len(rs)), pct(sb, len(rs))]
        w('| ' + ' | '.join(row) + ' |')
w()
w("Technology and design items, all samples vs. samples that name neither the successor nor the "
  "baseline (n = retained samples).\n")
w("| item | model | D all | D anonymous (n) | D' all | D' anonymous (n) |")
w("|---|---|---|---|---|---|")
r2rows = []
for pn, item in ITEMS:
    if item == 'successor_named': continue
    for m in ['S4.5', 'S4.6']:
        f = lambda r, pn=pn: re.search(SUCC[pn] + '|' + BASE[pn], r['response'], re.I) is not None
        row = [f"{pn}.{item}", m]
        for c in ['D', 'Dp']:
            ka, na = rate(pn, item, c, m)
            kf, nf = rate(pn, item, c, m, filt=f)
            row += [pct(ka, na), f"{pct(kf, nf)} ({nf})"]
            r2rows.append((pn, item, m, c, ka / na, (kf / nf) if nf else None, nf))
        w('| ' + ' | '.join(row) + ' |')
w()
big = [(f"{p}.{i}", m, c, round(100*a), round(100*b), n) for p, i, m, c, a, b, n in r2rows
       if b is not None and n >= 10 and a - b >= 0.15]
w(f"Items whose anonymous-subset rate drops by 15 points or more (n_retained >= 10): {big if big else 'none'}\n")
thin = [(f"{p}.{i}", m, c, n) for p, i, m, c, a, b, n in r2rows if n < 10]
w(f"Cells with fewer than 10 anonymous samples (estimate unreliable): {thin}\n")

# ------------------------------------------------------------------ R3
w("## R3. All A-D gaps with Newcombe 95% intervals (Claude, N=50 per cell)\n")
w("| item | model | A | D | A-D [95% CI] | sign |")
w("|---|---|---|---|---|---|")
neg, pos, null = [], [], []
for pn, item in ITEMS:
    for m in ['S4.5', 'S4.6']:
        ka, na = rate(pn, item, 'A', m); kd, nd = rate(pn, item, 'D', m)
        d, lo, hi = newcombe(ka, na, kd, nd)
        s = '+' if lo > 0 else ('-' if hi < 0 else '0')
        (pos if s == '+' else neg if s == '-' else null).append((f"{pn}.{item}", m, round(100*d)))
        w(f"| {pn}.{item} | {m} | {100*ka/na:.0f} | {100*kd/nd:.0f} | {100*d:+.0f} [{100*lo:+.0f}, {100*hi:+.0f}] | {s} |")
w()
w(f"Significantly positive (A>D): {len(pos)} of 52 item-model cells: {pos}\n")
w(f"Significantly negative (D>A): {len(neg)} of 52: {neg}\n")
w(f"Interval includes zero: {len(null)} of 52\n")

# ------------------------------------------------------------------ R4
w("## R4. Full distribution over the 26 audited items\n")
UNITS = {  # related items counted once (union of hits within a sample where same pair; mean where different pairs)
    'SiPM (darkside+exo200)': [('darkside', 'sipm_adoption'), ('exo200', 'sipm_adoption')],
    'FD squeezing+filter cavity (aligo)': [('aligo', 'fd_squeezing'), ('aligo', 'filter_cavity')],
}
def unit_rate(members, cond, m):
    if len({p for p, _ in members}) == 1:
        pn = members[0][0]; rs = cells[(pn, cond, m)]
        return sum(any(hit(pn, i, r['response']) for _, i in members) for r in rs) / len(rs)
    return statistics.mean(rate(p, i, cond, m)[0] / rate(p, i, cond, m)[1] for p, i in members)
grouped = {x for v in UNITS.values() for x in v}
units = [(f"{p}.{i}", [(p, i)]) for p, i in ITEMS if (p, i) not in grouped] + list(UNITS.items())
bins = [(0, .10, '0-10'), (.10, .25, '10-25'), (.25, .50, '25-50'), (.50, .75, '50-75'), (.75, .90, '75-90'), (.90, 1.01, '90-100')]
for label, unitlist in [('26 items', [(f"{p}.{i}", [(p, i)]) for p, i in ITEMS]), (f'{len(units)} independent units', units)]:
    w(f"### {label}\n")
    w("| model | cond | " + ' | '.join(b[2] for b in bins) + " | median |")
    w("|---|---|" + '---|' * (len(bins) + 1))
    for m in ['S4.5', 'S4.6']:
        for c in ['A', 'B', 'C', 'D', 'Dp']:
            rs_ = [unit_rate(mem, c, m) for _, mem in unitlist]
            cnt = [sum(lo <= x < hi for x in rs_) for lo, hi, _ in bins]
            w(f"| {m} | {c} | " + ' | '.join(map(str, cnt)) + f" | {100*statistics.median(rs_):.0f} |")
    w()
w("Reviewer's counts check (S4.5, condition A, 26 items): "
  f">=90%: {sum(rate(p,i,'A','S4.5')[0]>=45 for p,i in ITEMS)}, "
  f"<=22%: {sum(rate(p,i,'A','S4.5')[0]<=11 for p,i in ITEMS)}, "
  f">=90% in D: {sum(rate(p,i,'D','S4.5')[0]>=45 for p,i in ITEMS)}\n")
w("### Per-item rates, all conditions (rate %, N=50; D' N=20)\n")
w("| item | class | S4.5 A/B/C/D/D' | S4.6 A/B/C/D/D' |")
w("|---|---|---|---|")
for pn, item in ITEMS:
    row = [f"{pn}.{item}", pairs[pn]['items'][item]['class']]
    for m in ['S4.5', 'S4.6']:
        row.append(' / '.join(f"{100*k/n:.0f}" for k, n in (rate(pn, item, c, m) for c in ['A','B','C','D','Dp'])))
    w('| ' + ' | '.join(row) + ' |')
w()

# ------------------------------------------------------------------ R6
w("## R6. Open-weight comparison on shared cells, with a length control\n")
def toks(r):
    u = r.get('usage') or {}
    return u.get('output_tokens')
for m in ['S4.5', 'S4.6', 'Q32', 'Q72']:
    t = [toks(r) for k, v in cells.items() if k[2] == m and k[1] in 'ABCD' for r in v if toks(r)]
    ch = [len(r['response']) for k, v in cells.items() if k[2] == m and k[1] in 'ABCD' for r in v]
    w(f"- {m}: median output tokens {statistics.median(t):.0f}, median characters {statistics.median(ch):.0f}")
w()
qcells = {(p, c) for (p, c, m) in cells if m == 'Q72' and c in 'ABC'}
shared_pairs = sorted({p for p, c in qcells})
w(f"Pairs with paper conditions on BOTH Qwen sizes: {shared_pairs}. D is available for all ten pairs on both sizes.\n")
# truncation: cut each Claude response to the median Qwen-72B character length of the same pair x condition
trunc = {}
for (p, c, m), rs in cells.items():
    if m == 'Q72' and c in 'ABCD':
        trunc[(p, c)] = int(statistics.median(len(r['response']) for r in rs))
w("Claude rates are shown in full and truncated to the median Qwen-72B response length (characters) "
  "of the same pair and condition. Truncation is a crude lower bound: it removes later-listed proposals, "
  "whereas a shorter answer would choose what to include.\n")
w("| item | cond | Q32 | Q72 | S4.5 full | S4.5 trunc | S4.6 full | S4.6 trunc |")
w("|---|---|---|---|---|---|---|---|")
agg = defaultdict(list)
for pn, item in ITEMS:
    for c in ['A', 'D']:
        if (pn, c) not in trunc: continue
        if c == 'A' and pn not in shared_pairs: continue
        vals = {}
        for m in ['Q32', 'Q72']:
            k, n = rate(pn, item, c, m); vals[m] = k / n
        for m in ['S4.5', 'S4.6']:
            k, n = rate(pn, item, c, m); vals[m] = k / n
            k2, n2 = rate(pn, item, c, m, trunc=trunc); vals[m + 't'] = k2 / n2
        for kk, v in vals.items(): agg[(c, kk)].append(v)
        w(f"| {pn}.{item} | {c} | " + ' | '.join(f"{100*vals[x]:.0f}" for x in ['Q32','Q72','S4.5','S4.5t','S4.6','S4.6t']) + ' |')
w()
for c in ['A', 'D']:
    w(f"- Mean over shared {c} items: " + ', '.join(f"{k}: {100*statistics.mean(agg[(c,k)]):.0f}" for k in ['Q32','Q72','S4.5','S4.5t','S4.6','S4.6t']))
w()
w("Within-Qwen 32B -> 72B, condition D, all ten pairs (identity vs technology items):\n")
w("| item | class | Q32 D | Q72 D |")
w("|---|---|---|---|")
for pn in pairs:
    for item, spec in pairs[pn]['items'].items():
        k1, n1 = rate(pn, item, 'D', 'Q32'); k2, n2 = rate(pn, item, 'D', 'Q72')
        w(f"| {pn}.{item} | {spec['class']} | {pct(k1,n1)} | {pct(k2,n2)} |")
w()

# ------------------------------------------------------------------ minors
w("## Minor: VeloPix, both models\n")
for m in ['S4.5', 'S4.6']:
    w(f"- {m}: A {pct(*rate('lhcb','velopix','A',m))}, D {pct(*rate('lhcb','velopix','D',m))}, D' {pct(*rate('lhcb','velopix','Dp',m))}")
w()
open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
print('wrote', OUT)
