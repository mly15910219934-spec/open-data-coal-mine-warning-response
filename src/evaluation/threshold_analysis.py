"""Recompute cutoff and matched-burden outputs through the original joint runner."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow import train
if __name__=='__main__':train()
