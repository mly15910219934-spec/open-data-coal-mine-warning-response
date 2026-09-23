"""Export editable PowerPoint sources without redesigning conceptual diagrams.

Requires Windows and a working Microsoft PowerPoint COM session. This optional
backend is not needed to reproduce model tables or statistical figures.
"""
from pathlib import Path
import argparse, subprocess, tempfile, shutil, sys
ROOT=Path(__file__).resolve().parents[2]
def export(source,slide,stem):
    if sys.platform!='win32':raise RuntimeError('Diagram export requires Windows/PowerPoint; editable PPTX sources are supplied.')
    from PIL import Image
    folder=ROOT/'output/figures';folder.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='coal_mine_diagram_') as t:
        temp=Path(t);deck=temp/'source.pptx';shutil.copy2(source,deck)
        script=ROOT/'src/figure_generation/export_powerpoint.ps1'
        subprocess.run(['powershell','-NoProfile','-NonInteractive','-File',str(script),'-Source',str(deck),'-Destination',str(temp/'figure.png'),'-Slide',str(slide)],check=True)
        with Image.open(temp/'figure.png') as img:
            rgba=img.convert('RGBA');white=Image.new('RGBA',img.size,'white');white.alpha_composite(rgba);rgb=white.convert('RGB')
            rgb.save(folder/(stem+'.png'),dpi=(600,600))
            rgb.save(folder/(stem+'.tiff'),compression='tiff_lzw',dpi=(600,600))
    print('Exported',stem)
def main(default_source,slide,stem):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check-source',action='store_true');a=p.parse_args()
    source=ROOT/'src/figure_generation/sources'/default_source
    if not source.exists():raise FileNotFoundError(source.name)
    if a.check_source:
        import zipfile
        with zipfile.ZipFile(source) as z:
            assert z.testzip() is None and f'ppt/slides/slide{slide}.xml' in z.namelist()
        print('PPTX source and slide present; rendering not performed.')
    else:export(source,slide,stem)
