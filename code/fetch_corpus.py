#!/usr/bin/env python3
"""Fetch baseline papers from arXiv and extract text into corpus/.
Usage: pip install pypdf   then   python fetch_corpus.py
Skips pairs whose corpus file already exists."""
import json, os, time, urllib.request
from pypdf import PdfReader

cfg = json.load(open("keys.json", encoding="utf-8"))
os.makedirs("corpus", exist_ok=True)
for p in cfg["pairs"]:
    txt = p["paper_txt"]
    if os.path.exists(txt):
        print(f"have    {p['name']:10s} {txt}"); continue
    aid = p["arxiv"]
    pdf = txt.replace(".txt", ".pdf")
    url = f"https://export.arxiv.org/pdf/{aid}"
    print(f"fetch   {p['name']:10s} {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-fetch/1.0 (academic use)"})
    with urllib.request.urlopen(req, timeout=120) as r, open(pdf, "wb") as f:
        f.write(r.read())
    text = "\n".join((pg.extract_text() or "") for pg in PdfReader(pdf).pages)
    open(txt, "w", encoding="utf-8").write(text)
    print(f"        -> {len(text.split())} words")
    time.sleep(3)  # be polite to arXiv
print("done. Now run:  python score_probe.py   (leakage audit before any sampling)")
