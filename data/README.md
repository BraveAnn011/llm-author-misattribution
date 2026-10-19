# Data

## Canonical dataset

**`Master_results_ALL_v2.csv`** is the only file the analysis uses. It has one row per item per session (3 rows per session) and 3,243 rows in total. 18 rows carry `dup_response_flag = 1` and are excluded, leaving the analysis N of **3,225**. Columns are defined in [`../docs/Study_Codebook.md`](../docs/Study_Codebook.md).

## Collection batches (`runs/`)

The master file is the row-for-row concatenation of seven collection batches. Each row's `source_file` column names its batch. The batch files and the raw model outputs (full prompts, responses and reveal-turn text) are kept in `runs/` for audit. They are not needed to reproduce the analysis.

| Batch results | Raw outputs | Date | Conditions | Models | Rows |
|---|---|---|---|---|---:|
| `results_v2.csv` | `raw_outputs_v2.json` | 2026-07-12 | A, B, C | GPT-5.6, GPT-4o, Grok, DeepSeek | 216 |
| `results_v3.csv` | `raw_outputs_v3.json` | 2026-07-12 | A, B, C | + Claude | 270 |
| `results_v4.csv` | `raw_outputs_20260712_v4.json` | 2026-07-12 | A, B, C, D, P | Claude, GPT-5.6, GPT-4o, Grok, DeepSeek | 447 |
| `results_v5.csv` | `raw_outputs_v5.json` | 2026-07-12 | A, B, C, D, P | Claude, GPT-5.6, GPT-4o, Grok, DeepSeek | 450 |
| `results_v7.csv` | `raw_outputs_v7.json` | 2026-07-13 | A–E, P | all six | 639 |
| `results_v7_except_claude.csv` | `raw_outputs_v7_except_claude.json` | 2026-07-13 | A–E, P | all six (Claude partial) | 579 |
| `results_master.csv` | `raw_outputs_20260714.json` | 2026-07-14 | A–E, P | all six | 642 |
| **Total** | | | | | **3,243** |

## Why per-model N differs

Not every model was run in every batch:

- **Gemini 3.1 Pro** appears only in the three batches from July 13–14, giving 309 rows.
- **Claude Fable 5** is absent from the first batch and partial in `v7_except_claude`, giving 486 rows.
- **The other four models** appear in all seven batches, giving 603–609 rows.

Conditions D and P start in the third batch, and E in the fifth, so those cells are smaller than A, B and C. Every analysis is reported per model and per condition, never pooled across models. Cell sizes are printed by `analysis/analyze_master.py`.
