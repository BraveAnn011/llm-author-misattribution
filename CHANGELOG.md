# Changelog

## 2026-10-19
### Added
- README: models and API ids, conditions, headline results table, key findings, limitations, reproduction steps, citation.
- `docs/Methods_Draft.md`, `docs/Findings_Arc.md`, `docs/Study_Codebook.md`, `docs/Baseline_Packet.md` (previously empty).
- `data/README.md`: canonical dataset, batch provenance, and why per-model N differs.
- `analysis/analyze_master.py`: exact two-sided binomial test against chance and omnibus χ² for Condition A. These reproduce the paper's Table 1.

### Changed
- Per-batch results and raw outputs moved to `data/runs/`. Nothing was deleted, and the canonical dataset is unchanged.
- `human-baseline/PROTOCOL.md` now points to the rater packet. Status: not yet run.

## 2026-09-18
### Added
- Initial public release: methodology, data, analysis scripts, findings.
