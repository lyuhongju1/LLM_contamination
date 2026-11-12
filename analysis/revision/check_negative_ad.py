#!/usr/bin/env python3
"""False-negative check of the ten significantly negative A-D cells (exploratory).

For each cell, applies the frozen key and a broader concept expression to every condition-A and
condition-D response, reports both rates, and samples the responses that only the broader
expression matches, for manual reading. Frozen scores are unchanged.
Usage: python check_negative_ad.py <repo_root> <out_md>
"""
import json, os, random, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
ROOT, OUT = sys.argv[1], sys.argv[2]
SHORT = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6'}
best = {}
for l in open(os.path.join(ROOT, 'data', 'raw_v2.jsonl'), encoding='utf-8'):
    r = json.loads(l)
    k = (r['pair'], r['condition'], r['model'], r['sample'])
    if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
cells = defaultdict(list)
for (pn, c, m, s), r in best.items(): cells[(pn, c, SHORT.get(m, m))].append(r['response'])
keys = {p['name']: p for p in json.load(open(os.path.join(ROOT, 'keys.json'), encoding='utf-8'))['pairs']}

NEG = [('darkside', 'veto_upgrade_gd', 'S4.5'), ('xenon1t', 'neutron_veto', 'S4.5'), ('lux', 'successor_named', 'S4.6'),
       ('lux', 'outer_detector', 'S4.6'), ('icecube', 'degg', 'S4.5'), ('icecube', 'degg', 'S4.6'),
       ('gerda', 'successor_named', 'S4.6'), ('gerda', 'inverted_coaxial', 'S4.6'), ('exo200', 'tonne_scale', 'S4.6'),
       ('lhcb', 'software_trigger', 'S4.6')]
BROAD = {
    'veto_upgrade_gd': r'gadolin|\bgd\b|gd[\s-]?(loaded|doped)',
    'neutron_veto': r'neutron[\s-]?(veto|tagging|tagger|tag\b|capture detector)|gd[\s-]?(loaded|doped)|gadolin',
    'successor_named@lux': r'\blz\b|lux[\s-]?zeplin|\blux[\s-]?lz\b',
    'outer_detector': r'outer detector|(?:gd|gadolin\w*)[^.\n]{0,60}(?:scintillat\w*|\blab\b|alkylbenzene)[^\n]{0,200}veto|veto[^\n]{0,200}(?:gd|gadolin\w*)[^.\n]{0,60}(?:scintillat\w*|\blab\b|alkylbenzene)|outer[^.\n]{0,30}scintillator[^.\n]{0,30}veto|scintillator[^.\n]{0,40}outer veto',
    'degg': r'd[\s-]?egg|dual[\s-]?pmt (module|dom|configuration|design|optical)|(two|2)[\s-]pmts? per (module|dom)|(one|an?) (upward|downward)[\s-](facing|looking)[^.\n]{0,80}(plus|and|with) (one|an?|a second) (upward|downward)',
    'successor_named@gerda': r'\blegend\b',
    'inverted_coaxial': r'inverted[\s-]?coax|\bicpc|\bic[\s-]?pc\b',
    'tonne_scale': r'(tonne|ton)[\s-]scale|multi[\s-]?(tonne|ton)\b|\b[1-9]\d?[\s-]?(tonne|ton|t)\b[^.\n]{0,40}(xenon|xe\b|136|enriched|detector|lxe)',
    'software_trigger': r'(software|full)[\s-]?only trigger|trigger[\s-]?less|(remov|eliminat|drop|abolish|bypass)\w*[^.\n]{0,40}(hardware|l0|level[\s-]?0)[^.\n]{0,20}trigger|full[\s-]?software trigger|(fully|purely|entirely)[\s-]software[\s-](based )?trigger',
}
rng = random.Random(11)
out = ["# Negative A-D cells: frozen key vs broader concept expression (exploratory)\n",
       "| item | model | A frozen | A broad | D frozen | D broad | A-D frozen | A-D broad |", "|---|---|---|---|---|---|---|---|"]
snips = []
for pn, it, m in NEG:
    key = keys[pn]['items'][it]['regex']; br = BROAD.get(f'{it}@{pn}', BROAD.get(it))
    row = {}
    for c in 'AD':
        rs = cells[(pn, c, m)]
        f = [bool(re.search(key, x, re.I)) for x in rs]; b = [fi or bool(re.search(br, x, re.I)) for fi, x in zip(f, rs)]
        row[c] = (100 * sum(f) / len(rs), 100 * sum(b) / len(rs))
        extra = [x for fi, bi, x in zip(f, b, rs) if bi and not fi]
        snips.append(f"\n## {pn}.{it} {m} condition {c}: {len(extra)} responses matched only by the broader expression")
        for x in rng.sample(extra, min(5, len(extra))):
            mm = re.search(br, x, re.I); s = mm.start()
            snips.append('- ...' + x[max(0, s - 220):s + 220].replace('\n', ' ') + '...')
    out.append(f"| {pn}.{it} | {m} | {row['A'][0]:.0f} | {row['A'][1]:.0f} | {row['D'][0]:.0f} | {row['D'][1]:.0f} | "
               f"{row['A'][0] - row['D'][0]:+.0f} | {row['A'][1] - row['D'][1]:+.0f} |")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out + ['\n# Sample of responses matched only by the broader expression'] + snips) + '\n')
print('\n'.join(out))
