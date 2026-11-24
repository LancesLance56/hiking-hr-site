from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "hike_data.xlsx"
OUT = ROOT / "figures"

GREY, BLUE = "#6B6B6B", "#1F5A96"
PTS = ["Start", "200 m", "400 m", "600 m", "800 m", "1000 m"]
LABELS = ["Start", "200", "400", "600", "800", "1 km"]


def load(sheet):
    return pd.read_excel(DATA, sheet, header=3).set_index("Subject")


def panel(title, no_rest, rest, path):
    means = pd.DataFrame({"No rest": no_rest[PTS].mean().values,
                          "Rest": rest[PTS].mean().values}, index=LABELS)
    ax = means.plot(grid=True, color=[GREY, BLUE], linewidth=2.0, marker="o", markersize=6,
                    figsize=(3.4, 2.6), legend=False)
    ax.set_title(title, weight="bold")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Mean heart rate (bpm)")
    ax.set_ylim(80, 130)
    ax.figure.tight_layout()
    ax.figure.savefig(path, format="svg")
    plt.close(ax.figure)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fn, fr, bn, br = (load(s) for s in ["Farm - No rest", "Farm - Rest", "Biak - No rest", "Biak - Rest"])
    panel("Duran Farm", fn, fr, OUT / "fig2-duran-farm.svg")
    panel("Biak-na-Bato", bn, br, OUT / "fig2-biak-na-bato.svg")
    print("wrote", *sorted(p.name for p in OUT.glob("*.svg")))
