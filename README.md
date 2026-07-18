# Open-data coal-mine warning-response analysis

Version 2.0.0, aligned with the submission manuscript titled “Open-data evaluation of seismic-hazard warning models, response workload, and public safety records in coal mines”.

## 1. Purpose

This repository reproduces the frozen v2 open-data evaluation of four baseline warning classifiers, Logistic Regression decision-cut-off sensitivity, robustness analyses, and descriptive public-record response-chain summaries. It is a preliminary reproducible framework, not a mine-site deployment or a new machine-learning algorithm.

## 2. Repository contents

- `config/`: frozen analysis and model settings.
- `src/`: data acquisition, validation, final analysis, figure generation, and case-summary code.
- `tests/`: automated dataset, split, preprocessing, output-schema, threshold, and configuration checks.
- `data/public_cases/`: public-case coding records and retrospective screening metadata.
- `outputs/final_tables/`, `outputs/final_figures/`, and `outputs/final_metadata/`: frozen expected outputs.

## 3. Data sources

The model analysis uses the UCI Seismic-bumps dataset (doi:10.24432/C5W902). The response-chain assessment uses a non-exhaustive purposive sample of 32 public accident and engineering cases. The public-case records are not a systematic review, exhaustive sample, representative industry sample, field validation, or deployed safety system.

## 4. Data acquisition

The UCI archive is not packaged in this release. `python -m src.run_all` downloads it into `data/raw/` when network access is available, then validates 2,584 records, 170 hazardous cases, and 2,414 non-hazardous cases. See `data/README.md` for the source URL and expected files.

## 5. Environment installation

Python 3.12 is required. From a fresh environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e .
# macOS/Linux
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
```

Pinned package versions are listed in `requirements.txt`, `environment.yml`, and `pyproject.toml`.

## 6. Complete run commands

```bash
python -m src.run_all
pytest -q
```

The final entry point downloads and validates the data, fits the four frozen pipelines, writes tables and metadata, generates figures, performs repeated cross-validation and bootstrap analyses, and summarizes public-case coding.

## 7. Manuscript output mapping

- Table 4: `outputs_v2/tables/model_performance.csv` after a fresh run; frozen copy at `outputs/final_tables/model_performance.csv`.
- Table 5: `outputs_v2/tables/logistic_regression_threshold_sensitivity.csv`; frozen copy at `outputs/final_tables/logistic_regression_threshold_sensitivity.csv`.
- Fig 4: `outputs_v2/figures/roc_pr_curves.png`; frozen copy at `outputs/final_figures/roc_pr_curves.png`.
- Fig 5: `outputs_v2/figures/threshold_workload.png`; frozen copy at `outputs/final_figures/threshold_workload.png`.
- S1 Fig: `outputs_v2/robustness/logistic_regression_calibration_curve.png`; frozen copy at `outputs/final_figures/logistic_regression_calibration_curve.png`.

The figure-generation code is in `src/v2_pipeline.py`. The release sets the plotting font family to Arial for submission compatibility; this does not change any numerical result.

## 8. Random seeds

The frozen stratified 70:30 held-out split uses random seed 42. Repeated stratified cross-validation uses the declared fixed seed in `config/frozen_analysis_v2.yaml`, and the 2,000-resample bootstrap uses its separately declared fixed seed. No seed search was performed.

## 9. Output directories

Fresh runs write `outputs_v2/tables/`, `outputs_v2/figures/`, `outputs_v2/metadata/`, and `outputs_v2/robustness/`. Public-case selection counts are written to `outputs/tables/`.

## 10. Expected results

The validated dataset contains 2,584 rows (170 hazardous, 2,414 non-hazardous). The held-out test set contains 776 rows (51 hazardous, 725 non-hazardous). `outputs/final_tables/model_performance.csv` and the frozen metadata provide the exact expected metrics. Tests verify `TP + FN = 51`, `warning workload = TP + FP`, and `missed hazardous cases = FN`.

## 11. Known limitations

The model analysis is an open-data benchmark and is not evidence of calibrated absolute hazard probabilities, accident-rate reduction, shorter response time, productivity improvement, or field-level operational effectiveness. Decision thresholds are model cut-offs. The 32 public cases are a non-exhaustive purposive sample, and the original complete search history was not retained. No intra-coder agreement statistic is reported.

## 12. Citation

See `CITATION.cff`. A permanent repository DOI has not yet been assigned; see `DOI_REQUIRED_BEFORE_SUBMISSION.md`.

## 13. License

The authors or authorized rights holders have not yet confirmed an open-source
license. See `LICENSE` and `LICENSE_SELECTION_REQUIRED.md`. The repository must
remain private until the license has been selected and approved.

## 14. Version correspondence

Release version 2.0.0 corresponds to the author-approved frozen v2 replacement analysis used in the PLOS ONE submission-ready manuscript. It is not claimed to be the exact configuration used for any earlier manuscript version.
