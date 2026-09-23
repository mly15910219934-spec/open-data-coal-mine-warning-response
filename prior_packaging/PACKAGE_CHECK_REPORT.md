# Package check report — Version 2.1.0

Verification date: 2026-09-23.

**Numerical reproduction: PASS. Public-release readiness: AUTHOR CONFIRMATION REQUIRED.**

This report distinguishes successfully executed analysis from external publication, licensing and optional application-dependent figure export. The package has not been uploaded to Zenodo or GitHub. No manuscript, reference, supplementary workbook or original supplied archive was modified.

## 1. File completeness and provenance

| Check | Result | Evidence / qualification |
|---|---|---|
| Requested directory layout | PASS | README, LICENSE, environment, frozen YAML, five code subdirectories, data, output and metadata are present. Additional `src/`, `tests/` and reference/history directories preserve reproducibility. |
| Original frozen YAML files | PASS | Byte-identical to the supplied original baseline; SHA-256 comparisons in `metadata/frozen_configuration_integrity.json`. |
| Original analysis functionality | PASS, with documented generations | Original baseline `src/` retained; revision engines relocated without changing numerical calculations. Historical auxiliary scripts retained as source text, not misrepresented as current tested entry points. |
| Dataset | PASS | Original 141669-byte ARFF supplied; hash checked before fitting; 2584 rows, 170 positives and 2414 negatives. |
| Public-case folder mapping | PASS | S1-01 to S1-32 match inventory IDs. Every supplied archive member has size and SHA-256. No new case coding was performed. |
| Current numerical outputs | PASS | Recomputed from raw data; frozen references are stored separately. |
| Requested six discoverable figure-code filenames | PASS | All six present; historical figure-number aliases are explained in README. No nonexistent Python drawing origin is claimed for PPT-authored conceptual figures. |
| README referenced project paths | PASS | Automated path check found no missing paths. |
| Active Python imports | PASS | All 30 `.py` files parsed and imported successfully, each in a separate subprocess. |
| Embedded workstation / absolute filesystem paths | PASS | Text/code/configuration scan found none. Historical workstation references were redacted and logged. Runtime paths are derived from the extracted package location. |
| Personal runtime / caches in release | PASS | No virtual environment, Python bytecode or pytest cache included in ZIP. Installed package versions are specified, not copied from a workstation into the release. |

The final file manifest is `metadata/package_file_manifest.csv`. Historical script identities and any path redactions are in `metadata/source_migration_manifest.json`. Scripts stored as historical `.txt` are archival source records, not part of the 30 active Python modules and not claimed to pass current command-line execution.

## 2. Environment and actual execution

Python **3.12.14** was used in a **new virtual environment**. All 27 pinned dependencies from `requirements.txt` were installed with pip from locally available original wheel distributions; `pip check` reported **No broken requirements found**. The installed versions match the supplied stage-two lock file. This was a fresh installation, not reuse of an activated previous analysis environment.

An ordinary internet installation was attempted but blocked by Windows host network permissions. Consequently online PyPI installation, a fresh UCI network download, and Conda environment creation are **not independently verified here**. Local wheel files were used only to install the testing environment and are not dependencies of the extracted release. A reviewer may install the pinned public packages normally on a network-enabled system.

Executed twice:

```text
python code/run_all.py
python -m pytest -q
```

The second run used a separately extracted archive copy. All `output/`, `outputs/` and `outputs_v2/` files were omitted before that run. Thus no previous fitted predictions, generated table, bootstrap cache or manual intermediate file was available as a computed input. Bundled raw data, frozen configurations and immutable reference files remained available. References were used to check results, not to supply predictions to training.

Both full numerical runs returned exit code 0. First scientific test pass: **26 passed in 20.34 s**. Clean-extraction scientific test pass: **26 passed in 20.64 s**. The staged README commands call these same executed workflow functions; the all-in-one sequence was the clean-extraction command tested. The optional online/historical commands and PowerPoint-rendering commands are not included in that PASS claim.

## 3. Manuscript-target reproduction

| Manuscript target | Recomputed source table | Verification |
|---|---|---|
| Table 4 | `model_performance_revision.csv` — 4 models | Exact dataframe equality with supplied revision reference |
| Table 5 | `table5_matched_operating_point.csv` — 4 models | Exact dataframe equality; common attained burden 147 |
| S4 Table | `bootstrap_2000_summary.csv` — 20 model/metric rows | Exact dataframe equality for every point estimate and CI endpoint |
| Bootstrap underlying draws | `bootstrap_2000_raw.csv` — 8000 model/resample rows | Exact dataframe equality; all 2000 paired stratified index draws independently checked |

The package also exactly reproduced the 776 held-out prediction rows, 2584 split assignments, 396 threshold rows, repeated-CV summaries, RandomOverSampler summaries, cost-sensitivity summaries, DeLong and McNemar tables. Thirteen reference tables/prediction datasets were compared with exact dataframe equality, not only rounded manuscript values. See `output/metadata/reference_comparison.json`.

Manuscript-named CSV aliases are generated by `code/evaluation/export_tables.py` without altering precision. The historical 82-cell Table 4/5 baseline gate was separately recomputed before the revision models; it is not a substitute for checking the revised tables above.

The tests check split composition, leakage boundaries, TP + FN = 51, TN + FP = 725, alert burden = TP + FP, missed hazardous cases = FN, threshold counts, calibration summaries, training-only preprocessing and resampling, statistical comparisons, bootstrap calculations and absence of Unnamed columns. All explicit stochastic seeds remain 42.

## 4. Figures

Five statistical figures were freshly generated from the recomputed results. All five passed the retained export checks (RGB TIFF, 300 dpi, width 2250 pixels, height <= 2625 pixels, LZW and < 10 MB). The retained plotting routine confirmed 36 exact source-data-to-curve bindings. PNG and editable SVG versions are also included. This does not claim an additional manual visual audit of every rendered label in this packaging task.

The two current conceptual TIFFs were copied unchanged from the author's final figure folder. Both were opened successfully, and the historical export report's source-PPT SHA-256 matches the supplied editable PPT. Provenance and dimensions are recorded in `metadata/diagram_source_provenance.json`. These supplied TIFFs are 7500 x 7000 pixels at 600 dpi; current journal upload-size suitability should be checked separately rather than inferred from the statistical-figure checks.

The optional new PowerPoint export wrappers preserve slide proportions and render at 4500 pixels wide before saving 600-dpi PNG/TIFF. Source availability was checked for all three conceptual-figure script slots, but actual PowerPoint COM rendering was **not tested in this packaging run**. Model reproduction does not use PowerPoint.

Editorial issue retained rather than silently changed: the supplied slide 2 says **“Cohen’s κappa assessment”** instead of **“Cohen’s κ assessment”**. The author should confirm the label before uploading the figure. No scientific values or conceptual diagram contents were altered here.

## 5. Missing / externally controlled items and release blockers

1. **License:** the source repository explicitly says no license has been selected by the authors. `LICENSE.md` preserves that notice. A rights-holder-approved license is required before calling this an open-source release. No MIT/CC license was invented.
2. **Zenodo provenance:** the author-supplied DOI and version identify the intended predecessor, but the remote Zenodo page could not be inspected. This report does not certify a byte-for-byte match with the published Version 2.0.0. No Version 2.1.0 DOI was fabricated.
3. **Third-party case reports:** the approximately 2.4 GB archive is not duplicated inside the software ZIP pending redistribution-scope confirmation. The complete member inventory and hashes are included. The reports are not needed to reproduce Tables 4, 5 or S4.
4. **Current consensus workbook:** no new final S1 workbook or coder agreement result is generated. Historical baseline case CSVs are distinctly labeled and must not be presented as the current consensus coding. This package makes no new Cohen's kappa claim.
5. **Optional rendering and network operations:** PowerPoint COM rendering, online dependency installation, fresh UCI retrieval and Conda creation remain outside the verified scope. Their requirements and limitations are disclosed in README.

## 6. Preservation and release decision

The original ZIPs, raw source folders, manuscript and previous outputs were not overwritten. The package contains newly organized copies plus reproducibly regenerated outputs; neither seeds nor parameters were searched to match old results. The published numerical results were not edited.

**The numerical package is independently executable after extraction with its pinned environment and bundled UCI data. It is a validated local 2.1.0 candidate, not yet an authorized open-source publication. Resolve the license, confirm remote version provenance and review the conceptual-figure label before public release.**
