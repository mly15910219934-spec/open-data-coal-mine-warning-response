"""Regenerate the five statistical figures from calculated source tables."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import workflow

if __name__=='__main__':workflow.figures()
