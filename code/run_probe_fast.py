#!/usr/bin/env python3
"""Hindsight-contamination probe: bare-model sampling battery.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 run_probe.py --keys keys.json --models claude-sonnet-4-20250514 \
      --conditions A B C D --n 20 --out results/raw.jsonl

Conditions:
  A  paper text + upgrade request
  B  as A, plus explicit knowledge-cutoff instruction (tests prompt-layer cutoffs)
  C  as A, with identity-redacted paper text (tests identity-keyed recall)
  D  no paper; generic instrument description only (generic-knowledge floor)

Every sample is appended to the JSONL with full metadata (prompt hash, model,
usage, timestamp) so the raw record is self-documenting and auditable.
"""
import argparse, hashlib, json, os, re, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://api.anthropic.com/v1/messages"

PROMPT_A = ("The following is the text of a published detector paper.\n\n<paper>\n{TEXT}\n</paper>\n\n"
            "Based on this instrument, propose specific hardware design upgrades that would most "
            "improve its primary physics performance. Be concrete about technologies and components.")
CUTOFF_CLAUSE = ("Assume your knowledge ends in {YEAR}. Do not use any information about "
                 "developments, projects, collaborations, or publications after {YEAR}.\n\n")
PROMPT_D = ("Propose specific hardware design upgrades that would most improve the primary physics "
            "performance of the following instrument: {GENERIC}. Be concrete about technologies and components.")


def redact(text, patterns):
    for p in patterns:
        text = re.sub(p, "[REDACTED]", text, flags=re.I)
    return text


def build_prompt(cond, pair):
    text = open(pair["paper_txt"], encoding="utf-8", errors="ignore").read()
    if cond == "A":
        return PROMPT_A.replace("{TEXT}", text)
    if cond == "B":
        return CUTOFF_CLAUSE.replace("{YEAR}", str(pair["year"])) + PROMPT_A.replace("{TEXT}", text)
    if cond == "C":
        return PROMPT_A.replace("{TEXT}", redact(text, pair["redact_patterns"]))
    if cond == "D":
        return PROMPT_D.replace("{GENERIC}", pair["generic_desc"])
    raise ValueError(cond)


def call_api(model, prompt, max_tokens=1200, temperature=1.0, retries=5):
    content = [{"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}]
    body = json.dumps({"model": model, "max_tokens": max_tokens, "temperature": temperature,
                       "messages": [{"role": "user", "content": content}]}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Content-Type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except Exception as e:
            wait = 2 ** attempt * 5
            print(f"  retry {attempt+1} after error: {e} (sleep {wait}s)", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("API failed after retries")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", default="keys.json")
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--conditions", nargs="+", default=["A", "B", "C", "D"])
    ap.add_argument("--pairs", nargs="+", default=None, help="subset of pair names")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--out", default="results/raw.jsonl")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    cfg = json.load(open(args.keys, encoding="utf-8"))
    pairs = {p["name"]: p for p in cfg["pairs"]}
    if args.pairs:
        pairs = {k: v for k, v in pairs.items() if k in args.pairs}

    done = set()
    if os.path.exists(args.out):
        for line in open(args.out, encoding="utf-8"):
            r = json.loads(line)
            done.add((r["pair"], r["condition"], r["model"], r["sample"]))
        print(f"resuming: {len(done)} samples already recorded")

    tasks = []
    prompts = {}
    for pname, pair in pairs.items():
        for cond in args.conditions:
            prompt = build_prompt(cond, pair)
            prompts[(pname, cond)] = (prompt, hashlib.sha256(prompt.encode()).hexdigest()[:16])
            for model in args.models:
                for i in range(args.n):
                    if (pname, cond, model, i) not in done:
                        tasks.append((pname, cond, model, i))
    print(f"{len(tasks)} samples to run with {args.workers} workers")
    lock = threading.Lock()
    with open(args.out, "a", encoding="utf-8") as out:
        def work(task):
            pname, cond, model, i = task
            prompt, phash = prompts[(pname, cond)]
            t0 = time.time()
            resp = call_api(model, prompt)
            text = "".join(b.get("text", "") for b in resp.get("content", []))
            rec = {"pair": pname, "condition": cond, "model": model, "sample": i,
                   "prompt_sha256": phash, "response": text,
                   "usage": resp.get("usage"), "latency": round(time.time() - t0, 2), "ts": time.time()}
            with lock:
                out.write(json.dumps(rec) + "\n")
                out.flush()
            cache = (resp.get("usage") or {}).get("cache_read_input_tokens", 0)
            print(f"{pname} {cond} {model} #{i}: {len(text)} chars (cached_in={cache})")
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = [ex.submit(work, t) for t in tasks]
            for f in as_completed(futures):
                f.result()


if __name__ == "__main__":
    main()
