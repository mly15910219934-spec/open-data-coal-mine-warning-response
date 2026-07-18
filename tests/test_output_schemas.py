from pathlib import Path

import pandas as pd

from src.utils import ROOT


def test_all_generated_csv_tables_have_named_columns():
    tables = list((ROOT / "outputs_v2").rglob("*.csv"))
    assert tables
    for path in tables:
        frame = pd.read_csv(path)
        assert not any(str(column).startswith("Unnamed") for column in frame.columns), path


def test_expected_readme_outputs_exist():
    expected = [
        "outputs_v2/tables/model_performance.csv",
        "outputs_v2/tables/logistic_regression_threshold_sensitivity.csv",
        "outputs_v2/figures/roc_pr_curves.png",
        "outputs_v2/figures/threshold_workload.png",
        "outputs_v2/metadata/model_parameters.json",
        "outputs_v2/metadata/run_metadata.json",
        "outputs_v2/robustness/repeated_cv_summary.csv",
        "outputs_v2/robustness/bootstrap_intervals.json",
        "outputs_v2/robustness/logistic_regression_calibration.json",
        "outputs_v2/robustness/logistic_regression_calibration_curve.png",
    ]
    for relative in expected:
        path = ROOT / relative
        assert path.is_file() and path.stat().st_size > 0, relative

