#!/usr/bin/env python3
"""Cross-vendor open-weight run via an OpenAI-compatible inference API
(DeepInfra, Together, Fireworks). Runs the identical rendered prompts.
Setup:  $env:OPENWEIGHT_API_KEY="..."
Usage:  python code/run_probe_openweight.py --base-url https://api.deepinfra.com/v1/openai --model meta-llama/Llama-3.3-70B-Instruct --n 20
Resumable; appends to data/raw_openweight.jsonl in the standard schema."""
import argparse, json, os, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

def call(base, key, model, prompt, max_tokens):
    body = json.dumps({"model": model, "temperature": 1.0, "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 5: raise
            detail = getattr(e, "code", "")
            print(f"  retry {attempt+1} ({detail or e}) sleep {5*2**attempt}s")
            time.sleep(5 * 2 ** attempt)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--conditions", nargs="+", default=list("ABCD"))
    ap.add_argument("--pairs", nargs="+", default=None)
    ap.add_argument("--out", default="data/raw_openweight.jsonl")
    ap.add_argument("--max-prompt-tokens", type=int, default=None,
                    help="skip prompts whose estimated tokens exceed this (documented subset)")
    args = ap.parse_args()
    key = os.environ["OPENWEIGHT_API_KEY"]
    prompts = {}
    for fn in sorted(os.listdir("prompts")):
        if fn.endswith(".txt"):
            pair, cond, h = fn[:-4].rsplit("_", 2)
            prompts[(pair, cond)] = (open(f"prompts/{fn}", encoding="utf-8").read(), h)
    done = set()
    if os.path.exists(args.out):
        for line in open(args.out, encoding="utf-8"):
            r = json.loads(line)
            done.add((r["pair"], r["condition"], r["model"], r["sample"]))
    skipped = set()
    if args.max_prompt_tokens:
        for (p, c), (prompt, h) in prompts.items():
            if len(prompt) / 3.5 > args.max_prompt_tokens:
                skipped.add((p, c))
        for p, c in sorted(skipped):
            print(f"SKIP {p} {c}: prompt exceeds --max-prompt-tokens (documented subset)")
    tasks = [(p, c, i) for (p, c) in sorted(prompts) for i in range(args.n)
             if c in args.conditions and (not args.pairs or p in args.pairs)
             and (p, c) not in skipped and (p, c, args.model, i) not in done]
    print(f"{len(tasks)} samples to run, {args.workers} workers")
    lock = threading.Lock()
    with open(args.out, "a", encoding="utf-8") as out:
        def work(t):
            p, c, i = t
            prompt, h = prompts[(p, c)]
            t0 = time.time()
            resp = call(args.base_url, key, args.model, prompt, args.max_tokens)
            ch = resp["choices"][0]
            fr = ch.get("finish_reason")
            rec = {"schema_version": 2, "pair": p, "condition": c, "model": args.model,
                   "sample": i, "max_tokens": args.max_tokens,
                   "prompt_sha256": h, "response": ch["message"]["content"] or "",
                   "stop_reason": "end_turn" if fr == "stop" else fr,
                   "usage": {"input_tokens": (resp.get("usage") or {}).get("prompt_tokens"),
                             "output_tokens": (resp.get("usage") or {}).get("completion_tokens")},
                   "latency": round(time.time() - t0, 2), "batch_id": None,
                   "backend": args.base_url, "ts": time.time()}
            with lock:
                out.write(json.dumps(rec) + "\n"); out.flush()
            print(f"{p} {c} #{i}: {len(rec['response'])} chars ({rec['stop_reason']}, {rec['latency']}s)")
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for f in as_completed([ex.submit(work, t) for t in tasks]):
                f.result()
    from collections import Counter
    recs = [json.loads(l) for l in open(args.out, encoding="utf-8")]
    print("stop_reason census:", Counter(r["stop_reason"] for r in recs))

if __name__ == "__main__":
    main()
