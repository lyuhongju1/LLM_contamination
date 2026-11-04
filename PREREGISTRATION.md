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

---
## AMENDMENT 4 (2026-08-02, after v2 sampling, before any distractor scoring)
Motivated by external review: hit-based scoring lacks a specificity denominator. A frozen distractor set (distractor_keys.json) of twenty items, two per pair, specifies technologies that were plausible candidates at each baseline's date and were not adopted in the documented upgrade. The set was specified after sampling and before any distractor scoring; because scoring is mechanical and the responses predate the set, the operative freeze point is before scoring, and this timing is disclosed. The same leakage-audit rule applies; audit status at scoring time: darkside and protodune distractors audited clean, remaining eight pairs pending the local corpus audit, with the note that the reported conclusions are robust in direction to the pending audits.
Additional disclosures adopted in this amendment: (1) The condition-D generic descriptions were written by the author simultaneously with the answer keys and not blind to the documented outcomes; several contain de-identified specification detail (for example, photosensor type) that may prompt the adopted answer. The direction of this bias inflates condition-D availability, which is conservative for the no-evidential-weight conclusion and anticonservative for any reading of condition D as a pure class baseline; condition D is to be interpreted accordingly. (2) The class-wise-suppression mechanism observation rests on one strong and one weak instance and is downgraded to a stated hypothesis with a discriminating test: a constructed battery of pre-cutoff successor-associated items against post-cutoff items lacking successor branding. (3) A cross-vendor extension on locally hosted open-weight models over the identical rendered prompts is planned; pairs whose prompts exceed local context limits may be run as a documented subset.

### Amendment 4 completion note (2026-08-02)
The distractor leakage audit was completed across all ten baselines using the deposited corpus texts. No distractor item matches any baseline text. The pending-status and direction-robustness language of Amendment 4 is superseded by this completed result.

### Amendment 4 execution note (2026-08-02)
The planned cross-vendor open-weight run is executed on identical open weights via a hosted OpenAI-compatible inference endpoint instead of local hosting, for compute reasons. Weights, prompts, sampling temperature, N, and schema are unchanged; the execution venue is recorded per sample in a backend field.

---
## AMENDMENT 5 (2026-08-02, before any extension sampling)
The Anthropic-model sweep is extended uniformly from N=20 to N=50 per cell, motivated by interval resolution (95 percent Wilson half-widths of roughly 20 points at mid-range rates under N=20, roughly 13 under N=50) following external review of interval-limited contrasts. The extension applies to every cell identically and independently of observed outcomes. The pre-registered N=20 results remain the primary confirmatory analysis; the N=50 results are reported as the extended analysis, with any qualitative disagreements between the two disclosed explicitly. Execution, QC, and resampling rules of Amendment 3 apply unchanged to extension samples (batch API, 4,000-token cap, stop reasons recorded, single 8,000-token resample for capped responses). The open-weight cross-vendor arm targets the same N=50 where compute allows, with its realized N stated.

---
## AMENDMENT 6 (2026-08-05, before any battery scoring and before D-prime sampling)
Two additions responding to external review.
(1) MECHANISM BATTERY, scored on the existing N=50 condition A and B responses with keys frozen here before scoring. Class P items are technologies or names first described BEFORE the pair's cutoff year yet saliently associated with the successor program: p_lz for the lux pair, regex "\blz\b|lux[\s-]?zeplin" (LZ collaboration formed 2012, cutoff 2013), joining the already-measured DarkSide-20k (2017, cutoff 2018) and X-ARAPUCA (2018-2019, cutoff 2021). Class Q items are named programs first described AFTER the pair's cutoff and NOT the pair's successor: q_xlzd for darkside, regex "\bxlzd\b" (2021, cutoff 2018); q_cupid for gerda, regex "\bcupid\b" (2015, cutoff 2013); q_dayabay_juno for sno, regex "daya[\s-]?bay|\bjuno\b" (2006 and 2013, cutoff 2000); q_ce for aligo, regex "cosmic explorer" (2019, cutoff 2015). Dates are stated to the author's best knowledge and any correction will be disclosed. Predictions, frozen: date-level compliance retains P under condition B and suppresses Q; association-level compliance suppresses P (successor-branded) and is indifferent to Q. The same leakage audit gates every item.
(2) CONDITION D-PRIME: a spec-stripped one-line description per pair (all identifying specification detail removed, retaining only class and physics goal), sampled at N=20 per pair and Claude model via one batch, to bound the concern that condition D's specification detail prompts the adopted answer. The descriptions are recorded in dprime_descs.json at amendment time; they remain author-written and non-blind, which stays disclosed. If saturated items persist on D-prime, the specification-prompting concern is empirically bounded; divergences are reported per item.

### Amendment 6 completion note, battery (2026-08-05)
The battery leakage audit found all five new items clean against their baseline texts. Scored on the existing N=50 responses: all class Q items suppress to at or near zero under condition B on both models, and the class P item p_lz suppresses on both models despite predating its cutoff, joining DarkSide-20k and VeloPix. Combined with the retention of pre-cutoff technologies and suppression of the post-cutoff inverted-coaxial item, the frozen predictions resolve as: date-level filtering for technologies, association-level suppression for successor-branded names. D-prime sampling remains pending.

### Amendment 6 completion note, D-prime (2026-08-05)
D-prime sampling completed: 400 samples, 397 terminating naturally, three cap-terminated responses scored as-is and flagged. Outcome: rates on the stripped one-line descriptions equal or exceed condition D on nearly every key item, including identity elicitation. The specification-prompting concern is empirically bounded; the direction of the effect is opposite to the concern.

### Amendment 6 completion note, scale contrast (2026-08-06)
The 72B run completed: 1,250 samples, all terminating naturally, paper conditions covering the five shortest baselines under the 32,768-token guard (a smaller subset than the 32B run's, which served at 49,152), condition D complete for all ten pairs. Outcome: salience-default items rise strongly with scale while successor naming, program-specific adopted technologies, and cutoff compliance remain absent, decomposing the frontier-model contamination into a default component that scales and an episodic component that does not appear in this family at either scale.
---
## AMENDMENT 7 (2026-11-03, before any paraphrase sampling)
Motivated by referee report 1 (point 7 and the minor comment on A/D template wording). Each condition so far used a single prompt template, and the A and D templates differ in wording as well as content. This amendment adds a prompt-sensitivity study. It changes no existing score.

(1) TEMPLATES, frozen here. Two paraphrase families, P1 and P2. Within each family the paper condition (A) and the description condition (D) share identical wording apart from the material supplied, removing the A/D wording confound. The cutoff condition (B) prepends a paraphrased cutoff instruction to the family's A template.

P1-A: "Below is the text of a published paper describing a physics instrument.\n\n<material>\n{TEXT}\n</material>\n\nWhat changes to the hardware of the instrument described above would most improve its primary physics performance? Name specific technologies and components."
P1-D: identical, with "Below is a short description of a physics instrument." and {GENERIC} in place of {TEXT}.
P1-B: "Answer as of the end of {YEAR}: use only knowledge that was available by then, and nothing published, proposed, or announced afterward.\n\n" + P1-A.

P2-A: "You are advising the team that operates the instrument described below.\n\n<material>\n{TEXT}\n</material>\n\nRecommend the hardware upgrades you would prioritize to improve the instrument's main physics reach. Be specific about the technologies and components you would use."
P2-D: identical, with {GENERIC} in place of {TEXT}.
P2-B: "Your knowledge cutoff is {YEAR}. Ignore any experiments, collaborations, technologies, or publications that appeared after {YEAR}.\n\n" + P2-A.

{TEXT}, {GENERIC}, and {YEAR} are the same paper texts, condition-D generic descriptions, and years as the original sweep (keys.json). Condition C is not rerun.

(2) SAMPLING, frozen. Conditions A, B, D; both families; all ten pairs; claude-sonnet-4-5-20250929 and claude-sonnet-4-6; N = 50 per cell; temperature 1.0; no extended thinking; 6,000 requests. Execution, QC, and resampling rules of Amendment 3 apply unchanged (Message Batches API, 4,000-token cap, stop reason recorded, single 8,000-token resample of capped responses). The supplied material block may be marked for prompt caching; caching does not change the prompt text, and every rendered prompt is hashed and released.

(3) SCORING, frozen. The frozen keys of keys.json, the same leakage exclusions, Wilson 95 percent intervals, and Newcombe intervals for differences. No key is added or changed.

(4) ROBUSTNESS CRITERIA, frozen before sampling. A finding is reported as robust to wording if it holds under both P1 and P2; otherwise the template dependence is reported as a finding.
 R1 Saturation: each item at or above 90 percent in condition D on the original template remains at or above 75 percent in D under each family.
 R2 Paper-triggered recall: VeloPix on Sonnet 4.5 has A minus D at or above 50 points under each family.
 R3 Cutoff suppression on Sonnet 4.6: DarkSide-20k naming, inverted-coaxial detectors, VeloPix, and SNO+ naming each fall from A to B with a Newcombe interval excluding zero under each family.
 R4 Anchoring: the significantly negative A minus D cells of the original template keep a negative point estimate under each family.
 Per-item rates under all three templates and the maximum across-template shift per item are reported in full, whatever the outcome.

(6) EXTENDED-THINKING ARM, frozen. Motivated by the referee's remark that extended thinking is a built-in loop that could reject proposals drawn from the backbone's prior. The original v2 templates, byte-identical to the released prompts (hashes verified), for conditions A, B, and D on eight pairs (darkside, protodune, icecube, lhcb, sno, aligo, gerda, exo200), both models, N = 20 per cell, 960 requests, with extended thinking enabled at a budget of 4,000 tokens, temperature 1.0, and a 12,000-token cap (QC resample once at 16,000). Only the final answer text is scored; the thinking text is recorded and released separately, and the rate at which a key item appears in the thinking but not in the answer is reported as a descriptive measure of rejection. Comparison is against the original no-thinking cells. No robustness threshold is set; the outcome is descriptive and is reported whatever its direction.

(7) DISCLOSURE. The templates were written by the author after seeing the original results. They are fixed here before any paraphrase sample is drawn.

---
## AMENDMENT 8 (2026-11-03, before any sampling on the models named here)
Extends the original protocol to three further Claude models along two axes, to separate generation from scale within one vendor. Motivated by referee report 1 (point 6, and the single-commercial-family limitation) and by the optional tertiary model already named in Amendment 1. No existing data, key, or score is changed.

(1) MODELS. Generation axis at fixed tier: claude-sonnet-4-5-20250929, claude-sonnet-4-6 (existing), and claude-sonnet-5 (new; the generational tertiary of Amendment 1). claude-sonnet-5 is served as an alias without a dated snapshot, so the model string returned by the API is recorded on every sample. Scale axis at fixed generation: claude-haiku-4-5-20251001 (new), claude-sonnet-4-5-20250929 (existing), claude-opus-4-5-20251101 (new).

(2) PROTOCOL, unchanged. The 50 released rendered prompts in prompts/ are sent verbatim after verifying each file's hash against its filename: conditions A, B, C, D at N = 50 and D-prime at N = 20 per pair, 2,200 requests per model, 6,600 in total. Temperature 1.0, no extended thinking, Message Batches API, 4,000-token cap, stop reason recorded, one 8,000-token resample of capped responses (Amendment 3). The paper text may be marked as a prompt-cache prefix; the prompt text is unchanged.

(3) SCORING, unchanged. Frozen keys, leakage exclusions, distractor set (Amendment 4), mechanism battery (Amendment 6), Wilson intervals, Newcombe intervals for differences.

(4) EXPECTATIONS, frozen before sampling. These are stated so that agreement or disagreement is informative; every outcome is reported.
 G1 Generation, cutoff: on claude-sonnet-5, condition B suppresses the four successor-branded items that 4.6 suppressed (DarkSide-20k, LZ, VeloPix, SNO+) at least as strongly as 4.6, and retains pre-cutoff technologies (SiPMs, X-ARAPUCA, SciFi).
 G2 Generation, identity: condition-D successor naming on claude-sonnet-5 is at least as high as on 4.6, pair by pair, for a majority of pairs.
 S1 Scale, defaults: the technology items saturated (at or above 90 percent) in condition D on Sonnet 4.5 are at or above 50 percent on Haiku 4.5.
 S2 Scale, dissociation (from the Qwen 32B to 72B contrast): averaged over condition D, Haiku 4.5 retains a larger fraction of Sonnet 4.5's technology-item rate than of its identity-item (successor_named) rate.
 S3 Scale, upward: Opus 4.5 is at least as high as Sonnet 4.5 on identity items in condition D.

(5) DISCLOSURES. The three models have different documented training cutoffs, and on the scale axis Opus 4.5 was released later than Haiku 4.5 and Sonnet 4.5, so scale and training data are not fully separated; published training cutoffs from the model documentation are reported alongside the results. The models were chosen by the author after seeing results on the existing two models, for the axes stated above, before any sample on them was drawn.

---
## AMENDMENT 9 (2026-11-03, before any sampling or judging named here)
Motivated by the Amendment 7 outcome (median across-template shift of 32 points on mid-range items, and a template that cut Sonnet 4.5 response length by a factor of three) and by referee report 1 (points 1, 2, 6 and 7). Four parts. No existing data, key, or score is changed.

(a) TEMPLATE SPREAD. Two further paraphrase families, P3 and P4, frozen in code/run_amend9.py, with A/D wording matched as in Amendment 7 and paraphrased cutoff instructions for B. Conditions A, B, D; all ten pairs; claude-sonnet-4-5-20250929 and claude-sonnet-4-6; N = 50; 6,000 requests. Together with the original template and P1, P2 this gives five templates per cell. Reported per item and model: the mean across the five templates, the between-template standard deviation, and the range. An item is classed wording-robust in a condition if its range across the five templates is at most 30 points.

(b) LENGTH CONTROL. Two families, K5 and K15, asking for exactly 5 or exactly 15 numbered upgrades, with matched A/D wording. Conditions A and D; all ten pairs; both core models; N = 50; 4,000 requests. Reported per item: the K15 minus K5 difference with a Newcombe interval. An item is classed breadth-sensitive if K15 minus K5 is at least 30 points; otherwise breadth-robust. Expectation, frozen: saturated items (at or above 90 percent in D on the original template) are breadth-robust; named paper-triggered items such as VeloPix are breadth-sensitive.

(c) NEWEST GENERATION. claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5, and claude-fable-5-1 on the 50 released prompts verbatim (hash-verified), conditions A, B, C, D at N = 50 and D-prime at N = 20, 8,800 requests, temperature 1.0, no extended thinking, Amendment 3 execution and QC rules. These are served as aliases; the returned model string is recorded per sample. Expectations, frozen: S1 to S3 of Amendment 8 are re-tested on the Haiku 5.5, Sonnet 5.5, Opus 5.5 ladder; G1 and G2 of Amendment 8 are re-tested with Sonnet 5.5 as the newest Sonnet. Fable 5.1 is reported descriptively, with no expectation, because the author has no basis for placing it on either axis.

(d) CONCEPT-LEVEL JUDGE. Every final response in the released logs and in parts (a) to (c) is scored by claude-opus-5-5 against the frozen rubric judge_rubric.json, which defines for each of the 30 adopted items and 20 distractors a concept criterion (the response proposes the substance, in any wording) and a named criterion (it also uses the specific name). Mentions as existing equipment, background, or rejected options do not count. One judge call per response covers the five items of its pair; the judge sees only the response, the instrument line, and the rubric, and is told not to use its own knowledge of the historical outcome. The judge is run without a temperature setting because the model does not accept one. The regex scores remain the primary, pre-registered measure; the judge scores are reported alongside them as a secondary measure, never in place of them.
Validation, frozen: the author hand-labels, blind to the judge's verdict, a random sample of 200 response-item judgments stratified to contain 100 judge-positive and 100 judge-negative concept verdicts across all pairs and sources. Reported: agreement and Cohen's kappa for concept and for named, and judge-regex agreement on the full set. If kappa for concept is below 0.6, the judge scores are reported as unreliable and not interpreted further.
Pilot disclosure: before this amendment, the judge pipeline was run on 60 existing responses to test parsing and the API configuration; the rubric text below was not changed after the pilot except where stated in the pilot note appended to this amendment.

(e) DISCLOSURE. Parts (a) to (d) were designed after seeing the Amendment 7 and 8 results. Every outcome is reported whatever its direction. The judge model is from the same vendor as most evaluated models, which is disclosed as a limitation.

### Amendment 9 pilot note (2026-11-03, before freezing)
The judge pipeline was piloted on 60 existing responses. claude-opus-5-5 rejects a temperature setting, so the judge runs without one. 58 of 60 responses parsed; the two failures were a JSON answer truncated at the 600-token cap and one empty answer, so the cap was raised to 2,000 tokens. No rubric text was changed. Pilot agreement with the regex: 252 of the 290 judgments from the 58 parsed responses agree on presence. Of 16 regex-positive, judge-negative cases, inspection showed mentions rather than proposals (e.g., "exceeding far detector specs", "demonstrated in SNO+"); of 22 regex-negative, judge-positive cases, several were proposals phrased outside the frozen expressions (e.g., removal of the L0 hardware trigger) and a few looked like judge over-reach (e.g., "segmented photon collection" read as segmented germanium). The pilot verdicts are not used in any analysis.

---
## AMENDMENT 10 (2026-11-03, after Amendment 9 part (c) sampling, before any scoring or judging of it, and before any rerun)
Quality control on Amendment 9 part (c) found that all four newest-generation models reason internally by default. Every one of their 8,800 responses carries hidden reasoning tokens (median 1,978 to 2,513 per response), contrary to the "no extended thinking" specification, and the reasoning consumed most of the 4,000-token cap: 8,288 of 8,800 responses (94 percent) stopped at the cap, mid-answer. As with the first sweep (Amendment 3), detection of a key item in a truncated answer cannot be a false positive, but absence claims and all cross-model comparisons are unsupportable on these data. No score was computed on them before this amendment.

(1) The Amendment 9 part (c) responses are declared superseded. They are preserved and released, together with 3,499 of their capped responses already resampled at 8,000 tokens before the defect was diagnosed; the remaining capped responses are not resampled. They are not scored for any reported result.

(2) RERUN, frozen. Part (c) is rerun on the same 50 released prompts, models, conditions, N, and temperature, with the minimum reasoning each model accepts, verified by test calls on 2026-11-03: claude-haiku-5-5 with thinking disabled; claude-sonnet-5-5 with thinking type "between_tools", which the API documents as no thinking before responding; claude-opus-5-5 and claude-fable-5-1 with adaptive thinking at effort "low", the lowest level offered, because these two models do not allow reasoning to be disabled. The output cap is 16,000 tokens, with one resample at 32,000 tokens for capped responses. Hidden reasoning tokens, and any reasoning text returned, are recorded per sample; only the final answer text is scored.

(3) DISCLOSURE. Opus 5.5 and Fable 5.1 results therefore include low-effort reasoning (about 700 to 1,300 tokens in test calls), unlike every other model in the study. The extended-thinking arm of Amendment 7 found that reasoning changed Sonnet 4.5 and 4.6 item rates by only a few points on average, which bounds but does not remove this difference. Expectations S1 to S3 and G1 to G2 as re-tested under Amendment 9 are unchanged; the S3 contrast (Opus 5.5 against Sonnet 5.5) is flagged as confounded by reasoning.

(4) AMENDMENT 9 PARTS (a) AND (b) are unaffected (claude-sonnet-4-5 and claude-sonnet-4-6 returned no reasoning tokens). Their 526 capped responses are resampled once at 8,000 tokens under Amendment 3, unchanged.

(5) JUDGE. The judge (part d) is applied to the rerun responses, not to the superseded ones.
