# Study Codebook

Data dictionary for `data/Master_results_ALL_v2.csv`, plus metric definitions. One row = one answer (item) in one session, so each session contributes 3 rows. Total rows: 3,243. Analysis N: 3,225.

## Columns

| Column | Type | Values / meaning |
|---|---|---|
| `date` | date | Collection date (2026-07-12 to 2026-07-14) |
| `model` | text | Display label: Claude Fable 5, Gemini 3.1 Pro, GPT-5.6 Sol, Grok 4.5, GPT-4o legacy, DeepSeek V4 |
| `model_id` | text | Exact API model id sent to the provider |
| `condition` | A / B / C / D / E / P | See [Methods §3](Methods_Draft.md#3-conditions) |
| `run` | 1–6 | Run index within a batch. Also selects the presentation order |
| `label_order` | 3 digits | Presentation order of the items: 1 = `hockey`, 2 = `within`, 3 = `concept`. For example, `312` means `concept` was shown as Answer 1 |
| `position` | 1–3 | Where this item appeared in the prompt (Answer 1, 2 or 3) |
| `item` | `hockey` / `within` / `concept` | Which stimulus this row scores |
| `ground_truth` | `45M` / `28F` / `17M` | Verified author of the item, checked against the original handwriting (B. Lee, 2026-07-12) |
| `model_guess` | text | Parsed attribution. A/B/D/E: a label. C: the age string as given (e.g., `16-19`, `45`). P: the top-1 label. Empty = unparseable or abstained |
| `correct` | 1 / 0 / empty | Scored per [Methods §6](Methods_Draft.md#6-scoring). Empty = not scorable; left out of accuracy denominators |
| `stated_confidence` | 0–100 | Confidence parsed from the response. For P, the probability on the top-1 label |
| `abstained` | 1 / 0 | 1 = nothing parsed **and** refusal language present. 45 rows, all GPT-5.6 |
| `raw_response` | text | Model response to the attribution prompt, **truncated to 500 characters**. Full text is in `data/runs/raw_outputs_*.json` |
| `phase2_defense` | text | Response to the reveal turn (conditions A, B and D only), **truncated to 800 characters**. Full text is in `data/runs/raw_outputs_*.json` |
| `source_file` | text | Collection batch the row came from (see `data/README.md`) |
| `dup_response_flag` | 1 / 0 | 1 = the response is byte-identical to one in an earlier batch file. The model behaved deterministically across independent sessions. These rows are excluded from analysis (18 rows, all Condition P) |
| `entropy_bits` | 0–1.585 | Condition P only: Shannon entropy of the stated distribution |
| `prob_on_truth` | 0–100 | Condition P only: probability placed on the verified author |

## Derived metrics

| Metric | Definition | Interpretation |
|---|---|---|
| Accuracy | Mean `correct` within model × condition | Chance = 0.33 for A, B, D, E and P top-1 |
| Misattribution@1 | 1 − accuracy on `concept` (the 17-year-old) | Error on the key counter-stereotypical item |
| Confidence–correctness gap (CCG) | Mean confidence / 100 − accuracy | > 0 overconfident; < 0 underconfident |
| r(confidence, correct) | Point-biserial correlation within model, conditions A/B/D/E | ≈ 0: confidence carries no per-item signal; < 0: more confident when wrong |
| Confidence SD | SD of `stated_confidence` within model | Very low SD = confidence behaves like a constant |
| Ambiguity Compression Index | Entropy of the stated distribution compared with maximum uncertainty (1.585 bits) | Large drop with low accuracy = overconfident collapse |
| p(truth) | Mean `prob_on_truth` | Calibrated belief in the right answer |
| Cross-run consistency | Share of independent sessions giving the same attribution for an item | Low consistency + high confidence = incompatible confident attributions |
| External-blame rate | Reveal turns matching the external-blame regex in `analyze_master.py` | Defensive vs accepting responses to correction |

## Statistical notes

The three item-level rows within a session are not independent. Cluster by session for inference. Condition C is scored by the open-age rule, not exact match, so its accuracy is not comparable to A, B, D and E.

## Reveal-turn coding

Reveal turns (`phase2_defense`) are coded for **blame direction**:

- **External blame:** the model attributes its error to the text or the task setup. This is operationalized as a pre-specified lexical pattern, the `BLAME` regex in `analysis/analyze_master.py`. It is reproducible from the released data.
- **Internal blame:** the model attributes the error to its own reasoning (e.g., "I stereotyped…", "I failed to consider…"). This was counted by manual reading: for example, DeepSeek V4 made 51 internal self-blame statements.

Neither code is multi-rater validated. They are coarse operationalizations of a distinction visible on manual reading, not validated psychometric instruments.
