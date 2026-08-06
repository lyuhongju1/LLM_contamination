#!/usr/bin/env python3
"""Amendment 6 D-prime sweep: spec-stripped one-line descriptions, N=20,
both Claude models, one small batch each. Run from the repo root:
  $env:ANTHROPIC_API_KEY="sk-ant-..."
  python code/run_probe_dprime.py"""
import hashlib, json, os, time, urllib.request

API = "https://api.anthropic.com/v1"
HDRS = lambda: {"Content-Type": "application/json",
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01"}
TMPL = ("Propose specific hardware design upgrades that would most improve "
        "the primary physics performance of the following instrument: {G}. "
        "Be concrete about technologies and components.")
MODELS = ["claude-sonnet-4-5-20250929", "claude-sonnet-4-6"]

def api(method, path, body=None, raw=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(raw or API+path, data=data, headers=HDRS(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=1800) as r: payload = r.read()
    except urllib.error.HTTPError as e:
        print("API", e.code, e.read().decode(errors="replace")[:800]); raise
    try: return json.loads(payload)
    except json.JSONDecodeError:
        return [json.loads(l) for l in payload.decode().splitlines() if l.strip()]

descs = json.load(open("dprime_descs.json", encoding="utf-8"))
os.makedirs("results", exist_ok=True); os.makedirs("prompts", exist_ok=True)
prompts = {}
for pn, g in descs.items():
    pr = TMPL.replace("{G}", g)
    h = hashlib.sha256(pr.encode()).hexdigest()[:16]
    prompts[pn] = (pr, h)
    open(f"prompts/{pn}_Dp_{h}.txt", "w", encoding="utf-8").write(pr)
state_path = "results/batch_state_dprime.json"
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
for model in MODELS:
    if model in state: continue
    reqs = [{"custom_id": f"{pn}__Dp__{i}__mt4000",
             "params": {"model": model, "max_tokens": 4000, "temperature": 1.0,
                        "messages": [{"role": "user", "content": prompts[pn][0]}]}}
            for pn in descs for i in range(20)]
    b = api("POST", "/messages/batches", {"requests": reqs})
    state[model] = b["id"]; json.dump(state, open(state_path, "w"))
    print(f"submitted {b['id']} ({model}, {len(reqs)} requests)")
with open("results/raw_dprime.jsonl", "a", encoding="utf-8") as out:
    for model, bid in state.items():
        while True:
            b = api("GET", f"/messages/batches/{bid}")
            print(f"  {bid}: {b['processing_status']} {b.get('request_counts')}")
            if b["processing_status"] == "ended": break
            time.sleep(60)
        for row in api("GET", "", raw=b["results_url"]):
            pn, c, i, mt = row["custom_id"].split("__")
            res = row["result"]
            if res["type"] != "succeeded": print("NONSUCCESS", row["custom_id"]); continue
            msg = res["message"]
            out.write(json.dumps({"schema_version": 2, "pair": pn, "condition": "Dp",
                "model": model, "sample": int(i), "max_tokens": 4000,
                "prompt_sha256": prompts[pn][1],
                "response": "".join(bl.get("text","") for bl in msg.get("content",[])),
                "stop_reason": msg.get("stop_reason"), "usage": msg.get("usage"),
                "latency": None, "batch_id": bid, "ts": time.time()}) + "\n")
        out.flush()
from collections import Counter
recs = [json.loads(l) for l in open("results/raw_dprime.jsonl", encoding="utf-8")]
print("stop_reason census:", Counter(r["stop_reason"] for r in recs))
print("done: results/raw_dprime.jsonl")
