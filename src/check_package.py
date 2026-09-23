"""Check active Python imports, portable text paths, references and scientific outputs."""
from pathlib import Path
import argparse, ast, json, os, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
IMPORT_CODE='''import importlib,importlib.util,sys
from pathlib import Path
root=Path.cwd(); path=Path(sys.argv[1])
for p in [root,root/'src',root/'src/model_training',root/'src/statistics',root/'src/figure_generation',path.parent]:sys.path.insert(0,str(p))
if path.parent.name=='src':importlib.import_module('src.'+path.stem)
else:
    spec=importlib.util.spec_from_file_location('_package_check_'+path.stem,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
'''
def main():
    p=argparse.ArgumentParser();p.add_argument('--skip-imports',action='store_true');a=p.parse_args()
    result={'python_imports':[],'syntax_errors':[],'absolute_path_hits':[],'missing_readme_paths':[]}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',MPLBACKEND='Agg')
    for f in sorted(ROOT.rglob('*.py')):
        if any(x in f.parts for x in ['.venv','__pycache__']):continue
        rel=f.relative_to(ROOT).as_posix()
        try:ast.parse(f.read_text(encoding='utf-8-sig'))
        except SyntaxError as e:result['syntax_errors'].append({'file':rel,'error':str(e)});continue
        if not a.skip_imports:
            r=subprocess.run([sys.executable,'-c',IMPORT_CODE,str(f)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
            result['python_imports'].append({'file':rel,'pass':r.returncode==0,'error':r.stderr.replace(str(ROOT),'<PACKAGE_ROOT>') if r.returncode else ''})
    for f in ROOT.rglob('*'):
        if not f.is_file() or f.suffix not in ['.py','.md','.json','.yaml','.yml','.txt','.csv','.R','.ps1','.mjs']:continue
        if any(x in f.parts for x in ['.venv','__pycache__']):continue
        if f.name=='package_static_check.json':continue
        s=f.read_text(encoding='utf-8-sig',errors='replace')
        pattern=r'(?<![A-Za-z])[A-Za-z]:[\\/]|/'+r'mnt/data/|/'+r'home/\w+/'
        if re.search(pattern,s):result['absolute_path_hits'].append(f.relative_to(ROOT).as_posix())
    readme=(ROOT/'README.md').read_text(encoding='utf-8')
    for rel in re.findall(r'`((?:code|data|metadata|output|src|config|tests)/[^`*]+)`',readme):
        if not (ROOT/rel).exists():result['missing_readme_paths'].append(rel)
    import csv
    with (ROOT/'data/public_cases/source_package_inventory.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    expected={f'S1-{i:02d}' for i in range(1,33)}
    actual={r['Case ID'] for r in rows if r['Case ID']!='PACKAGE'}
    result['case_inventory_32_ids_match']=actual==expected
    result['case_subdirectories_32_match']={p.name for p in (ROOT/'data/public_cases').iterdir() if p.is_dir() and p.name.startswith('S1-')}==expected
    result['passed']=not any(result[k] for k in ['syntax_errors','absolute_path_hits','missing_readme_paths']) and all(x['pass'] for x in result['python_imports']) and actual==expected and result['case_subdirectories_32_match']
    out=ROOT/'output/metadata/package_static_check.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
