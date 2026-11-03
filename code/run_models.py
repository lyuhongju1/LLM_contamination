#!/usr/bin/env python3
"""Amendment 8: original protocol on additional Claude models (generation and scale axes).
Usage: python run_models.py <repo_root> [--dry-run]
Sends the RELEASED rendered prompts in <repo_root>/prompts/ (all 50: A, B, C, D, Dp), after verifying
that each file's sha256 prefix matches the hash in its filename. A-D at N=50, Dp at N=20, temperature
1.0, no thinking, 4000-token cap, one 8000-token resample of capped responses (Amendment 3 rules).
Writes <repo_root>/data/raw_models.jsonl; resumable via data/models_batch_state.json."""
import argparse, hashlib, json, os, sys, time, urllib.request, urllib.error
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ANTHROPIC_API_KEY") or open(os.path.join(HERE, '..', '.anthropic_key')).read().strip()
API = "https://api.anthropic.com/v1"
HDRS = {"Content-Type": "application/json", "x-api-key": KEY, "anthropic-version": "2023-06-01"}
MODELS = ["claude-sonnet-5", "claude-haiku-4-5-20251001", "claude-opus-4-5-20251101"]
N = {"A": 50, "B": 50, "C": 50, "D": 50, "Dp": 20}
SPLIT = "\n</paper>"   # cache breakpoint placed just before this marker; text is unchanged

def api(method, path, body=None, raw_url=None):
    url = raw_url or (API + path)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HDRS, method=method)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                payload = r.read()
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:1500]
            if e.code in (429, 500, 502, 503, 529) and attempt < 5:
                time.sleep(20 * (attempt + 1)); continue
            print(f"API {e.code} on {method} {url}\n{msg}", file=sys.stderr); raise
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return [json.loads(l) for l in payload.decode().splitlines() if l.strip()]

def content(text):
    i = text.find(SPLIT)
    if i < 0:
        return text
    return [{"type": "text", "text": text[:i], "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": text[i:]}]

def submit(model, tasks, prompts, max_tokens):
    reqs = [{"custom_id": f"{p}__{c}__{i}__mt{max_tokens}",
             "params": {"model": model, "max_tokens": max_tokens, "temperature": 1.0,
                        "messages": [{"role": "user", "content": content(prompts[(p, c)][0])}]}}
            for (p, c, i) in tasks]
    ids = []
    for k in range(0, len(reqs), 500):
        b = api("POST", "/messages/batches", {"requests": reqs[k:k + 500]})
        print(f"submitted {b['id']} ({model}, {len(reqs[k:k+500])} requests, max_tokens={max_tokens})", flush=True)
        ids.append(b["id"])
    return ids

def poll(bid):
    while True:
        b = api("GET", f"/messages/batches/{bid}")
        if b["processing_status"] == "ended":
            print(f"  {bid}: ended {b.get('request_counts')}", flush=True); return b
        time.sleep(60)

def harvest(bid, model, prompts, out):
    b = api("GET", f"/messages/batches/{bid}")
    n = 0
    for row in api("GET", "", raw_url=b["results_url"]):
        p, c, i, mt = row["custom_id"].split("__")
        res = row["result"]
        if res["type"] != "succeeded":
            print(f"  NONSUCCESS {row['custom_id']}: {res['type']}"); continue
        msg = res["message"]
        out.write(json.dumps({"schema_version": 3, "pair": p, "condition": c, "model": model,
            "model_returned": msg.get("model"), "sample": int(i), "max_tokens": int(mt[2:]),
            "prompt_sha256": prompts[(p, c)][1],
            "response": "".join(bl.get("text", "") for bl in msg.get("content", []) if bl.get("type") == "text"),
            "stop_reason": msg.get("stop_reason"), "usage": msg.get("usage"),
            "batch_id": bid, "ts": time.time()}) + "\n"); n += 1
    out.flush(); return n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    pdir = os.path.join(a.root, "prompts")
    prompts = {}
    for f in sorted(os.listdir(pdir)):
        pn, c, h = f[:-4].split("_")
        text = open(os.path.join(pdir, f), encoding="utf-8").read()
        assert hashlib.sha256(text.encode()).hexdigest()[:16] == h, f"hash mismatch {f}"
        prompts[(pn, c)] = (text, h)
    assert len(prompts) == 50 and {c for _, c in prompts} == set(N), sorted(prompts)
    tasks = [(p, c, i) for (p, c) in sorted(prompts) for i in range(N[c])]
    print(f"50 released prompts verified by hash; {len(tasks)} tasks per model, {len(tasks)*len(MODELS)} total", flush=True)
    if a.dry_run:
        return
    state_path = os.path.join(a.root, "data", "models_batch_state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    for m in MODELS:
        if m not in state:
            state[m] = submit(m, tasks, prompts, 4000); json.dump(state, open(state_path, "w"))
    raw = os.path.join(a.root, "data", "raw_models.jsonl")
    if not state.get("harvested"):
        with open(raw, "a", encoding="utf-8") as out:
            for m in MODELS:
                for bid in state[m]:
                    poll(bid); print(f"  harvested {harvest(bid, m, prompts, out)}", flush=True)
        state["harvested"] = True; json.dump(state, open(state_path, "w"))
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    capped = [r for r in recs if r["stop_reason"] == "max_tokens" and r["max_tokens"] == 4000]
    print(f"QC: {len(capped)} capped at 4000", flush=True)
    if capped and "qc" not in state:
        by_m = {}
        for r in capped: by_m.setdefault(r["model"], []).append((r["pair"], r["condition"], r["sample"]))
        state["qc"] = {m: submit(m, ts, prompts, 8000) for m, ts in by_m.items()}; json.dump(state, open(state_path, "w"))
    if "qc" in state and not state.get("qc_harvested"):
        with open(raw, "a", encoding="utf-8") as out:
            for m, bids in state["qc"].items():
                for bid in bids: poll(bid); harvest(bid, m, prompts, out)
        state["qc_harvested"] = True; json.dump(state, open(state_path, "w"))
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    print("records:", len(recs), "stop reasons:", Counter((r["model"], r["stop_reason"]) for r in recs))
    print("models returned:", Counter((r["model"], r["model_returned"]) for r in recs))
    u = Counter()
    for r in recs:
        for k, v in (r.get("usage") or {}).items():
            if isinstance(v, int): u[(r["model"], k)] += v
    print("usage totals:", dict(u))

if __name__ == "__main__":
    main()
