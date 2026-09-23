"""Recompute the complete revised workflow from the bundled raw dataset."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import workflow

if __name__=='__main__':
    workflow.all_analysis()
