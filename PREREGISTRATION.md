# Pre-Registration: Measuring Hindsight Contamination in LLM Backbones for Detector Design
### Frozen before any model sampling. Companion to run_probe.py / keys.json / score_probe.py.

## Research questions
RQ1. When given only a historical detector paper, at what rate do bare language models (no tools, no simulation) propose the specific technologies and successor projects the collaboration actually adopted afterward?
RQ2. Does a prompt-level knowledge-cutoff instruction reduce that rate? (Prompt-layer cutoffs are the enforcement mechanism used by current agentic systems; efficacy is unmeasured.)
RQ3. Is the recall keyed to experiment identity? (If redacting names collapses the rate, contamination operates through recognition of the specific instrument.)

## Design
Between-condition sampling battery. Conditions:
- A: paper text + upgrade request (baseline contamination measurement)
- B: A + explicit cutoff instruction pinned to the paper's publication year
- C: A with identity-redacted paper text
- D: no paper; generic physical description of the instrument class (generic-knowledge floor)

Primary contrast for RQ1: condition A item rates vs condition D. RQ2: A vs B. RQ3: A vs C.

## Materials
Paper pairs (baseline publication -> documented upgrade path). Two pairs ship with the kit, drawn from the public GRACE data release so that the probe inputs are byte-identical to what a deployed agent ingested; two optional pairs extend breadth.
1. DarkSide-50 (arXiv:1802.07198, 2018) -> DarkSide-20k. Frozen items: successor_named (DarkSide-20k), sipm_adoption, veto_upgrade_gd.
2. ProtoDUNE-SP (arXiv:2108.01902, 2021) -> DUNE FD photon detection. Frozen items: xarapuca, coverage_increase. (successor_named EXCLUDED by leakage audit: "far detector" occurs in input.)
3. Optional: XENON1T (arXiv:1708.07051) -> XENONnT. 4. Optional: LUX (arXiv:1211.3788) -> LZ.

## Leakage rule (frozen)
An item whose regex matches the input paper text is not evidence of recall and is excluded from contamination scoring in conditions A/B/C (it remains reportable for D). The audit is automated (score_probe.py) and its output ships with the results. Audit result at freeze time: darkside items all clean; protodune.successor_named leaked and excluded; protodune.xarapuca and coverage_increase clean. Notably, neither "SiPM" nor "X-ARAPUCA" occurs anywhere in the respective input papers, making these strong recall markers.

## Sampling plan
N = 20 samples per (pair x condition x model), temperature 1.0, max_tokens 1200. Primary model: claude-sonnet-4-20250514, the pinned backbone of the public GRACE benchmark runs, so measured floors attach directly to a deployed system. Secondary models as access permits (a current Claude model; one non-Anthropic model if available). Estimated cost for two shipped pairs x 4 conditions x 20 samples x 2 models: roughly 8M input tokens, order $30-60 at current pricing.

## Metrics and analysis (frozen)
Per cell: item hit rate with Wilson 95% CI. Derived quantities: identity-recall rate (successor_named class), technology-recall rate (technology_recall class), cutoff-compliance delta (A minus B), identity-dependence delta (A minus C), contamination excess over generic knowledge (A minus D). No hypothesis tests beyond CIs; this is a measurement study. Manual adjudication of 5 random responses per cell against the regex verdicts; regex/manual disagreement rate reported. Negative results (e.g., cutoff instructions fully effective, or no excess over D) are reportable outcomes and will be published.

## Interpretation guardrails (frozen)
High recall establishes the contamination FLOOR that any agent built on the backbone inherits; it does not establish that any particular agent's output used recall. Low recall under D with high recall under A indicates paper-triggered retrieval; comparable rates under D indicate the knowledge is generic to the instrument class. These readings are fixed here to prevent post hoc reframing.

---
## AMENDMENT 1 (2026-07-31, before any sampling)
Discovery: the pre-registered primary model claude-sonnet-4-20250514, the pinned backbone of the GRACE benchmark runs (January 2026), is no longer served by the Anthropic API. The oldest available model at amendment time is claude-opus-4-1-20250805. The retirement occurred within roughly six months of the agentic runs it powered.

Amended model plan: primary claude-sonnet-4-5-20250929 (nearest same-family snapshot; the only available Sonnet predating the GRACE runs); secondary claude-sonnet-4-6; optional tertiary claude-sonnet-5 for a generational trend. All other design elements (pairs, conditions, N, keys, metrics, guardrails) unchanged.

Amended interpretation: measured rates characterize the contamination floor of the deployed backbone's nearest accessible relatives, not the backbone itself. The retirement is itself a reportable reproducibility finding: exact-backbone replay of the audited agentic system was already impossible at study time, which bounds what model-string pinning can guarantee and motivates archived-weight or open-weight backbones for reproducible agentic science.

---
## AMENDMENT 2 (2026-08-01, before any sampling on added pairs)
Corpus expanded from 2 active pairs to 10: darkside, protodune, xenon1t, lux, icecube (arXiv:1612.05093 -> Gen2/Upgrade), gerda (1212.4067 -> LEGEND), exo200 (1202.2192 -> nEXO), lhcb (1412.6352 -> Upgrade I), sno (nucl-ex/9910016 -> SNO+), aligo (1411.4547 -> A+). Item keys for the added pairs are recorded in keys.json at amendment time and are FROZEN, subject only to the automated leakage audit, which runs on each fetched paper text before any sampling of that pair and mechanically excludes items matching the input. Rationale for expansion: across-pair breadth, not per-pair sample size, powers the study's generalization claim.
Integrity rules restated and binding: (1) the sampling API provides no random seed; run-level bitwise reproducibility is out of scope and the raw log with prompt hashes is the reproducibility artifact; (2) stopping rule is fixed at N=20 per cell with no data-dependent extension; (3) every pair on which any sampling occurs is reported; item exclusions may come only from the automated leakage audit; (4) pairs whose leakage audit excludes all items are reported as such rather than silently dropped; (5) the scorer's adjudication subsample seed remains fixed at 0.

---
## AMENDMENT 3 (2026-08-02, after v1 sweep, before v2 sampling)
Quality control on the completed v1 sweep (1,600 samples) found 99.75% of responses terminated at the max_tokens cap of 1,200 rather than at a natural stop; only 1.75% end in sentence-final punctuation. Because detection of a key item within an emitted prefix cannot be a false positive, all v1 hit rates are strict lower bounds; claims of ABSENCE (the selectivity observations) and cross-condition contrasts sensitive to response length are not supportable on v1 data. The v1 log is preserved and will be released as superseded. The v1 schema also omitted stop_reason, the field that detects this failure immediately, and carried latency inconsistently across a mid-run runner change; both defects are disclosed.
V2 sampling plan (frozen): identical prompts, pairs, keys, conditions, N, and temperature; executed via the Message Batches API; max_tokens 4000; every record carries stop_reason, full usage, batch id, and schema_version 2. QC rule: any v2 response with stop_reason max_tokens is resampled exactly once at max_tokens 8000; if it caps again it is scored as-is and flagged. The 40 rendered prompts are published alongside the log. Latency is not defined for batch execution and is recorded as null by design.
