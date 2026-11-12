# Analysis of the mechanical test results from my final-year project.
# Five composite samples (A to E) made from Luffa fibre, sweet potato peel
# starch and gum Arabic, with fibre content going from 40% to 60%.
# Run this from the same folder as data.csv.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tests = [
    "compression_force_N",
    "tensile_uts_MPa",
    "flexural_strength_MPa",
    "rockwell_hardness_HRA",
]

df = pd.read_csv("data.csv")


def min_max(column):
    # lowest value becomes 0, highest becomes 1
    return (column - column.min()) / (column.max() - column.min())


def r_squared(y, fitted):
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot


# CDI = average of the four scaled test results for each sample
df["CDI"] = df[tests].apply(min_max).mean(axis=1)
df["binder_to_fibre"] = (df["starch_percent"] + df["gum_arabic_percent"]) / df["fibre_percent"]

print(df[["sample", "fibre_percent", "binder_to_fibre", "CDI"]].round(3).to_string(index=False))

best = df.loc[df["CDI"].idxmax()]
print(f"\nBest sample: {best['sample']} with {best['fibre_percent']:.0f}% fibre (CDI {best['CDI']:.3f})")

# how well does a quadratic curve fit each result against fibre content?
print("\nR squared of a quadratic fit against fibre content:")
x = df["fibre_percent"].to_numpy(dtype=float)
for name in tests + ["CDI"]:
    y = df[name].to_numpy(dtype=float)
    curve = np.polyfit(x, y, 2)
    print(f"  {name}: {r_squared(y, np.polyval(curve, x)):.3f}")

# bar chart of the CDI, with the fibre content under each sample letter
labels = [f"{s}\n{f:.0f}%" for s, f in zip(df["sample"], df["fibre_percent"])]
plt.figure(figsize=(6, 4))
plt.bar(labels, df["CDI"], color="#1F3864")
plt.xlabel("Sample and fibre content")
plt.ylabel("CDI")
plt.title("CDI for each sample")
plt.tight_layout()
plt.savefig("cdi_chart.png", dpi=150)
print("\nSaved cdi_chart.png")
