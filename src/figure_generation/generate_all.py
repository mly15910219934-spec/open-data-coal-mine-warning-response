"""Regenerate the five statistical figures; editable conceptual diagrams are separate."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow import figures
if __name__=='__main__':figures()
