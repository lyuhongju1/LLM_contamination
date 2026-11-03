#!/usr/bin/env python3
"""Amendment 9 sampling: (a) paraphrase families P3, P4; (b) length-controlled families K5, K15;
(c) newest-generation models on the 50 released prompts.
Usage: python run_amend9.py <repo_root> [--dry-run] [--part a|b|c ...]
Robust resume: state is saved after every submitted chunk; harvest skips records already on disk;
results are always parsed as JSONL. Output: <repo_root>/data/raw_amend9.jsonl."""
import argparse, hashlib, json, os, sys, time, urllib.request, urllib.error
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ANTHROPIC_API_KEY") or open(os.path.join(HERE, '..', '.anthropic_key')).read().strip()
API = "https://api.anthropic.com/v1"
HDRS = {"Content-Type": "application/json", "x-api-key": KEY, "anthropic-version": "2023-06-01"}
CHUNK = 500

CORE = ["claude-sonnet-4-5-20250929", "claude-sonnet-4-6"]
NEWEST = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1"]

# ---------------- frozen templates (Amendment 9) ----------------
FAM = {
 "P3": {"A_intro": "The following is a detector paper.", "D_intro": "The following describes a detector.",
        "ask": "You are an experienced detector physicist. Suggest the most valuable hardware upgrades for this "
               "instrument to improve its physics performance, with concrete technology choices.",
        "cutoff": "Respond using only knowledge that existed in or before {YEAR}; treat anything later as unknown.\n\n",
        "conds": ["A", "B", "D"]},
 "P4": {"A_intro": "I am writing a proposal to upgrade the instrument described in the paper below.",
        "D_intro": "I am writing a proposal to upgrade the instrument described below.",
        "ask": "Which specific hardware upgrades should the proposal include to get the most physics out of this "
               "instrument? Please be concrete about technologies and components.",
        "cutoff": "Pretend it is {YEAR}. You know nothing that was published, proposed, or announced after {YEAR}.\n\n",
        "conds": ["A", "B", "D"]},
 "K5":  {"A_intro": "Below is the text of a published paper describing a physics instrument.",
         "D_intro": "Below is a short description of a physics instrument.",
         "ask": "Propose exactly 5 specific hardware upgrades to the instrument described above that would most "
                "improve its primary physics performance. Number them 1 to 5 and name the technologies and components.",
         "conds": ["A", "D"]},
 "K15": {"A_intro": "Below is the text of a published paper describing a physics instrument.",
         "D_intro": "Below is a short description of a physics instrument.",
         "ask": "Propose exactly 15 specific hardware upgrades to the instrument described above that would most "
                "improve its primary physics performance. Number them 1 to 15 and name the technologies and components.",
         "conds": ["A", "D"]},
}

def render_fam(fam, cond, pair, root):
    t = FAM[fam]
    if cond == "D":
        intro, material = t["D_intro"], pair["generic_desc"]
    else:
        intro = t["A_intro"]
        material = open(os.path.join(root, pair["paper_txt"]), encoding="utf-8", errors="ignore").read()
    head = (t["cutoff"].replace("{YEAR}", str(pair["year"])) if cond == "B" else "") + intro + "\n\n<material>\n"
    return head + material, "\n</material>\n\n" + t["ask"]

def content(prefix, suffix, cache):
    if not cache:
        return prefix + suffix
    return [{"type": "text", "text": prefix, "cache_control": {"type": "ephemeral"}}, {"type": "text", "text": suffix}]

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
                print(f"  network error ({e}); retrying", flush=True); time.sleep(30 * (attempt + 1)); continue
            raise
    if raw_url:
        return [json.loads(l) for l in payload.decode().splitlines() if l.strip()]
    return json.loads(payload)

def build(root, parts):
    cfg = json.load(open(os.path.join(root, "keys.json"), encoding="utf-8"))
    pairs = {p["name"]: p for p in cfg["pairs"]}
    reqs, prompts = [], {}
    pdir = os.path.join(root, "prompts_amend9"); os.makedirs(pdir, exist_ok=True)
    fams = (["P3", "P4"] if "a" in parts else []) + (["K5", "K15"] if "b" in parts else [])
    for fam in fams:
        for pn, pair in pairs.items():
            for c in FAM[fam]["conds"]:
                pre, suf = render_fam(fam, c, pair, root)
                h = hashlib.sha256((pre + suf).encode()).hexdigest()[:16]
                prompts[(fam, pn, c)] = h
                open(os.path.join(pdir, f"{pn}_{c}_{fam}_{h}.txt"), "w", encoding="utf-8").write(pre + suf)
                for m in CORE:
                    for i in range(50):
                        reqs.append((f"{fam}__{pn}__{c}__{i}", m, content(pre, suf, c != "D"), h))
    if "c" in parts:
        odir = os.path.join(root, "prompts")
        for f in sorted(os.listdir(odir)):
            pn, c, h = f[:-4].split("_")
            text = open(os.path.join(odir, f), encoding="utf-8").read()
            assert hashlib.sha256(text.encode()).hexdigest()[:16] == h, f"hash mismatch {f}"
            i = text.find("\n</paper>")
            body = content(text[:i], text[i:], True) if i >= 0 else text
            for m in NEWEST:
                for s in range(20 if c == "Dp" else 50):
                    reqs.append((f"O__{pn}__{c}__{s}", m, body, h))
    return reqs

def submit_all(reqs, max_tokens, state, key, state_path):
    """Submit in deterministic chunks; state[key] holds one batch id per chunk, saved after each."""
    state.setdefault(key, [])
    chunks = [reqs[k:k + CHUNK] for k in range(0, len(reqs), CHUNK)]
    for n, ch in enumerate(chunks):
        if n < len(state[key]): continue
        body = {"requests": [{"custom_id": f"{cid}__{m}__mt{max_tokens}".replace(".", "p"),
                              "params": {"model": m, "max_tokens": max_tokens, "temperature": 1.0,
                                         "messages": [{"role": "user", "content": msg}]}}
                             for (cid, m, msg, h) in ch]}
        b = api("POST", "/messages/batches", body)
        state[key].append(b["id"]); json.dump(state, open(state_path, "w"))
        print(f"submitted {b['id']} ({key}, chunk {n+1}/{len(chunks)}, {len(ch)} requests)", flush=True)

def harvest_all(bids, hashes, raw):
    have = set()
    if os.path.exists(raw):
        for l in open(raw, encoding="utf-8"): have.add(json.loads(l)["custom_id"])
    with open(raw, "a", encoding="utf-8") as out:
        for bid in bids:
            while True:
                b = api("GET", f"/messages/batches/{bid}")
                if b["processing_status"] == "ended": break
                time.sleep(60)
            n = 0
            for row in api("GET", "", raw_url=b["results_url"]):
                cid = row["custom_id"]
                if cid in have: continue
                res = row["result"]
                if res["type"] != "succeeded":
                    print(f"  NONSUCCESS {cid}: {res['type']}", flush=True); continue
                fam, p, c, i, m, mt = cid.split("__")
                msg = res["message"]
                out.write(json.dumps({"schema_version": 3, "custom_id": cid, "template": fam, "pair": p,
                    "condition": c, "model": msg.get("model"), "sample": int(i), "max_tokens": int(mt[2:]),
                    "prompt_sha256": hashes.get(cid.rsplit("__", 2)[0]),
                    "response": "".join(bl.get("text", "") for bl in msg.get("content", []) if bl.get("type") == "text"),
                    "stop_reason": msg.get("stop_reason"), "usage": msg.get("usage"),
                    "batch_id": bid, "ts": time.time()}) + "\n"); have.add(cid); n += 1
            out.flush(); print(f"  {bid}: harvested {n} {b.get('request_counts')}", flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--part", nargs="+", default=["a", "b", "c"])
    a = ap.parse_args()
    reqs = build(a.root, set(a.part))
    print(f"{len(reqs)} requests: " + str(Counter((cid.split('__')[0], m) for cid, m, _, _ in reqs)), flush=True)
    if a.dry_run: return
    hashes = {cid: h for cid, m, _, h in reqs}
    state_path = os.path.join(a.root, "data", "amend9_batch_state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    raw = os.path.join(a.root, "data", "raw_amend9.jsonl")
    submit_all(reqs, 4000, state, "main", state_path)
    harvest_all(state["main"], hashes, raw)
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    capped = {r["custom_id"].rsplit("__", 2)[0] + "__" + r["custom_id"].split("__")[4] for r in recs
              if r["stop_reason"] == "max_tokens" and r["max_tokens"] == 4000}
    byid = {f"{cid}__{m}".replace(".", "p"): (cid, m, msg, h) for cid, m, msg, h in reqs}
    qc = [byid[k] for k in sorted(capped) if k in byid]
    print(f"QC: {len(qc)} capped at 4000", flush=True)
    if qc:
        submit_all(qc, 8000, state, "qc", state_path)
        harvest_all(state["qc"], hashes, raw)
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    print("records:", len(recs), Counter((r["template"], r["model"], r["stop_reason"]) for r in recs), flush=True)
    u = Counter()
    for r in recs:
        for k, v in (r.get("usage") or {}).items():
            if isinstance(v, int): u[(r["model"], k)] += v
    print("usage totals:", dict(u), flush=True)

if __name__ == "__main__":
    main()
