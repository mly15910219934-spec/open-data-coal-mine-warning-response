"""CSV-only plots of frozen predictions and stage-two sensitivity outputs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'statistics'))
import json,hashlib
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.metrics import roc_curve,precision_recall_curve
from supplement_v2 import ROOT,OUT,read,guard,NAMES,ABBR

F=ROOT/'output/figures';checks=[];bindings=[]
plt.rcParams.update({'font.family':'Arial','font.size':8.5,'axes.labelsize':8.5,'legend.fontsize':8,'axes.titlesize':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'axes.linewidth':.8,'lines.linewidth':1.4,'savefig.facecolor':'white'})
colors=dict(zip(NAMES,['#2671A1','#D17B26','#3B8C72','#9D6AA7']))
styles=dict(zip(NAMES,['-','--','-.',':']))
def line(ax,x,y,name,source,**kw):
    obj=ax.plot(x,y,color=colors.get(name,'#555555'),linestyle=styles.get(name,'-'),**kw)[0]
    assert np.array_equal(obj.get_xdata(),np.asarray(x)) and np.array_equal(obj.get_ydata(),np.asarray(y))
    bindings.append({'source':source,'series':name,'n':len(x),'exact_curve_match':True})
    return obj
def panel(ax,label):ax.text(-.15,1.035,label,transform=ax.transAxes,fontsize=11,fontweight='bold')
def save(fig,stem):
    for ax in fig.axes:
        lo,hi=ax.get_xlim();ax.set_xticks([t for t in ax.get_xticks() if lo<=t<=hi])
        lo,hi=ax.get_ylim();ax.set_yticks([t for t in ax.get_yticks() if lo<=t<=hi])
    fig.canvas.draw();renderer=fig.canvas.get_renderer();w,h=fig.canvas.get_width_height()
    for text in fig.findobj(matplotlib.text.Text):
        if text.get_visible() and text.get_text():
            bb=text.get_window_extent(renderer)
            assert bb.x0>=-1 and bb.y0>=-1 and bb.x1<=w+1 and bb.y1<=h+1,(stem,text.get_text(),bb.bounds,w,h)
    fig.savefig(F/(stem+'.png'),dpi=300);fig.savefig(F/(stem+'.svg'))
    with Image.open(F/(stem+'.png')) as im:im.convert('RGB').save(F/(stem+'.tif'),compression='tiff_lzw',dpi=(300,300))
    with Image.open(F/(stem+'.tif')) as im:
        im.load();size=(F/(stem+'.tif')).stat().st_size
        ok=im.format=='TIFF' and im.mode=='RGB' and im.size[0]==2250 and im.size[1]<=2625 and im.info['compression']=='tiff_lzw' and all(abs(v-300)<.01 for v in im.info['dpi']) and size<10_000_000
        assert ok
        checks.append({'File':stem+'.tif','Pixels':str(im.size),'DPI':str(im.info['dpi']),'Mode':im.mode,'Compression':im.info['compression'],'Size MB':size/1e6,'Result':'PASS'})
    plt.close(fig)
def main():
    guard();p=read('held_out_predictions.csv');perf=read('model_performance_revision.csv').set_index('Model');curves=read('curve_source_data.csv')
    fig,axes=plt.subplots(1,2,figsize=(7.5,3.55));fig.subplots_adjust(left=.09,right=.98,bottom=.17,top=.92,wspace=.3)
    for name in NAMES:
        s=p[ABBR[name]+'_score'].to_numpy();fpr,tpr,_=roc_curve(p.label,s);precision,recall,_=precision_recall_curve(p.label,s)
        for k,x,y,metric,kind in [(0,fpr,tpr,'ROC-AUC','ROC'),(1,recall,precision,'PR-AUC','PR')]:
            c=curves[(curves.Model==name)&(curves.Curve==kind)];assert np.array_equal(c.x,x) and np.array_equal(c.y,y)
            line(axes[k],c.x,c.y,name,'curve_source_data.csv',label=f'{ABBR[name]} = {perf.loc[name,metric]:.3f}')
    axes[0].plot([0,1],[0,1],color='.65',ls='--',lw=.8);axes[1].axhline(170/2584,color='.5',ls='--',lw=.8,label='Dataset prevalence = 0.066')
    axes[0].set(xlabel='False positive rate',ylabel='True positive rate',xlim=(0,1),ylim=(0,1.02));axes[1].set(xlabel='Recall',ylabel='Precision',xlim=(0,1),ylim=(0,1.02))
    axes[0].legend(title='ROC-AUC',loc='lower right',frameon=False);axes[1].legend(title='PR-AUC (average precision)',loc='upper right',frameon=False)
    for ax,l in zip(axes,'ab'):panel(ax,l)
    save(fig,'Fig4_revision_combined')
    sweep=read('threshold_analysis_all_models.csv');fig,axes=plt.subplots(1,2,figsize=(7.5,3.55));fig.subplots_adjust(left=.09,right=.98,bottom=.18,top=.92,wspace=.42)
    for name in NAMES:
        d=sweep[sweep.Model==name]
        for ax,k in zip(axes,['Recall','Warning workload']):line(ax,d.Threshold,d[k],name,'threshold_analysis_all_models.csv',label=ABBR[name])
    for ax,l in zip(axes,'ab'):ax.set(xlabel='Decision cut-off',xlim=(0,1));ax.legend(frameon=False);panel(ax,l)
    axes[0].set(ylabel='Recall',ylim=(0,1.02));axes[1].set(ylabel='Held-out test-set alert burden',ylim=(0,len(p)*1.02))
    save(fig,'Fig5_revision_tradeoff')
    bins=read('calibration_bin_data.csv');fig,axes=plt.subplots(2,2,figsize=(7.5,5.6));fig.subplots_adjust(left=.1,right=.98,bottom=.1,top=.94,hspace=.46,wspace=.33)
    for ax,name,l in zip(axes.flat,NAMES,'abcd'):
        d=bins[bins.Model==name];line(ax,d['Mean decision score'],d['Observed positive fraction'],name,'calibration_bin_data.csv',marker='o',markersize=3)
        ax.plot([0,1],[0,1],ls='--',color='.6',lw=.8);ax.set(xlabel='Mean model decision score',ylabel='Observed positive fraction',xlim=(0,1),ylim=(0,1),title=f'{ABBR[name]}   Brier = {perf.loc[name,"Brier Score"]:.3f}');panel(ax,l)
    save(fig,'S1_Fig_revision_calibration')
    matched=read('matched_alert_burden_analysis.csv');fig,ax=plt.subplots(figsize=(7.5,4.1));fig.subplots_adjust(left=.1,right=.98,bottom=.16,top=.95)
    for name in NAMES:
        d=matched[matched.Model==name].sort_values('Warning workload');line(ax,d['Warning workload'],d.Recall,name,'matched_alert_burden_analysis.csv',marker='o',markersize=4,label=ABBR[name])
    ax.set(xlabel='Held-out test-set alert burden',ylabel='Recall',ylim=(0,1));ax.legend(frameon=False,ncol=4,loc='lower right');save(fig,'S2_Fig_matched_alert_burden')
    costs=read('cost_ratio_sensitivity_full.csv');fig,axes=plt.subplots(2,2,figsize=(7.5,5.8));fig.subplots_adjust(left=.12,right=.98,bottom=.11,top=.94,hspace=.48,wspace=.35)
    for ax,name,l in zip(axes.flat,NAMES,'abcd'):
        for ratio,c,st in zip([1,10,100],['#56788D','#CB8A40','#804B68'],['-','--',':']):
            d=costs[(costs.Model==name)&(costs['FN:FP cost ratio']==ratio)];obj=ax.plot(d.Threshold,d['Cost per test record'],color=c,ls=st,label=f'{ratio}:1')[0]
            assert np.array_equal(obj.get_ydata(),d['Cost per test record']);bindings.append({'source':'cost_ratio_sensitivity_full.csv','series':f'{name} {ratio}:1','n':len(d),'exact_curve_match':True})
        ax.set(xlabel='Decision cut-off',ylabel='Relative weighted cost\nper test record',title=ABBR[name],xlim=(0,1),ylim=(0,7));ax.legend(title='Hypothetical FN:FP cost',frameon=False,fontsize=8,title_fontsize=8);panel(ax,l)
    save(fig,'S3_Fig_cost_sensitivity')
    pd.DataFrame(checks).to_csv(ROOT/'output/metadata/figure_export_audit_v2.csv',index=False)
    (ROOT/'output/metadata/figure_source_bindings_v2.json').write_text(json.dumps(bindings,indent=2));guard()
    print(pd.DataFrame(checks).to_string(index=False))
if __name__=='__main__':main()
