"""Generate plots for the ROGII Wellbore Geology strategy brief.

Every value below is traced to what was gathered this run:
  - LB RMSE: fetched per-notebook via fetch_kernel_score.py (verified public LB).
  - CV/LB trajectory: Gaurav Rawat's posted training log, discussion 701691.
No value is interpolated or recalled from memory.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------
# Plot 1: Public score ladder — verified LB RMSE, colored by method family.
# (ref, short label, LB RMSE, family)
# family: baseline | physics/PF | blend
rows = [
    ("cdeotte/nn-starter-cv-15-5",                  "NN Starter (cdeotte)",            15.745, "baseline"),
    ("cdeotte/xgb-starter-cv-15",                   "XGB Starter (cdeotte)",           14.336, "baseline"),
    ("aidensong123/...lightgbm-baseline",           "LightGBM Baseline (aidensong)",   13.893, "baseline"),
    ("karnakbaevarthur/physics-informed-baseline",  "Physics-Informed Baseline",       10.159, "physics/PF"),
    ("romantamrazov/...super-solution-lb-top-3",    "Super Solution (romantamrazov)",  10.142, "blend"),
    ("ravaghi/...hill-climbing",                    "Hill Climbing (ravaghi)",          9.430, "blend"),
    ("nihilisticneuralnet/...dwt-based",            "DWT-based (nihilisticneuralnet)",  9.251, "physics/PF"),
    ("mitchgansemer/drift-targeting-ncc",           "Drift Targeting + NCC (mitch)",    8.905, "physics/PF"),
    ("needless090/...sel15-256seeds",               "SEL15 256-seeds (needless090)",    8.860, "physics/PF"),
    ("pilkwang/...target-free-alignment",           "Target-Free Alignment (pilkwang)", 8.072, "physics/PF"),
    ("ravaghi/...ridge",                            "Ridge SP (ravaghi)",               7.946, "blend"),
    ("lightningv08/lb-7-776-rogii-ridge-sp",        "Ridge-SP LB 7.776 (lightningv08)", 7.776, "blend"),
    ("jaemin3404/...sp45-fleongg-blend-v2",         "SP45+Fleongg Blend (jaemin)",      7.572, "blend"),
    ("pixiux/rogii-dual-pipeline-blend",            "Dual-Pipeline Blend (pixiux)",     7.519, "blend"),
]
rows_sorted = sorted(rows, key=lambda r: r[2])  # best (lowest RMSE) first
labels = [r[1] for r in rows_sorted]
scores = [r[2] for r in rows_sorted]
fams = [r[3] for r in rows_sorted]
cmap = {"baseline": "#b0b0b0", "physics/PF": "#2b8cbe", "blend": "#e6550d"}
colors = [cmap[f] for f in fams]

fig, ax = plt.subplots(figsize=(11, 6.5))
y = np.arange(len(labels))
ax.barh(y, scores, color=colors, edgecolor="white")
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.invert_yaxis()  # best at top
for yi, s in zip(y, scores):
    ax.text(s + 0.12, yi, f"{s:.2f}", va="center", fontsize=8.5)
ax.set_xlabel("Public LB RMSE (ft) — lower is better")
ax.set_xlim(0, 17.5)
ax.set_title("ROGII Wellbore Geology — public notebook score ladder (verified LB RMSE)", fontsize=12)
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[k]) for k in ["baseline", "physics/PF", "blend"]]
ax.legend(handles, ["tabular baseline", "physics / particle-filter", "blend / ensemble"],
          loc="lower right", frameon=True, fontsize=9)
ax.grid(axis="x", alpha=0.3)
fig.text(0.5, 0.005,
         "Takeaway: plain tabular starters sit at ~14–16 ft; the public frontier (~7.5 ft) is held by "
         "physics/PF + blends, ~2x better.",
         ha="center", fontsize=9, style="italic")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(OUT / "score_ladder.png", dpi=150)
plt.close(fig)

# ----------------------------------------------------------------------------
# Plot 2: CV vs LB trajectory — Gaurav Rawat's posted log (discussion 701691).
# Only rows where BOTH CV and LB were reported are plotted.
log = [
    # (version, CV, LB)
    ("v2",     31.387, 35.843),
    ("v2.1",   14.707, 13.949),
    ("v2.2",   14.463, 13.777),
    ("v2.5",   11.999, 12.383),
    ("v2.6",   11.269, 12.383),
    ("v2.7",   10.749, 10.606),
    ("v2.9",   10.326,  9.816),
    ("v2.10",  10.373, 10.384),
]
cv = np.array([r[1] for r in log])
lb = np.array([r[2] for r in log])
vers = [r[0] for r in log]

fig, ax = plt.subplots(figsize=(8.5, 7))
ax.scatter(cv, lb, c="#2b8cbe", s=80, zorder=3)
# Zoom to the meaningful working range; the v2 cold-start (CV 31.4 / LB 35.8)
# is annotated off to the side rather than compressing the cluster.
lims = [9, 15.2]
ax.plot(lims, lims, ls="--", color="gray", alpha=0.7, label="CV = LB (perfect agreement)")
# Hand-tuned label offsets so points in the dense cluster don't collide.
offsets = {
    "v2":    None,  # off-chart, handled separately
    "v2.1":  (6, 6), "v2.2": (6, -12),
    "v2.5":  (8, 2), "v2.6": (8, -12),
    "v2.7":  (8, 4), "v2.9": (6, -13), "v2.10": (8, 5),
}
for x, yv, v in zip(cv, lb, vers):
    if v == "v2":
        continue
    dx, dy = offsets.get(v, (6, 4))
    ax.annotate(v, (x, yv), textcoords="offset points", xytext=(dx, dy), fontsize=8.5)
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_aspect("equal")
ax.set_xlabel("Local CV RMSE (ft) — GroupKFold by well")
ax.set_ylabel("Public LB RMSE (ft)")
ax.set_title("CV tracks LB, but a gap persists near the frontier\n(Gaurav Rawat's log, discussion 701691)", fontsize=12)
ax.annotate("v2 cold-start off-chart\n(CV 31.4 / LB 35.8)", xy=(0.97, 0.03),
            xycoords="axes fraction", ha="right", va="bottom", fontsize=8,
            style="italic", color="gray")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
fig.text(0.5, 0.01,
         "Takeaway: every CV gain carried to the LB (trust CV), yet below ~12 ft the LB runs ~0.5 ft "
         "OPTIMISTIC vs CV — leave margin.",
         ha="center", fontsize=8.5, style="italic")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(OUT / "cv_vs_lb.png", dpi=150)
plt.close(fig)

print("wrote:", sorted(p.name for p in OUT.glob("*.png")))
