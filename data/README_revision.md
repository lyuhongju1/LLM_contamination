# Revision data (Amendments 7–10)

All files are append-only JSONL with one record per API response. The final record for a sample is the one with the largest `max_tokens` (the Amendment 3 resample rule). Prompt hashes refer to the rendered prompts in `prompts/`, `prompts_paraphrase/`, and `prompts_amend9/`.

| File | Amendment | Contents | Status |
|---|---|---|---|
| `raw_paraphrase.jsonl` | 7 | Templates P1, P2 (A, B, D; Sonnet 4.5/4.6; N=50) and the extended-thinking arm `T` (original templates, 8 pairs, N=20). Thinking text in `thinking`; only `response` is scored | scored |
| `raw_models.jsonl` | 8 | Original 50 prompts on claude-sonnet-5, claude-haiku-4-5, claude-opus-4-5 | scored |
| `raw_amend9_ab.jsonl` | 9 (a, b) | Templates P3, P4 (A, B, D) and length control K5, K15 (A, D), Sonnet 4.5/4.6, N=50 | scored |
| `raw_amend9_c_superseded.jsonl.gz` | 9 (c) | Newest-generation run with default reasoning; 94% truncated at the cap | **superseded, not scored** (Amendment 10) |
| `raw_amend10.jsonl` | 10 | Rerun of 9(c) with minimum reasoning per model and a 16,000-token cap; `thinking_setting` and `thinking_tokens` recorded | scored |
| `*_batch_state.json` | 7–10 | Message Batches API batch ids, for audit | — |

Amendment 9 (d) also registered a secondary concept-level scoring by a language-model judge (rubric in `judge_rubric.json`, runner in `code/run_judge.py`). It was run, but its validation against blind hand labels was not completed, so it is not used in the revision and its outputs are not released here. The regex scores are the only measure reported.

Scoring scripts are in `analysis/revision/`; result tables are in `revision/`. `analysis/revision/score_round3.py` produces `revision/round3_results.md` (nine-model counts over independent units and post-baseline items, response lengths, the false-negative check on low cells, and the threshold sensitivity of the low-item count) and `revision/round3_fn_snippets.md`; these analyses are exploratory and change no frozen score. The dating of answer-key items (referee point 1) is in `revision/dating_table.md`, and its independent re-check is in `revision/dating_verification.md`.
