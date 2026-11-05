#!/usr/bin/env python3
"""Figure 1 for the revision: atlas heatmap (Sonnet 4.5, Sonnet 4.6, Qwen2.5 32B, 72B; conditions A-D)
with each row labeled by its dating class (Pre / Cont. / Post, Table tab:dating).
Usage: python make_fig1.py <repo_root> <out_pdf>"""
import json, re, os, sys
from collections import defaultdict
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
def load(fn):
    best = {}
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l); k = (r['pair'], r['condition'], r['model'], r['sample'])
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    return list(best.values())
recs = load('raw_v2.jsonl') + load('raw_local.jsonl')
cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for it, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, it))
hits = defaultdict(int); n = defaultdict(int)
for r in recs:
    n[(r['pair'], r['condition'], r['model'])] += 1
    for it, spec in pairs[r['pair']]['items'].items():
        if re.search(spec['regex'], r['response'], re.I): hits[(r['pair'], it, r['condition'], r['model'])] += 1
CLS = {('darkside','successor_named'):'Pre',('darkside','sipm_adoption'):'Pre',('darkside','veto_upgrade_gd'):'Post',
       ('protodune','xarapuca'):'Pre',('protodune','coverage_increase'):'Cont.',('xenon1t','radon_column'):'Cont.',
       ('xenon1t','neutron_veto'):'Cont.',('lux','successor_named'):'Pre',('lux','xenon_skin'):'Post',('lux','outer_detector'):'Pre',
       ('icecube','mdom'):'Pre',('icecube','degg'):'Pre',('gerda','successor_named'):'Post',('gerda','inverted_coaxial'):'Post',
       ('gerda','argon_instrumentation'):'Pre',('exo200','sipm_adoption'):'Post',('exo200','tonne_scale'):'Pre',
       ('lhcb','velopix'):'Pre',('lhcb','scifi'):'Cont.',('lhcb','software_trigger'):'Pre',('sno','successor_named'):'Post',
       ('sno','scintillator_fill'):'Post',('sno','tellurium'):'Post',('aligo','fd_squeezing'):'Pre',('aligo','filter_cavity'):'Pre',
       ('aligo','successor_named'):'Cont.'}
items = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
assert len(items) == 26 and all(x in CLS for x in items)
MODELS = [('claude-sonnet-4-5-20250929', 'Sonnet 4.5'), ('claude-sonnet-4-6', 'Sonnet 4.6'),
          ('qwen2.5:32b-instruct', 'Qwen2.5 32B'), ('qwen2.5:72b-instruct', 'Qwen2.5 72B')]
def rate(p, i, c, m):
    k = n[(p, c, m)]; return 100 * hits[(p, i, c, m)] / k if k else np.nan
items.sort(key=lambda x: -sum(rate(x[0], x[1], 'A', m) for m, _ in MODELS[:2]))
fig, axes = plt.subplots(1, 4, figsize=(12, 8.2), sharey=True)
for ax, (m, title) in zip(axes, MODELS):
    M = np.array([[rate(p, i, c, m) for c in 'ABCD'] for p, i in items])
    ax.imshow(np.nan_to_num(M, nan=0), cmap='Greys', vmin=0, vmax=100, aspect='auto')
    ax.set_xticks(range(4)); ax.set_xticklabels(list('ABCD')); ax.set_title(title, fontsize=10)
    for y in range(len(items)):
        for x in range(4):
            v = M[y, x]
            if np.isnan(v):
                ax.add_patch(plt.Rectangle((x - .5, y - .5), 1, 1, color='white')); ax.text(x, y, '–', ha='center', va='center', fontsize=7)
            else:
                ax.text(x, y, f"{v:.0f}", ha='center', va='center', fontsize=6.5, color='white' if v > 55 else 'black')
lab = {'successor_named': 'successor named'}
axes[0].set_yticks(range(len(items)))
axes[0].set_yticklabels([f"{p}: {lab.get(i, i.replace('_', ' '))}  [{CLS[(p, i)]}]" for p, i in items], fontsize=7)
for tl, (p, i) in zip(axes[0].get_yticklabels(), items):
    if CLS[(p, i)] == 'Post': tl.set_fontweight('bold')
plt.tight_layout(); plt.savefig(OUT, bbox_inches='tight'); plt.close()
print('wrote', OUT)
