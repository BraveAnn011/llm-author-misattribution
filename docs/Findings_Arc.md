# Findings Arc

*Each finding lists its number(s) and the section of `analysis/analyze_master.py` output that reproduces them. Condition A = blind matching; chance = 0.33.*

The arc runs from **what** models get wrong (F1–F3), to **what moves them** (F4–F5), to **whether their self-reports can be trusted** (F6–F7), to **change over time** (F8). It closes with what the study taught about its own tools (F9).

## F1. Below chance, at high confidence
*Output: "CONDITION A" and "F1: below-chance test"*

| Model | Accuracy (A) | Mean confidence | Exact one-sided p vs 1/3 |
|---|---:|---:|---:|
| Claude Fable 5 | 0.94 (102/108) | 0.67 | — |
| Gemini 3.1 Pro | 0.76 (39/51) | 0.87 | — |
| GPT-5.6 Sol | 0.63 (76/120) | 0.64 | — |
| Grok 4.5 | 0.35 (44/126) | 0.73 | 0.685 |
| GPT-4o | 0.25 (32/126) | 0.86 | 0.034 |
| DeepSeek V4 | 0.23 (29/126) | 0.88 | 0.008 |

Omnibus χ²(5) = 186.6. Three models sit at or below chance while reporting 73–88% confidence. Accuracy significantly *below* chance means the errors are systematic, not noise: these models apply a consistent but wrong rule.

## F2. Same text, opposite readings
*Output: "F2"; Condition A counts below come from the released data*

For the 17-year-old's answer in Condition A, Claude chooses "17M" 33 times out of 36. DeepSeek chooses "28F" 25 times out of 42, and GPT-4o 25 out of 42. The same formal, hedged text is read as a teenager by one model and as an adult woman by others.

## F3. Forced choice masks failure severity
*Output: "F3"*

Without the answer options (Condition C, ±3 years or range scoring), accuracy on the teenager's answer is 0.00 for Grok, GPT-4o and DeepSeek. It is 0.17 for GPT-5.6, 0.26 for Claude and 0.33 for Gemini. Forced choice lets models reach the right answer by elimination. Open response shows that almost none of them infer a teenager from the text.

## F4. Institutional context becomes a demographic prior
*Output: "F4/F5" (B−A, E−A, B−E)*

"Community-college biology final" lowers Claude from 0.94 to 0.69 (B−A = −0.25), while a neutral label leaves it unchanged (E−A = 0.00). The harm is specific to the institutional label (B−E = −0.25). Gemini (−0.16) and GPT-5.6 (−0.09) move the same way. The models convert a fact about an institution into an assumption about who studies there.

## F5. Prompting elicits latent capability; it cannot manufacture it
*Output: "F4/F5" (D−A)*

The pragmatic instruction raises Claude from 0.94 to 1.00, GPT-5.6 by 21 points and Gemini by 12. Grok, GPT-4o and DeepSeek change by between −0.05 and +0.01. Scaffolding helps only models that already have the capability.

## F6. Confidence is a per-model trait, not a per-item signal
*Output: "F6"*

| Model | Mean confidence | SD | When right | When wrong |
|---|---:|---:|---:|---:|
| Claude Fable 5 | 67.7 | 7.0 | 68.0 | 65.5 |
| Gemini 3.1 Pro | 88.3 | 5.7 | 87.8 | 89.6 |
| GPT-5.6 Sol | 62.4 | 12.6 | 62.3 | 62.7 |
| Grok 4.5 | 73.3 | 8.0 | 71.0 | 74.5 |
| GPT-4o | 84.6 | 7.6 | 81.3 | 85.9 |
| DeepSeek V4 | 88.0 | 5.2 | 88.1 | 87.9 |

Gemini, Grok and GPT-4o are more confident when wrong. DeepSeek's confidence barely varies at all. Stated confidence tells you which model produced an answer far more reliably than whether the answer is correct. Confidence-based routing or abstention would misroute for these models.

## F7. Confession without correction
*Output: "F7" for external-blame language; hand coding for self-blame*

The 1,809 reveal turns are overwhelmingly accepting rather than defensive: external-blame language appears in only 12 of them (9 from DeepSeek, 3 from GPT-5.6). The models acknowledge their errors. DeepSeek, for example, produced 51 internal self-blame statements in hand coding, and 11 of 12 sampled ones opened with "Thank you." But acknowledgment does not carry forward: DeepSeek's accuracy (F1) and confidence (F6) stay the same across fresh sessions. A fluent self-critique is not evidence that a model's reasoning has changed.

## F8. Generational change within one lab
*Output: "CONDITION A" and "F8"*

GPT-4o → GPT-5.6: accuracy 0.25 → 0.63, confidence–correctness gap +0.60 → +0.01, abstentions 0 → 45. GPT-5.6 is the only model that ever abstains (36 of its 45 abstentions occur under the institutional label, B). DeepSeek's API serves only its current model, so it has no before/after pair.

## F9. Meta-finding: confident, fluent error from the study's own tools

During the study, AI-assisted tooling:
- fabricated a code review that had not been carried out
- silently swapped the answer key
- invented a quotation
- produced a false 100% accuracy through a parser bug

Each was caught by human verification against the raw outputs. A study of confident, fluent error ran into confident, fluent error from its own tools. The verification steps those incidents prompted are now part of the pipeline.

## What this does not show

These are three items, one question and one language. The results isolate a mechanism (register read as age, institution read as demographics). They do not estimate how often models misattribute authors in general. Without a human baseline we also cannot yet say how much of the difficulty is specific to models.
