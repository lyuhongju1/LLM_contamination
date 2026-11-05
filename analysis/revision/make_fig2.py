#!/usr/bin/env python3
"""Figure 2 for the revision: effect of the cutoff instruction (A -> B) for every item shifting by >= 15 points,
readable labels with dating class, legend, axis label. Also prints the shifts and LEGEND loose counts.
Usage: python make_fig2.py <repo_root> <out_pdf>"""
import json, re, os, sys
from collections import defaultdict
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.stdout.reconfigure(encoding='utf-8')
ROOT, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(ROOT, *a)
best = {}
for l in open(P('data', 'raw_v2.jsonl'), encoding='utf-8'):
    r = json.loads(l); k = (r['pair'], r['condition'], r['model'], r['sample'])
    if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
recs = list(best.values())
cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for it, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, it))
hits = defaultdict(int); n = defaultdict(int); loose = defaultdict(int)
for r in recs:
    n[(r['pair'], r['condition'], r['model'])] += 1
    if r['pair'] == 'gerda' and re.search('legend', r['response'], re.I): loose[(r['condition'], r['model'])] += 1
    for it, spec in pairs[r['pair']]['items'].items():
        if re.search(spec['regex'], r['response'], re.I): hits[(r['pair'], it, r['condition'], r['model'])] += 1
rate = lambda p, i, c, m: 100 * hits[(p, i, c, m)] / n[(p, c, m)]
CLS = {('darkside','successor_named'):'Pre',('darkside','sipm_adoption'):'Pre',('darkside','veto_upgrade_gd'):'Post',
       ('protodune','xarapuca'):'Pre',('protodune','coverage_increase'):'Cont.',('xenon1t','radon_column'):'Cont.',
       ('xenon1t','neutron_veto'):'Cont.',('lux','successor_named'):'Pre',('lux','xenon_skin'):'Post',('lux','outer_detector'):'Pre',
       ('icecube','mdom'):'Pre',('icecube','degg'):'Pre',('gerda','successor_named'):'Post',('gerda','inverted_coaxial'):'Post',
       ('gerda','argon_instrumentation'):'Pre',('exo200','sipm_adoption'):'Post',('exo200','tonne_scale'):'Pre',
       ('lhcb','velopix'):'Pre',('lhcb','scifi'):'Cont.',('lhcb','software_trigger'):'Pre',('sno','successor_named'):'Post',
       ('sno','scintillator_fill'):'Post',('sno','tellurium'):'Post',('aligo','fd_squeezing'):'Pre',('aligo','filter_cavity'):'Pre',
       ('aligo','successor_named'):'Cont.'}
NAME = {'darkside': 'DarkSide', 'protodune': 'ProtoDUNE', 'xenon1t': 'XENON1T', 'lux': 'LUX', 'icecube': 'IceCube',
        'gerda': 'GERDA', 'exo200': 'EXO-200', 'lhcb': 'LHCb', 'sno': 'SNO', 'aligo': 'aLIGO'}
INAME = {'successor_named': 'successor named', 'sipm_adoption': 'SiPM adoption', 'veto_upgrade_gd': 'Gd veto',
         'xarapuca': 'X-ARAPUCA', 'coverage_increase': 'coverage increase', 'radon_column': 'radon column',
         'neutron_veto': 'neutron veto', 'xenon_skin': 'xenon skin', 'outer_detector': 'outer detector', 'mdom': 'multi-PMT mDOM',
         'degg': 'D-Egg', 'inverted_coaxial': 'inverted-coaxial', 'argon_instrumentation': 'argon instrumentation',
         'tonne_scale': 'tonne scale', 'velopix': 'VeloPix', 'scifi': 'SciFi tracker', 'software_trigger': 'software trigger',
         'scintillator_fill': 'scintillator fill', 'tellurium': 'tellurium', 'fd_squeezing': 'freq.-dep. squeezing',
         'filter_cavity': 'filter cavity'}
items = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
MODELS = [('claude-sonnet-4-5-20250929', 'Sonnet 4.5'), ('claude-sonnet-4-6', 'Sonnet 4.6')]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.9))
for ax, (m, title) in zip(axes, MODELS):
    sel = [(p, i) for p, i in items if abs(rate(p, i, 'A', m) - rate(p, i, 'B', m)) >= 15]
    sel.sort(key=lambda x: rate(x[0], x[1], 'B', m) - rate(x[0], x[1], 'A', m))
    print(title, [(f"{p}.{i}", round(rate(p, i, 'A', m)), round(rate(p, i, 'B', m))) for p, i in sel])
    for y, (p, i) in enumerate(sel):
        a, b = rate(p, i, 'A', m), rate(p, i, 'B', m)
        ax.annotate('', xy=(b, y), xytext=(a, y), arrowprops=dict(arrowstyle='->', color='0.55', lw=1.2, shrinkA=4, shrinkB=4))
        ax.scatter([a], [y], s=34, c='black', zorder=3)
        ax.scatter([b], [y], s=34, facecolor='white', edgecolor='black', zorder=3)
    ax.set_yticks(range(len(sel)))
    ax.set_yticklabels([f"{NAME[p]}: {INAME[i]}  [{CLS[(p, i)]}]" for p, i in sel], fontsize=7.5)
    for tl, (p, i) in zip(ax.get_yticklabels(), sel):
        if CLS[(p, i)] == 'Post': tl.set_fontweight('bold')
    ax.set_title(title, fontsize=10); ax.set_xlim(-4, 104); ax.grid(axis='x', color='0.9')
    ax.set_xlabel('Proposal rate (percent of 50 samples)')
    ax.set_ylim(-0.7, len(sel) - 0.3)
fig.legend(handles=[Line2D([], [], marker='o', ls='', color='black', label='A: paper'),
                    Line2D([], [], marker='o', ls='', markerfacecolor='white', markeredgecolor='black', label='B: paper with cutoff instruction')],
           loc='lower center', ncol=2, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.0))
plt.tight_layout(rect=(0, 0.035, 1, 1)); plt.savefig(OUT, bbox_inches='tight'); plt.close()
print('LEGEND any mention (S4.6): A', loose[('A', 'claude-sonnet-4-6')], 'B', loose[('B', 'claude-sonnet-4-6')], 'D', loose[('D', 'claude-sonnet-4-6')])
print('wrote', OUT)
