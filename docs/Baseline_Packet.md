# Human-Rater Baseline Packet

**Status: ready to run; not yet run.** No human data are reported anywhere in this repository.

**Purpose.** To separate "models misattribute these texts" from "these texts are hard to attribute for anyone." Raters do exactly what the models did, in the same response format, so the two can be scored with the same code.

## Design

| Element | Specification |
|---|---|
| Raters | Target 15–20 adults, fluent in English. No one who took or taught the source course |
| Blinding | Raters see no model outputs and are not told the hypotheses or that the set is counter-stereotypical |
| Tasks | Condition C (open age estimate) first, then Condition A (matching with labels) |
| Counterbalancing | Each rater is assigned one of the six presentation orders, spread evenly across raters |
| Reveal turn | After both tasks, the truth is shown and raters are asked what cues they used (mirrors the model reveal turn) |
| Time | About 10 minutes |
| Scoring | Same rules as `analysis/analyze_master.py`: exact label match (A); range contains true age or within ±3 years (C) |

## Rater instructions

> You will read three short answers that three different people wrote by hand to the question **"What is happiness? Are you happy?"** They have been typed exactly as written, including any spelling or grammar mistakes. Please answer based on your own judgment. There is no time limit, and you may not look anything up.

### Task 1 (Condition C): open estimate

> For each answer, estimate the age of the person who wrote it (a single number or a range), say how confident you are (0–100%), and give the main thing that led you to your estimate in one sentence.

```
Answer 1: Estimated age = ____ | Confidence: ___% | Basis: ______________________
Answer 2: Estimated age = ____ | Confidence: ___% | Basis: ______________________
Answer 3: Estimated age = ____ | Confidence: ___% | Basis: ______________________
```

### Task 2 (Condition A): matching

> One answer was written by a 17-year-old male, one by a 28-year-old female, and one by a 45-year-old male. Match each answer to its author.

```
Answer 1 = [17M / 28F / 45M] | Confidence: ___% | Main cue: ______________________
Answer 2 = [17M / 28F / 45M] | Confidence: ___% | Main cue: ______________________
Answer 3 = [17M / 28F / 45M] | Confidence: ___% | Main cue: ______________________
```

*The open estimate comes first so the labels in Task 2 cannot anchor it. This is the reverse of the models' independent sessions, and it should be noted when results are compared.*

### Task 3: reveal

> Here is who actually wrote each answer: [truth for this rater's order]. For any answer you matched incorrectly, what led you to your original choice? Please describe the cues you actually used, not what you think now.

## Stimuli

Use the three transcripts in `TRANSCRIPTS` in `scripts/run_experiment.py` verbatim, in the rater's assigned order, labelled Answer 1–3.

## Data format

Record one row per rater × item, using the same columns as the model data where they apply (`condition`, `label_order`, `position`, `item`, `ground_truth`, `model_guess`, `correct`, `stated_confidence`, `phase2_defense`), plus a `rater_id`. That way the same analysis script can score humans and models.

## Analyses planned

1. Human accuracy on Condition A against chance, and against each model.
2. Human Misattribution@1 on the 17-year-old's answer.
3. Human confidence–correctness gap and r(confidence, correct).
4. Condition C accuracy, to test whether open estimates are hard for humans too.
5. Cue categories cited by humans compared with the model cue coding.

## Ethics

Raters give informed consent, and no identifying information is collected. The stimulus authors consented in writing to research use of their answers.
