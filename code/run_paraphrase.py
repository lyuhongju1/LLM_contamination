#!/usr/bin/env python3
"""Amendment 7 paraphrase sweep via the Message Batches API.
Usage: python run_paraphrase.py <repo_root> [--dry-run] [--n 50]
Reads the API key from ../.anthropic_key (relative to this file). Resumable: batch ids in
<repo_root>/data/paraphrase_batch_state.json. Writes <repo_root>/data/raw_paraphrase.jsonl and
<repo_root>/prompts_paraphrase/. Applies the Amendment 3 QC rule (one 8000-token resample)."""
import argparse, hashlib, json, os, sys, time, urllib.request, urllib.error
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ANTHROPIC_API_KEY") or open(os.path.join(HERE, '..', '.anthropic_key')).read().strip()
API = "https://api.anthropic.com/v1"
HDRS = {"Content-Type": "application/json", "x-api-key": KEY, "anthropic-version": "2023-06-01"}
MODELS = ["claude-sonnet-4-5-20250929", "claude-sonnet-4-6"]
CONDS = ["A", "B", "D"]
FAMS = ["P1", "P2"]

# ---- frozen templates (Amendment 7). Each is (prefix, suffix) around the material block. ----
T = {
 "P1": {"A_intro": "Below is the text of a published paper describing a physics instrument.",
        "D_intro": "Below is a short description of a physics instrument.",
        "ask": "What changes to the hardware of the instrument described above would most improve its "
               "primary physics performance? Name specific technologies and components.",
        "cutoff": "Answer as of the end of {YEAR}: use only knowledge that was available by then, and "
                  "nothing published, proposed, or announced afterward.\n\n"},
 "P2": {"A_intro": "You are advising the team that operates the instrument described below.",
        "D_intro": "You are advising the team that operates the instrument described below.",
        "ask": "Recommend the hardware upgrades you would prioritize to improve the instrument's main "
               "physics reach. Be specific about the technologies and components you would use.",
        "cutoff": "Your knowledge cutoff is {YEAR}. Ignore any experiments, collaborations, technologies, "
                  "or publications that appeared after {YEAR}.\n\n"},
}

# ---- thinking arm (Amendment 7, part 6): ORIGINAL templates, byte-identical to the v2 sweep ----
ORIG_A = ("The following is the text of a published detector paper.\n\n<paper>\n", "\n</paper>\n\n"
          "Based on this instrument, propose specific hardware design upgrades that would most "
          "improve its primary physics performance. Be concrete about technologies and components.")
ORIG_CUTOFF = ("Assume your knowledge ends in {YEAR}. Do not use any information about "
               "developments, projects, collaborations, or publications after {YEAR}.\n\n")
ORIG_D = ("Propose specific hardware design upgrades that would most improve the primary physics "
          "performance of the following instrument: ", ". Be concrete about technologies and components.")
THINK_PAIRS = ["darkside", "protodune", "icecube", "lhcb", "sno", "aligo", "gerda", "exo200"]
THINK_N = 20
THINK_BUDGET, THINK_MAX = 4000, 12000

def render(fam, cond, pair, root):
    if fam == "T":
        if cond == "D":
            return ORIG_D[0], pair["generic_desc"], ORIG_D[1]
        material = open(os.path.join(root, pair["paper_txt"]), encoding="utf-8", errors="ignore").read()
        head = (ORIG_CUTOFF.replace("{YEAR}", str(pair["year"])) if cond == "B" else "") + ORIG_A[0]
        return head, material, ORIG_A[1]
    t = T[fam]
    if cond == "D":
        intro, material = t["D_intro"], pair["generic_desc"]
    else:
        intro = t["A_intro"]
        material = open(os.path.join(root, pair["paper_txt"]), encoding="utf-8", errors="ignore").read()
    head = (t["cutoff"].replace("{YEAR}", str(pair["year"])) if cond == "B" else "") + intro + "\n\n<material>\n"
    tail = "\n</material>\n\n" + t["ask"]
    return head, material, tail

def content_blocks(head, material, tail, cache):
    # Text is identical to head+material+tail; the split only places a cache breakpoint after the material.
    if not cache:
        return head + material + tail
    return [{"type": "text", "text": head + material, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": tail}]

def api(method, path, body=None, raw_url=None):
    url = raw_url or (API + path)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HDRS, method=method)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
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

def submit(model, tasks, prompts, max_tokens):
    reqs = []
    for (fam, p, c, i) in tasks:
        head, material, tail, _ = prompts[(fam, p, c)]
        mt = max_tokens
        params = {"model": model, "temperature": 1.0,
                  "messages": [{"role": "user", "content": content_blocks(head, material, tail, c != 'D' and fam != 'T')}]}
        if fam == "T":
            mt = THINK_MAX if max_tokens == 4000 else THINK_MAX + 4000   # QC resample raises the cap by 4000
            params["thinking"] = {"type": "enabled", "budget_tokens": THINK_BUDGET}
        params["max_tokens"] = mt
        reqs.append({"custom_id": f"{fam}__{p}__{c}__{i}__mt{mt}", "params": params})
    ids = []
    for k in range(0, len(reqs), 500):  # size-capped chunks, as in the extension sweep
        b = api("POST", "/messages/batches", {"requests": reqs[k:k + 500]})
        print(f"submitted {b['id']} ({model}, {len(reqs[k:k+500])} requests, max_tokens={max_tokens})"); ids.append(b["id"])
    return ids

def poll(bid):
    while True:
        b = api("GET", f"/messages/batches/{bid}")
        if b["processing_status"] == "ended":
            print(f"  {bid}: ended {b.get('request_counts')}"); return b
        time.sleep(60)

def harvest(bid, model, prompts, out):
    b = api("GET", f"/messages/batches/{bid}")
    n = 0
    for row in api("GET", "", raw_url=b["results_url"]):
        fam, p, c, i, mt = row["custom_id"].split("__")
        res = row["result"]
        if res["type"] != "succeeded":
            print(f"  NONSUCCESS {row['custom_id']}: {res['type']}"); continue
        msg = res["message"]
        out.write(json.dumps({"schema_version": 3, "template": fam, "pair": p, "condition": c, "model": model,
            "sample": int(i), "max_tokens": int(mt[2:]), "prompt_sha256": prompts[(fam, p, c)][3],
            "response": "".join(bl.get("text", "") for bl in msg.get("content", []) if bl.get("type") == "text"),
            "thinking": "".join(bl.get("thinking", "") for bl in msg.get("content", []) if bl.get("type") == "thinking") or None,
            "stop_reason": msg.get("stop_reason"), "usage": msg.get("usage"),
            "batch_id": bid, "ts": time.time()}) + "\n"); n += 1
    out.flush(); return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--n", type=int, default=50); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(a.root, "keys.json"), encoding="utf-8"))
    pairs = {p["name"]: p for p in cfg["pairs"]}
    pdir = os.path.join(a.root, "prompts_paraphrase"); os.makedirs(pdir, exist_ok=True)
    prompts = {}
    for fam in FAMS:
        for pn, pair in pairs.items():
            for c in CONDS:
                head, material, tail = render(fam, c, pair, a.root)
                full = head + material + tail
                h = hashlib.sha256(full.encode()).hexdigest()[:16]
                prompts[(fam, pn, c)] = (head, material, tail, h)
                open(os.path.join(pdir, f"{pn}_{c}_{fam}_{h}.txt"), "w", encoding="utf-8").write(full)
    for pn in THINK_PAIRS:
        for c in CONDS:
            head, material, tail = render("T", c, pairs[pn], a.root)
            full = head + material + tail
            h = hashlib.sha256(full.encode()).hexdigest()[:16]
            prompts[("T", pn, c)] = (head, material, tail, h)
            orig = [f for f in os.listdir(os.path.join(a.root, "prompts")) if f.startswith(f"{pn}_{c}_")]
            assert orig and orig[0].endswith(f"_{h}.txt"), f"thinking-arm prompt for {pn}/{c} not byte-identical to v2: {orig} vs {h}"
    print("thinking-arm prompts verified byte-identical to the v2 prompts (hash match)")
    tasks = [(fam, pn, c, i) for fam in FAMS for pn in pairs for c in CONDS for i in range(a.n)]
    tasks += [("T", pn, c, i) for pn in THINK_PAIRS for c in CONDS for i in range(THINK_N)]
    print(f"{len(prompts)} prompts rendered to {pdir}; {len(tasks)} tasks per model, {len(tasks)*len(MODELS)} total")
    if a.dry_run:
        fam, pn, c = "P1", "gerda", "B"; h, m, t, _ = prompts[(fam, pn, c)]
        print("--- example P1/gerda/B (material truncated) ---\n" + h + m[:300] + " ...\n" + t)
        h, m, t, _ = prompts[("P2", "gerda", "D")]; print("--- example P2/gerda/D ---\n" + h + m + t)
        return

    state_path = os.path.join(a.root, "data", "paraphrase_batch_state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    for m in MODELS:
        if m not in state:
            state[m] = submit(m, tasks, prompts, 4000); json.dump(state, open(state_path, "w"))
    raw = os.path.join(a.root, "data", "raw_paraphrase.jsonl")
    if not state.get("harvested"):
        with open(raw, "a", encoding="utf-8") as out:
            for m in MODELS:
                for bid in state[m]:
                    poll(bid); print(f"  harvested {harvest(bid, m, prompts, out)}")
        state["harvested"] = True; json.dump(state, open(state_path, "w"))
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    capped = [r for r in recs if r["stop_reason"] == "max_tokens" and r["max_tokens"] in (4000, THINK_MAX)]
    print(f"QC: {len(capped)} capped at the first-pass cap")
    if capped and "qc" not in state:
        by_m = {}
        for r in capped: by_m.setdefault(r["model"], []).append((r["template"], r["pair"], r["condition"], r["sample"]))
        state["qc"] = {m: submit(m, ts, prompts, 8000) for m, ts in by_m.items()}; json.dump(state, open(state_path, "w"))
    if "qc" in state and not state.get("qc_harvested"):
        with open(raw, "a", encoding="utf-8") as out:
            for m, bids in state["qc"].items():
                for bid in bids: poll(bid); harvest(bid, m, prompts, out)
        state["qc_harvested"] = True; json.dump(state, open(state_path, "w"))
    recs = [json.loads(l) for l in open(raw, encoding="utf-8")]
    print("records:", len(recs), "stop reasons:", Counter(r["stop_reason"] for r in recs))
    u = Counter()
    for r in recs:
        for k, v in (r.get("usage") or {}).items():
            if isinstance(v, int): u[k] += v
    print("usage totals:", dict(u))

if __name__ == "__main__":
    main()
