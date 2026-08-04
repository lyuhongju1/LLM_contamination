#!/usr/bin/env python3
"""Extension sweep via the Anthropic Message Batches API (Amendments 3+5).
Reads results/raw_v2.jsonl, submits ONLY samples not yet recorded up to --n,
appends to the same file with identical schema and QC rules.

  $env:ANTHROPIC_API_KEY="sk-ant-..."
  python run_probe_batch.py --models claude-sonnet-4-5-20250929 claude-sonnet-4-6

Submits one batch per model (all 800 requests each), polls until ended,
downloads results, writes results/raw_v2.jsonl (schema_version 2 with
stop_reason), dumps the 40 rendered prompts to prompts/, then applies the
pre-registered QC rule: any max_tokens-stopped response is resampled ONCE
at max_tokens 8000 via a follow-up batch. Resumable: batch ids are stored
in results/batch_state.json; rerun the same command to continue polling.
"""
import argparse, hashlib, json, os, re, sys, time, urllib.request

API = "https://api.anthropic.com/v1"
HDRS = lambda: {"Content-Type": "application/json",
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01"}

PROMPT_A = ("The following is the text of a published detector paper.\n\n<paper>\n{TEXT}\n</paper>\n\n"
            "Based on this instrument, propose specific hardware design upgrades that would most "
            "improve its primary physics performance. Be concrete about technologies and components.")
CUTOFF = ("Assume your knowledge ends in {YEAR}. Do not use any information about "
          "developments, projects, collaborations, or publications after {YEAR}.\n\n")
PROMPT_D = ("Propose specific hardware design upgrades that would most improve the primary physics "
            "performance of the following instrument: {GENERIC}. Be concrete about technologies and components.")

def redact(text, pats):
    for p in pats: text = re.sub(p, "[REDACTED]", text, flags=re.I)
    return text

def build_prompt(cond, pair):
    text = open(pair["paper_txt"], encoding="utf-8", errors="ignore").read()
    if cond == "A": return PROMPT_A.replace("{TEXT}", text)
    if cond == "B": return CUTOFF.replace("{YEAR}", str(pair["year"])) + PROMPT_A.replace("{TEXT}", text)
    if cond == "C": return PROMPT_A.replace("{TEXT}", redact(text, pair["redact_patterns"]))
    if cond == "D": return PROMPT_D.replace("{GENERIC}", pair["generic_desc"])
    raise ValueError(cond)

def api(method, path, body=None, raw_url=None):
    url = raw_url or (API + path)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HDRS(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            payload = r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:2000]
        print(f"API {e.code} on {method} {url}\n{body}", file=sys.stderr)
        raise
    try:    return json.loads(payload)
    except json.JSONDecodeError:  # results endpoint returns JSONL
        return [json.loads(l) for l in payload.decode().splitlines() if l.strip()]

def submit(model, tasks, prompts, max_tokens):
    reqs = [{"custom_id": f"{p}__{c}__{i}__mt{max_tokens}",
             "params": {"model": model, "max_tokens": max_tokens, "temperature": 1.0,
                        "messages": [{"role": "user", "content": prompts[(p, c)][0]}]}}
            for (p, c, i) in tasks]
    b = api("POST", "/messages/batches", {"requests": reqs})
    print(f"submitted batch {b['id']} ({model}, {len(reqs)} requests, max_tokens={max_tokens})")
    return b["id"]

def poll(bid):
    while True:
        b = api("GET", f"/messages/batches/{bid}")
        st = b["processing_status"]
        c = b.get("request_counts", {})
        print(f"  {bid}: {st} {c}")
        if st == "ended": return b
        time.sleep(60)

def harvest(bid, model, prompts, out, seen):
    b = api("GET", f"/messages/batches/{bid}")
    for row in api("GET", "", raw_url=b["results_url"]):
        cid = row["custom_id"]; p, c, i, mt = cid.split("__")
        res = row["result"]
        if res["type"] != "succeeded":
            print(f"  NONSUCCESS {cid}: {res['type']}"); continue
        msg = res["message"]
        rec = {"schema_version": 2, "pair": p, "condition": c, "model": model,
               "sample": int(i), "max_tokens": int(mt[2:]),
               "prompt_sha256": prompts[(p, c)][1],
               "response": "".join(bl.get("text", "") for bl in msg.get("content", [])),
               "stop_reason": msg.get("stop_reason"), "usage": msg.get("usage"),
               "latency": None, "batch_id": bid, "ts": time.time()}
        key = (p, c, model, int(i))
        if key in seen:  # QC resample replaces the capped record downstream; keep both, flag
            rec["qc_resample"] = True
        out.write(json.dumps(rec) + "\n"); seen.add(key)
    out.flush()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--keys", default="keys.json")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--max-tokens", type=int, default=4000)
    args = ap.parse_args()

    cfg = json.load(open(args.keys, encoding="utf-8"))
    pairs = {p["name"]: p for p in cfg["pairs"] if os.path.exists(p["paper_txt"])}
    prompts = {}
    os.makedirs("prompts", exist_ok=True); os.makedirs("results", exist_ok=True)
    for pn, pair in pairs.items():
        for c in "ABCD":
            pr = build_prompt(c, pair)
            h = hashlib.sha256(pr.encode()).hexdigest()[:16]
            prompts[(pn, c)] = (pr, h)
            open(f"prompts/{pn}_{c}_{h}.txt", "w", encoding="utf-8").write(pr)
    print(f"{len(prompts)} rendered prompts written to prompts/")

    done = set()
    if os.path.exists("results/raw_v2.jsonl"):
        for line in open("results/raw_v2.jsonl", encoding="utf-8"):
            r = json.loads(line)
            done.add((r["pair"], r["condition"], r["model"], r["sample"]))
    state_path = "results/batch_state_ext.json"
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    def missing(model):
        return [(pn, c, i) for pn in pairs for c in "ABCD" for i in range(args.n)
                if (pn, c, model, i) not in done]

    for model in args.models:
        if model not in state:
            tasks = missing(model)
            print(f"{model}: {len(tasks)} missing samples")
            if not tasks: continue
            state[model] = submit(model, tasks, prompts, args.max_tokens)
            json.dump(state, open(state_path, "w"))

    seen = set()
    with open("results/raw_v2.jsonl", "a", encoding="utf-8") as out:
        for model in args.models:
            if model in state:
                poll(state[model]); harvest(state[model], model, prompts, out, seen)

    # pre-registered QC: resample max_tokens-stopped responses once at 8000
    recs = [json.loads(l) for l in open("results/raw_v2.jsonl", encoding="utf-8")]
    recs = [r for r in recs if r["sample"] >= 20]  # QC scope: extension samples only
    capped = [(r["pair"], r["condition"], r["sample"], r["model"]) for r in recs
              if r["stop_reason"] == "max_tokens" and r["max_tokens"] == args.max_tokens]
    print(f"\nQC: {len(capped)} responses stopped on max_tokens at {args.max_tokens}")
    if capped and "qc" not in state:
        by_model = {}
        for p, c, i, m in capped: by_model.setdefault(m, []).append((p, c, i))
        state["qc"] = {m: submit(m, ts, prompts, 8000) for m, ts in by_model.items()}
        json.dump(state, open(state_path, "w"))
    if "qc" in state:
        with open("results/raw_v2.jsonl", "a", encoding="utf-8") as out:
            for m, bid in state["qc"].items():
                poll(bid); harvest(bid, m, prompts, out, seen)
    # final stop_reason census
    recs = [json.loads(l) for l in open("results/raw_v2.jsonl", encoding="utf-8")]
    from collections import Counter
    print("stop_reason census:", Counter(r["stop_reason"] for r in recs))
    print("done. Score with: python score_probe.py --raw results/raw_v2.jsonl")

if __name__ == "__main__":
    main()
