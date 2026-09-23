"""Portable orchestration; scientific engines retain the supplied calculations."""
from pathlib import Path
import hashlib, json, shutil, sys, runpy
ROOT=Path(__file__).resolve().parents[1]
for p in [ROOT,ROOT/'src/model_training',ROOT/'src/statistics',ROOT/'src/figure_generation']:
    sys.path.insert(0,str(p))
TABLES=ROOT/'output/tables'
LOG=ROOT/'output/metadata'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dirs():
    for p in [TABLES,LOG,ROOT/'output/figures',ROOT/'data/raw']:
        p.mkdir(parents=True,exist_ok=True)
def preprocess(download=False):
    dirs()
    if download:
        from src.download_data import main
        main()
    raw=ROOT/'data/raw/seismic-bumps.arff'
    expected=json.loads((ROOT/'metadata/reference_results/run_metadata_v2.json').read_text())['data_sha256']
    if not raw.exists():
        raise FileNotFoundError('Raw data absent. Restore the bundled data/raw snapshot or run preprocessing with --download.')
    assert sha(raw)==expected,'Dataset SHA-256 mismatch; no automatic substitution permitted.'
    from src.validate_data import main
    from src.v2_pipeline import split_data
    main()
    Xtr,Xte,ytr,yte,X,y=split_data()
    assert len(X)==2584 and int(y.sum())==170 and len(Xte)==776 and int(yte.sum())==51
    assert set(Xtr.index).isdisjoint(Xte.index)
    receipt={'rows':len(X),'positive':int(y.sum()),'negative':int((y==0).sum()),'train_n':len(Xtr),'test_n':len(Xte),'test_positive':int(yte.sum()),'test_negative':int((yte==0).sum()),'seed':42,'data_sha256':sha(raw),'missing_values':int(X.isna().sum().sum()),'preprocessing_fit':'inside each model Pipeline, on fitting subset only'}
    (LOG/'preprocessing_check.json').write_text(json.dumps(receipt,indent=2))
def compare(names):
    import numpy as np,pandas as pd
    records=[]
    for n in names:
        a=pd.read_csv(ROOT/'metadata/reference_results'/n,float_precision='round_trip')
        b=pd.read_csv(TABLES/n,float_precision='round_trip')
        pd.testing.assert_frame_equal(a,b,check_exact=True)
        records.append({'file':n,'comparison':'exact dataframe match','rows':len(a)})
    path=LOG/'reference_comparison.json'
    previous=json.loads(path.read_text()) if path.exists() else []
    combined={r['file']:r for r in previous+records}
    path.write_text(json.dumps(list(combined.values()),indent=2))
    return records
def train():
    preprocess()
    # Recompute the historical 82-cell baseline gate, rather than trust a saved PASS.
    from src import v2_pipeline as baseline
    *_,y_all,fitted,scores,table=baseline.fit_held_out()
    Xtr,Xte,ytr,yte,X,y=baseline.split_data()
    baseline.threshold_analysis(yte,scores['Logistic Regression'])
    shutil.copy2(ROOT/'metadata/manuscript_baseline_tables.json',LOG/'manuscript_baseline_tables.json')
    old_argv=sys.argv
    try:
        sys.argv=['check_baseline.py']
        try:runpy.run_path(str(ROOT/'src/evaluation/check_baseline.py'),run_name='__main__')
        except SystemExit as e:
            if e.code not in (0,None):raise
    finally:sys.argv=old_argv
    import run_revision
    run_revision.main()
    compare(['model_performance_revision.csv','table5_matched_operating_point.csv','held_out_predictions.csv','threshold_analysis_all_models.csv','split_assignments.csv'])
    import supplement_v2
    manifest={'results/'+n:sha(TABLES/n) for n in supplement_v2.FROZEN}
    (LOG/'v2_source_manifest.json').write_text(json.dumps(manifest,indent=2))
    source_manifest={p.relative_to(ROOT).as_posix():sha(p) for folder in ['src','config'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.py','.yaml']}
    (LOG/'original_source_manifest.json').write_text(json.dumps(source_manifest,indent=2))
    supplement_v2.stage1()
def bootstrap():
    import supplement_v2
    supplement_v2.bootstrap()
    compare(['bootstrap_2000_raw.csv','bootstrap_2000_summary.csv'])
    shutil.copy2(TABLES/'bootstrap_2000_summary.csv',TABLES/'S4_Table_bootstrap_confidence_intervals.csv')
def robustness():
    import supplement_v2
    supplement_v2.cv_run()
    supplement_v2.resampling()
    supplement_v2.costs()
    supplement_v2.reverify()
    compare(['repeated_cv_summary.csv','resampling_sensitivity_test.csv','resampling_cv_summary.csv','cost_ratio_sensitivity_summary.csv','delong_pairwise.csv','mcnemar_pairwise.csv'])
def tables():
    import supplement_v2
    supplement_v2.guard()
    compare(['model_performance_revision.csv','table5_matched_operating_point.csv','bootstrap_2000_summary.csv'])
    for a,b in [('model_performance_revision.csv','Table4_heldout_model_performance.csv'),('table5_matched_operating_point.csv','Table5_decision_cutoff_alert_burden.csv'),('bootstrap_2000_summary.csv','S4_Table_bootstrap_confidence_intervals.csv')]:
        shutil.copy2(TABLES/a,TABLES/b)
def figures():
    import plot_v2
    plot_v2.main()
def all_analysis():
    train();bootstrap();robustness();tables();figures()
