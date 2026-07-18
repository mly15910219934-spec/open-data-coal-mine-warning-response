# Test report

## Environment

- Fresh virtual environment: created with Python 3.12.13.
- Editable install command: `python -m pip install -e .`.
- The pinned editable installation completed successfully.
- Pinned runtime: NumPy 2.5.1, pandas 3.0.3, SciPy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, PyYAML 6.0.3, pytest 9.1.1.

## Final command result

Command: `pytest -q`

Result after the complete clean run: **PASS — 8 passed in 1.73 s.**

Final packaging regression after re-downloading the source data: **PASS — 8 passed in 7.34 s.** The downloaded raw files were then removed so the deposited `data/raw/` directory contains only `.gitkeep`.

One non-failing `FutureWarning` was emitted by scikit-learn 1.9.0 because the explicitly frozen Logistic Regression `penalty='l2'` parameter is deprecated for future removal. The parameter was not changed because the approved frozen configuration must remain fixed.

The test suite checks dataset counts, split counts, model-output accounting, threshold identities, output schemas, train-only preprocessing fit, lack of leakage, frozen parameters, and absence of `Unnamed` columns.
