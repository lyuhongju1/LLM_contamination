# Hindsight-Contamination Probe Kit and Atlas Dataset
Data, code, prompts, and pre-registration for "Measuring Hindsight Contamination in
Language Models for Particle Detector Design" (H. J. Ryoo).

## What this is
A pre-registered measurement of how often bare language models, given a historical
detector paper or a two-line generic description, propose the technologies and
successor projects the collaborations actually adopted. Ten baseline-to-upgrade
pairs, four conditions, two models, N=20 per cell, 1,600 final samples.

## Layout
- PREREGISTRATION.md   frozen design plus dated Amendments 1-3 (read the amendments;
                       they document a retired backbone, an invalidated first sweep,
                       and the quality controls added in response)
- keys.json            frozen answer keys, redaction patterns, generic descriptions
- code/                runners (interactive, parallel, batch), corpus fetcher, scorer
- corpus/              baseline paper texts (see PACKING_CHECKLIST if incomplete)
- prompts/             all 40 rendered prompts, verbatim (see PACKING_CHECKLIST)
- data/raw_v1_superseded.jsonl   first sweep, invalidated by output truncation
                                 (99.75 percent capped at 1,200 tokens); preserved
- data/raw_v2.jsonl    reported dataset; every record carries prompt_sha256, model,
                       usage, stop_reason, batch id; includes the QC resamples
- data/leakage_audit.txt, data/batch_state.json, data/atlas_scores_v2.csv
- analysis/analyze.py  reproduces the replacement rule, audit, scores, and figures

## Reproduce
python analysis/analyze.py   (from this directory; requires matplotlib)
Verification without trust: prompt hashes in the logs match sha256 of prompts/;
sample timestamps postdate the amendment dates in PREREGISTRATION.md; the leakage
audit is recomputable from corpus/ and keys.json.

## License and citation
Code under the MIT License. Data and text under CC-BY-4.0. Cite via CITATION.cff
(DOI minted on Zenodo deposit).
