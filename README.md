# Hindsight-Contamination Probe Kit and Atlas Dataset

Data, code, prompts, and pre-registration for "Measuring Hindsight Contamination in
Language Models for Particle Detector Design" (H. J. Ryoo).

## What this is

A pre-registered measurement of how often bare language models, given a historical
detector paper, a generic description, or a single stripped line, propose the
technologies and successor projects the collaborations actually adopted. Ten
baseline-to-upgrade pairs; conditions A (paper), B (paper plus knowledge-cutoff
instruction), C (redacted paper), D (generic description), and D-prime (one-line
description); two Claude models at N=50 per cell (N=20 pre-registered primary,
N=50 extended per Amendment 5); a frozen twenty-item distractor set; a mechanism
battery; and an open-weight cross-vendor arm (Qwen2.5 at 32B and 72B, run on NCSA
Delta under NSF ACCESS allocation bgde-delta-gpu). 8,850 raw samples in total
across all arms, including the superseded first sweep.

## Read this first

PREREGISTRATION.md is the study's ledger: the frozen design followed by dated
Amendments 1-6 with their completion notes. The amendments document, in order: a
retired backbone, an invalidated first sweep and the quality controls added in
response, the distractor set and its completed leakage audit, the uniform N=50
extension, and the mechanism battery, D-prime condition, and open-weight scale
contrast. Every deviation and every disclosed attenuation lives there.

## Layout

- PREREGISTRATION.md    frozen design plus dated Amendments 1-6 and completion notes
- keys.json             frozen answer keys, redaction patterns, generic descriptions
- distractor_keys.json  frozen plausible-but-unadopted distractor set (Amendment 4)
- dprime_descs.json     frozen one-line stripped descriptions (Amendment 6)
- adjudication_report.md  systematic 80-sample adjudication of headline cells
- code/                 all runners (interactive, parallel, batch, extension,
                        local/Ollama, hosted open-weight, D-prime), corpus fetcher,
                        scorers, SLURM job scripts
- corpus/               baseline paper texts, plain and redacted
- prompts/              all 50 rendered prompts, verbatim (40 A-D, 10 D-prime)
- data/raw_v1_superseded.jsonl  first sweep, invalidated by output truncation
                                (99.75 percent capped); preserved as disclosed
- data/raw_v2.jsonl     Claude sweep, N=50 per cell with QC resamples (dedupe by
                        max_tokens per sample id when analyzing)
- data/raw_local.jsonl  open-weight arm, Qwen2.5-32B and 72B via Ollama on Delta
- data/raw_dprime.jsonl D-prime condition, both Claude models
- data/leakage_audit.txt  adopted-key audit output (four excluded items)
- data/atlas_scores_v3_n50.csv  scored atlas, per-cell Wilson intervals (extended)
- data/atlas_scores_v2.csv      scored atlas at the pre-registered N=20 (primary)
- data/qwen_scores.csv          open-weight arm scores
- analysis/analyze.py   regenerates every number and figure (N-flexible)
- atlas_ollama_*.log    SLURM job transcripts of the cluster runs

## Reproducing

python analysis/analyze.py from the repository root rebuilds the scored atlas and
both figures from the raw logs. python code/score_distractors.py reproduces the
distractor audit and rates. Sampling is seedless by API design; the raw append-only
logs with prompt hashes and stop reasons are the reproducibility artifact.

## Funding and independence

Claude sampling used Anthropic AI for Science API credits; the open-weight arm ran
on NSF ACCESS allocation bgde-delta-gpu (Delta, NCSA). Neither funder had any role
in design, analysis, or the decision to publish.
