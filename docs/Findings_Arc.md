# Findings Arc

*A guided walk through the findings of [arXiv:2610.31946](https://arxiv.org/abs/2610.31946). Every statistic below is reproduced by `python3 analysis/stats_paper.py data/Master_results_ALL_v2.csv`. Where this page and the paper differ, the paper is authoritative. Condition A = blind matching.*

The arc runs from **what** models get wrong (F1–F3), to **what moves them** (F4–F5), to **whether their self-reports can be trusted** (F6–F7), to **change over time** (F8). It closes with what the study taught about its own tools (F9).

## F1. At or near chance, at high confidence (paper Table 1)

| Model | Accuracy (A) [95% CI] | Mean confidence | Sessions 0/1/3 correct | Mean per session | p (mean vs 1) |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 | 0.94 [0.88, 0.97] | 0.67 | 0/3/33 | 2.83 | < 0.001 |
| Gemini 3.1 Pro | 0.76 [0.63, 0.86] | 0.87 | 2/3/12 | 2.29 | < 0.001 |
| GPT-5.6 Sol | 0.63 [0.54, 0.71] | 0.64 | 4/16/20 | 1.90 | < 0.001 |
| Grok 4.5 | 0.35 [0.27, 0.44] | 0.73 | 14/20/8 | 1.05 | 0.758 |
| GPT-4o (2024) | 0.25 [0.19, 0.34] | 0.86 | 24/11/7 | 0.76 | 0.123 |
| DeepSeek V4 | 0.23 [0.17, 0.31] | 0.88 | 19/20/3 | 0.69 | 0.045 |

Under one-to-one matching a session can score only 0, 1 or 3, so the three rows of a session are not independent. Tests against chance therefore use session scores: a z-test of the mean against 1 and a χ² goodness-of-fit test of the 0/1/3 distribution. Item-level binomial tests are not used for inference because they are anticonservative.

- **Grok 4.5** is indistinguishable from chance on both the mean and the distribution (p = 0.91). That means performance equivalent to guessing on this task, not proof that it guesses at random.
- **DeepSeek V4**'s mean is below chance (p = 0.045), but its distribution is not detectably different (p = 0.13). Below-chance performance is *suggestive, not established*.
- **GPT-4o (2024)**'s mean is not detectably below chance (p = 0.12), but its distribution departs from chance (p = 0.003): 24 of 42 sessions were entirely wrong, against 14 expected.

The models differ sharply overall: χ²(5) = 186.6 on item rows; Kruskal–Wallis on session scores H = 84.0, p = 1.2 × 10⁻¹⁶.

## F2. Same text, opposite readings (paper Table 2)

Condition A only, the 17-year-old's answer (`concept`), label assigned (raw counts):

| Model | 17M (correct) | 28F | 45M |
|---|---:|---:|---:|
| Claude Fable 5 | 33 | 3 | 0 |
| Gemini 3.1 Pro | 12 | 2 | 3 |
| GPT-5.6 Sol | 20 | 16 | 4 |
| Grok 4.5 | 8 | 22 | 12 |
| GPT-4o (2024) | 8 | 25 | 9 |
| DeepSeek V4 | 4 | 25 | 13 |

The pattern reads as a folk theory, not noise: formal, hedged phrasing reads as older.

## F3. Forced choice masks failure severity

Without the answer options (Condition C, scored correct if a stated range contains 17 or a point estimate is within ±3 years), accuracy on the teenager's answer is 0.00 for Grok, GPT-4o and DeepSeek (n = 42 each), 0.17 for GPT-5.6 (n = 40), 0.26 for Claude (n = 31) and 0.33 for Gemini (n = 18). Matching accuracy partly reflects ruling out two disclosed alternatives, which is far easier than free estimation.

## F4/F5. Context inversion and a capability-gated fix (paper Table 3)

Fisher's exact tests against Condition A for the same model:

| Model | A | B (institutional) | p(B) | D (instruction) | p(D) | E (neutral) | p(E) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 | 0.94 | 0.69 | < 0.001 | 1.00 | 0.082 | 0.94 | 1.000 |
| Gemini 3.1 Pro | 0.76 | 0.61 | 0.135 | 0.89 | 0.121 | 0.64 | 0.261 |
| GPT-5.6 Sol | 0.63 | 0.54 | 0.266 | 0.84 | 0.002 | 0.67 | 0.848 |
| Grok 4.5 | 0.35 | 0.33 | 0.894 | 0.36 | 1.000 | 0.31 | 0.732 |
| GPT-4o (2024) | 0.25 | 0.29 | 0.670 | 0.22 | 0.631 | 0.46 | 0.008 |
| DeepSeek V4 | 0.23 | 0.21 | 0.761 | 0.18 | 0.398 | 0.30 | 0.354 |

Two effects reach significance. The institutional label damages the strongest model (Claude, 0.94 → 0.69) while the neutral label does not. The audience-awareness instruction improves GPT-5.6 by 21 points. For the three weakest models, neither manipulation produces a detectable change, read as a floor effect. GPT-4o's rise under the neutral label (0.25 → 0.46, p = 0.008) is the only significant Condition E effect and is reported without interpretation, as a candidate for replication.

## F6. Confidence is a per-model trait, not a per-item signal (paper Table 4)

| Model | n | Mean confidence | SD | r(confidence, correct) | p |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 | 324 | 67.7 | 7.0 | +0.119 | 0.032 |
| Gemini 3.1 Pro | 201 | 88.3 | 5.7 | −0.143 | 0.043 |
| GPT-5.6 Sol | 309 | 62.4 | 12.6 | −0.015 | 0.790 |
| Grok 4.5 | 393 | 73.3 | 8.0 | −0.207 | < 0.001 |
| GPT-4o (2024) | 396 | 84.6 | 7.6 | −0.273 | < 0.001 |
| DeepSeek V4 | 396 | 88.0 | 5.2 | +0.015 | 0.762 |

Pooled over conditions A, B, D and E. Gemini, Grok and GPT-4o are more confident when wrong. DeepSeek's near-null correlation is not evidence of calibration: its confidence barely varies, so it carries almost no per-item information. Routing answers by stated confidence would misroute for several of these models.

## F7. Confession without correction (paper Table 5)

Reveal turns (conditions A, B and D) are coded once per session, 603 sessions, with pre-specified lexical patterns:

| Model | Sessions | External blame | *stereotyp-* | Opens with "thank" |
|---|---:|---:|---:|---:|
| Claude Fable 5 | 96 | 0 | 18 | 0 |
| Gemini 3.1 Pro | 52 | 0 | 10 | 0 |
| GPT-5.6 Sol | 114 | 1 | 16 | 0 |
| Grok 4.5 | 113 | 0 | 5 | 0 |
| GPT-4o (2024) | 114 | 0 | 2 | 0 |
| DeepSeek V4 | 114 | 3 | 68 | 108 |

External blame is rare (4 of 603 sessions). DeepSeek's explanations are the most self-critical: the stem *stereotyp-* appears in 68 of 114, and the passages read use it about the model's own reasoning. The count is lexical and does not by itself separate self-blame from other uses. Yet DeepSeek has the lowest accuracy and highest confidence under blind presentation. Sessions are stateless, so no transfer between sessions was possible and the study does not claim the model "failed to learn". The finding is narrower: the quality of a model's self-diagnosis does not track the quality of its judgment.

## F8. Generational change within one lab

GPT-4o (2024) → GPT-5.6 Sol (2026): accuracy 0.25 → 0.63 (Fisher's exact p = 2.2 × 10⁻⁹), mean confidence 0.86 → 0.64, confidence–accuracy gap +0.60 → +0.01, abstentions 0 → 15 sessions (45 rows). Every abstention refused all three labels, and 12 of the 15 occurred under the institutional label. DeepSeek V4, among the newer models, has the lowest accuracy and never abstained, so the improvement looks lab-specific rather than an automatic effect of recency.

## F9. Meta-finding: confident, fluent error from the study's own tools

During the study, AI-assisted tooling produced:
- a fabricated code-review summary
- a silently altered answer key
- an invented quotation offered as supporting evidence
- one transient false result in an intermediate analysis pass, from a parser defect

Each was caught by manual verification before inclusion in the released data or the paper. A study of confident, fluent error ran into confident, fluent error from its own tools.

## What this does not show

These are three items, one question and one language. The results isolate a mechanism (register read as age, institution read as demographics). They do not estimate how often models misattribute authors in general. Without a human baseline we also cannot yet say how much of the difficulty is specific to models.
