#!/usr/bin/env python3
"""Reproduce every number and figure in the article from data/raw_v2.jsonl.
Applies the pre-registered replacement rule (mt8000 resample supersedes its
capped mt4000 original), re-runs the leakage audit against corpus/, scores all
items, writes the scores CSV with Wilson intervals, and regenerates both figures.
Usage: python analysis/analyze.py   (from the repository root; needs matplotlib)"""
import json, re, csv, math, os
from collections import defaultdict

recs = [json.loads(l) for l in open('data/raw_v2.jsonl', encoding='utf-8')]
final = {}
for r in recs:
    k = (r['pair'], r['condition'], r['model'], r['sample'])
    if k not in final or r['max_tokens'] > final[k]['max_tokens']:
        final[k] = r
recs = list(final.values())
from collections import Counter as _C
_cells = _C((r['pair'], r['condition'], r['model']) for r in recs)
N_CELL = max(_cells.values())
assert len(set(_cells.values())) == 1, f"uneven cells: {sorted(set(_cells.values()))}"
print(f"records: {len(recs)} ({N_CELL} per cell)")
assert all(r['stop_reason'] == 'end_turn' for r in recs)

cfg = json.load(open('keys.json', encoding='utf-8'))
pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    if os.path.exists(p['paper_txt']):
        text = open(p['paper_txt'], encoding='utf-8', errors='ignore').read()
        for item, spec in p['items'].items():
            if re.search(spec['regex'], text, re.I):
                leaked.add((pn, item))
print('leakage-excluded items (from available corpus files):', sorted(leaked))

def wilson(k, n=None, z=1.96):
    n = n or N_CELL
    p = k/n; d = 1+z*z/n
    c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return p, max(0, c-h), min(1, c+h)

score = defaultdict(lambda: defaultdict(int))
for r in recs:
    for item, spec in pairs[r['pair']]['items'].items():
        if re.search(spec['regex'], r['response'], re.I):
            score[(r['pair'], item, r['model'])][r['condition']] += 1

with open('data/atlas_scores_v2.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['pair','item','class','model','condition','hits','n','rate','ci_lo','ci_hi','leak_excluded'])
    for (p,i,m), s in sorted(score.items()):
        for c in 'ABCD':
            r_, lo, hi = wilson(s[c])
            w.writerow([p, i, pairs[p]['items'][i]['class'], m, c, s[c], N_CELL,
                        f"{r_:.3f}", f"{lo:.3f}", f"{hi:.3f}", (p,i) in leaked and c != 'D'])
print('scores written to data/atlas_scores_v2.csv')

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
models = sorted({r['model'] for r in recs})
LEAKED_CANONICAL = {('protodune','successor_named'),('xenon1t','successor_named'),
                    ('icecube','successor_named'),('exo200','successor_named')}
excl = leaked or LEAKED_CANONICAL
items = [(p,i) for p in pairs for i in pairs[p]['items'] if (p,i) not in excl]
items.sort(key=lambda pi: -sum(score[(pi[0],pi[1],m)]['A'] for m in models))
fig, axes = plt.subplots(1, 2, figsize=(9, 8), sharey=True)
for ax, m, t in zip(axes, models, ['Sonnet 4.5', 'Sonnet 4.6']):
    M = np.array([[score[(p,i,m)][c]*100/N_CELL for c in 'ABCD'] for p,i in items])
    ax.imshow(M, cmap='Greys', vmin=0, vmax=100, aspect='auto')
    ax.set_xticks(range(4)); ax.set_xticklabels(list('ABCD')); ax.set_title(t)
    for y in range(len(items)):
        for x in range(4):
            v = M[y,x]
            ax.text(x, y, f"{v:.0f}", ha='center', va='center', fontsize=6.5,
                    color='white' if v > 55 else 'black')
axes[0].set_yticks(range(len(items)))
axes[0].set_yticklabels([f"{p}.{i}" for p,i in items], fontsize=7)
plt.tight_layout(); plt.savefig('analysis/fig1_heatmap.pdf', bbox_inches='tight'); plt.close()

fig, axes = plt.subplots(1, 2, figsize=(9, 4.6), sharex=True)
for ax, m, t in zip(axes, models, ['Sonnet 4.5', 'Sonnet 4.6']):
    sel = [(p,i) for p,i in items if abs(score[(p,i,m)]['A']-score[(p,i,m)]['B'])*100/N_CELL >= 15]
    sel.sort(key=lambda pi: score[(pi[0],pi[1],m)]['B']-score[(pi[0],pi[1],m)]['A'])
    for y,(p,i) in enumerate(sel):
        a, b = score[(p,i,m)]['A']*100/N_CELL, score[(p,i,m)]['B']*100/N_CELL
        ax.plot([a,b],[y,y], color='0.6', lw=1.2)
        ax.scatter([a],[y], s=34, c='black')
        ax.scatter([b],[y], s=34, facecolor='white', edgecolor='black')
    ax.set_yticks(range(len(sel))); ax.set_yticklabels([f"{p}.{i}" for p,i in sel], fontsize=7)
    ax.set_title(t); ax.set_xlim(-4,104); ax.grid(axis='x', color='0.9')
plt.tight_layout(); plt.savefig('analysis/fig2_cutoff.pdf', bbox_inches='tight'); plt.close()
print('figures regenerated in analysis/')
