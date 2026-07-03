#!/usr/bin/env python3
"""Plots for the ROGII top-kernel report. Every number traces to work/data.json,
which was built only from verified per-version Kaggle public-LB scores and
byte-level code diffs fetched this run."""
import json
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "work" / "data.json"))

# ---- validated palette (dataviz reference, light surface) ----
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
SUB = "#52514e"
BLUE = "#2a78d6"
AQUA = "#1baf7a"
YELLOW = "#eda100"
VIOLET = "#4a3aa7"
RED = "#e34948"
ORANGE = "#eb6834"
MAGENTA = "#e87ba4"
GREEN = "#008300"
GRID = "#e4e3df"

mpl.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.family": "DejaVu Sans",
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": "#c9c8c3",
    "xtick.color": SUB, "ytick.color": SUB, "font.size": 11,
    "axes.titlesize": 12.5, "axes.titleweight": "bold",
})


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# =====================================================================
# PLOT 1 — version-score trajectories for the six fully-diffed kernels,
# marking which version transitions were real code changes vs identical reruns.
# =====================================================================
def plot_trajectories():
    order = ["xgb_starter", "ridge", "dwt", "rebuild7295", "dualpipe_blend", "dualpipe_sv"]
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 7.4))
    for ax, key in zip(axes.flat, order):
        rows = D["diff"][key]
        m = D["meta"][key]
        xs = [r["version"] for r in rows]
        ys = [fnum(r["score"]) for r in rows]
        ax.plot(xs, ys, "-", color="#bfbeb9", lw=1.6, zorder=1)
        for r in rows:
            y = fnum(r["score"])
            if y is None:
                continue
            trans = r["vs_prev"]
            if trans == "IDENTICAL rerun":
                c, mk, lbl = MAGENTA, "D", "identical rerun"
            elif trans == "CHANGED":
                c, mk, lbl = BLUE, "o", "code changed"
            else:
                c, mk, lbl = SUB, "s", "first version"
            ax.scatter([r["version"]], [y], s=95, color=c, marker=mk,
                       edgecolor="white", linewidth=1.1, zorder=3)
            ax.annotate(f"{y:.3f}", (r["version"], y), textcoords="offset points",
                        xytext=(0, 9), ha="center", fontsize=8.4, color=INK)
        # best (lowest) marker
        valid = [(r["version"], fnum(r["score"])) for r in rows if fnum(r["score"])]
        bx, by = min(valid, key=lambda t: t[1])
        ax.scatter([bx], [by], s=230, facecolor="none", edgecolor=GREEN,
                   linewidth=2.0, zorder=4)
        ax.set_title(f"{m['owner']} · {m['title'][:26]}", fontsize=10.5)
        ax.set_xticks(xs)
        ax.grid(True, color=GRID, lw=0.8)
        ax.margins(y=0.28)
        ax.set_xlabel("version", fontsize=9)
    for ax in axes[:, 0]:
        ax.set_ylabel("public LB RMSE (↓)", fontsize=9)
    handles = [
        Line2D([], [], marker="o", color="white", markerfacecolor=BLUE, markersize=10, label="real code change"),
        Line2D([], [], marker="D", color="white", markerfacecolor=MAGENTA, markersize=10, label="identical-code rerun"),
        Line2D([], [], marker="o", color="white", markerfacecolor="none", markeredgecolor=GREEN, markersize=13, label="best version (kept)"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 1.005), fontsize=10.5)
    fig.suptitle("Per-version public LB by kernel — green ring = best version, "
                 "diamond = code byte-identical to previous version",
                 y=1.055, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    fig.savefig(ROOT / "plots" / "version_trajectories.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote version_trajectories.png")


# =====================================================================
# PLOT 2 — "same code, different score": identical-code groups and the
# public-LB spread they produce. Answers: are reruns really identical, and
# how much does the score move for free?
# =====================================================================
def plot_rerun_noise():
    # groups of runs sharing an identical code hash (verified this run)
    groups = [
        ("nihilisticneuralnet/DWT-based\n(v1–v4, one code hash)",
         [9.631, 9.632, 9.251, 9.395]),
        ("bernubritz/LB7295 Rebuild\n(v1 & v3, one code hash)",
         [7.153, 7.302]),
        ("pixiux v3  ==  lightningv08 v1\n(cross-author fork, identical bytes)",
         [7.559, 7.470]),
    ]
    fig, ax = plt.subplots(figsize=(11.2, 4.6))
    ypos = list(range(len(groups)))[::-1]
    for y, (label, scores) in zip(ypos, groups):
        lo, hi = min(scores), max(scores)
        ax.plot([lo, hi], [y, y], color="#ccccc6", lw=6, solid_capstyle="round", zorder=1)
        ax.scatter(scores, [y] * len(scores), s=130, color=MAGENTA,
                   edgecolor="white", linewidth=1.2, zorder=3)
        ax.annotate(f"spread {hi - lo:.3f} RMSE", ((lo + hi) / 2, y + 0.18),
                    ha="center", fontsize=9.5, color=RED, fontweight="bold")
        # stagger labels that sit too close on the x-axis
        ssort = sorted(scores)
        last_x = -1e9
        below = True
        for s in ssort:
            close = (s - last_x) < 0.12
            below = (not below) if close else True
            dy = -0.24 if below else -0.40
            ax.annotate(f"{s:.3f}", (s, y + dy), ha="center", fontsize=8.2, color=SUB)
            last_x = s
    ax.set_yticks(ypos)
    ax.set_yticklabels([g[0] for g in groups], fontsize=9.5)
    ax.set_xlabel("public LB RMSE — every dot below shares byte-identical code")
    ax.set_title("Same code, different leaderboard score: the stochastic-rerun band",
                 loc="left")
    ax.grid(True, axis="x", color=GRID, lw=0.8)
    ax.set_ylim(-0.7, len(groups) - 0.3)
    ax.margins(x=0.08)
    fig.tight_layout()
    fig.savefig(ROOT / "plots" / "rerun_noise.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote rerun_noise.png")


# =====================================================================
# PLOT 3 — code-change size vs score movement. Each dot = one version
# transition. x=lines touched (added+removed), y=score delta vs prev.
# Reruns (0 lines) still move the score — the noise floor.
# =====================================================================
def plot_change_vs_delta():
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    colors = {"xgb_starter": BLUE, "ridge": AQUA, "dwt": VIOLET,
              "rebuild7295": ORANGE, "dualpipe_blend": YELLOW, "dualpipe_sv": RED}
    for key, col in colors.items():
        rows = D["diff"][key]
        for i in range(1, len(rows)):
            prev, cur = rows[i - 1], rows[i]
            yp, yc = fnum(prev["score"]), fnum(cur["score"])
            if yp is None or yc is None:
                continue
            touched = cur["added"] + cur["removed"]
            delta = yc - yp  # negative = improvement
            x = touched + 0.6  # log-safe offset so reruns (0) sit at left
            ax.scatter([x], [delta], s=90, color=col, edgecolor="white",
                       linewidth=1.0, zorder=3,
                       label=D["meta"][key]["owner"])
    ax.axhline(0, color=SUB, lw=1.0, ls="--")
    ax.axvspan(0.35, 1.4, color=MAGENTA, alpha=0.10, zorder=0)
    ax.annotate("identical reruns\n(0 lines changed) —\nscore still drifts ±0.4",
                (0.86, -0.55), fontsize=8.8, color=RED, ha="center", va="top")
    # annotate the story points
    ax.annotate("cdeotte XGB: a 4-line baseline swap\n(recent-slope → last-known-TVT)  →  −4.71 RMSE",
                (8.6, -4.71), textcoords="offset points", xytext=(-14, 26),
                ha="right", fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1))
    ax.annotate("pixiux: 150-line rewrite\n(.py → notebook)  →  ≈ 0",
                (150, -0.001), textcoords="offset points", xytext=(-6, 34),
                ha="right", fontsize=9, color=YELLOW,
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=1.1))
    ax.set_xscale("log")
    ax.set_xlabel("lines of code touched in this version (added + removed, log scale)")
    ax.set_ylabel("Δ public LB vs previous version  (negative = improved ↓)")
    ax.set_title("Code-change size does not predict score movement", loc="left")
    ax.grid(True, color=GRID, lw=0.8)
    # dedup legend
    h, l = ax.get_legend_handles_labels()
    seen = dict(zip(l, h))
    ax.legend(seen.values(), seen.keys(), frameon=False, fontsize=9,
              title="kernel author", title_fontsize=9, loc="lower right")
    fig.tight_layout()
    fig.savefig(ROOT / "plots" / "change_vs_delta.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote change_vs_delta.png")


if __name__ == "__main__":
    plot_trajectories()
    plot_rerun_noise()
    plot_change_vs_delta()
