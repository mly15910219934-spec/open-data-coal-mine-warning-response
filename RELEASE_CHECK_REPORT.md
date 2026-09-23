# RELEASE CHECK REPORT — Version 2.1.0

Final recommendation: **READY FOR ZENODO UPLOAD**

Scope: the local software release for the revised PLOS ONE manuscript, not confirmation of a completed Zenodo upload or journal acceptance. Author-confirmed concept DOI: **10.5281/zenodo.21423640**. This release corresponds to the revised manuscript submitted to PLOS ONE.

| Required check | Result | Evidence / boundary |
|---|---|---|
| Structure | PASS | One package root; no nested duplicate; required config/data/src/scripts/output/tests/metadata and top-level files present. Historical compatibility files retained deliberately. |
| Environment | PASS | Fresh Python 3.12.14 venv; all 27 exact dependencies installed from a local wheel cache; pip check passes. No existing site-packages used. |
| Reproduction | PASS | ZIP extracted into an independent directory; output/, outputs/ and outputs_v2/ removed from the TEST COPY before the complete entry point was run. Full workflow then regenerated results from bundled raw data. |
| Table 4 reproduction | PASS | Four models actually refitted; full-precision performance and held-out predictions match immutable reference results exactly. |
| Table 5 reproduction | PASS | Threshold sweep and matched operating points recomputed; common attained burden 147; all fields match exactly. |
| S4 reproduction | PASS | 2000 paired stratified bootstrap resamples at seed 42; raw replicates, summaries and manuscript CSV alias match exactly. |
| Security | PASS | No personal absolute paths, high-confidence secret patterns, hidden files or cache directories in the release. Pattern scan is not a malware certification. |

## What was fixed

- Removed only the accidental nested duplicate package from the new release; the source ZIP remains untouched.
- Migrated current reviewer-stage code/ modules to src/ using path-only substitutions. Existing Python ASTs match after reversing those path substitutions; model algorithms and statistical calculations were not rewritten.
- Added the three requested portable scripts and tests/reproducibility_check.py.
- Added the standard MIT License, explicitly authorized by the author, and ordered eight-author CITATION.cff with Version 2.1.0 and the unchanged concept DOI.
- Updated English README, VERSION.txt, CHANGELOG.md and third-party UCI CC BY 4.0 attribution. Software MIT licensing does not relicense third-party data/reports.
- Kept original frozen YAML, raw data, reference numerical results, models/settings, seed 42 and statistical methods unchanged. Retained older required baseline modules and outputs for compatibility, without retaining a second full package.

## Executed checks (Windows, Python 3.12.14)

| Command | Seconds | Result |
|---|---:|---|
| `python -m pip check` | 0.574 | PASS |
| `python -m compileall -q .` | 0.424 | PASS |
| `python scripts/run_all_analysis.py` | 740.140 | PASS |
| `python src/check_package.py` | 19.074 | PASS |
| `python src/preprocessing/preprocess.py` | 1.748 | PASS |
| `python scripts/generate_tables.py` | 1.655 | PASS |
| `python scripts/generate_figures.py` | 3.470 | PASS |
| `python tests/reproducibility_check.py` | 19.080 | PASS |

Tests: **26 passed in 18.54s**.

An initial README-path check ran before the packaging manifest had been written and correctly reported that file missing; all Python imports already passed. The manifest was then generated, the check rerun, and the complete manifest regenerated and hash-verified at final packaging. No scientific engine change was required. The initial diagnostic log is retained separately for transparency.

The complete entry point actually ran model training, original regression gate, training-only CV, 2000-resample bootstrap, 5-fold × 10-repeat CV, separate train-only RandomOverSampler sensitivity, DeLong and exact McNemar comparisons with the retained adjustments, table export and statistical figure generation. This replaces the earlier audit's startup-only/minimal-run limitation.

30 available CSV reference result files were compared exactly after the completed run, as were all three manuscript aliases. Raw ARFF, frozen configs and reference results were also hash-checked. Statistical figures were regenerated from their computed sources; source bindings and figure-export checks passed. No scientific number was patched to achieve a match.

Evidence: metadata/release_validation/, metadata/scientific_logic_preservation.json, metadata/layout_migration.json and metadata/package_file_manifest.csv. The checksum manifest excludes itself to avoid self-reference.

## Explicit limitations (not numerical-release blockers)

- Installation was a fresh **offline pip** installation from pre-existing wheels, not a Conda or online-package-index installation. The environment.yml recipe is supplied, but Conda creation and other operating systems were not executed. Cross-platform bitwise agreement is not claimed.
- Network re-download was not required or tested. The bundled original dataset enables offline reproduction and is checked against its known hash.
- The frozen scikit-learn version emits deprecation warnings for retained LR/GB/SVM parameter interfaces. They are warnings, not failed calculations. Versions and parameters were not upgraded to suppress them, because doing so would change the validated scientific environment.
- Optional conceptual-diagram PowerPoint COM export was not rerun. Editable sources and existing exports were preserved; statistical figures are generated separately. Existing conceptual source wording, including the previously noted kappa label, was not silently edited as part of packaging.
- The external 32-case primary-source PDF package and final independent/consensus coding workbook are not redistributed here. This is not an independent replication of human coding or kappa. They are not inputs to Tables 4, 5 or S4. The Data Availability statement must not describe this ZIP as containing those excluded materials.
- DOI type, creator order and MIT authorization follow the author's explicit confirmation. No version-specific DOI was invented, and no remote Zenodo publication was performed.
- Final manuscript rounded cells, authors' Zenodo account fields and journal upload choices remain the author's submission responsibilities; this check validates the archived numerical workflow.

## Final package verification

The final ZIP has a single correctly named top-level directory. Every included member can be read; release hashes are checked against the checksum manifest. Active Python/config/script files are identical to the files used in the successful extraction test. The final delivery directory contains only the requested ZIP and this report.

License text basis: https://opensource.org/license/mit . Dataset provenance/license: https://archive.ics.uci.edu/dataset/266/seismic%2Bbumps and https://creativecommons.org/licenses/by/4.0/ .
