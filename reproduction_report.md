# Reproduction report

## Final outcome

**PASS.** The public release was reproduced from an empty `data/raw/` directory (only `.gitkeep` present) in a fresh Python 3.12.13 virtual environment.

## Commands

```bash
python -m src.run_all
pytest -q
```

## Clean execution result

The release was run from an empty `data/raw/` directory. The complete run finished with exit code 0 in **447.9 seconds**, and the subsequent test run passed all eight tests. Configuration lookup uses the single approved `frozen_analysis_v2.yaml`. No data, preprocessing, model settings, seeds, thresholds, or results were changed during final packaging.

## Data and model results

- Data loaded and validated: 2,584 rows, 18 predictors, 170 hazardous cases, 2,414 non-hazardous cases, zero missing values.
- Held-out test set: 776 rows, 51 hazardous, 725 non-hazardous.
- All four models ran under the approved frozen configuration.
- Fresh `model_performance.csv`, LR threshold table, repeated-CV table, bootstrap JSON, calibration JSON, fitted parameters, and run metadata were compared with the frozen copies. Equality was exact; maximum numeric difference was 0.
- `TP + FN = 51`, warning workload = `TP + FP`, false alarms = `FP`, and missed hazardous cases = `FN` passed for all applicable rows.

## Figures

- Fig 4, Fig 5, and S1 Fig were regenerated from the successful final run.
- Plot typography was set to Arial without changing calculations.
- S1 Fig uses “Mean model decision score” and “Observed positive fraction”; decision scores are not presented as absolute hazard probabilities.
- All six final TIFFs passed dimension, DPI, mode, alpha, LZW, size, caption, and visual checks.

## Tests

`pytest -q` completed with 8 passes and one non-failing scikit-learn deprecation warning.

## Manual steps remaining

Repository DOI assignment, Academic Editor selection, author approval of an open-source license, and final confirmation of funding/ethics fields remain manual. The original complete public-case search history remains unavailable and is represented as `NR`. No coding-agreement statistic is generated.

## Unresolved technical issues

None affecting numerical reproduction. LibreOffice was unavailable for DOCX rendering; WPS/PDF visual QA was used as the documented fallback.
