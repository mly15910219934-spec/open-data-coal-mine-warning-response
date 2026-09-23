"""Run the scientific regression suite from any working directory."""
from pathlib import Path
import subprocess,sys
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q'],cwd=root))
