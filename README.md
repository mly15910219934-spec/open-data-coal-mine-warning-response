# Overview

This repository contains the reproducible analysis package for the revised manuscript submitted to PLOS ONE.

**Open-data evaluation of seismic-hazard warning models, alert burden, and public safety records in coal mines**

It reproduces Table 4 (held-out model performance), Table 5 (matched alert burden), and S4 Table (bootstrap confidence intervals), and retains repeated cross-validation, DeLong/McNemar comparisons, RandomOverSampler sensitivity and statistical figures. It is not merely a figure-code collection.

# Version

Version: **3.0.0**

This release corresponds to the revised manuscript submitted to PLOS ONE.

Concept DOI: [10.5281/zenodo.21423640](https://doi.org/10.5281/zenodo.21423640), confirmed by the author. This identifies the version family; cite Version 2.1.0 explicitly. No version-specific DOI or publication date has been invented. Preparing this ZIP does not publish a Zenodo record.

# Contents

- `config/`: original frozen analysis/model YAML files, unchanged.
- `data/`: bundled UCI raw snapshot and provenance; public-case source inventory, not a new coding exercise.
- `src/preprocessing/`: validation and preprocessing entry point.
- `src/model_training/`: original reviewer-stage joint four-model engine.
- `src/evaluation/`: model/threshold evaluation and table exports.
- `src/statistics/`: bootstrap, cross-validation, weighting/resampling sensitivity and comparisons.
- `src/figure_generation/`: statistical plot code and editable conceptual sources/exporters.
- `scripts/`: unified commands.
- `output/`: revised tables, figures and machine-readable run metadata.
- `tests/`: scientific regression tests and a portable launcher.
- `metadata/`: version, migration evidence, unchanged reference results and file checksums.

Compatibility files at the root of `src/`, plus `outputs/` and `outputs_v2/`, retain the historical baseline used by the original regression gate. They are not a second copy of this package. Do not substitute the historical baseline results for the revised results in `output/`.

# Environment

Python **3.12.14**. Main pinned dependencies: NumPy 2.5.1, pandas 3.0.3, SciPy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, imbalanced-learn 0.14.2, PyYAML 6.0.3, Pillow 12.3.0 and pytest 9.1.1. All 27 dependencies are pinned in `requirements.txt`.

The numerical workflow runs without Word or PowerPoint. Arial is requested for statistical plots; install it for matching typography. Optional conceptual-diagram exports require Windows and Microsoft PowerPoint. Model scores are decision values, not calibrated absolute hazard probabilities.

# Installation

From the extracted package root:

```sh
conda env create -f environment.yml
conda activate coal-mine-warning-response-2.1.0
```

Alternatively, with Python 3.12.14:

```sh
python -m venv .venv
```

Activate using `.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` in a POSIX shell, then:

```sh
python -m pip install -r requirements.txt
python -m pip check
```

The release check states the actual tested platform and installation route. Conda/network installation and cross-platform bitwise identity are not inferred from offline validation.

# Reproduction workflow

## Step 1 — Install environment

Use the installation commands above. Run subsequent commands from the extracted root. Outputs are resolved relative to the scripts, not a personal working directory.

## Step 2 — Prepare data

The raw UCI archive and ARFF are bundled for offline reproduction. Validate them:

```sh
python src/preprocessing/preprocess.py
```

This verifies the SHA-256, 2584 rows, 170 positives, 2414 negatives, 18 predictors and absence of missing values. The 70:30 stratified split has 1808 training records and 776 test records (51 positive, 725 negative). To fetch a fresh official copy deliberately, append `--download`; this requires network access. A changed checksum causes failure rather than silent substitution.

## Step 3 — Run analysis

```sh
python scripts/run_all_analysis.py
```

This refits the historical regression-gate models, fits the revised LR/RF/GB/SVM models, recomputes model performance, threshold sweeps and matched burden, runs 2000 bootstrap resamples, repeated training-only CV (5 folds × 10 repeats), DeLong and exact McNemar comparisons, separate train-only RandomOverSampler sensitivity, and generates tables and five statistical figures. This is the complete workflow and takes substantially longer than plotting saved results. No alternate seed search is performed.

The four categorical features are one-hot encoded; fourteen numeric features are standardized for LR/SVM and passed through for tree models. Pipeline/ColumnTransformer are fitted only on the training subset/fold. There is no imputation. Main imbalance handling uses balanced class weights for LR/RF/SVM and training-derived balanced sample weights for GB. No resampling is used in the main analysis. The separate ROS sensitivity disables class/sample weights. These reviewer-stage overrides to the historical frozen YAML are documented in `metadata/reproducibility_notes.md` and exported actual parameters.

## Step 4 — Generate manuscript results

After numerical computation, these commands verify/export tables and regenerate plots without refitting:

```sh
python scripts/generate_tables.py
python scripts/generate_figures.py
python tests/reproducibility_check.py
```

| Manuscript result | Calculation entry | Output |
|---|---|---|
| Table 4 | `src/evaluation/model_performance.py` delegates to `src/model_training/run_revision.py` | `output/tables/Table4_heldout_model_performance.csv` |
| Table 5 | `src/evaluation/threshold_analysis.py` delegates to the same joint runner | `output/tables/Table5_decision_cutoff_alert_burden.csv` |
| S4 Table | `src/statistics/bootstrap_analysis.py` | `output/tables/S4_Table_bootstrap_confidence_intervals.csv` |

The named CSV aliases are created by `scripts/generate_tables.py` and the complete workflow. Table 4 includes ROC-AUC, PR-AUC (average precision), Brier, precision, recall, F1, confusion counts and alert burden. Table 5 uses the common achievable alert count nearest the target of 150 while preserving score ties (147 in the frozen results). The complete 0.01–0.99 cutoff sweep is retained separately. S4 has 2000 paired, class-stratified resamples and percentile 95% intervals. Precision is defined as zero when no positives are predicted. DeLong/McNemar and repeated CV are separate outputs, not mislabeled as S4.

Reference results under `metadata/reference_results/` are used for comparisons only, not to replace calculated predictions. Exact comparisons stop on numerical differences. Keep software versions and scientific settings fixed.

Figure 4, Figure 5 and S1/S2/S3 Figs are generated as PNG/SVG/TIFF. Conceptual Figure 1/2 retain their editable two-slide source. Historical script slots `figure2_architecture.py` and `figure3_response_chain.py` do not introduce a new main Figure 3: the former exports a legacy diagram; the latter exports current Figure 2. Conceptual export is optional and separate from numerical reproduction.

# Random seed

All stochastic procedures use random seed 42.

# Data availability

Sikora, M. & Wrobel, L. (2010). seismic-bumps [Dataset]. UCI Machine Learning Repository. [10.24432/C5W902](https://doi.org/10.24432/C5W902). The unchanged raw snapshot is included under `data/raw/` and licensed by its source under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), not MIT. See `data/README.md` for provenance and SHA-256.

The separately supplied 32-case public-record archive is inventoried with hashes but not redistributed here. The historical baseline case CSVs are not the current final consensus S1 Table. This release does not independently reproduce human coding or Cohen's kappa and does not replace the final supplementary coding workbook. None of those case materials is required for Table 4, Table 5 or S4 numerical reproduction. The sample is purposive and non-exhaustive; model evaluation is not operational end-to-end validation.

# Citation

Liu, Y.; Miao, K.; Zhang, L.; Dai, W.; Li, H.; Meng, J.; Miao, J.; Mu, L. Open-data evaluation of seismic-hazard warning models, alert burden, and public safety records in coal mines. Software, Version 2.1.0. Zenodo. Concept DOI: [10.5281/zenodo.21423640](https://doi.org/10.5281/zenodo.21423640).

Machine-readable author order and version are in `CITATION.cff`.

# License and release checks

Author-owned software and associated documentation are released under the standard MIT License in `LICENSE.md`, authorized by the author. Third-party data and reports retain their own rights; see `metadata/THIRD_PARTY_NOTICES.md`.

See `RELEASE_CHECK_REPORT.md` for actual verification and its limits. `metadata/prior_packaging/` contains superseded packaging receipts for provenance, not the current license/DOI status. `metadata/package_file_manifest.csv` covers all release files except itself. No virtual environment, wheel cache, personal computer path, duplicate nested package or automatic upload function is included.
