# V2 starting state check

PASS. Original data hash, fixed split, six frozen files and every held-out metric verified. Point estimates match exactly after round-trip CSV parsing.

| Model | ROC-AUC | PR-AUC (average precision) | Brier |
|---|---:|---:|---:|
| Logistic Regression | 0.783421230561 | 0.214252540467 | 0.171687786251 |
| Random Forest | 0.761798512508 | 0.243627028314 | 0.064147938144 |
| Gradient Boosting | 0.751386071670 | 0.258092094142 | 0.110017490114 |
| SVM | 0.696064908722 | 0.170283221109 | 0.058711316132 |

Train n=1808; held-out n=776, positive=51, negative=725. Seed 42.

Frozen files are read-only inputs to this extension. Original metadata remains historical; new settings are in run_metadata_v2.json. No main model is refitted by this extension.
