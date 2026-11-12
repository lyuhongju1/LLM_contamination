#!/usr/bin/env python3
"""Third-round reanalysis (exploratory, not pre-registered).

1. Nine-model table columns: saturated counts over 26 items, 24 independent units, and the
   8 post-baseline items; median response length (output tokens minus reasoning tokens,
   conditions A-D, original template).
2. VeloPix in condition A under every template (floor check for the length control).
3. Items low (<=10%) in every cell, per model.
4. False-negative check on the low cells of the Sonnet 4 models: broader concept expressions
   for the two items the frozen keys undercount, with rates under both, and a sample of
   broad-pattern matches among responses the frozen key scored as misses (for reading).
5. Sensitivity of the low-item count to the threshold, and the binomial probability that an
   item with a given true rate clears the bar in every cell.

The frozen regex scores are not changed by anything here.
Usage: python score_round3.py <repo_root> <out_md> <snippets_md>
"""
import ast, json, os, random, re, statistics as st, sys
from collections import defaultdict
from math import comb
sys.stdout.reconfigure(encoding='utf-8')
ROOT, OUT, SNIP = sys.argv[1], sys.argv[2], sys.argv[3]
P = lambda *a: os.path.join(ROOT, *a)
out = []; w = lambda s="": out.append(s)

SHORT = {'claude-sonnet-4-5-20250929': 'S4.5', 'claude-sonnet-4-6': 'S4.6', 'claude-sonnet-5': 'S5',
         'claude-haiku-4-5-20251001': 'H4.5', 'claude-opus-4-5-20251101': 'O4.5',
         'claude-haiku-5-5': 'H5.5', 'claude-sonnet-5-5': 'S5.5', 'claude-opus-5-5': 'O5.5', 'claude-fable-5-1': 'F5.1'}
ORDER = ['H4.5', 'S4.5', 'O4.5', 'S4.6', 'S5', 'H5.5', 'S5.5', 'O5.5', 'F5.1']

# ---- load (final record per sample = largest max_tokens, Amendment 3 rule)
cells = defaultdict(list); toks = defaultdict(list); templates = set()
def load(fn, skip=()):
    best = {}
    for l in open(P('data', fn), encoding='utf-8'):
        r = json.loads(l); t = r.get('template', 'O'); templates.add(t)
        if t in skip: continue
        k = (t, r['pair'], r['condition'], r['model'], r['sample'])
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    for (t, pn, c, m, s), r in best.items():
        m = SHORT.get(m, m); cells[(t, pn, c, m)].append(r['response'])
        if t == 'O' and c in 'ABCD':
            u = r.get('usage'); u = ast.literal_eval(u) if isinstance(u, str) else (u or {})
            toks[m].append(u['output_tokens'] - (r.get('thinking_tokens') or 0))
load('raw_v2.jsonl'); load('raw_dprime.jsonl'); load('raw_models.jsonl'); load('raw_amend10.jsonl')
load('raw_paraphrase.jsonl', skip=('O', 'T')); load('raw_amend9_ab.jsonl', skip=('O',))

cfg = json.load(open(P('keys.json'), encoding='utf-8')); pairs = {p['name']: p for p in cfg['pairs']}
leaked = set()
for pn, p in pairs.items():
    text = open(P(p['paper_txt']), encoding='utf-8', errors='ignore').read()
    for item, spec in p['items'].items():
        if re.search(spec['regex'], text, re.I): leaked.add((pn, item))
ITEMS = [(p, i) for p in pairs for i in pairs[p]['items'] if (p, i) not in leaked]
assert len(ITEMS) == 26
POST = [('darkside', 'veto_upgrade_gd'), ('lux', 'xenon_skin'), ('gerda', 'successor_named'), ('gerda', 'inverted_coaxial'),
        ('exo200', 'sipm_adoption'), ('sno', 'successor_named'), ('sno', 'scintillator_fill'), ('sno', 'tellurium')]
CONCEPT = {  # broader expressions for items the frozen keys undercount (exploratory; frozen keys stay primary)
    ('sno', 'tellurium'): r'tellur|(?<![a-z0-9])(?:\^?\{?130\}?|¹³⁰|nat)?\s?te(?![a-z])(?:[\s-]?(?:load|diol|dop)|\s*\(|\))|(?:load|dop|dissolv)\w*[^.\n]{0,40}(?<![a-z])(?:¹³⁰|130)?te(?![a-z])|lab\s?\+\s?te\b',
    ('lux', 'outer_detector'): r'(?:gd|gadolin\w*)[^.\n]{0,60}(?:scintillat\w*|\blab\b|alkylbenzene)[^\n]{0,200}veto|(?:veto)[^\n]{0,200}(?:gd|gadolin\w*)[^.\n]{0,60}(?:scintillat\w*|\blab\b|alkylbenzene)|outer[^.\n]{0,30}scintillator[^.\n]{0,30}veto|scintillator[^.\n]{0,40}outer veto',
}
BROAD = {  # wide net used only to pull candidate misses for manual reading
    ('lux', 'outer_detector'): r'(scintillat\w*|gadolin\w*|\bgd\b).{0,80}veto|veto.{0,80}(scintillat\w*|gadolin\w*|\bgd\b)|active veto|anti-?coincidence',
    ('sno', 'tellurium'): r'tellur|\bte\b|130te|double[\s-]beta|0\s?ν\s?ββ|0nubb|neutrinoless|isotope load|load\w* (the )?scintillator with',
}
KNOWN_FAILURE = {('protodune', 'coverage_increase')}  # adjudicated at 19/20 against a frozen 0%
SPEC12 = [('O', c) for c in ('A', 'C', 'D', 'Dp')] + [(t, c) for t in ('P1', 'P2', 'P3', 'P4') for c in 'AD']

def hits(t, pn, item, c, m, concept=False):
    rx = pairs[pn]['items'][item]['regex']; cx = CONCEPT.get((pn, item)) if concept else None
    return [bool(re.search(rx, x, re.I) or (cx and re.search(cx, x, re.I))) for x in cells.get((t, pn, c, m), [])]
def rate(t, pn, item, c, m, concept=False):
    h = hits(t, pn, item, c, m, concept); return 100 * sum(h) / len(h) if h else None
def units(c, m):
    u = {k: rate('O', *k, c, m) for k in ITEMS
         if k not in [('darkside', 'sipm_adoption'), ('exo200', 'sipm_adoption'), ('aligo', 'fd_squeezing'), ('aligo', 'filter_cavity')]}
    u['sipm'] = (rate('O', 'darkside', 'sipm_adoption', c, m) + rate('O', 'exo200', 'sipm_adoption', c, m)) / 2
    a, b = hits('O', 'aligo', 'fd_squeezing', c, m), hits('O', 'aligo', 'filter_cavity', c, m)
    u['squeeze'] = 100 * sum(x or y for x, y in zip(a, b)) / len(a)
    assert len(u) == 24; return u

w("# Round-3 reanalysis (exploratory)\n")
w("Frozen regex scores are unchanged by everything below.\n")
# ---- 1
w("## 1. Nine models, original template\n")
w("Counts of items at >=90%. Units: 24 independent units (SiPM items averaged; squeezing and filter cavity scored as one). "
  "Post: of the 8 post-baseline items (number of pairs in parentheses). Length: median output tokens minus reasoning tokens, conditions A-D.\n")
w("| model | A >=90 (26) | A median | D >=90 (26) | D units >=90 (24) | D post >=90 (8) | D median | length |")
w("|---|---|---|---|---|---|---|---|")
for m in ORDER:
    rA = {k: rate('O', *k, 'A', m) for k in ITEMS}; rD = {k: rate('O', *k, 'D', m) for k in ITEMS}
    ps = [k for k in POST if rD[k] >= 90]
    w(f"| {m} | {sum(v >= 90 for v in rA.values())} | {st.median(rA.values()):.0f} | {sum(v >= 90 for v in rD.values())} | "
      f"{sum(v >= 90 for v in units('D', m).values())} | {len(ps)} ({len({k[0] for k in ps})}) | {st.median(rD.values()):.0f} | {st.median(toks[m]):.0f} |")
w()
# ---- 2
w("## 2. VeloPix, condition A, by template\n")
for m in ('S4.5', 'S4.6'):
    w(f"- {m}: " + ", ".join(f"{t} {rate(t, 'lhcb', 'velopix', 'A', m):.0f}" for t in sorted(templates)
                             if rate(t, 'lhcb', 'velopix', 'A', m) is not None))
w("\nK5 and K15 share the P1 opening; on Sonnet 4.5 VeloPix is at the floor under that opening, so breadth sensitivity cannot be tested there.\n")
# ---- 3
w("## 3. Items <=10% in every cell (frozen keys)\n")
w("Sonnet 4 models: conditions A, C, D, D' (original) and A, D under P1-P4 (12 cells; condition B excluded because its instruction suppresses items by design). Other models: A and D, original template only.\n")
for m in ORDER:
    spec = SPEC12 if m in ('S4.5', 'S4.6') else [('O', 'A'), ('O', 'D')]
    low = [k for k in ITEMS if all(rate(t, *k, c, m) is not None and rate(t, *k, c, m) <= 10 for t, c in spec)]
    w(f"- {m}: {len(low)}: " + ", ".join('.'.join(k) for k in low))
w()
# ---- 4
w("## 4. False-negative check on the Sonnet 4 low cells\n")
w("Rates per cell under the frozen key -> frozen key or broader concept expression.\n")
for k in CONCEPT:
    for m in ('S4.5', 'S4.6'):
        w(f"- {'.'.join(k)} {m}: " + " ".join(f"{t}/{c} {rate(t, *k, c, m):.0f}->{rate(t, *k, c, m, True):.0f}" for t, c in SPEC12))
w(f"\nProtoDUNE coverage increase is the known regex failure (adjudicated 19 of 20). Broad-pattern candidates among scored misses are listed in {os.path.basename(SNIP)} for reading.\n")
rng = random.Random(7); snip = ["# Broad-pattern matches among responses the frozen key scored as misses (sample for manual reading)\n"]
for k, broad in BROAD.items():
    key = pairs[k[0]]['items'][k[1]]['regex']
    for m in ('S4.5', 'S4.6'):
        n = miss = 0; cand = []
        for t, c in SPEC12:
            for x in cells.get((t, k[0], c, m), []):
                n += 1
                if re.search(key, x, re.I): continue
                miss += 1; mm = re.search(broad, x, re.I)
                if mm: s = mm.start(); cand.append(f"[{t}/{c}] ..." + x[max(0, s - 200):s + 250].replace('\n', ' ') + "...")
        snip.append(f"\n## {'.'.join(k)} {m}: {n} responses, {miss} scored miss, {len(cand)} broad matches\n")
        snip += ['- ' + s for s in rng.sample(cand, min(12, len(cand)))]
open(SNIP, 'w', encoding='utf-8').write('\n'.join(snip) + '\n')
# ---- 5
w("## 5. Threshold sensitivity of the low-item count (Sonnet 4 models, 12 cells)\n")
w("ProtoDUNE coverage increase excluded (known regex failure).\n")
w("| model | expression | max<=10 | max<=15 | max<=25 | pooled<=5 | pooled<=10 | pooled<=15 |"); w("|---|---|---|---|---|---|---|---|")
detail = []
for m in ('S4.5', 'S4.6'):
    for concept in (False, True):
        stt = {}
        for k in ITEMS:
            if k in KNOWN_FAILURE: continue
            per, allh = [], []
            for t, c in SPEC12:
                h = hits(t, *k, c, m, concept); per.append(100 * sum(h) / len(h)); allh += h
            stt[k] = (max(per), 100 * sum(allh) / len(allh))
        crit = [lambda s: s[0] <= 10, lambda s: s[0] <= 15, lambda s: s[0] <= 25, lambda s: s[1] <= 5, lambda s: s[1] <= 10, lambda s: s[1] <= 15]
        w(f"| {m} | {'concept' if concept else 'frozen'} | " + " | ".join(str(sum(f(s) for s in stt.values())) for f in crit) + " |")
        detail.append(f"- {m} {'concept' if concept else 'frozen'}: " + "; ".join(
            f"{'.'.join(k)} max {s[0]:.0f} pooled {s[1]:.1f}" for k, s in stt.items() if s[1] <= 15))
w(); w("Items with pooled rate <=15 (max over cells, pooled rate):\n"); out.extend(detail); w()
def cdf(k, n, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))
w("Probability that an item with true rate p in every cell clears the bar in all 12 cells (11 cells N=50, D' N=20):\n")
for p in (0.03, 0.05):
    w(f"- p={p}: " + ", ".join(f"bar {b}%: {cdf(int(b * 50 / 100), 50, p)**11 * cdf(int(b * 20 / 100), 20, p):.2f}" for b in (10, 15)))
open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('wrote', OUT, SNIP)
