"""Reviewer-requested extension of the supplied frozen-v2 pipeline.

No model or preprocessing reimplementation: build_models and split_data come
from the retained original source. Only GB fit receives train-derived weights.
"""
from pathlib import Path
import sys, json, hashlib, platform, itertools, warnings
from datetime import datetime, timezone
import importlib.metadata
import numpy as np
import pandas as pd
from scipy.stats import norm, binomtest
from sklearn.base import clone
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (roc_auc_score, average_precision_score, accuracy_score,
    precision_score, recall_score, f1_score, brier_score_loss, confusion_matrix,
    roc_curve, precision_recall_curve)

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT
sys.path.insert(0, str(BASE))
from src.v2_pipeline import build_models, split_data, configs

OUT = ROOT/'output/tables'
SEED = 42
NAMES = ['Logistic Regression','Random Forest','Gradient Boosting','SVM']
ABBR = dict(zip(NAMES, ['LR','RF','GB','SVM']))

def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, default=str, allow_nan=False), encoding='utf-8')

def save(name, rows):
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT/name, index=False, float_format='%.17g')
    return frame

def counts(y, pred):
    tn, fp, fn, tp = confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {'TP':int(tp),'FP':int(fp),'TN':int(tn),'FN':int(fn),
        'Accuracy':accuracy_score(y,pred),'Precision':precision_score(y,pred,zero_division=0),
        'Recall':recall_score(y,pred,zero_division=0),'F1-score':f1_score(y,pred,zero_division=0),
        'False alarm rate':fp/(fp+tn),'Warning workload':int(tp+fp),
        'Warning workload percentage':float((tp+fp)/len(y)),
        'False alarms':int(fp),'Missed hazardous cases':int(fn)}

def fit(pipe, name, X, y):
    if name=='Gradient Boosting':
        weights=compute_sample_weight('balanced', y)
        pipe.fit(X,y,model__sample_weight=weights)
    else: pipe.fit(X,y)
    return pipe

def score_row(name, y, score):
    return {'Model':name, 'ROC-AUC':roc_auc_score(y,score),
        'PR-AUC':average_precision_score(y,score),'Brier Score':brier_score_loss(y,score),
        'Decision cutoff':.5,**counts(y,score>=.5)}

def attainable(score):
    # All score ties stay together; no labels are used to choose operating points.
    cutoffs=np.r_[np.nextafter(score.max(),np.inf),np.unique(score)[::-1]]
    return [(float(t),int(np.sum(score>=t))) for t in cutoffs]

def calibration(name,y,score,edges,method):
    b=np.searchsorted(edges[1:-1],score,side='left')
    rows=[]
    for i in range(len(edges)-1):
        selected=b==i
        if selected.sum():
            rows.append({'Model':name,'Method':method,'Bin':i+1,'Lower edge':float(edges[i]),
                'Upper edge':float(edges[i+1]),'N':int(selected.sum()),
                'Positive':int(np.sum(y[selected])), 'Mean decision score':float(np.mean(score[selected])),
                'Observed positive fraction':float(np.mean(y[selected]))})
    return rows

def holm(rows,key='Raw p'):
    ordered=sorted(range(len(rows)), key=lambda i:rows[i][key]); current=0.
    for rank,i in enumerate(ordered):
        current=max(current, min(1.,(len(rows)-rank)*rows[i][key]))
        rows[i]['Holm adjusted p']=current
    return rows

def delong(y,scores):
    structural_pos=[];structural_neg=[];aucs=[]
    for name in NAMES:
        s=scores[name];p=s[y==1];n=s[y==0]
        kernel=(p[:,None]>n[None,:]).astype(float)+.5*(p[:,None]==n[None,:])
        structural_pos.append(kernel.mean(axis=1));structural_neg.append(kernel.mean(axis=0));aucs.append(kernel.mean())
    cov=np.cov(structural_pos,ddof=1)/sum(y==1)+np.cov(structural_neg,ddof=1)/sum(y==0)
    rows=[]
    for i,j in itertools.combinations(range(4),2):
        effect=aucs[i]-aucs[j];var=cov[i,i]+cov[j,j]-2*cov[i,j];se=np.sqrt(max(0.,var))
        p=2*norm.sf(abs(effect/se)) if se>0 else (1. if effect==0 else 0.)
        rows.append({'Model A':NAMES[i],'Model B':NAMES[j],'ROC-AUC difference A-B':effect,
            'SE':se,'Lower 95% CI':effect-1.959963984540054*se,'Upper 95% CI':effect+1.959963984540054*se,'Raw p':p})
    save('delong_pairwise.csv',holm(rows));dump('delong_covariance.json',{'order':NAMES,'covariance':cov.tolist(),'aucs':aucs})

def main():
    gate=json.loads((ROOT/'output/metadata/baseline_comparison.json').read_text())
    if not gate['passed']: raise RuntimeError('Baseline gate failed; revision prohibited.')
    start=datetime.now(timezone.utc).isoformat()
    Xtr,Xte,ytr,yte,X,y=split_data();yt=yte.to_numpy()
    assert len(X)==2584 and int(y.sum())==170 and len(Xte)==776 and int(yte.sum())==51
    assert set(Xtr.index).isdisjoint(Xte.index)
    assert not X.isna().any().any()
    assert len(X.columns)==18
    analysis,params=configs()
    split_rows=[{'row_index_zero_based':int(i),'split':'train' if i in Xtr.index else 'test','label':int(y.loc[i])} for i in X.index]
    save('split_assignments.csv',split_rows)
    models=build_models();fitted={};scores={};perf=[];settings=[];actual={};fit_receipts=[]
    for name,pipe in models.items():
        print('Held-out fit:',name,flush=True)
        fitted[name]=fit(pipe,name,Xtr,ytr);s=pipe.predict_proba(Xte)[:,1];scores[name]=s
        perf.append(score_row(name,yt,s));actual[name]={k:repr(v) if not isinstance(v,(str,int,float,bool,type(None),list,dict,tuple)) else v for k,v in pipe.get_params(deep=True).items()}
        settings.append({'Model':name,'Imbalance strategy':'compute_sample_weight balanced on fitting subset' if name=='Gradient Boosting' else 'class_weight=balanced', 'Parameters':json.dumps(pipe.named_steps['model'].get_params(deep=True),sort_keys=True),'Random seed':SEED})
        pre=pipe.named_steps['preprocess']
        assert pre.n_features_in_==18
        if name in ['Logistic Regression','SVM']:
            scaler=pre.named_transformers_['numeric']
            assert int(scaler.n_samples_seen_)==len(Xtr)
            assert np.allclose(scaler.mean_, Xtr[analysis['numeric_features']].mean().to_numpy())
        fit_receipts.append({'Model':name,'Fitting records':len(Xtr),'Positive':int(ytr.sum()),'Negative':int((ytr==0).sum()),'GB weight negative':len(ytr)/(2*sum(ytr==0)) if name=='Gradient Boosting' else None,'GB weight positive':len(ytr)/(2*sum(ytr==1)) if name=='Gradient Boosting' else None})
    save('model_performance_revision.csv',perf);save('model_configuration_revision.csv',settings);dump('actual_pipeline_parameters.json',actual)
    save('training_weight_audit.csv',fit_receipts)
    pred=pd.DataFrame({'row_index_zero_based':Xte.index,'label':yt})
    for name,s in scores.items():pred[ABBR[name]+'_score']=s
    pred['SVM_decision_function']=fitted['SVM'].decision_function(Xte);pred['SVM_predict']=fitted['SVM'].predict(Xte)
    pred.to_csv(OUT/'held_out_predictions.csv',index=False,float_format='%.17g')

    sweep=[];att={};matched=[]
    for name,s in scores.items():
        for t in np.arange(1,100)/100:
            sweep.append({'Model':name,'Threshold':float(t),**counts(yt,s>=t)})
        att[name]=attainable(s)
        for target in [50,100,150,200,300,400]:
            cutoff,n=min(att[name],key=lambda q:(abs(q[1]-target),q[1]))
            matched.append({'Model':name,'Target alerts':target,'Decision cutoff':cutoff,'Burden difference':n-target,**counts(yt,s>=cutoff)})
    save('threshold_analysis_all_models.csv',sweep);save('matched_alert_burden_analysis.csv',matched)
    common=set(n for t,n in att[NAMES[0]])
    for name in NAMES[1:]:common &=set(n for t,n in att[name])
    common_n=min(common,key=lambda n:(abs(n-150),n))
    exact=[];matched_predictions={}
    for name,s in scores.items():
        cutoff=next(t for t,n in att[name] if n==common_n)
        matched_predictions[name]=s>=cutoff
        exact.append({'Model':name,'Decision cutoff':cutoff,'Target alerts':150,'Common attained alerts':common_n,**counts(yt,s>=cutoff)})
    save('table5_matched_operating_point.csv',exact)

    bins=[];cal=[]
    for name,s in scores.items():
        bins+=calibration(name,yt,s,np.quantile(s,np.linspace(0,1,11)),'10 quantile bins')
        cal.append({'Model':name,'Brier Score':brier_score_loss(yt,s),'Calibration bins':10,'Strategy':'quantile','Test samples':len(yt),'Positive samples':int(yt.sum())})
    save('calibration_results.csv',cal);save('calibration_bin_data.csv',bins)
    save('LR_calibration_fixed_bins.csv',calibration('Logistic Regression',yt,scores['Logistic Regression'],np.linspace(0,1,11),'fixed width 0.1'))
    svm_p=scores['SVM']>=.5;svm_d=pred['SVM_decision_function'].to_numpy()>0;svm_predict=pred['SVM_predict'].to_numpy()==1
    svm=[]
    for rule,p in [('predict_proba >= 0.5',svm_p),('decision_function > 0',svm_d),('predict',svm_predict)]:
        svm.append({'Rule':rule,'Agreement with proba rule':float(np.mean(p==svm_p)),'Difference samples vs proba':int(np.sum(p!=svm_p)),**counts(yt,p)})
    save('SVM_probability_check.csv',svm)
    save('SVM_disagreement_records.csv',[{'row_index_zero_based':int(i),'label':int(label),'proba_score':float(s),'decision_function':float(d)} for i,label,s,d,dis in zip(Xte.index,yt,scores['SVM'],pred['SVM_decision_function'],svm_p!=svm_d) if dis])

    delong(yt,scores)
    mc=[];rng=np.random.default_rng(SEED);boot_idx=rng.integers(0,len(yt),(2000,len(yt)))
    for a,b in itertools.combinations(NAMES,2):
        ca=matched_predictions[a]==yt;cb=matched_predictions[b]==yt
        bcount=int(np.sum(ca & ~cb));ccount=int(np.sum(~ca & cb));n=bcount+ccount
        diff=ca.astype(float)-cb.astype(float);boot=diff[boot_idx].mean(axis=1)
        mc.append({'Model A':a,'Model B':b,'Common alerts':common_n,'A correct B wrong':bcount,'A wrong B correct':ccount,'Accuracy difference A-B':float(diff.mean()),'Lower 95% CI':float(np.quantile(boot,.025)),'Upper 95% CI':float(np.quantile(boot,.975)),'Raw p':float(binomtest(bcount,n,.5).pvalue) if n else 1.})
    save('mcnemar_pairwise.csv',holm(mc))

    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=SEED);foldrows=[];foldaudit=[]
    for fold,(tri,vai) in enumerate(cv.split(Xtr,ytr),1):
        xf,yf=Xtr.iloc[tri],ytr.iloc[tri];xv,yv=Xtr.iloc[vai],ytr.iloc[vai]
        assert set(xf.index).isdisjoint(xv.index) and set(xf.index).isdisjoint(Xte.index) and set(xv.index).isdisjoint(Xte.index)
        foldaudit.append({'Fold':fold,'Train row indices':list(map(int,xf.index)),'Validation row indices':list(map(int,xv.index)),'Training positive':int(yf.sum()),'Training negative':int((yf==0).sum()),'GB weight positive':len(yf)/(2*sum(yf==1)),'GB weight negative':len(yf)/(2*sum(yf==0))})
        for name in NAMES:
            print('CV',fold,name,flush=True)
            pipe=fit(clone(models[name]),name,xf,yf);s=pipe.predict_proba(xv)[:,1]
            if name in ['Logistic Regression','SVM']:assert int(pipe.named_steps['preprocess'].named_transformers_['numeric'].n_samples_seen_)==len(xf)
            foldrows.append({'Model':name,'Fold':fold,'ROC-AUC':roc_auc_score(yv,s),'PR-AUC':average_precision_score(yv,s),'Validation N':len(yv),'Validation positive':int(yv.sum())})
    folds=save('cross_validation_fold_results.csv',foldrows)
    cvsummary=[]
    for name in NAMES:
        f=folds[folds.Model==name]
        cvsummary.append({'Model':name,'ROC-AUC mean':f['ROC-AUC'].mean(),'ROC-AUC std':f['ROC-AUC'].std(ddof=1),'PR-AUC mean':f['PR-AUC'].mean(),'PR-AUC std':f['PR-AUC'].std(ddof=1),'Folds':5,'Scope':'70% training subset','Random seed':SEED})
    save('cross_validation_results.csv',cvsummary);dump('cross_validation_fit_audit.json',foldaudit)

    curves=[]
    for name,s in scores.items():
        fpr,tpr,_=roc_curve(yt,s)
        for x,yv in zip(fpr,tpr):curves.append({'Model':name,'Curve':'ROC','x':x,'y':yv})
        precision,recall,_=precision_recall_curve(yt,s)
        for x,yv in zip(recall,precision):curves.append({'Model':name,'Curve':'PR','x':x,'y':yv})
    save('curve_source_data.csv',curves)
    versions={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','scikit-learn','matplotlib','PyYAML','pytest','Pillow']}
    raw=BASE/'data/raw/seismic-bumps.arff'
    dump('run_metadata.json',{'analysis_version':'major_revision_ml_1','started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'package_versions':versions,'random_seed':SEED,'original_analysis_config':analysis,'original_model_config':params,'change':'GB train-only balanced sample weights; reviewer-requested evaluation extensions','cv':{'n_splits':5,'shuffle':True,'random_state':SEED,'scope':'training subset only','SD_ddof':1},'common_alert_count_table5':common_n,'threshold_grid':[i/100 for i in range(1,100)],'pr_auc_definition':'average_precision_score','score_rule':'predict_proba[:,1] >= cutoff','data_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'train_n':len(Xtr),'test_n':len(Xte),'test_positive':int(yt.sum()),'resampling':'none','imputation':'none','statistical_correction':'Holm separately within ROC and McNemar families','bootstrap_accuracy_difference':{'iterations':2000,'seed':SEED},'independence_boundary':'No site/time grouping identifiers available; row-wise split does not establish external or temporal generalization.'})
    print(pd.DataFrame(perf).to_string(index=False),flush=True)
    print('Revision complete; common alerts:',common_n,flush=True)

if __name__=='__main__':
    main()
