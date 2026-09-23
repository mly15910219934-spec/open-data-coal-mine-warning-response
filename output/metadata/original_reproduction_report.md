# Original reproduction report

UTC verification time: 2026-09-23T08:44:18.896080+00:00
Gate: PASS

Dataset: 2584 records, 170 positive, 2414 negative, positive ratio 0.065789473684; 18 input features.

The unmodified supplied code was executed with `python -m src.run_all` in a separate environment. The initial launch occurred while installation was still completing and failed on an unavailable pandas import; the retained successful rerun log is authoritative. Original source files outside revision_analysis were not changed.

Comparison uses exact agreement for counts and 0.000500001 tolerance for manuscript values printed to three decimal places.

| Table | Model | Metric | Manuscript | Recomputed | Match |
|---|---|---|---|---|---|
| 4 | Random Forest | accuracy | 0.921 | 0.921391752577 | True |
| 4 | Random Forest | precision | 0.308 | 0.307692307692 | True |
| 4 | Random Forest | recall | 0.157 | 0.156862745098 | True |
| 4 | Random Forest | f1 | 0.208 | 0.207792207792 | True |
| 4 | Random Forest | roc_auc | 0.762 | 0.761798512508 | True |
| 4 | Random Forest | pr_auc | 0.244 | 0.243627028314 | True |
| 4 | Random Forest | tp | 8 | 8 | True |
| 4 | Random Forest | fp | 18 | 18 | True |
| 4 | Random Forest | fn | 43 | 43 | True |
| 4 | Random Forest | warning_workload | 26 | 26 | True |
| 4 | Logistic Regression | accuracy | 0.803 | 0.802835051546 | True |
| 4 | Logistic Regression | precision | 0.193 | 0.192771084337 | True |
| 4 | Logistic Regression | recall | 0.627 | 0.627450980392 | True |
| 4 | Logistic Regression | f1 | 0.295 | 0.294930875576 | True |
| 4 | Logistic Regression | roc_auc | 0.783 | 0.783421230561 | True |
| 4 | Logistic Regression | pr_auc | 0.214 | 0.214252540467 | True |
| 4 | Logistic Regression | tp | 32 | 32 | True |
| 4 | Logistic Regression | fp | 134 | 134 | True |
| 4 | Logistic Regression | fn | 19 | 19 | True |
| 4 | Logistic Regression | warning_workload | 166 | 166 | True |
| 4 | Gradient Boosting | accuracy | 0.927 | 0.926546391753 | True |
| 4 | Gradient Boosting | precision | 0.200 | 0.2 | True |
| 4 | Gradient Boosting | recall | 0.039 | 0.0392156862745 | True |
| 4 | Gradient Boosting | f1 | 0.066 | 0.0655737704918 | True |
| 4 | Gradient Boosting | roc_auc | 0.745 | 0.744759972955 | True |
| 4 | Gradient Boosting | pr_auc | 0.189 | 0.189436508806 | True |
| 4 | Gradient Boosting | tp | 2 | 2 | True |
| 4 | Gradient Boosting | fp | 8 | 8 | True |
| 4 | Gradient Boosting | fn | 49 | 49 | True |
| 4 | Gradient Boosting | warning_workload | 10 | 10 | True |
| 4 | SVM | accuracy | 0.934 | 0.934278350515 | True |
| 4 | SVM | precision | 0.000 | 0 | True |
| 4 | SVM | recall | 0.000 | 0 | True |
| 4 | SVM | f1 | 0.000 | 0 | True |
| 4 | SVM | roc_auc | 0.696 | 0.696064908722 | True |
| 4 | SVM | pr_auc | 0.170 | 0.170283221109 | True |
| 4 | SVM | tp | 0 | 0 | True |
| 4 | SVM | fp | 0 | 0 | True |
| 4 | SVM | fn | 51 | 51 | True |
| 4 | SVM | warning_workload | 0 | 0 | True |
| 5 | Logistic Regression at 0.1 | precision | 0.066 | 0.0660621761658 | True |
| 5 | Logistic Regression at 0.1 | recall | 1.000 | 1 | True |
| 5 | Logistic Regression at 0.1 | f1 | 0.124 | 0.123936816525 | True |
| 5 | Logistic Regression at 0.1 | warning_workload | 772 | 772 | True |
| 5 | Logistic Regression at 0.1 | false_alarms | 721 | 721 | True |
| 5 | Logistic Regression at 0.1 | missed_hazardous_cases | 0 | 0 | True |
| 5 | Logistic Regression at 0.2 | precision | 0.079 | 0.0793157076205 | True |
| 5 | Logistic Regression at 0.2 | recall | 1.000 | 1 | True |
| 5 | Logistic Regression at 0.2 | f1 | 0.147 | 0.146974063401 | True |
| 5 | Logistic Regression at 0.2 | warning_workload | 643 | 643 | True |
| 5 | Logistic Regression at 0.2 | false_alarms | 592 | 592 | True |
| 5 | Logistic Regression at 0.2 | missed_hazardous_cases | 0 | 0 | True |
| 5 | Logistic Regression at 0.3 | precision | 0.103 | 0.102505694761 | True |
| 5 | Logistic Regression at 0.3 | recall | 0.882 | 0.882352941176 | True |
| 5 | Logistic Regression at 0.3 | f1 | 0.184 | 0.183673469388 | True |
| 5 | Logistic Regression at 0.3 | warning_workload | 439 | 439 | True |
| 5 | Logistic Regression at 0.3 | false_alarms | 394 | 394 | True |
| 5 | Logistic Regression at 0.3 | missed_hazardous_cases | 6 | 6 | True |
| 5 | Logistic Regression at 0.4 | precision | 0.138 | 0.137795275591 | True |
| 5 | Logistic Regression at 0.4 | recall | 0.686 | 0.686274509804 | True |
| 5 | Logistic Regression at 0.4 | f1 | 0.230 | 0.229508196721 | True |
| 5 | Logistic Regression at 0.4 | warning_workload | 254 | 254 | True |
| 5 | Logistic Regression at 0.4 | false_alarms | 219 | 219 | True |
| 5 | Logistic Regression at 0.4 | missed_hazardous_cases | 16 | 16 | True |
| 5 | Logistic Regression at 0.5 | precision | 0.193 | 0.192771084337 | True |
| 5 | Logistic Regression at 0.5 | recall | 0.627 | 0.627450980392 | True |
| 5 | Logistic Regression at 0.5 | f1 | 0.295 | 0.294930875576 | True |
| 5 | Logistic Regression at 0.5 | warning_workload | 166 | 166 | True |
| 5 | Logistic Regression at 0.5 | false_alarms | 134 | 134 | True |
| 5 | Logistic Regression at 0.5 | missed_hazardous_cases | 19 | 19 | True |
| 5 | Logistic Regression at 0.6 | precision | 0.237 | 0.236842105263 | True |
| 5 | Logistic Regression at 0.6 | recall | 0.529 | 0.529411764706 | True |
| 5 | Logistic Regression at 0.6 | f1 | 0.327 | 0.327272727273 | True |
| 5 | Logistic Regression at 0.6 | warning_workload | 114 | 114 | True |
| 5 | Logistic Regression at 0.6 | false_alarms | 87 | 87 | True |
| 5 | Logistic Regression at 0.6 | missed_hazardous_cases | 24 | 24 | True |
| 5 | Logistic Regression at 0.7 | precision | 0.253 | 0.253164556962 | True |
| 5 | Logistic Regression at 0.7 | recall | 0.392 | 0.392156862745 | True |
| 5 | Logistic Regression at 0.7 | f1 | 0.308 | 0.307692307692 | True |
| 5 | Logistic Regression at 0.7 | warning_workload | 79 | 79 | True |
| 5 | Logistic Regression at 0.7 | false_alarms | 59 | 59 | True |
| 5 | Logistic Regression at 0.7 | missed_hazardous_cases | 31 | 31 | True |

## Configuration

```json
{
  "configuration_statement": "This is a new reproducible configuration and is not claimed to be the exact configuration originally used for the manuscript.",
  "software_versions": {
    "python": "3.12.14",
    "numpy": "2.5.1",
    "pandas": "3.0.3",
    "scipy": "1.18.0",
    "scikit_learn": "1.9.0",
    "matplotlib": "3.11.0"
  },
  "analysis_config": {
    "configuration_status": "new reproducible configuration; not the verified original manuscript configuration",
    "required_statement": "This is a new reproducible configuration and is not claimed to be the exact configuration originally used for the manuscript.",
    "dataset": {
      "name": "Seismic-bumps",
      "doi": "10.24432/C5W902",
      "url": "https://archive.ics.uci.edu/static/public/266/seismic+bumps.zip",
      "archive_file": "seismic+bumps.zip",
      "data_file": "seismic-bumps.arff"
    },
    "target": "class",
    "categorical_features": [
      "seismic",
      "seismoacoustic",
      "shift",
      "ghazard"
    ],
    "numeric_features": [
      "genergy",
      "gpuls",
      "gdenergy",
      "gdpuls",
      "nbumps",
      "nbumps2",
      "nbumps3",
      "nbumps4",
      "nbumps5",
      "nbumps6",
      "nbumps7",
      "nbumps89",
      "energy",
      "maxenergy"
    ],
    "preprocessing": {
      "missing_values": "no imputation; validation fails if missing values are present",
      "categorical": "OneHotEncoder(handle_unknown=\"ignore\")",
      "scaled_numeric_models": [
        "Logistic Regression",
        "SVM"
      ],
      "numeric_scaler": "StandardScaler()",
      "tree_numeric_transform": "passthrough",
      "fit_scope": "preprocessing is fitted inside Pipeline on training data only",
      "resampling": "none"
    },
    "split": {
      "train_fraction": 0.7,
      "test_fraction": 0.3,
      "stratify": true,
      "random_state": 42
    },
    "score": {
      "method": "predict_proba[:, 1]",
      "positive_rule": "score >= decision_cutoff",
      "interpretation": "decision cut-offs, not absolute hazard probabilities"
    },
    "thresholds": [
      0.1,
      0.2,
      0.3,
      0.4,
      0.5,
      0.6,
      0.7
    ],
    "robustness": {
      "folds": 5,
      "repeats": 10,
      "random_state": 42,
      "bootstrap_iterations": 2000,
      "bootstrap_random_state": 42
    }
  },
  "train_records": 1808,
  "test_records": 776,
  "test_positive": 51,
  "test_negative": 725,
  "score_method": "predict_proba[:, 1]",
  "sampling": "none",
  "missing_value_handling": "no imputation; validated absent"
}
```

Full model settings: code/original_baseline/config/frozen_model_parameters_v2.yaml. Actual parameter export: code/original_baseline/outputs_v2/metadata/model_parameters.json. Split: 70:30 stratified, seed 42. Preprocessing: four categorical variables one-hot encoded; 14 numeric variables standardized for LR/SVM and passed through for RF/GB; no imputation or resampling; preprocessing fitted on training data inside Pipeline.