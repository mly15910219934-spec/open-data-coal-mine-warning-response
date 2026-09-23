# Reproducibility notes

## Source authority and generations

The author-supplied local `PLOS_final_figure_code (2).zip`, particularly `revision_analysis_v2`, controls the revised numerical analysis. The separate `Final_Coder_Source_Package.zip` controls the frozen case-source inventory. No inference is made that the local bundle is byte-identical to Zenodo Version 2.0.0: the cited remote record could not be inspected.

Original frozen YAML files and model constructors are retained verbatim. Historical baseline modules remain at the root of `src/`, including `src/run_all.py`. The current reviewer-stage workflow is orchestrated by `scripts/run_all_analysis.py` and `src/workflow.py`, using the subdirectories of `src/`. It retains train-derived balanced sample weights for GB, balanced class weights for LR/RF/SVM, training-only CV, paired stratified bootstrap, and separate RandomOverSampler sensitivity. Do not run the historical `python -m src.run_all` command and label its output as the revised Table 4 or S4.

## Numerical protocol (unchanged)

- 70:30 stratified row-wise split; seed 42; 1808 training and 776 held-out records, including 51 held-out positives and 725 negatives.
- Original 18 features retained. OneHotEncoder with unknown categories ignored; StandardScaler for LR/SVM numeric features; numeric passthrough for RF/GB. Pipeline / ColumnTransformer fitted only to the fitting subset. No missing values; no imputation.
- No tuning or feature selection. All explicit stochastic seeds remain 42. Complete fitted parameter exports are regenerated in `output/tables/actual_pipeline_parameters.json` and `resampling_actual_pipeline_parameters.json`.
- Main imbalance strategy: LR/RF/SVM balanced class weights; GB balanced sample weights computed from its fitting subset. No main-analysis resampling.
- Table 4 reference cut-off: score >= 0.5. PR-AUC is average precision. Precision is defined as zero when no positive prediction exists.
- Table 5 preserves whole score ties and chooses the common attainable alert count closest to the predeclared target of 150 without using labels for selection. The reproduced common count is 147. The full sweep is 0.01 through 0.99 for each model.
- Repeated CV: 5 folds x 10 repeats on the fixed training subset; sample SD uses ddof=1. Preprocessing and weights are fitted within folds.
- S4 intervals: 2000 paired, class-stratified bootstrap samples from the fixed held-out predictions, seed 42, percentile 2.5/97.5 bounds. These are conditional intervals, not repeated model refits.
- Paired DeLong ROC comparisons and exact McNemar tests use Holm corrections within their own families. The original McNemar accuracy-difference interval uses a separate unstratified paired bootstrap, unchanged from the source implementation.
- RandomOverSampler is train-only and uses no balanced class/sample weights, preventing double correction. It is a sensitivity arm, not a replacement model configuration.
- Scores are decision values, not calibrated absolute hazard probabilities. Alert burden is test-set predicted-positive count, not measured dispatch workload. No field validation or causal accident-reduction claim is made.

## Engineering changes only

Paths were relocated relative to the package, and thin command wrappers were added. The baseline comparison now runs against newly fitted baseline values before fitting revision models. Stage-two checksums are rebuilt for that newly completed run (timestamps legitimately differ), while full-precision scientific results are separately compared against immutable supplied reference tables. No result is patched to make a check pass.

The old documentation's local manuscript path is replaced with its basename and historical provenance label. Original project scripts not needed by the new numerical command are retained as historical source text, with source hashes and redactions recorded. This prevents obsolete Word/Excel builder scripts from executing during import checks. They are not advertised as tested current commands.

## Release authorization and verification

The author explicitly authorized MIT licensing and confirmed the eight-creator order in CITATION.cff. The supplied DOI 10.5281/zenodo.21423640 is the author-confirmed concept DOI. Third-party materials retain their own licenses. No new DOI is fabricated, and no manuscript or coding result is modified.

Current verification is recorded in RELEASE_CHECK_REPORT.md. Prior packaging reports are historical receipts, not current release instructions. Numerical validation is distinguished from optional PowerPoint rendering, network download and Conda creation.
