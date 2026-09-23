from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow import preprocess
def main():
    p=argparse.ArgumentParser();p.add_argument('--download',action='store_true');args=p.parse_args()
    preprocess(args.download)
if __name__=='__main__':main()
