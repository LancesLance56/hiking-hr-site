from pathlib import Path

import pandas as pd
from scipy import stats

DATA = Path(__file__).resolve().parent.parent / "data" / "hike_data.xlsx"
MOVING = ["200 m", "400 m", "600 m", "800 m", "1000 m"]
MARKS = ["200 m", "400 m", "600 m", "800 m"]  # stops happen after these readings


def load(sheet):
    df = pd.read_excel(DATA, sheet, header=3).set_index("Subject")
    df.index = df.index.astype(float).astype(int)  # the sheets mix "3" and 3.0
    return df


sheets = {
    ("farm", "no rest"): load("Farm - No rest"), ("farm", "rest"): load("Farm - Rest"),
    ("biak", "no rest"): load("Biak - No rest"), ("biak", "rest"): load("Biak - Rest"),
}
moving = pd.DataFrame({k: v[MOVING].mean(axis=1) for k, v in sheets.items()})

print("Table 1")
effect = {}
for trail in ("farm", "biak"):
    no, rest = moving[(trail, "no rest")], moving[(trail, "rest")]
    effect[trail] = rest - no
    print(f"  {trail:5s} no rest {no.mean():.1f}  rest {rest.mean():.1f}  "
          f"effect {effect[trail].mean():+.1f} (p = {stats.ttest_rel(rest, no).pvalue:.3f})")
for cond in ("no rest", "rest"):
    b, f = moving[("biak", cond)], moving[("farm", cond)]
    print(f"  biak minus farm, {cond}: {(b - f).mean():+.1f} (p = {stats.ttest_rel(b, f).pvalue:.3f})")
d = effect["biak"] - effect["farm"]
print(
    f"  biak minus farm, effect of resting: {d.mean():+.1f} (p = {stats.ttest_rel(effect['biak'], effect['farm']).pvalue:.3f})")
print("  subjects with a bigger drop on Biak:", int((d < 0).sum()), "of", len(d))

print("\nTable A1")
table = moving.copy()
table.insert(0, "resting", sheets[("farm", "no rest")]["Resting HR"])
print(table.round(1).to_string())

print("\nreading before rest - reading after rest")
for trail in ("farm", "biak"):
    r = sheets[(trail, "rest")]
    drop = pd.concat([r[m] - r[f"{m} after rest"] for m in MARKS])
    nxt = ["400 m", "600 m", "800 m", "1000 m"]
    back = pd.concat([r[n] - r[f"{m} after rest"] for m, n in zip(MARKS, nxt)])
    print(f"  {trail:5s} drop {drop.mean():.1f}, climb back by next reading {back.mean():.1f}")
