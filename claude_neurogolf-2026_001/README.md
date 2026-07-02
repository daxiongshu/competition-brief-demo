# NeuroGolf 2026 Competition Brief — Claude / nvidia-kaggle-skill demo

## Prompt

> use agent skill in /nvidia-kaggle to create a beautiful and informative report of
> https://www.kaggle.com/competitions/neurogolf-2026
> cover recent top discussions and kernels.
>
> *(follow-up, sent mid-run)* html format

See [`prompt.txt`](./prompt.txt) for the verbatim turns.

## What happened

Claude used the `nvidia-kaggle-skill` (competition overview, dataset description, discussion
ingest/query, kernel ingest/query/read, and live per-kernel score fetches) plus the Kaggle CLI to
pull the live public leaderboard (2,757 teams), 100 indexed discussions (782 comments), 100 indexed
kernels, and API-verified scores for 24 of the top-voted kernels. It then wrote its own analysis and
matplotlib charts (score distribution, votes-vs-score, score ladder) and assembled everything into a
single self-contained HTML report — no template, no fixed brief format, just the skill's
research-brief principles (accurate mechanics, sourced techniques, a measured score ladder, honest
plots) applied freely.

## Output

- [`neurogolf_2026_report.html`](./neurogolf_2026_report.html) — the final report (open in a browser).
- [`trace.html`](./trace.html) — self-contained, read-only viewer of the full agent session that
  produced the report (every prompt, tool call, and tool result, including the mid-run "html format"
  follow-up and the GitHub Pages debugging that came after).

## Time

**~10 minutes** wall-clock, interactive, end-to-end (skill discovery → data gathering → chart
generation → HTML assembly → visual QA via a headless-browser screenshot pass).
