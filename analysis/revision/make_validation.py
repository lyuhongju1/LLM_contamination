#!/usr/bin/env python3
"""Build the blind judge-validation sheet (Amendment 9 d): 100 judge-positive + 100 judge-negative concept
verdicts, random seed 2026, across all pairs and sources. Writes the sheet (no verdicts) and a hidden key.
Usage: python make_validation.py <repo_root> <sheet_html> <key_json>"""
import json, sys, os, random, hashlib, html

ROOT, SHEET, KEYF = sys.argv[1:4]
rub = json.load(open(os.path.join(ROOT, 'judge_rubric.json'), encoding='utf-8'))['pairs']
resp = {}
for src in ['raw_v2.jsonl', 'raw_dprime.jsonl', 'raw_local.jsonl', 'raw_paraphrase.jsonl', 'raw_models.jsonl']:
    best = {}
    for l in open(os.path.join(ROOT, 'data', src), encoding='utf-8'):
        r = json.loads(l); k = (r.get('template', 'O'), r['pair'], r['condition'], r['model'], r['sample'])
        if k not in best or r.get('max_tokens', 0) > best[k].get('max_tokens', 0): best[k] = r
    for k, r in best.items():
        resp[hashlib.sha256(json.dumps([src, *k]).encode()).hexdigest()[:20]] = r['response']
pos, neg = [], []
for l in open(os.path.join(ROOT, 'data', 'judge_existing.jsonl'), encoding='utf-8'):
    j = json.loads(l)
    if not j['items']: continue
    for it, v in j['items'].items():
        (pos if v['concept'] else neg).append((j['rid'], j['pair'], it, v['concept'], v['named'], j['source']))
rng = random.Random(2026)
sample = rng.sample(pos, 100) + rng.sample(neg, 100)
rng.shuffle(sample)
key = [{"n": i + 1, "rid": s[0], "pair": s[1], "item": s[2], "judge_concept": s[3], "judge_named": s[4], "source": s[5]}
       for i, s in enumerate(sample)]
json.dump(key, open(KEYF, 'w', encoding='utf-8'), indent=1)

cards = []
for i, s in enumerate(sample):
    rid, pn, it = s[0], s[1], s[2]; d = rub[pn]['items'][it]
    cards.append(f"""<section class="card" id="c{i+1}" data-n="{i+1}">
<div class="hdr"><span class="num">{i+1} / 200</span> <span class="inst">{html.escape(rub[pn]['instrument'])}</span></div>
<div class="def"><div><b>Item:</b> {html.escape(it)}</div>
<div><b>Concept</b> (proposes, in any wording): {html.escape(d['concept'])}</div>
<div><b>Named</b> (also uses the name): {html.escape(d['named'])}</div></div>
<details><summary>Show response ({len(resp[rid])} characters)</summary><pre>{html.escape(resp[rid])}</pre></details>
<div class="ans" role="group" aria-label="Verdict for item {i+1}">
<span>Concept:</span><label><input type="radio" name="c{i+1}" value="1"> yes</label><label><input type="radio" name="c{i+1}" value="0"> no</label>
<span class="gap">Named:</span><label><input type="radio" name="m{i+1}" value="1"> yes</label><label><input type="radio" name="m{i+1}" value="0"> no</label>
</div></section>""")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Judge Validation Sheet</title><style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--muted:#6b6b66;--card:#fff;--line:#deded8;--accent:#2f5d8a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--fg:#e8e8e3;--muted:#9a9a93;--card:#1f1f1d;--line:#34342f;--accent:#8ab4e0}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:16px}}
main{{max-width:880px;margin:0 auto}} h1{{font-size:22px;margin:8px 0}} p{{color:var(--muted)}}
.bar{{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:1}}
button{{font:inherit;padding:6px 12px;border:1px solid var(--accent);background:var(--accent);color:var(--bg);border-radius:6px;cursor:pointer}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:14px 0}}
.card.done{{border-left:4px solid var(--accent)}} .hdr{{color:var(--muted);font-size:13px}} .num{{font-weight:600;color:var(--fg)}}
.def{{margin:8px 0}} .def div{{margin:2px 0}} pre{{white-space:pre-wrap;word-wrap:break-word;font:13px/1.45 ui-monospace,monospace;max-height:60vh;overflow:auto;border-top:1px solid var(--line);padding-top:8px}}
.ans{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:8px}} .gap{{margin-left:16px}} label{{cursor:pointer}}
</style></head><body><main>
<h1>Judge validation: 200 judgments</h1>
<p>For each card, read the response and decide whether it <b>proposes</b> the item as an upgrade (concept), and if so whether it uses the item's specific name (named). Mentions of existing equipment, background, or rejected options are "no". If concept is no, named is no. Answers save in this browser automatically; click Download CSV when finished and send the file back.</p>
<div class="bar"><span id="prog">0 / 200 complete</span><button id="dl" type="button">Download CSV</button></div>
{''.join(cards)}
</main><script>
const KEY='judge-validation-v1';let st={{}};
try{{st=JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{st={{}}}}
function save(){{try{{localStorage.setItem(KEY,JSON.stringify(st))}}catch(e){{}}}}
function refresh(){{let d=0;document.querySelectorAll('.card').forEach(c=>{{const n=c.dataset.n;const ok=st['c'+n]!==undefined&&st['m'+n]!==undefined;c.classList.toggle('done',ok);if(ok)d++}});document.getElementById('prog').textContent=d+' / 200 complete'}}
document.querySelectorAll('input[type=radio]').forEach(r=>{{if(st[r.name]===r.value)r.checked=true;r.addEventListener('change',()=>{{st[r.name]=r.value;if(r.name[0]==='c'&&r.value==='0'){{const n=r.name.slice(1);st['m'+n]='0';const m=document.querySelector('input[name=m'+n+'][value="0"]');if(m)m.checked=true}}save();refresh()}})}});
document.getElementById('dl').addEventListener('click',()=>{{let s='n,concept,named\\n';for(let n=1;n<=200;n++)s+=n+','+(st['c'+n]??'')+','+(st['m'+n]??'')+'\\n';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([s],{{type:'text/csv'}}));a.download='judge_validation_labels.csv';a.click()}});
refresh();
</script></body></html>"""
open(SHEET, 'w', encoding='utf-8').write(page)
print('sheet', SHEET, 'key', KEYF, 'pos/neg pool', len(pos), len(neg))
