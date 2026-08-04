#!/usr/bin/env python3
"""Amendment 4 distractor scoring + leakage audit. Run from the repo root.
Usage: python code/score_distractors.py"""
import json, re, os
from collections import defaultdict
recs = [json.loads(l) for l in open('data/raw_v2.jsonl', encoding='utf-8')]
final = {}
for r in recs:
    k = (r['pair'], r['condition'], r['model'], r['sample'])
    if k not in final or r['max_tokens'] > final[k]['max_tokens']: final[k] = r
recs = list(final.values())
keys = json.load(open('keys.json', encoding='utf-8'))
dk = json.load(open('distractor_keys.json', encoding='utf-8'))['distractors']
pairs = {p['name']: p for p in keys['pairs']}
print("=== distractor leakage audit ===")
for pn, items in dk.items():
    p = pairs[pn]
    if not os.path.exists(p['paper_txt']):
        print(f"  {pn}: corpus file missing, audit pending"); continue
    text = open(p['paper_txt'], encoding='utf-8', errors='ignore').read()
    for item, rx in items.items():
        hits = re.findall(rx, text, re.I)
        print(f"  {pn}.{item}: {'LEAKED ('+str(len(hits))+'x)' if hits else 'clean'}")
print("\n=== distractor hit rates by condition (both models pooled) ===")
tab = defaultdict(lambda: [0,0])
for r in recs:
    for item, rx in dk[r['pair']].items():
        tab[(r['pair'], item, r['condition'])][1] += 1
        tab[(r['pair'], item, r['condition'])][0] += bool(re.search(rx, r['response'], re.I))
for (pn, item, c), v in sorted(tab.items()):
    if c == 'A':
        print(f"  {pn}.{item:20s} A: {100*v[0]/v[1]:5.1f}%")
