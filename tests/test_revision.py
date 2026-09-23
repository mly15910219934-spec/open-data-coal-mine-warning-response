import sys, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'output/tables'
def read(n):return pd.read_csv(R/n,float_precision='round_trip')
ABBR={'Logistic Regression':'LR','Random Forest':'RF','Gradient Boosting':'GB','SVM':'SVM'}

def test_baseline_gate():
    gate=json.loads((ROOT/'output/metadata/baseline_comparison.json').read_text())
    assert gate['passed'] and len(gate['checks'])==82

def test_data_and_split():
    a=read('split_assignments.csv');p=read('held_out_predictions.csv')
    assert len(a)==2584 and a.label.sum()==170 and (a.label==0).sum()==2414
    assert len(p)==776 and p.label.sum()==51 and (p.label==0).sum()==725
    assert a.row_index_zero_based.is_unique and p.row_index_zero_based.is_unique
    assert set(p.row_index_zero_based)==set(a.loc[a.split=='test','row_index_zero_based'])
    assert set(a.loc[a.split=='train','row_index_zero_based']).isdisjoint(p.row_index_zero_based)

def assert_counts(row,y,p):
    assert row.TP==int(np.sum((y==1)&p));assert row.FP==int(np.sum((y==0)&p))
    assert row.TN==int(np.sum((y==0)&~p));assert row.FN==int(np.sum((y==1)&~p))
    assert row.TP+row.FN==51 and row.TN+row.FP==725
    assert row['Warning workload']==row.TP+row.FP
    assert row['Missed hazardous cases']==row.FN and row['False alarms']==row.FP

def test_performance_from_saved_predictions():
    p=read('held_out_predictions.csv');y=p.label.to_numpy()
    for _,r in read('model_performance_revision.csv').iterrows():
        s=p[ABBR[r.Model]+'_score'].to_numpy()
        assert_counts(r,y,s>=.5)
        assert np.isclose(r['ROC-AUC'],roc_auc_score(y,s),rtol=0,atol=1e-14)
        assert np.isclose(r['PR-AUC'],average_precision_score(y,s),rtol=0,atol=1e-14)
        assert np.isclose(r['Brier Score'],brier_score_loss(y,s),rtol=0,atol=1e-14)

def test_all_threshold_counts():
    t=read('threshold_analysis_all_models.csv');p=read('held_out_predictions.csv');y=p.label.to_numpy()
    assert len(t)==396
    for name,g in t.groupby('Model'):
        assert np.allclose(g.Threshold,np.arange(1,100)/100)
        assert np.all(np.diff(g['Warning workload'])<=0)
        s=p[ABBR[name]+'_score'].to_numpy()
        for _,r in g.iterrows():assert_counts(r,y,s>=r.Threshold)

def test_matched_counts_and_cutoffs():
    p=read('held_out_predictions.csv');y=p.label.to_numpy()
    for file in ['matched_alert_burden_analysis.csv','table5_matched_operating_point.csv']:
        t=read(file)
        for _,r in t.iterrows():assert_counts(r,y,p[ABBR[r.Model]+'_score'].to_numpy()>=r['Decision cutoff'])
    t=read('table5_matched_operating_point.csv')
    assert t['Warning workload'].nunique()==1

def test_cv_excludes_heldout_and_weights():
    p=read('held_out_predictions.csv');test=set(p.row_index_zero_based)
    audits=json.loads((R/'cross_validation_fit_audit.json').read_text());validation=[]
    for a in audits:
        tr=set(a['Train row indices']);va=set(a['Validation row indices'])
        assert tr.isdisjoint(va) and tr.isdisjoint(test) and va.isdisjoint(test)
        assert len(tr)+len(va)==1808
        assert np.isclose(a['GB weight positive'],len(tr)/(2*a['Training positive']))
        assert np.isclose(a['GB weight negative'],len(tr)/(2*a['Training negative']))
        validation.extend(va)
    assert len(validation)==1808 and len(set(validation))==1808
    folds=read('cross_validation_fold_results.csv');summ=read('cross_validation_results.csv')
    assert len(folds)==20
    for _,r in summ.iterrows():
        f=folds[folds.Model==r.Model]
        assert np.isclose(r['ROC-AUC mean'],f['ROC-AUC'].mean())
        assert np.isclose(r['PR-AUC std'],f['PR-AUC'].std(ddof=1))

def test_calibration_counts():
    p=read('held_out_predictions.csv');bins=read('calibration_bin_data.csv')
    for name,g in bins.groupby('Model'):
        assert g.N.sum()==776 and g.Positive.sum()==51
        assert np.allclose(g['Observed positive fraction'],g.Positive/g.N)
        assert np.isclose(np.sum(g['Mean decision score']*g.N)/776,p[ABBR[name]+'_score'].mean())

def test_delong_auc_and_covariance():
    from run_revision import delong, NAMES
    d=json.loads((R/'delong_covariance.json').read_text());p=read('held_out_predictions.csv')
    expected=[roc_auc_score(p.label,p[ABBR[n]+'_score']) for n in NAMES]
    assert np.allclose(d['aucs'],expected)
    c=np.asarray(d['covariance']);assert np.allclose(c,c.T)
    assert np.linalg.eigvalsh(c).min()>-1e-12
    for f in ['delong_pairwise.csv','mcnemar_pairwise.csv']:
        x=read(f);assert len(x)==6
        assert (x['Holm adjusted p']>=x['Raw p']-1e-15).all()
        assert x['Holm adjusted p'].between(0,1).all()

def test_schema_and_source_hashes():
    for p in R.glob('*.csv'):
        a=pd.read_csv(p)
        assert not any(str(c).startswith('Unnamed') for c in a.columns)
    copy=ROOT
    manifest=json.loads((ROOT/'output/metadata/original_source_manifest.json').read_text())
    for relative,expected in manifest.items():
        assert hashlib.sha256((copy/relative).read_bytes()).hexdigest()==expected

def test_gb_only_model_training_change():
    old=pd.read_csv(ROOT/'outputs_v2/tables/model_performance.csv').set_index('model')
    new=read('model_performance_revision.csv').set_index('Model')
    for name in ['Logistic Regression','Random Forest','SVM']:
        for a,b in [('roc_auc','ROC-AUC'),('pr_auc','PR-AUC'),('recall','Recall')]:
            assert np.isclose(old.loc[name,a],new.loc[name,b],atol=1e-14,rtol=0)

def test_curve_source_data():
    from sklearn.metrics import roc_curve, precision_recall_curve
    p=read('held_out_predictions.csv');c=read('curve_source_data.csv')
    for name,abbr in ABBR.items():
        x,y,_=roc_curve(p.label,p[abbr+'_score']);q=c[(c.Model==name)&(c.Curve=='ROC')]
        assert np.allclose(q.x,x) and np.allclose(q.y,y)
        precision,recall,_=precision_recall_curve(p.label,p[abbr+'_score']);q=c[(c.Model==name)&(c.Curve=='PR')]
        assert np.allclose(q.x,recall) and np.allclose(q.y,precision)
