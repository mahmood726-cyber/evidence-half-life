# The Evidence Half-Life

When does a cumulative meta-analysis conclusion become stable across reasonable analytical specifications, and what proportion of reviews never stabilize? We applied eight multiverse specifications combining four variance estimators with two CI methods to 307 eligible Cochrane reviews from the Pairwise70 dataset. Studies were ordered by publication year and robustness scores computed cumulatively from k equals three onward, with stabilization defined as sustained robustness above seventy percent. Only 147 of 307 reviews achieved sustained stabilization, yielding a 95% CI for the never-stabilized prevalence of 46.4-57.7%, with a median half-life of six studies. Mean conclusion volatility was 8.2 robustness percentage points per added study, and 63 reviews were early stabilizers reaching robust conclusions by k equals five. More than half of Cochrane meta-analyses never produce conclusions that are analytically robust regardless of the number of accumulated primary studies. Nonetheless, this analysis is limited to eight specifications and cannot capture sensitivity to outcome definitions, risk-of-bias exclusions, or subgroup choices.

**Live dashboard:** <https://mahmood726-cyber.github.io/evidencehalflife/>

## Run

Open `index.html` (or `index.html`) in any modern browser. No build step.

For local development:

```bash
python -m http.server 8000
# then open http://localhost:8000/
```

## Test

```bash
python -m pytest -q
```

The suite under `tests/` includes 1 test file(s).

## Repo layout

| Path | Purpose |
|---|---|
| `index.html` | the dashboard (main artifact) |
| `index.html` | landing page |
| `tests/` | pytest tests |
| `e156-submission/` | E156 micro-paper bundle |
| `E156-PROTOCOL.md` | project metadata (E156 entry #52) |

## License

See `LICENSE` (MIT).
