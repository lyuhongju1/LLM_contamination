#!/usr/bin/env python3
"""Amendment 9 (d): concept-level judging of every response with a frozen rubric.
Usage: python run_judge.py <repo_root> [--dry-run] [--pilot N]
Judges the final answer text of every final record in data/raw_v2, raw_dprime, raw_local, raw_paraphrase,
raw_models, raw_amend9. One judge call per response covers all five items of its pair (3 adopted + 2 distractors).
Output: data/judge.jsonl with one row per response: {source, record key, items: {item: {concept, named}}}."""
import argparse, json, os, sys, time, urllib.request, urllib.error, hashlib
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ANTHROPIC_API_KEY") or open(os.path.join(HERE, '..', '.anthropic_key')).read().strip()
API = "https://api.anthropic.com/v1"
HDRS = {"Content-Type": "application/json", "x-api-key": KEY, "anthropic-version": "2023-06-01"}
JUDGE = "claude-opus-5-5"
SOURCES = ["raw_v2.jsonl", "raw_dprime.jsonl", "raw_local.jsonl", "raw_paraphrase.jsonl", "raw_models.jsonl", "raw_amend9.jsonl"]

SYSTEM = (
 "You are scoring responses in a study of what language models propose when asked to upgrade a physics detector. "
 "For each listed item, decide two things about the RESPONSE ONLY.\n"
 "concept: true if the response proposes or recommends the substance described in the item's concept definition as an "
 "upgrade, in any wording. False if the item is absent, mentioned only as existing equipment or background, mentioned "
 "only to be rejected or ruled out, or only alluded to so vaguely that a physicist could not tell it is meant.\n"
 "named: true only if concept is true AND the response uses the specific name given for the item (case and minor "
 "spelling variants allowed).\n"
 "Do not use your own knowledge of what the collaboration actually did; judge only what the response says. "
 "Return only a JSON object mapping each item key to {\"concept\": true|false, \"named\": true|false}, with no other text.")

def user_msg(pair_name, pair, response):
    lines = [f"Instrument: {pair['instrument']}", "", "Items:"]
    for k, v in pair["items"].items():
        lines.append(f"- {k}: concept = {v['concept']}; named = {v['named']}")
    lines += ["", "<response>", response, "</response>"]
    return "\n".join(lines)

def api(method, path, body=None, raw_url=None):
    url = raw_url or (API + path)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HDRS, method=method)
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                payload = r.read()
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:1500]
            if e.code in (429, 500, 502, 503, 529) and attempt < 7:
                time.sleep(30 * (attempt + 1)); continue
            print(f"API {e.code} on {method} {url}\n{msg}", file=sys.stderr, flush=True); raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt < 7:
                time.sleep(30 * (attempt + 1)); continue
            raise
    if raw_url:
        return [json.loads(l) for l in payload.decode().splitlines() if l.strip()]
    return json.loads(payload)

def final_records(root):
    out = []
    for src in SOURCES:
        p = os.path.join(root, "data", src)
        if not os.path.exists(p): continue
        best = {}
        for l in open(p, encoding="utf-8"):
            r = json.loads(l)
            k = (r.get("template", "O"), r["pair"], r["condition"], r["model"], r["sample"])
            if k not in best or r.get("max_tokens", 0) > best[k].get("max_tokens", 0): best[k] = r
        for k, r in best.items():
            rid = hashlib.sha256(json.dumps([src, *k]).encode()).hexdigest()[:20]
            out.append((rid, src, k, r["response"]))
    return out

def parse(text, keys):
    t = text.strip()
    if t.startswith("```"): t = t.strip("`").split("\n", 1)[1] if "\n" in t else t
    i, j = t.find("{"), t.rfind("}")
    d = json.loads(t[i:j + 1])
    return {k: {"concept": bool(d[k]["concept"]), "named": bool(d[k]["concept"]) and bool(d[k]["named"])} for k in keys}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pilot", type=int, default=0)
    a = ap.parse_args()
    rub = json.load(open(os.path.join(HERE, "..", "judge_rubric.json") if not os.path.exists(os.path.join(HERE, "judge_rubric.json")) else os.path.join(HERE, "judge_rubric.json"), encoding="utf-8"))["pairs"]
    recs = final_records(a.root)
    print(f"{len(recs)} responses to judge: {Counter(r[1] for r in recs)}", flush=True)
    if a.pilot: recs = recs[::max(1, len(recs) // a.pilot)][:a.pilot]
    if a.dry_run:
        rid, src, k, resp = recs[0]; print(SYSTEM + "\n\n" + user_msg(k[1], rub[k[1]], resp[:400])); return
    tag = f"pilot{a.pilot}" if a.pilot else "full"
    state_path = os.path.join(a.root, "data", f"judge_state_{tag}.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {"batches": []}
    reqs = [{"custom_id": rid, "params": {"model": JUDGE, "max_tokens": 2000,
             "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": user_msg(k[1], rub[k[1]], resp)}]}} for rid, src, k, resp in recs]
    for n, s in enumerate(range(0, len(reqs), 1000)):
        if n < len(state["batches"]): continue
        b = api("POST", "/messages/batches", {"requests": reqs[s:s + 1000]})
        state["batches"].append(b["id"]); json.dump(state, open(state_path, "w"))
        print(f"submitted {b['id']} ({n+1}/{(len(reqs)+999)//1000})", flush=True)
    meta = {rid: (src, k) for rid, src, k, _ in recs}
    outp = os.path.join(a.root, "data", f"judge_{tag}.jsonl")
    have = set()
    if os.path.exists(outp):
        for l in open(outp, encoding="utf-8"): have.add(json.loads(l)["rid"])
    bad = Counter()
    with open(outp, "a", encoding="utf-8") as out:
        for bid in state["batches"]:
            while True:
                b = api("GET", f"/messages/batches/{bid}")
                if b["processing_status"] == "ended": break
                time.sleep(60)
            for row in api("GET", "", raw_url=b["results_url"]):
                rid = row["custom_id"]
                if rid in have: continue
                src, k = meta[rid]
                if row["result"]["type"] != "succeeded": bad["api"] += 1; continue
                msg = row["result"]["message"]; text = "".join(x.get("text", "") for x in msg["content"] if x.get("type") == "text")
                try: items = parse(text, list(rub[k[1]]["items"]))
                except Exception: bad["parse"] += 1; items = None
                out.write(json.dumps({"rid": rid, "source": src, "template": k[0], "pair": k[1], "condition": k[2],
                    "model": k[3], "sample": k[4], "items": items, "raw": None if items else text,
                    "usage": msg.get("usage")}) + "\n"); have.add(rid)
            out.flush(); print(f"  {bid} harvested", flush=True)
    print("failures:", dict(bad), flush=True)

if __name__ == "__main__":
    main()
