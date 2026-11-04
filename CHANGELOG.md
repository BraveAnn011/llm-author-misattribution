# Changelog

## v1.1.0 (2026-11-04)
### Added
- README: models and API ids, conditions, the paper's Table 1 with Wilson intervals and session-level chance tests, key findings, limitations, a consent and provenance section, reproduction steps and the arXiv citation.
- `docs/Methods_Draft.md`, `docs/Findings_Arc.md`, `docs/Study_Codebook.md`, `docs/Baseline_Packet.md`, aligned with the paper (arXiv:2610.31946).
- `data/README.md`: canonical dataset, batch provenance, session counts and why per-model N differs.

### Changed
- Per-batch results and raw outputs moved to `data/runs/`. Nothing was deleted, and the canonical dataset is unchanged.
- `human-baseline/PROTOCOL.md` now points to the rater packet. Status: not yet run.
- Statistical claims now follow the paper: tests against chance use session scores, not item-level binomial tests.
- Consent wording now matches the paper's ethics statement.

## 2026-10-27
### Added
- arXiv identifier 2610.31946, BibTeX and companion-study link in the README.

## 2026-10-22
### Added
- `analysis/stats_paper.py`: reproduces every statistic in the manuscript.
- CC BY 4.0 data license (`LICENSE-DATA`).

## 2026-09-18
### Added
- Initial public release: methodology, data, analysis scripts, findings.
