# Competition Intel Briefing Demo

```bash
COMPETITION="rogii-wellbore-geology-prediction"
OUTPUT_FOLDER="demo/competition-intel-briefing/runs/${COMPETITION}_manual"
mkdir -p "$OUTPUT_FOLDER/plots"

PROMPT="Research the ${COMPETITION} Kaggle competition with the nvidia-kaggle skill and write me
a strategy brief on what it takes to do well. Include the key public notebooks
and discussions as links, and a few plots for insight. Save the brief to ${OUTPUT_FOLDER}/brief.md
and put any plot files under ${OUTPUT_FOLDER}/plots."
```

## Codex

```bash
codex exec \
  --skip-git-repo-check \
  -C /nvidia-kaggle \
  --dangerously-bypass-approvals-and-sandbox \
  "$PROMPT"
```

## Claude

```bash
claude -p "$PROMPT" \
  --add-dir /nvidia-kaggle \
  --allowedTools "Bash Read Write Skill"
```
