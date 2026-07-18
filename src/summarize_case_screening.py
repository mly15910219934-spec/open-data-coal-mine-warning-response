from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .utils import ROOT, ensure_output_dirs


def main() -> None:
    ensure_output_dirs()
    log = pd.read_csv(ROOT / "data/public_cases/screening_log.csv", keep_default_na=False)
    counts = pd.DataFrame([
        {"stage": "identification", "count": "NR"}, {"stage": "deduplication", "count": "NR"},
        {"stage": "title/source screening", "count": "NR"}, {"stage": "full-record eligibility review", "count": "NR"},
        {"stage": "final inclusion", "count": str((log.eligibility_status == "included").sum())},
    ])
    counts.to_csv(ROOT / "outputs/tables/case_selection_counts.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 5)); ax.axis("off")
    for i, row in counts.iterrows():
        y = 1 - i * .2; ax.text(.5, y, f"{row.stage}\n{row['count']}", ha="center", va="center", bbox={"boxstyle":"round,pad=.5", "fc":"#eef4f8", "ec":"#4c7899"})
        if i < len(counts)-1: ax.annotate("", xy=(.5,y-.14), xytext=(.5,y-.07), arrowprops={"arrowstyle":"->", "color":"#4c7899"})
    ax.set_xlim(0,1); ax.set_ylim(.05,1.08); fig.tight_layout(); fig.savefig(ROOT / "outputs/figures/case_selection_flow.png", dpi=300); plt.close(fig)


if __name__ == "__main__": main()
