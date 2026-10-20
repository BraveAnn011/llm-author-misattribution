# Which Answer Did the Seventeen-Year-Old Write?
### Author-age misattribution, miscalibrated confidence, and confession without correction in six frontier LLMs

Companion study: [ai-halo-valuation-bias](https://github.com/BraveAnn011/ai-halo-valuation-bias). It uses the same design logic (verified ground truth, counterfactual framing, reveal turns) on context-driven price valuation in vision-language models.

**Author:** Brianne (Sunhwa) Lee, independent researcher · **Data collected:** July 12–14, 2026 · **Status:** write-up in preparation; human baseline not yet run

---

## The question in one paragraph

Three people answered the same handwritten exam question: *"What is happiness? Are you happy?"* Their ages and sexes are verified with written consent: 17M, 28F and 45M. The set is **counter-stereotypical by construction**: the most formal, hedged answer was written by the teenager. Each model was told the three authors and asked which one wrote which answer, with a confidence rating. Chance accuracy is 1/3. We then varied the framing (institutional label, neutral label, pragmatic instruction, open-ended estimate, full probability distribution). We also revealed the truth in-session and coded how each model explained its own errors.

This is a **three-item, single-topic, single-language case study** designed to isolate a mechanism. It is not an estimate of population bias rates. See [Limitations](#limitations).

## Models

| Model (as labelled in data) | API model id | Analysis rows | Sessions |
|---|---|---:|---:|
| Claude Fable 5 | `claude-fable-5` | 486 | 162 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | 309 | 103 |
| GPT-5.6 Sol | `gpt-5.6` | 609 | 203 |
| Grok 4.5 | `grok-4.5` | 603 | 201 |
| GPT-4o (2024; generational anchor) | `gpt-4o` | 609 | 203 |
| DeepSeek V4 | `deepseek-chat` | 609 | 203 |
| **Total** | | **3,225** | **1,075** |

There are 3,243 rows in total. 18 rows flagged as duplicate responses are excluded, leaving the analysis N of 3,225. Per-model N differs because not every model was run in every collection batch; see [`data/README.md`](data/README.md).

## Conditions

| Code | Manipulation | Scoring |
|---|---|---|
| A | Blind matching (three labels given) | Exact label match; chance = 0.33 |
| B | A + institutional label: "community-college biology final exam" | Same as A |
| E | A + neutral label: "a written survey" (control for B) | Same as A |
| D | A + one-paragraph pragmatic instruction (think about audience and register) | Same as A |
| C | Open-ended age estimate, no labels given | Correct if a stated range contains the true age, or a point estimate is within ±3 years |
| P | Full probability distribution over the three labels | Top-1 accuracy, p(truth), Shannon entropy |

All six label orderings are used, giving full positional counterbalancing. Every session is fresh and stateless. In conditions A, B and D a **reveal turn** follows in the same session: the model is given the verified truth and asked to explain the cues it actually relied on ("do not revise history"). Full details are in [`docs/Methods_Draft.md`](docs/Methods_Draft.md).

## Headline results (Condition A, blind matching)

| Model | Accuracy | Mean confidence | Confidence − accuracy | Misattribution of the 17-year-old's answer | r(confidence, correct)* |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 | **0.94** | 0.67 | −0.27 (under-confident) | 0.08 | +0.12 |
| Gemini 3.1 Pro | 0.76 | 0.87 | +0.10 | 0.29 | −0.14 |
| GPT-5.6 Sol | 0.63 | 0.64 | +0.01 | 0.50 | −0.02 |
| Grok 4.5 | 0.35 | 0.73 | +0.38 | 0.81 | −0.21 |
| GPT-4o | 0.25 | 0.86 | +0.60 | 0.81 | −0.27 |
| DeepSeek V4 | 0.23 | 0.88 | +0.65 | 0.90 | +0.02 |

\* Point-biserial correlation, pooled over matching conditions A, B, D and E. Every number in this README is reproduced by `python3 analysis/analyze_master.py data/Master_results_ALL_v2.csv`.

## Key findings

1. **Below chance at high confidence.** Three of six models score at or below chance while reporting 73–88% confidence. DeepSeek V4 scores 0.23, significantly *below* chance (29/126; exact two-sided binomial test against 1/3, p = 0.014). GPT-4o's 0.25 is marginal (p = 0.059), and Grok's 0.35 is indistinguishable from chance (p = 0.71). Accuracy differs strongly by model: χ²(5) = 186.6.
2. **Same text, opposite readings.** Claude assigns the 17-year-old's answer correctly 33/36 times. DeepSeek assigns it to "28F" 25/42 times.
3. **Forced choice masks failure severity.** Without the answer options (Condition C), accuracy on the teenager's answer is 0.00 for Grok, GPT-4o and DeepSeek, and 0.26 for Claude.
4. **An institutional label hurts the strongest model.** "Community-college biology final" drops Claude from 0.94 to 0.69. A neutral label changes nothing (0.94 → 0.94). Institutional metadata is turned into a demographic prior.
5. **Prompting elicits latent capability; it cannot manufacture it.** The pragmatic instruction (D) lifts Claude to 1.00 and GPT-5.6 by 21 points. It does nothing for the bottom three.
6. **Confidence is a per-model trait, not a per-item signal.** Gemini, Grok and GPT-4o are *more* confident when wrong than when right. DeepSeek's confidence has SD = 5.2 across all trials.
7. **Confession without correction.** 1,809 reveal turns were collected. DeepSeek V4 wrote self-critiques naming the cue it had misused (51 internal self-blame statements, hand-coded). It then repeated the identical error, at unchanged confidence, in fresh sessions. See [`docs/Findings_Arc.md`](docs/Findings_Arc.md).
8. **Generational change within one lab.** GPT-4o → GPT-5.6: accuracy 0.25 → 0.63, overconfidence gap +0.60 → +0.01, and abstentions 0 → 45 (GPT-5.6 is the only model that ever abstains).
9. **Meta-finding.** AI-assisted tooling used during the study fabricated a code review, silently swapped the answer key, invented a quotation, and a parser bug produced a false 100%. Human verification caught all of them.

## Limitations

- **Three items, one prompt, one language.** The design isolates a mechanism (register read as age). It does not estimate how often models misattribute authors in general.
- **No human baseline yet.** We cannot yet separate "models are wrong" from "the task is hard for people too." A rater packet is ready ([`docs/Baseline_Packet.md`](docs/Baseline_Packet.md)), but the baseline has not been run.
- **Unequal per-model N.** Gemini 3.1 Pro has about half the rows of most models, and Claude about 80%. Per-model estimates for those two are less precise.
- **Pooled collection batches.** Data come from several runs of the evolving runner (v2 to v9.1) over three days. Conditions D, E and P were added in later batches, so their cells are smaller.
- **Provider defaults.** No temperature was set; each provider's default sampling was used. Model behavior may change after July 2026.
- **Not pre-registered** with a public registry.
- **Heuristic coding** of reveal turns was done by a single coder and has not been multi-rater validated.

## Repository structure

```
scripts/run_experiment.py     experiment runner (multi-provider; conditions A–E, P; reveal turn)
scripts/keys_template.json    copy to keys.json (git-ignored) and add your API keys
analysis/analyze_master.py    reproduces every number in this README
data/Master_results_ALL_v2.csv   canonical analysis dataset (one row per item per session)
data/runs/                    per-batch results and raw model outputs, kept for audit
docs/Methods_Draft.md         full methods
docs/Findings_Arc.md          findings with the exact analysis behind each
docs/Study_Codebook.md        data dictionary and metric definitions
docs/Baseline_Packet.md       human-rater materials (not yet run)
human-baseline/PROTOCOL.md    human-baseline protocol and status
```

## Reproduce

```bash
python3 analysis/analyze_master.py data/Master_results_ALL_v2.csv
```

No dependencies beyond the Python 3 standard library are needed for the analysis. The runner needs `requests` and your own API keys.

## How this was built

The runner, parsers and analysis scripts were written with Claude Code and checked by hand. Ground-truth labels were verified against the original handwritten papers (July 12, 2026). The verification step caught several AI-tooling errors (finding 9). Those checks are now part of the pipeline: duplicate-response flagging, audits of raw logs instead of trusting exit codes, and hand-checked samples of parsed output.

## Further reading

- [Six AI Models. Six Ways to Fail. (Substack)](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu)

## Citation and license

Lee, B. (S.) (2026). *Which answer did the seventeen-year-old write? Author-age misattribution, miscalibrated confidence, and confession without correction in six frontier LLMs.* GitHub: BraveAnn011/llm-author-misattribution.

Code: MIT ([LICENSE](LICENSE)). Data and text: CC BY 4.0. Stimulus texts are used with the authors' written consent.
