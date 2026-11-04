# Which Answer Did the Seventeen-Year-Old Write?
### Author-age misattribution, miscalibrated confidence, and non-corrective self-explanation in six frontier language models

**Paper:** Lee, B. (2026). arXiv:[2610.31946](https://arxiv.org/abs/2610.31946) [cs.CL]
**Author:** Brianne (Sunhwa) Lee, independent researcher · **Data collected:** July 12–14, 2026 · **Human baseline:** not yet run

Companion study: [ai-halo-valuation-bias](https://github.com/BraveAnn011/ai-halo-valuation-bias) (arXiv:[2610.34591](https://arxiv.org/abs/2610.34591)). It uses the same design logic (verified ground truth, counterfactual framing, reveal turns) on context-driven price valuation in vision-language models.

This repository holds the data, code and raw model outputs for the paper. **Where this README and the paper differ, the paper is authoritative.** Every statistic in the paper is reproduced by `analysis/stats_paper.py`.

---

## The question in one paragraph

Three students answered the same handwritten exam prompt: *"What is happiness? Are you happy?"* Their ages and genders, recorded at collection, are 17M, 28F and 45M. The set is **counter-stereotypical by design**: the most formal, hedged answer was written by the teenager. Each model was given the three answers and the three labels and asked to match them one to one, with a confidence rating. Chance is one correct label out of three. We then varied the framing (institutional label, neutral label, audience-awareness instruction, open-ended estimate, full probability distribution). In conditions A, B and D we also revealed the truth within the session and recorded how each model explained its errors.

This is a **three-item, single-topic, single-language case study** designed to isolate a mechanism. It is not an estimate of population bias rates. See [Limitations](#limitations).

## Models

| Model (as labelled in data) | API model id | Analysis rows | Sessions analysed |
|---|---|---:|---:|
| Claude Fable 5 | `claude-fable-5` | 486 | 162 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | 309 | 103 |
| GPT-5.6 Sol | `gpt-5.6` | 609 | 203 |
| Grok 4.5 | `grok-4.5` | 603 | 201 |
| GPT-4o (2024; earlier-generation anchor) | `gpt-4o` | 609 | 203 |
| DeepSeek V4 | `deepseek-chat` | 609 | 203 |
| **Total** | | **3,225** | **1,075** |

The full grid produced **1,081 API sessions** and 3,243 item rows (three per session). Six sessions (18 rows, all in Condition P) were flagged for duplicated model responses and excluded, leaving 3,225 rows from 1,075 sessions (paper §3.4). Per-model N differs because not every model was run in every collection batch; see [`data/README.md`](data/README.md).

## Conditions

| Code | Manipulation | Scoring |
|---|---|---|
| A | Blind matching (three labels given) | Label match; chance mean = 1 correct per session |
| B | A + institutional label: "a community-college biology final" | Same as A |
| E | A + neutral label: "a written survey" (control for B) | Same as A |
| D | A + one audience-awareness instruction (writers adapt register to their reader) | Same as A |
| C | Open-ended age estimate, no labels given | Correct if a stated range contains the true age, or a point estimate is within ±3 years |
| P | Probability distribution over the three labels | Top-1 accuracy, p(truth), Shannon entropy |

All six presentation orders are used, giving full positional counterbalancing. Every session is fresh and stateless. In conditions A, B and D (603 sessions) a **reveal turn** follows in the same session: the model is given the true labels and asked to explain what led to its original assignments. Full details are in [`docs/Methods_Draft.md`](docs/Methods_Draft.md).

## Headline results (Condition A, blind matching; paper Table 1)

| Model | Accuracy [95% CI] | Mean confidence | Confidence − accuracy | Misattribution of the 17-year-old's answer | Mean correct per session (chance = 1) |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 | **0.94** [0.88, 0.97] | 0.67 | −0.27 (under-confident) | 0.08 | 2.83 (p < 0.001) |
| Gemini 3.1 Pro | 0.76 [0.63, 0.86] | 0.87 | +0.10 | 0.29 | 2.29 (p < 0.001) |
| GPT-5.6 Sol | 0.63 [0.54, 0.71] | 0.64 | +0.01 | 0.50 | 1.90 (p < 0.001) |
| Grok 4.5 | 0.35 [0.27, 0.44] | 0.73 | +0.38 | 0.81 | 1.05 (p = 0.758) |
| GPT-4o (2024) | 0.25 [0.19, 0.34] | 0.86 | +0.60 | 0.81 | 0.76 (p = 0.123) |
| DeepSeek V4 | 0.23 [0.17, 0.31] | 0.88 | +0.65 | 0.90 | 0.69 (p = 0.045) |

Accuracy is pooled across items with Wilson 95% intervals. Because one-to-one matching makes the three rows of a session dependent, **tests against chance use session scores** (z-test of the mean session score against 1). Item-level binomial p-values are not used for inference. Reproduce with `python3 analysis/stats_paper.py data/Master_results_ALL_v2.csv`.

## Key findings

1. **At or near chance, at high confidence.** Grok 4.5, GPT-4o and DeepSeek V4 average 0.69–1.05 correct per session against a chance mean of 1, while reporting 73–88% mean confidence. Grok is indistinguishable from chance. DeepSeek's mean session score is below chance (p = 0.045), but its session distribution is not detectably different from chance (p = 0.13), so the paper treats its below-chance performance as *suggestive, not established*. GPT-4o's mean is not detectably below chance (p = 0.12), but 24 of its 42 sessions were entirely wrong (14 expected; distribution p = 0.003). Models differ sharply overall (χ²(5) = 186.6 on item rows; Kruskal–Wallis on session scores H = 84.0, p = 1.2 × 10⁻¹⁶).
2. **Same text, opposite readings.** On the 17-year-old's answer in Condition A, Claude assigns the correct label in 33 of 36 trials. Grok, GPT-4o and DeepSeek mostly assign it to "28F" (22, 25 and 25 of 42).
3. **Forced choice masks the severity.** Without the answer options (Condition C), accuracy on the teenager's answer is 0.00 for Grok, GPT-4o and DeepSeek (n = 42 each), 0.17 for GPT-5.6, 0.26 for Claude and 0.33 for Gemini.
4. **An institutional label hurts the strongest model.** "A community-college biology final" drops Claude from 0.94 to 0.69 (Fisher's exact p < 0.001). The neutral label leaves it at 0.94 (p = 1.000).
5. **An instruction elicits capability that is already there.** The audience-awareness instruction lifts GPT-5.6 from 0.63 to 0.84 (p = 0.002) and moves Claude to ceiling, 72 of 72 (p = 0.082, not detectable at this sample size). No detectable effect for the three weakest models, read as a floor effect.
6. **Confidence is a per-model trait, not a per-item signal.** Confidence correlates positively with correctness only for Claude (r = +0.12, p = 0.032). It correlates negatively for Gemini, Grok and GPT-4o: they are more confident when wrong. DeepSeek's confidence barely varies (SD 5.2 on a 0–100 scale), so it carries almost no per-item information.
7. **Confession without correction.** Reveal turns are coded once per session (603 sessions). External-blame language is rare: 4 of 603 sessions, 3 of them DeepSeek's. In 68 of DeepSeek's 114 explanations the stem *stereotyp-* appears, far more than for any other model, and 108 of 114 open by thanking the user. Yet DeepSeek has the lowest accuracy and highest confidence under blind presentation. Sessions are stateless, so this is not a claim that the model "failed to learn". The narrower point is that fluent self-diagnosis does not track the quality of judgment.
8. **Generational change within one lab.** GPT-4o → GPT-5.6: accuracy 0.25 → 0.63 (p = 2.2 × 10⁻⁹), confidence–accuracy gap +0.60 → +0.01, abstentions 0 → 15 sessions (45 rows; 12 of the 15 under the institutional label). GPT-5.6 is the only model that ever abstains.
9. **Meta-finding.** AI-assisted tooling used during the study produced a fabricated code-review summary, a silently altered answer key, an invented quotation and, through a parser defect, one transient false result. Each was caught by manual verification before release.

## Limitations

Read these before citing the results (paper §6).

- **Three items, one prompt, one language.** The design isolates a mechanism (register read as age). It does not estimate how often models misattribute authors in general.
- **Non-independence.** The three rows of a session are dependent. Tests against chance use session scores; between-condition comparisons and correlations still pool item rows.
- **Low power at the floor.** The null results for the three weakest models are not evidence that context has no effect.
- **No human baseline yet.** A rater packet is ready ([`docs/Baseline_Packet.md`](docs/Baseline_Packet.md)), but no human data have been collected.
- **Uneven cell sizes.** Gemini 3.1 Pro appears in three of the seven batches and Claude Fable 5 is partly missing from two, so their intervals are wider.
- **Lexical coding of reveal turns.** The external-blame flag and the *stereotyp-* count are pattern matches, not multi-rater validated codes. The *stereotyp-* count does not separate self-blame from other uses of the word.
- **Provider defaults.** No temperature was set. Consumer chat products built on the same models may behave differently.
- **Not pre-registered** with a public registry.

## Stimulus texts and consent

The three answers were handwritten extra-credit responses to a community-college biology final, collected in 2025. Each writer recorded an age and gender at collection, and the texts are de-identified in all released materials. The writers signed their answers as part of the class activity; the study idea arose after collection, and the signed originals were later lost. **All three writers have since given written consent for research use and publication.** The consent forms are kept private. No formal ethics review was conducted. The Ethics Statement in arXiv v1 (paper §7) was written before consent was obtained and will be updated in the next version.

## Repository structure

```
scripts/run_experiment.py        experiment runner (multi-provider; conditions A–E, P; reveal turn)
scripts/keys_template.json       copy to keys.json (git-ignored) and add your API keys
analysis/stats_paper.py          reproduces every statistic in the paper (pandas, numpy, scipy)
analysis/analyze_master.py       quick descriptive summary (standard library only)
data/Master_results_ALL_v2.csv   canonical analysis dataset (one row per item per session)
data/runs/                       per-batch results and raw model outputs, kept for audit
docs/Methods_Draft.md            methods as implemented in the runner
docs/Findings_Arc.md             findings with the analysis behind each
docs/Study_Codebook.md           data dictionary and metric definitions
docs/Baseline_Packet.md          human-rater materials (not yet run)
human-baseline/PROTOCOL.md       human-baseline protocol and status
```

## Reproduce

```bash
pip install pandas numpy scipy
python3 analysis/stats_paper.py data/Master_results_ALL_v2.csv     # every statistic in the paper
python3 analysis/analyze_master.py data/Master_results_ALL_v2.csv  # descriptive summary, no dependencies
```

The runner needs `requests` and your own API keys.

## How this was built

The runner, parsers and analysis scripts were written with Claude Code and checked by hand. The verification step caught several AI-tooling errors (finding 9). Those checks are now part of the pipeline: duplicate-response flagging, audits of raw logs instead of trusting exit codes, and hand-checked samples of parsed output.

## Further reading

- [Six AI Models. Six Ways to Fail. (Substack)](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu)

## Citation

Lee, B. (2026). Which Answer Did the Seventeen-Year-Old Write? A Behavioral Case Study of Author-Age Misattribution, Miscalibrated Confidence, and Non-Corrective Self-Explanation in Six Frontier Language Models. arXiv:2610.31946 [cs.CL]. https://arxiv.org/abs/2610.31946

```bibtex
@misc{lee2026misattribution,
  title         = {Which Answer Did the Seventeen-Year-Old Write? A Behavioral Case Study of Author-Age Misattribution, Miscalibrated Confidence, and Non-Corrective Self-Explanation in Six Frontier Language Models},
  author        = {Lee, Brianne},
  year          = {2026},
  eprint        = {2610.31946},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL},
  doi           = {10.48550/arXiv.2610.31946}
}
```

Companion study: Lee, B. (2026). Does the Outfit Change the Price? Context Halo in Vision-Language Model Valuation of an Identical Low-Cost Necklace. arXiv:2610.34591, https://arxiv.org/abs/2610.34591

## License

- Code (`scripts/`, `analysis/`): MIT, see [LICENSE](LICENSE).
- Data and text (`data/`, documentation): CC BY 4.0, see [LICENSE-DATA](LICENSE-DATA).
