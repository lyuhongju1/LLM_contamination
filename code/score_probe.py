#!/usr/bin/env python3
"""Score contamination-probe responses against pre-registered keys.

  python3 score_probe.py --keys keys.json --raw results/raw.jsonl --outdir results/

Outputs: leakage_audit.txt, scores.csv, summary.md, adjudication_sample.md
"""
import argparse, csv, json, math, os, random, re
from collections import defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0, c - h), min(1, c + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", default="keys.json")
    ap.add_argument("--raw", default="results/raw.jsonl")
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()

    cfg = json.load(open(args.keys, encoding="utf-8"))
    pairs = {p["name"]: p for p in cfg["pairs"] if os.path.exists(p["paper_txt"])}

    # ---- input-leakage audit: an item that already matches the input text is
    # not evidence of recall; it is excluded from contamination scoring. ----
    leaked = defaultdict(set)
    with open(os.path.join(args.outdir, "leakage_audit.txt"), "w", encoding="utf-8") as la:
        for pname, pair in pairs.items():
            text = open(pair["paper_txt"], encoding="utf-8", errors="ignore").read()
            for item, spec in pair["items"].items():
                hits = re.findall(spec["regex"], text, re.I)
                if hits:
                    leaked[pname].add(item)
                    la.write(f"LEAKED  {pname}.{item}: pattern occurs {len(hits)}x in input "
                             f"(e.g. '{hits[0]}'); excluded from conditions A/B/C scoring\n")
                else:
                    la.write(f"clean   {pname}.{item}\n")

    rows = []
    cells = defaultdict(lambda: defaultdict(int))
    by_cell = defaultdict(list)
    for line in open(args.raw, encoding="utf-8"):
        r = json.loads(line)
        if r["pair"] not in pairs:
            continue
        pair = pairs[r["pair"]]
        cell = (r["pair"], r["condition"], r["model"])
        by_cell[cell].append(r)
        cells[cell]["n"] += 1
        for item, spec in pair["items"].items():
            if re.search(spec["regex"], r["response"], re.I):
                cells[cell][item] += 1

    with open(os.path.join(args.outdir, "scores.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pair", "condition", "model", "item", "class", "hits", "n",
                    "rate", "ci_lo", "ci_hi", "input_leaked"])
        for (pname, cond, model), c in sorted(cells.items()):
            for item, spec in pairs[pname]["items"].items():
                p, lo, hi = wilson(c[item], c["n"])
                w.writerow([pname, cond, model, item, spec["class"], c[item], c["n"],
                            f"{p:.3f}", f"{lo:.3f}", f"{hi:.3f}",
                            item in leaked[pname] and cond != "D"])
                rows.append((pname, cond, model, item, p, lo, hi, c[item], c["n"]))

    with open(os.path.join(args.outdir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("# Contamination probe summary\n\n")
        f.write("| pair | item | model | A | B (cutoff) | C (redacted) | D (no paper) |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        idx = {(p, c, m, i): (r, lo, hi) for p, c, m, i, r, lo, hi, k, n in rows}
        models = sorted({m for _, _, m, *_ in rows})
        for pname, pair in pairs.items():
            for item in pair["items"]:
                for model in models:
                    def cell(cond):
                        v = idx.get((pname, cond, model, item))
                        if not v:
                            return "--"
                        flag = " *leak*" if item in leaked[pname] and cond != "D" else ""
                        return f"{v[0]:.0%} [{v[1]:.0%}-{v[2]:.0%}]{flag}"
                    f.write(f"| {pname} | {item} | {model} | {cell('A')} | {cell('B')} | "
                            f"{cell('C')} | {cell('D')} |\n")
        f.write("\nA vs B measures prompt-layer cutoff efficacy. A vs C measures identity-keyed "
                "recall. D is the generic-knowledge floor. Items flagged *leak* match the input "
                "paper text and are excluded from contamination claims.\n")

    random.seed(0)
    with open(os.path.join(args.outdir, "adjudication_sample.md"), "w", encoding="utf-8") as f:
        f.write("# Random responses for manual adjudication (5 per cell)\n\n")
        for cell, rs in sorted(by_cell.items()):
            f.write(f"\n## {cell}\n")
            for r in random.sample(rs, min(5, len(rs))):
                f.write(f"\n--- sample {r['sample']} ---\n{r['response'][:1500]}\n")

    print(f"scored {sum(c['n'] for c in cells.values())} samples over {len(cells)} cells")
    print(f"leaked items: " + str({k: sorted(v) for k, v in leaked.items()}))


if __name__ == "__main__":
    main()
