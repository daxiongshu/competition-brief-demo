# ROGII Wellbore Geology Prediction — a top-kernel teardown: every version's score, what actually changed, and who depends on whom

*Compiled 2026-07-03 with the [nvidia-kaggle skill](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction). Every public-LB number below was fetched **per version** from Kaggle's kernel-version API; every "identical / changed" label comes from a **byte-level diff of the two versions' code**, not from the notebook title. Metric is **RMSE, lower is better**. For context, the public leaderboard leader on this date sits at **5.262** — well under any public notebook — so treat public-notebook scores as a floor to clear, not the ceiling.*

[Competition page](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction)

---

## Why this post exists

Kaggle stores **every** version of a public notebook and shows each one's leaderboard score — but it never shows you a **diff** between versions. So you can't tell, from the version list alone, whether "Version 7 (LB 9.251)" was a genuine improvement or just a **lucky rerun of identical code**. That distinction matters a lot here, because the strongest ROGII notebooks are **stochastic** (particle filters, random seeds), so the same code can land anywhere in a ~0.4-RMSE band from run to run.

This teardown answers three questions for eight of the most-upvoted public kernels:

1. **What did each version actually score?** (verified, per version)
2. **Was the change real, or an identical-code rerun?** (byte-level code diff)
3. **What does each kernel depend on, and at which version?** (data/kernel sources)

### How the "identical vs changed" call is made

![How a real edit is told apart from an identical rerun](https://raw.githubusercontent.com/daxiongshu/competition-brief-demo/main/claude_rogii_top_kernel_report_004/plots/diff_method.png)

For each version I download the exact source (`kernel_archive.py --version N`), strip cell outputs and execution counts, normalize trailing whitespace and blank lines, then hash and unified-diff consecutive versions. **Same hash ⇒ identical rerun** (any score move is pure run-to-run noise); **non-empty diff ⇒ real change** (I then read the actual edited lines). *SVG source: `plots/diff_method.svg`.*

---

## The eight kernels at a glance

Sorted by community votes. "Best LB" is the lowest verified public RMSE across the kernel's history; "best ver" is which version produced it — **often not the latest**.

| Kernel | Author | Votes | Versions | Best LB | Best ver | What the version history shows |
|---|---|---:|---:|---:|---:|---|
| [9.251 DWT-based](https://www.kaggle.com/code/nihilisticneuralnet/9-251-rogii-wellbore-geology-prediction-dwt-based) | nihilisticneuralnet | 645 | 4 | **9.251** | v3 | 4 versions, **one code hash** — score is pure rerun luck |
| [LB7295 Public Rebuild](https://www.kaggle.com/code/bernubritz/rogii-lb7295-public-rebuild) | bernubritz | 442 | 3 | **7.153** | v1 | v1 & v3 identical code, 7.153 vs 7.302 |
| [Dual Pipeline + Self-Verifying](https://www.kaggle.com/code/lightningv08/rogii-dual-pipeline-self-verifying) | lightningv08 | 281 | 2 | **7.470** | v1 | **v1 is a byte-for-byte fork** of pixiux's blend v3 |
| [Wellbore Geology \| Ridge](https://www.kaggle.com/code/ravaghi/wellbore-geology-prediction-ridge) | ravaghi | 260 | 6 | **7.946** | v6 | disciplined 1-line hyperparameter grind, 8.13 → 7.95 |
| [Dual-Pipeline Blend](https://www.kaggle.com/code/pixiux/rogii-dual-pipeline-blend) | pixiux | 229 | 3 | **7.519** | v1 | `.py` → notebook rewrite; best score was the first version |
| [Target-Free TVT Geosteering](https://www.kaggle.com/code/pilkwang/rogii-target-free-tvt-geosteering) | pilkwang | 213 | **42** | **7.501** | v36 | long real-iteration grind, 8.00 → 7.50 |
| [Public Score \[LB 7.159\]](https://www.kaggle.com/code/degnonguidi/public-score-rogii-lb-7-159) | degnonguidi | 200 | 18 | **7.159** | v16 | noisy: failed runs, one 3459-RMSE blowup, widest deps |
| [XGB Starter \[CV 15\]](https://www.kaggle.com/code/cdeotte/xgb-starter-cv-15) | cdeotte | 190 | 3 | **14.336** | v3 | a 4-line baseline swap moved LB 19.05 → 14.34 |

**Headline:** for three of these kernels the *best* score sits on a version whose code is **identical** to a version that scored differently — i.e. the "best" is partly luck. Read on.

---

## Per-version scores + diff verdicts

Below, **∆code** is added/removed lines vs the previous version (from the byte-diff); "identical" means the normalized code hash matched the previous version exactly.

### 1. nihilisticneuralnet — DWT-based (645 votes) — *the "same code, four scores" case*

| Ver | Public LB | vs prev code | Note |
|---:|---:|---|---|
| 1 | 9.631 | — | title *"Hill climbing 17bb04"* |
| 2 | 9.632 | **identical** (+0/−0) | rerun |
| 3 | **9.251** | **identical** (+0/−0) | rerun — this is the number in the title |
| 4 | 9.395 | **identical** (+0/−0) | rerun |

All four versions share one code hash (`c337477a`). The notebook is titled after its best rerun (9.251), but **the code that produced 9.632 and 9.395 is the same code**. This is the clearest example in the competition that a headline LB in a title can be a *sample from a noisy distribution*, not a reproducible result.

### 2. cdeotte — XGB Starter (190 votes) — *the highest-leverage 4 lines*

| Ver | Public LB | vs prev code | The actual edit |
|---:|---:|---|---|
| 1 | 19.047 | — | residual model over a *recent-slope* baseline |
| 2 | *(no score — run did not submit)* | — | |
| 3 | **14.336** | changed (+4/−4) | switched the residual baseline to **flat last-known-TVT**; keeps slope baselines only as features |

A four-line change — `cur["baseline_tvt"] = last_known_tvt` instead of `..._recent_slope`, plus dropping a test-row-map arg — cut **4.7 RMSE**. This is the reference "anchor on the last known `TVT_input`, predict the residual" trick, and its diff is the cheapest big win in the whole set.

### 3. ravaghi — "Ridge" (260 votes) — *a textbook hyperparameter grind*

Despite the name, this kernel is a **particle-filter ensemble blended with Ridge**. Every version is a 1–2 line tweak; nothing is a rerun.

| Ver | Public LB | vs prev code | The actual edit |
|---:|---:|---|---|
| 1 | 8.129 | — | PF ensemble, blend `0.3·tvt₁ + 0.7·tvt₂` |
| 2 | 8.308 | changed (+1/−1) | blend → `0.25 / 0.75` *(worse)* |
| 3 | 8.290 | changed (+1/−1) | blend → `0.35 / 0.65` |
| 4 | 8.252 | changed (+2/−2) | PF `n_seeds 128→256`; blend → `0.3 / 0.7` |
| 5 | 8.125 | changed (+1/−1) | PF `n_particles 500→600` |
| 6 | **7.946** | changed (+1/−1) | PF `n_seeds 256→150` *(the winning move)* |

The trajectory wobbles (v2 got worse) but trends down. The final gain came from *fewer* seeds (150) with *more* particles (600) — worth knowing before you copy someone's seed count as gospel.

### 4. pixiux — Dual-Pipeline Blend (229 votes) & 5. lightningv08 — Self-Verifying (281 votes) — *a cross-author fork*

| Kernel · Ver | Public LB | vs prev code | Note |
|---|---:|---|---|
| pixiux v1 | **7.519** | — | `.py` script; best of the three |
| pixiux v2 | 7.560 | changed (+43/−0) | `.py`, added logic |
| pixiux v3 | 7.559 | changed (+62/−88) | rewritten as a **notebook** |
| lightningv08 v1 | 7.470 | **identical to pixiux v3** | forked, ran, scored 0.089 better *for free* |
| lightningv08 v2 | 7.559 | changed (+101/−33) | added a **self-verifying** 2-submission blend selector |

`lightningv08/…-self-verifying` **version 1 is byte-for-byte identical** to `pixiux/…-blend` version 3 (verified: both 110,785 bytes, SHA `c952972e`). Same code, different public score (7.470 vs 7.559) — the stochastic band again. lightningv08's *own* contribution lands in v2 (a self-verifying blend of the fleongg + SP45 submissions), which traded 0.09 of public LB for robustness.

### 6. bernubritz — LB7295 Public Rebuild (442 votes)

| Ver | Public LB | vs prev code | Note |
|---:|---:|---|---|
| 1 | **7.153** | — | best version |
| 2 | *(no score)* | — | run did not submit |
| 3 | 7.302 | **identical to v1** (+0/−0) | rerun scored 0.149 worse |

The 2nd-most-upvoted kernel, and its best score is v1 — a later **identical rerun** did *worse*. If you fork this, fork **v1**.

### 7 & 8. The long grinds — real iteration, but read the noise

These two have too many versions to tabulate line-by-line, but the shape is the story (see the trajectory panel below). Verified best scores:

- **pilkwang — Target-Free TVT Geosteering: 42 versions**, 8.004 (v1) → **7.501 (v36)**, then drifts back up to ~7.58. Genuine iteration — but the last version is **not** the best; v36 is.
- **degnonguidi — Public Score [LB 7.159]: 18 versions**, best **7.159 (v16)**. History is noisy: several versions failed to score, and **v9 scored 3459.018** (a broken submission). Best ≠ latest here either.

---

## Seeing it: version score trajectories

![Per-version public LB for the six fully-diffed kernels](https://raw.githubusercontent.com/daxiongshu/competition-brief-demo/main/claude_rogii_top_kernel_report_004/plots/version_trajectories.png)

**Takeaway:** the green ring (best version) lands on the *latest* version only twice (ravaghi, cdeotte). For DWT, pixiux and bernubritz the best score is an earlier version — and for DWT/bernubritz it sits on **code identical** to a worse-scoring sibling. If you're forking for a submission, pick the version by *verified score*, not by "latest".

## The core finding: same code, different leaderboard score

![Identical-code groups and the LB spread they produce](https://raw.githubusercontent.com/daxiongshu/competition-brief-demo/main/claude_rogii_top_kernel_report_004/plots/rerun_noise.png)

Three independent cases where **byte-identical code** produced **different public LB scores**:

| Identical-code group | Score spread (RMSE) |
|---|---:|
| DWT v1–v4 (one hash) | 9.251 → 9.632 = **0.381** |
| LB7295 Rebuild v1 & v3 | 7.153 → 7.302 = **0.149** |
| pixiux v3 ≡ lightningv08 v1 (fork) | 7.470 → 7.559 = **0.089** |

**Implication for your own work:** a 0.1–0.4 RMSE move on the public LB between two of your submissions can be *pure rerun variance*. Don't trust a single run of a stochastic pipeline; average seeds and judge on CV. And treat "LB x.xxx" in a notebook title as *a draw from a distribution*, not a guarantee.

## Does the size of a code change predict the score change? No.

![Lines of code touched vs change in public LB](https://raw.githubusercontent.com/daxiongshu/competition-brief-demo/main/claude_rogii_top_kernel_report_004/plots/change_vs_delta.png)

Two extremes make the point: **cdeotte moved 4 lines and gained 4.7 RMSE**; **pixiux rewrote ~150 lines (script → notebook) and moved essentially 0**. Meanwhile the identical reruns (0 lines) still drift ±0.4. Read the *diff*, not the line count.

---

## Dependencies (with version info)

![Featured-kernel dependency web](https://raw.githubusercontent.com/daxiongshu/competition-brief-demo/main/claude_rogii_top_kernel_report_004/plots/dependency_web.png)

*SVG source: `plots/dependency_web.svg`.* Kaggle attaches data/kernel sources **unpinned** — a notebook references a dataset by `owner/slug` and resolves to that dataset's **latest** version at run time. So the versions below are each dataset's **current** version (fetched 2026-07-03), which is what a fork of these kernels loads today.

| Shared data source | Cur. version | Size | Used by (of the 8) |
|---|:--:|--:|---|
| `ravaghi/wellbore-geology-prediction-artifacts` | **v6** | 2.36 GB | **7** — dwt, ridge, pixiux, lightningv08, bernubritz, pilkwang, degnonguidi |
| `fleongg/rogii-claude-models-pub` | v1 | 0.01 GB | 5 — pixiux, lightningv08, bernubritz, pilkwang, degnonguidi |
| `phongnguyn23021656/koolbox-offline` | v1 | 0.05 GB | 4 — pixiux, lightningv08, bernubritz, degnonguidi *(offline pip wheels — internet is off in this comp)* |
| `pilkwang/rogii-model-package` | v9 | 0.22 GB | 1 — pilkwang |
| `thbdh5765/rogii-v10-fresh-artifacts` | v1 | 0.41 GB | 1 — degnonguidi |
| `needless090/rogii-tabicl-mirror` | v1 | 0.11 GB | 1 — degnonguidi |
| `nina2025/rogii-03` | v5 | <0.01 GB | 1 — degnonguidi |

**Two things worth knowing:**

- **One dataset is the backbone.** `ravaghi/…-artifacts` (v6, 2.36 GB — it ships `data/train.csv` plus pre-trained CatBoost models) is loaded by **7 of the 8** kernels. If it's ever revised, a lot of public notebooks shift underneath their authors. The blend family additionally shares the exact same trio (`koolbox-offline` + `rogii-claude-models-pub` + `artifacts`), consistent with them being forks of one lineage.
- **`kernel_sources` are mostly noise.** Every kernel's `kernel_sources` field points at auto-generated `packagemanager/pm-…` entries (Kaggle's offline-package snapshots), **not** at another notebook — so the metadata does *not* reveal the pixiux → lightningv08 fork. The only way I found that lineage was the **byte-identical code hash**. Metadata under-reports real code reuse in this competition; diff the source.

---

## Practical takeaways

1. **Pick a fork version by verified score, not "latest."** For DWT, pixiux, and bernubritz the best score is an earlier version; for DWT/bernubritz that best is a *lucky rerun* of code that also scored worse.
2. **Expect ±0.1–0.4 RMSE of rerun noise** on the stochastic pipelines. Average seeds; trust CV over a single public-LB draw.
3. **The cheapest verified win is cdeotte's residual-baseline swap** (recent-slope → last-known-TVT): 4 lines, −4.7 RMSE. Start there.
4. **The public frontier here (~7.15–7.5) is a shared-lineage plateau** built on one artifacts dataset + a couple of model packages. Real separation on the private LB (leader 5.26) will come from *decorrelating* from that lineage, not re-forking it.
5. **Don't trust `kernel_sources` for lineage** — diff the code hashes.

## Reproduce this

```bash
# per-version public LB scores for any kernel
python ./scripts/kernel_archive.py <owner/slug> --scores-only

# download a specific version's source to diff
python ./scripts/kernel_archive.py <owner/slug> <out_dir> --version N

# dependency sources
kaggle kernels pull <owner/slug> -m   # then read kernel-metadata.json
```

The diff classifier (`work/diff_versions.py`), the consolidated data (`work/data.json`), and the figure/SVG generators (`plots/make_plots.py`, `plots/make_svgs.py`) are all in this folder — every number above traces back to them.

---

### Kernels referenced
[DWT-based (nihilisticneuralnet)](https://www.kaggle.com/code/nihilisticneuralnet/9-251-rogii-wellbore-geology-prediction-dwt-based) ·
[LB7295 Rebuild (bernubritz)](https://www.kaggle.com/code/bernubritz/rogii-lb7295-public-rebuild) ·
[Dual Pipeline + Self-Verifying (lightningv08)](https://www.kaggle.com/code/lightningv08/rogii-dual-pipeline-self-verifying) ·
[Ridge (ravaghi)](https://www.kaggle.com/code/ravaghi/wellbore-geology-prediction-ridge) ·
[Dual-Pipeline Blend (pixiux)](https://www.kaggle.com/code/pixiux/rogii-dual-pipeline-blend) ·
[Target-Free TVT Geosteering (pilkwang)](https://www.kaggle.com/code/pilkwang/rogii-target-free-tvt-geosteering) ·
[Public Score LB 7.159 (degnonguidi)](https://www.kaggle.com/code/degnonguidi/public-score-rogii-lb-7-159) ·
[XGB Starter (cdeotte)](https://www.kaggle.com/code/cdeotte/xgb-starter-cv-15)
