#!/usr/bin/env python3
"""Cross-vendor extension (Amendment 4): run the identical 40 prompts on a local
open-weight model via Ollama. UNTESTED against a live Ollama instance; report
errors back for fixes.
Setup: install Ollama (ollama.com), then e.g.:  ollama pull qwen2.5:7b-instruct
Usage: python code/run_probe_local.py --model qwen2.5:7b-instruct --n 20 --num-ctx 65536
Notes: pairs whose prompts exceed --num-ctx are skipped and reported (protodune
needs ~60k tokens of context; with limited RAM run --num-ctx 32768 and accept
the documented subset per Amendment 4)."""
import argparse, hashlib, json, os, time, urllib.request

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--num-ctx", type=int, default=65536)
    ap.add_argument("--url", default="http://localhost:11434/api/generate")
    ap.add_argument("--out", default="data/raw_local.jsonl")
    ap.add_argument("--conditions", nargs="+", default=list("ABCD"))
    ap.add_argument("--pairs", nargs="+", default=None, help="subset of pair names; default all")
    args = ap.parse_args()
    prompts = {}
    for fn in sorted(os.listdir("prompts")):
        if not fn.endswith(".txt"): continue
        pair, cond, h = fn[:-4].rsplit("_", 2)
        prompts[(pair, cond)] = (open(f"prompts/{fn}", encoding="utf-8").read(), h)
    done = set()
    if os.path.exists(args.out):
        for line in open(args.out, encoding="utf-8"):
            r = json.loads(line)
            done.add((r["pair"], r["condition"], r["model"], r["sample"]))
    with open(args.out, "a", encoding="utf-8") as out:
        for (pair, cond), (prompt, h) in sorted(prompts.items()):
            if cond not in args.conditions: continue
            if args.pairs and pair not in args.pairs: continue
            if len(prompt) / 3.5 > args.num_ctx:
                print(f"SKIP {pair} {cond}: prompt exceeds num_ctx (documented subset)")
                continue
            for i in range(args.n):
                if (pair, cond, args.model, i) in done: continue
                body = json.dumps({"model": args.model, "prompt": prompt, "stream": False,
                                   "options": {"temperature": 1.0, "num_ctx": args.num_ctx,
                                               "num_predict": 4000}}).encode()
                req = urllib.request.Request(args.url, data=body,
                                             headers={"Content-Type": "application/json"})
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=3600) as r:
                    resp = json.load(r)
                rec = {"schema_version": 2, "pair": pair, "condition": cond,
                       "model": args.model, "sample": i, "prompt_sha256": h,
                       "response": resp.get("response", ""),
                       "stop_reason": "end_turn" if resp.get("done_reason") == "stop" else resp.get("done_reason"),
                       "usage": {"input_tokens": resp.get("prompt_eval_count"),
                                 "output_tokens": resp.get("eval_count")},
                       "latency": round(time.time() - t0, 2), "batch_id": None,
                       "backend": "ollama", "ts": time.time()}
                out.write(json.dumps(rec) + "\n"); out.flush()
                print(f"{pair} {cond} #{i}: {len(rec['response'])} chars, {rec['latency']}s")

if __name__ == "__main__":
    main()
