#!/usr/bin/env python3
"""False-negative check of the 21 significant A-D cells (11 positive, 10 negative; exploratory).

For each cell, applies the frozen key and a broader concept expression to every condition-A, -B,
and -D response, reports both rates with a Newcombe interval on the broad A-D difference, and
samples the responses that only the broader expression matches, for manual reading.
Frozen scores are unchanged.
Usage: python check_ad_cells.py <repo_root> <out_md>
"""
import json, math, os, random, re, sys
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

POS = [('darkside', 'successor_named', 'S4.5'), ('darkside', 'successor_named', 'S4.6'), ('xenon1t', 'radon_column', 'S4.6'),
       ('lux', 'successor_named', 'S4.5'), ('lhcb', 'velopix', 'S4.5'), ('lhcb', 'velopix', 'S4.6'), ('lhcb', 'scifi', 'S4.5'),
       ('lhcb', 'scifi', 'S4.6'), ('lhcb', 'software_trigger', 'S4.5'), ('sno', 'successor_named', 'S4.5'),
       ('sno', 'scintillator_fill', 'S4.5')]
NEG = [('darkside', 'veto_upgrade_gd', 'S4.5'), ('xenon1t', 'neutron_veto', 'S4.5'), ('lux', 'successor_named', 'S4.6'),
       ('lux', 'outer_detector', 'S4.6'), ('icecube', 'degg', 'S4.5'), ('icecube', 'degg', 'S4.6'),
       ('gerda', 'successor_named', 'S4.6'), ('gerda', 'inverted_coaxial', 'S4.6'), ('exo200', 'tonne_scale', 'S4.6'),
       ('lhcb', 'software_trigger', 'S4.6')]
BROAD = {
    'successor_named@darkside': r'darkside[\s-]*20\s?k|\bds[\s-]*20\s?k\b|darkside[\s-]*(20|twenty)[\s-]*(tonne|ton)',
    'radon_column': r'(radon|\brn\b|222\s?rn|²²²rn)[^.\n]{0,40}(distill\w*|column)|(distill\w*|column)[^.\n]{0,40}(radon|\brn\b|222\s?rn|²²²rn)',
    'velopix': r'velopix|velo[\s-]pix\b',
    'scifi': r'scifi|sci[\s-]fi\b|scintillating[\s-]fib(re|er)',
    'successor_named@sno': r'sno\s?\+|sno[\s-]?plus',
    'scintillator_fill': r'linear alkyl[\s-]?benzene|\blab\b[^.\n]{0,30}(scintillat|ppo)|(fill|replac|convert|refill)\w*[^.\n]{0,60}(liquid|organic) scintillat|(liquid|organic) scintillat\w*[^.\n]{0,40}(fill|in place of|instead of)',
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
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h
def newcombe(a, b):
    p1, l1, u1 = wilson(*a); p2, l2, u2 = wilson(*b); d = p1 - p2
    return 100 * d, 100 * (d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)), 100 * (d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))

rng = random.Random(11)
out = ["# Significant A-D cells: frozen key vs broader concept expression (exploratory)\n",
       "Rates in percent of 50. Broad = frozen key or broader concept expression. Interval: Newcombe 95% on the broad A-D difference.\n",
       "| sign | item | model | A frozen | A broad | B frozen | B broad | D frozen | D broad | A-D frozen | A-D broad [95% CI] |",
       "|---|---|---|---|---|---|---|---|---|---|---|"]
snips = []
OTHER = [('xenon1t', 'radon_column', 'S4.5')]  # not significant in A-D; its A-to-B rise is quoted in the cutoff section
for sign, lst in (('+', POS), ('-', NEG), ('n.s.', OTHER)):
    for pn, it, m in lst:
        key = keys[pn]['items'][it]['regex']; br = BROAD.get(f'{it}@{pn}', BROAD.get(it))
        row, kb = {}, {}
        for c in 'ABD':
            rs = cells[(pn, c, m)]
            f = [bool(re.search(key, x, re.I)) for x in rs]; b = [fi or bool(re.search(br, x, re.I)) for fi, x in zip(f, rs)]
            row[c] = (100 * sum(f) / len(rs), 100 * sum(b) / len(rs)); kb[c] = (sum(b), len(rs))
            if c == 'B': continue
            extra = [x for fi, bi, x in zip(f, b, rs) if bi and not fi]
            snips.append(f"\n## {pn}.{it} {m} condition {c}: {len(extra)} responses matched only by the broader expression")
            for x in rng.sample(extra, min(5, len(extra))):
                s = re.search(br, x, re.I).start()
                snips.append('- ...' + x[max(0, s - 220):s + 220].replace('\n', ' ') + '...')
        d, lo, hi = newcombe(kb['A'], kb['D'])
        out.append(f"| {sign} | {pn}.{it} | {m} | {row['A'][0]:.0f} | {row['A'][1]:.0f} | {row['B'][0]:.0f} | {row['B'][1]:.0f} | "
                   f"{row['D'][0]:.0f} | {row['D'][1]:.0f} | {row['A'][0] - row['D'][0]:+.0f} | {d:+.0f} [{lo:+.0f}, {hi:+.0f}] |")
open(OUT, 'w', encoding='utf-8').write('\n'.join(out + ['\n# Sample of responses matched only by the broader expression'] + snips) + '\n')
print('\n'.join(out))
