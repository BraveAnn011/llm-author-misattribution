# LLM Author Misattribution Study
Companion study: [ai-halo-valuation-bias](https://github.com/BraveAnn011/ai-halo-valuation-bias) — Another industry leading model panel, testing context-driven price valuation instead of author attribution.

## Methodology & Findings
This repository contains a six-model study evaluating author-age misattribution, miscalibrated confidence, and post-hoc confession without correction. The experiment measures text-only performance and confidence tracking across frontier large language models.

- **Sample Size:** N = 3,225 scored attributions
- **Models Evaluated:** 6 frontier Large Language Models
- **Key Focus:** Text-only study evaluating model calibration and text-only NLP performance

## Project Structure
- `scripts/`: Python execution scripts for running model evaluations.
- `analysis/`: Data processing and metric evaluation scripts. `stats_paper.py` reproduces every statistic in the manuscript: `python3 analysis/stats_paper.py data/Master_results_ALL_v2.csv` (requires pandas, numpy, scipy).
- `human-baseline/`: Experimental protocol for human-rater baseline comparison.

## License
- Code (`scripts/`, `analysis/`): MIT, see [LICENSE](LICENSE).
- Data and text (`data/`, documentation): CC BY 4.0, see [LICENSE-DATA](LICENSE-DATA).

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

Companion study: Lee, B. (2026). Does the Outfit Change the Price? arXiv:2610.34591, https://arxiv.org/abs/2610.34591

## Further Reading
- [Six AI Models. Six Ways to Fail. (Substack)](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu) — Behavioral failure fingerprints and calibration tracking data.

