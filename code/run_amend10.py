#!/usr/bin/env python3
"""Amendment 10. (1) Harvest the already-submitted Amendment 9 QC batches (kept with the superseded
newest-generation run). (2) Resample capped Amendment 9 part (a)/(b) responses once at 8,000 tokens.
(3) Rerun Amendment 9 part (c) with per-model minimum-thinking settings and a 16,000-token cap
(one resample at 32,000). Usage: python run_amend10.py <repo_root> [--dry-run]"""
import argparse, hashlib, json, os, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_amend9 as A9   # api(), build(), harvest_all(), content()

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
THINK = {  # minimum reasoning each model accepts (verified 2026-11-03)
    "claude-haiku-5-5": {"thinking": {"type": "disabled"}},
    "claude-sonnet-5-5": {"thinking": {"type": "between_tools"}},
    "claude-opus-5-5": {"thinking": {"type": "adaptive"}, "output_config": {"effort": "low"}},
    "claude-fable-5-1": {"thinking": {"type": "adaptive"}, "output_config": {"effort": "low"}},
}
CAP, CAP_QC = 16000, 32000

def submit(reqs, max_tokens, state, key, state_path):
    state.setdefault(key, [])
    chunks = [reqs[k:k + A9.CHUNK] for k in range(0, len(reqs), A9.CHUNK)]
    for n, ch in enumerate(chunks):
        if n < len(state[key]): continue
        body = {"requests": [{"custom_id": f"{cid}__{m}__mt{max_tokens}".replace(".", "p"),
                 "params": {"model": m, "max_tokens": max_tokens, "temperature": 1.0,
                            "messages": [{"role": "user", "content": msg}], **THINK.get(m, {})}}
                for (cid, m, msg, h) in ch]}
        b = A9.api("POST", "/messages/batches", body)
        state[key].append(b["id"]); json.dump(state, open(state_path, "w"))
        print(f"submitted {b['id']} ({key}, chunk {n+1}/{len(chunks)}, {len(ch)} requests)", flush=True)

def harvest(bids, hashes, raw):
    have = set()
    if os.path.exists(raw):
        for l in open(raw, encoding="utf-8"): have.add(json.loads(l)["custom_id"])
    with open(raw, "a", encoding="utf-8") as out:
        for bid in bids:
            while True:
                b = A9.api("GET", f"/messages/batches/{bid}")
                if b["processing_status"] == "ended": break
                time.sleep(60)
            n = 0
            for row in A9.api("GET", "", raw_url=b["results_url"]):
                cid = row["custom_id"]
                if cid in have: continue
                if row["result"]["type"] != "succeeded":
                    print(f"  NONSUCCESS {cid}: {row['result']['type']}", flush=True); continue
                fam, p, c, i, m, mt = cid.split("__"); msg = row["result"]["message"]; u = msg.get("usage") or {}
                out.write(json.dumps({"schema_version": 4, "custom_id": cid, "template": fam, "pair": p, "condition": c,
                    "model": msg.get("model"), "sample": int(i), "max_tokens": int(mt[2:]),
                    "prompt_sha256": hashes.get(cid.rsplit("__", 2)[0]),
                    "thinking_setting": THINK.get(msg.get("model"), {}),
                    "thinking_tokens": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
                    "response": "".join(x.get("text", "") for x in msg.get("content", []) if x.get("type") == "text"),
                    "thinking": "".join(x.get("thinking", "") for x in msg.get("content", []) if x.get("type") == "thinking") or None,
                    "stop_reason": msg.get("stop_reason"), "usage": u, "batch_id": bid, "ts": time.time()}) + "\n")
                have.add(cid); n += 1
            out.flush(); print(f"  {bid}: harvested {n}", flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    # ---- (1) and (2): finish Amendment 9 QC, parts (a)/(b) only ----
    reqs_ab = A9.build(a.root, {"a", "b", "c"})
    hashes = {cid: h for cid, m, _, h in reqs_ab}
    st9p = os.path.join(a.root, "data", "amend9_batch_state.json"); st9 = json.load(open(st9p))
    raw9 = os.path.join(a.root, "data", "raw_amend9.jsonl")
    recs = [json.loads(l) for l in open(raw9, encoding="utf-8")]
    final = {}
    for r in recs:
        k = r["custom_id"].rsplit("__", 1)[0]
        if k not in final or r["max_tokens"] > final[k]["max_tokens"]: final[k] = r
    capped_ab = sorted(k for k, r in final.items() if r["stop_reason"] == "max_tokens" and r["max_tokens"] == 4000 and r["template"] != "O")
    byid = {f"{cid}__{m}".replace(".", "p"): (cid, m, msg, h) for cid, m, msg, h in reqs_ab}
    qc_ab = [byid[k] for k in capped_ab if k in byid and not any(x for x in [])]
    already = set()
    print(f"(1) superseded-run QC batches to harvest: {len(st9.get('qc', []))}; (2) part a/b capped to resample: {len(qc_ab)}", flush=True)
    # ---- (3): part (c) rerun ----
    reqs_c = [x for x in A9.build(a.root, {"c"})]
    print(f"(3) part (c) rerun: {len(reqs_c)} requests: {Counter(m for _, m, _, _ in reqs_c)}", flush=True)
    if a.dry_run: return
    A9.harvest_all(st9.get("qc", []), hashes, raw9)
    # resample a/b capped responses whose 8000 resample is not already on disk
    have8 = {json.loads(l)["custom_id"].rsplit("__", 1)[0] for l in open(raw9, encoding="utf-8") if '"max_tokens": 8000' in l}
    qc_ab = [x for x in qc_ab if f"{x[0]}__{x[1]}".replace(".", "p") not in have8]
    print(f"part a/b resamples still needed: {len(qc_ab)}", flush=True)
    if qc_ab:
        A9.submit_all(qc_ab, 8000, st9, "qc_ab", st9p); A9.harvest_all(st9["qc_ab"], hashes, raw9)
    st10p = os.path.join(a.root, "data", "amend10_batch_state.json")
    st10 = json.load(open(st10p)) if os.path.exists(st10p) else {}
    raw10 = os.path.join(a.root, "data", "raw_amend10.jsonl")
    submit(reqs_c, CAP, st10, "main", st10p); harvest(st10["main"], hashes, raw10)
    recs = [json.loads(l) for l in open(raw10, encoding="utf-8")]
    capped = sorted({r["custom_id"].rsplit("__", 1)[0] for r in recs if r["stop_reason"] == "max_tokens" and r["max_tokens"] == CAP})
    byc = {f"{cid}__{m}".replace(".", "p"): (cid, m, msg, h) for cid, m, msg, h in reqs_c}
    qc = [byc[k] for k in capped if k in byc]
    print(f"part (c) rerun capped at {CAP}: {len(qc)}", flush=True)
    if qc:
        submit(qc, CAP_QC, st10, "qc", st10p); harvest(st10["qc"], hashes, raw10)
    recs = [json.loads(l) for l in open(raw10, encoding="utf-8")]
    print("records:", len(recs), Counter((r["model"], r["stop_reason"]) for r in recs), flush=True)
    tt = Counter(); n = Counter()
    for r in recs: tt[r["model"]] += r.get("thinking_tokens") or 0; n[r["model"]] += 1
    print("mean thinking tokens:", {m: round(tt[m] / n[m]) for m in n}, flush=True)

if __name__ == "__main__":
    main()
