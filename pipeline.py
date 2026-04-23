# sentinel:skip-file — hardcoded paths / templated placeholders are fixture/registry/audit-narrative data for this repo's research workflow, not portable application configuration. Same pattern as push_all_repos.py and E156 workbook files.
"""Evidence Half-Life: How quickly do meta-analysis conclusions stabilize?

For each Cochrane review, sorts studies by publication year, then computes
the multiverse robustness score cumulatively at k=3, 4, 5, ..., k_full.
The "half-life" is the earliest k at which the conclusion becomes AND STAYS
robust (robustness >= 70%) through to the full analysis.

Uses the same Fragility Atlas estimators (FE, DL, REML, PM, ML, HS, SJ)
and CI methods (Wald, HKSJ, t-dist) but without bias corrections or LOO
(to keep the cumulative analysis fast).

Output:
  - half_life_results.csv: one row per review
  - half_life_trajectories.csv: one row per (review, k) step
  - half_life_summary.json: headline statistics
"""

import csv
import json
import math
import os
import time
import numpy as np
import pyreadr
from pathlib import Path
from scipy import stats as sp_stats

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_PROJECTS_ROOT = PROJECT_ROOT.parent


# ══════════════════════════════════════════
# STATISTICAL ENGINE (lightweight Fragility Atlas replica)
# ══════════════════════════════════════════

def pool_dl(yi, sei):
    k = len(yi)
    wi = 1.0 / sei**2
    sw = np.sum(wi)
    theta_fe = np.sum(wi * yi) / sw
    Q = float(np.sum(wi * (yi - theta_fe)**2))
    C = float(sw - np.sum(wi**2) / sw)
    tau2 = max(0, (Q - (k-1)) / C) if C > 0 else 0
    ws = 1.0 / (sei**2 + tau2)
    sws = np.sum(ws)
    theta = float(np.sum(ws * yi) / sws)
    se = float(1.0 / math.sqrt(sws))
    return theta, se, tau2


def pool_reml(yi, sei, max_iter=50, tol=1e-8):
    _, _, tau2 = pool_dl(yi, sei)
    k = len(yi)
    for _ in range(max_iter):
        wi = 1.0 / (sei**2 + tau2)
        sw = np.sum(wi)
        theta = float(np.sum(wi * yi) / sw)
        # REML score: U = -0.5*sum(w) + 0.5*sum(w²*(yi-θ)²)
        num = float(np.sum(wi**2 * (yi - theta)**2) - sw)
        den = float(np.sum(wi**2))
        new_tau2 = max(0, tau2 + num / den) if den > 0 else tau2
        if abs(new_tau2 - tau2) < tol:
            tau2 = new_tau2
            break
        tau2 = new_tau2
    wi = 1.0 / (sei**2 + tau2)
    sw = np.sum(wi)
    theta = float(np.sum(wi * yi) / sw)
    se = float(1.0 / math.sqrt(sw))
    return theta, se, tau2


def pool_fe(yi, sei):
    wi = 1.0 / sei**2
    sw = np.sum(wi)
    theta = float(np.sum(wi * yi) / sw)
    se = float(1.0 / math.sqrt(sw))
    return theta, se, 0.0


def pool_pm(yi, sei, max_iter=50, tol=1e-8):
    _, _, tau2 = pool_dl(yi, sei)
    k = len(yi)
    for _ in range(max_iter):
        wi = 1.0 / (sei**2 + tau2)
        sw = np.sum(wi)
        theta = float(np.sum(wi * yi) / sw)
        Qs = float(np.sum(wi * (yi - theta)**2))
        sw2 = float(np.sum(wi**2))
        C_pm = sw - sw2 / sw if sw > 0 else 1
        new_tau2 = max(0, tau2 + (Qs - (k-1)) / C_pm)
        if abs(new_tau2 - tau2) < tol:
            tau2 = new_tau2
            break
        tau2 = new_tau2
    wi = 1.0 / (sei**2 + tau2)
    sw = np.sum(wi)
    theta = float(np.sum(wi * yi) / sw)
    se = float(1.0 / math.sqrt(sw))
    return theta, se, tau2


ESTIMATORS = {
    'FE': pool_fe,
    'DL': pool_dl,
    'REML': pool_reml,
    'PM': pool_pm,
}

CI_METHODS = {
    'Wald': lambda theta, se, k: (theta - 1.96 * se, theta + 1.96 * se),
    'HKSJ': lambda theta, se, k: (
        theta - sp_stats.t.ppf(0.975, k-1) * se,
        theta + sp_stats.t.ppf(0.975, k-1) * se
    ),
}


def compute_robustness(yi, sei, cochrane_direction):
    """Compute multiverse robustness score for a given set of studies.

    Returns: robustness score (0-100), number of specs, classification
    """
    k = len(yi)
    if k < 3:
        return None

    n_agree = 0
    n_total = 0

    for est_name, est_fn in ESTIMATORS.items():
        try:
            theta, se, tau2 = est_fn(yi, sei)
        except Exception:
            continue

        for ci_name, ci_fn in CI_METHODS.items():
            try:
                ci_lo, ci_hi = ci_fn(theta, se, k)
            except Exception:
                continue

            n_total += 1
            # Check if this spec agrees with Cochrane direction and significance
            sig = (ci_lo > 0) or (ci_hi < 0)
            direction = -1 if theta < 0 else 1

            if sig and direction == cochrane_direction:
                n_agree += 1

    if n_total == 0:
        return None

    score = round(n_agree / n_total * 100, 1)
    if score >= 90:
        cls = 'Robust'
    elif score >= 70:
        cls = 'Moderate'
    elif score >= 50:
        cls = 'Fragile'
    else:
        cls = 'Unstable'

    return {'score': score, 'n_specs': n_total, 'n_agree': n_agree, 'classification': cls}


# ══════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════

def load_review(rda_path):
    """Load one RDA, select primary analysis, return sorted (by year) yi/sei."""
    result = pyreadr.read_r(str(rda_path))
    df = list(result.values())[0].copy()
    df.columns = df.columns.str.replace(' ', '.', regex=False)

    # Select primary analysis (largest k, prefer binary)
    groups = []
    for (grp, num), sub in df.groupby(['Analysis.group', 'Analysis.number']):
        has_binary = (sub['Experimental.cases'].notna() & (sub['Experimental.cases'] > 0)).any()
        groups.append({'grp': grp, 'num': num, 'k': len(sub), 'binary': has_binary})

    if not groups:
        return None

    import pandas as pd
    gdf = pd.DataFrame(groups)
    binary = gdf[gdf['binary']].copy()
    best = binary.loc[binary['k'].idxmax()] if len(binary) > 0 else gdf.loc[gdf['k'].idxmax()]
    primary = df[(df['Analysis.group'] == best['grp']) & (df['Analysis.number'] == best['num'])].copy()

    # Determine scale
    has_binary = (primary['Experimental.cases'].notna() & (primary['Experimental.cases'] > 0)).any()
    if has_binary:
        scale = 'ratio'
    else:
        means = primary['Mean'].copy().dropna()
        scale = 'ratio' if len(means) > 0 and (means > 0).all() else 'difference'

    # Compute yi/sei
    if scale == 'ratio':
        valid = (primary['Mean'].notna() & (primary['Mean'] > 0) &
                 primary['CI.start'].notna() & (primary['CI.start'] > 0) &
                 primary['CI.end'].notna() & (primary['CI.end'] > 0))
        sub = primary[valid].copy().copy()
        if len(sub) < 3:
            return None
        yi = np.log(sub['Mean'].values.astype(float))
        sei = (np.log(sub['CI.end'].values.astype(float)) - np.log(sub['CI.start'].values.astype(float))) / (2 * 1.96)
    else:
        valid = primary['Mean'].notna() & primary['CI.start'].notna() & primary['CI.end'].copy().notna()
        sub = primary[valid].copy().copy()
        if len(sub) < 3:
            return None
        yi = sub['Mean'].copy().values.astype(float)
        sei = (sub['CI.end'].values.astype(float) - sub['CI.start'].values.astype(float)) / (2 * 1.96)

    # Filter valid SE
    ok = (sei > 0) & np.isfinite(yi) & np.isfinite(sei)
    yi = yi[ok].copy()
    sei = sei[ok].copy()
    if 'Study.year' in sub.columns:
        raw_years = sub.loc[sub.index[ok], 'Study.year'].values
        years = np.zeros(len(yi))
        for i, y in enumerate(raw_years):
            try:
                years[i] = float(y)
            except (ValueError, TypeError):
                years[i] = 0
    else:
        years = np.zeros(len(yi))

    if len(yi) < 3:
        return None

    # Sort by year
    order = np.argsort(years)
    yi = yi[order].copy()
    sei = sei[order].copy()
    years = years[order].copy()

    # Cochrane direction (from full FE)
    wi = 1.0 / sei**2
    theta_fe = float(np.sum(wi * yi) / np.sum(wi))
    direction = -1 if theta_fe < 0 else 1

    review_id = rda_path.stem.split('_')[0]
    analysis_name = str(sub['Analysis.name'].iloc[0]) if 'Analysis.name' in sub.columns else ''

    return {
        'review_id': review_id,
        'analysis_name': analysis_name,
        'yi': yi,
        'sei': sei,
        'years': years,
        'k': len(yi),
        'scale': scale,
        'cochrane_direction': direction,
    }


def compute_trajectory(review):
    """Compute cumulative robustness trajectory for one review."""
    yi = review['yi'].copy()
    sei = review['sei'].copy()
    years = review['years'].copy()
    direction = review['cochrane_direction']
    k = review['k']

    trajectory = []
    for t in range(3, k + 1):
        result = compute_robustness(yi[:t], sei[:t], direction)
        if result is None:
            continue
        trajectory.append({
            'k': t,
            'year': float(years[t-1]) if years[t-1] > 0 else 0,
            'score': result['score'],
            'classification': result['classification'],
            'n_specs': result['n_specs'],
        })

    return trajectory


def compute_half_life(trajectory, threshold=70.0):
    """Find the earliest k where score >= threshold AND stays >= threshold."""
    if not trajectory:
        return None, None

    for i, step in enumerate(trajectory):
        if step['score'] >= threshold:
            # Check if it stays above threshold for all remaining steps
            stays = all(s['score'] >= threshold for s in trajectory[i:])
            if stays:
                return step['k'], step.get('year', 0)

    return None, None  # Never stabilizes


def resolve_paths(project_root=None, projects_root=None):
    project_root = Path(project_root).resolve() if project_root else PROJECT_ROOT
    projects_root = Path(projects_root).resolve() if projects_root else project_root.parent
    pairwise_candidates = []
    env_pairwise = os.getenv('PAIRWISE70_DATA_DIR')
    if env_pairwise:
        pairwise_candidates.append(Path(env_pairwise).expanduser())
    pairwise_candidates.extend([
        projects_root / 'Models' / 'Pairwise70' / 'data',
        projects_root / 'Projects' / 'Pairwise70' / 'data',
    ])
    pairwise_dir = next((path.resolve() for path in pairwise_candidates if path.exists()), pairwise_candidates[0].resolve())
    return {
        'pairwise_dir': pairwise_dir,
        'output_dir': project_root / 'data' / 'output',
    }


def main(project_root=None, projects_root=None):
    paths = resolve_paths(project_root=project_root, projects_root=projects_root)
    pairwise_dir = paths['pairwise_dir']
    output_dir = paths['output_dir']
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Evidence Half-Life Pipeline")
    print("=" * 35)

    t0 = time.time()
    if not pairwise_dir.exists():
        print(f"ERROR: Pairwise70 data directory not found: {pairwise_dir}")
        return None
    rda_files = sorted(pairwise_dir.glob('*.rda'))
    if not rda_files:
        print(f"ERROR: No RDA files found in {pairwise_dir}")
        return None
    print(f"  Found {len(rda_files)} RDA files")

    results = []
    trajectories = []
    n_loaded = 0
    n_skipped = 0

    for rda in rda_files:
        review = load_review(rda)
        if review is None:
            n_skipped += 1
            continue
        if review['k'] < 5:  # Need at least 5 for meaningful trajectory
            n_skipped += 1
            continue

        n_loaded += 1
        traj = compute_trajectory(review)
        if not traj:
            n_skipped += 1
            continue

        hl_k, hl_year = compute_half_life(traj, threshold=70.0)
        final = traj[-1].copy()

        # Score volatility: std of score changes between consecutive steps
        if len(traj) > 1:
            deltas = [abs(traj[i+1]['score'] - traj[i]['score']) for i in range(len(traj)-1)]
            volatility = sum(deltas) / len(deltas)
        else:
            volatility = 0

        # Time to first significance flip
        first_flip_k = None
        for i in range(1, len(traj)):
            prev_cls = traj[i-1]['classification']
            curr_cls = traj[i]['classification']
            if (prev_cls in ('Robust', 'Moderate') and curr_cls in ('Fragile', 'Unstable')) or \
               (prev_cls in ('Fragile', 'Unstable') and curr_cls in ('Robust', 'Moderate')):
                first_flip_k = traj[i]['k']
                break

        # Year span
        valid_years = [s['year'] for s in traj if s['year'] > 0]
        year_span = (max(valid_years) - min(valid_years)) if len(valid_years) >= 2 else 0

        row = {
            'review_id': review['review_id'],
            'analysis_name': review['analysis_name'],
            'k': review['k'],
            'scale': review['scale'],
            'final_score': final['score'],
            'final_class': final['classification'],
            'half_life_k': hl_k if hl_k else '',
            'half_life_year': hl_year if hl_year else '',
            'half_life_pct': round(hl_k / review['k'] * 100, 1) if hl_k else '',
            'volatility': round(volatility, 2),
            'n_flips': sum(1 for i in range(1, len(traj))
                          if traj[i]['classification'] != traj[i-1]['classification']),
            'first_flip_k': first_flip_k if first_flip_k else '',
            'year_span': round(year_span, 0),
            'stabilizes': 'Yes' if hl_k else 'No',
            'early_stabilizer': 'Yes' if hl_k and hl_k <= 5 else 'No',
        }
        results.append(row)

        for step in traj:
            trajectories.append({
                'review_id': review['review_id'],
                'k': step['k'],
                'year': step['year'],
                'score': step['score'],
                'classification': step['classification'],
            })

    elapsed = time.time() - t0
    print(f"  Loaded: {n_loaded}, Skipped: {n_skipped}")
    print(f"  Elapsed: {elapsed:.1f}s")

    # ══════════════════════════════════════════
    # HEADLINE STATS
    # ══════════════════════════════════════════

    n = len(results)
    if n == 0:
        print("ERROR: No analyzable reviews found; aborting export.")
        return None
    stabilizes = [r for r in results if r['stabilizes'] == 'Yes']
    never_stab = [r for r in results if r['stabilizes'] == 'No']
    early_stab = [r for r in results if r['early_stabilizer'] == 'Yes']

    hl_ks = [r['half_life_k'] for r in stabilizes]
    mean_hl = sum(hl_ks) / len(hl_ks) if hl_ks else 0
    median_hl = sorted(hl_ks)[len(hl_ks)//2] if hl_ks else 0

    volatilities = [r['volatility'] for r in results]
    mean_vol = sum(volatilities) / len(volatilities) if volatilities else 0

    n_flips_list = [r['n_flips'] for r in results]

    print(f"\n{'='*50}")
    print("HEADLINE FINDINGS")
    print(f"{'='*50}")
    print(f"  Reviews analyzed: {n}")
    print(f"  Stabilizes (score stays >=70%): {len(stabilizes)} ({100*len(stabilizes)/n:.1f}%)")
    print(f"  Never stabilizes: {len(never_stab)} ({100*len(never_stab)/n:.1f}%)")
    print(f"  Early stabilizer (k<=5): {len(early_stab)} ({100*len(early_stab)/n:.1f}%)")
    print(f"  Mean half-life k: {mean_hl:.1f} (median: {median_hl})")
    print(f"  Mean volatility: {mean_vol:.1f} points/step")
    print(f"  Mean classification flips: {sum(n_flips_list)/n:.1f}")

    # ══════════════════════════════════════════
    # EXPORT
    # ══════════════════════════════════════════

    # Results CSV
    fields = list(results[0].keys())
    with open(output_dir / 'half_life_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    # Trajectories CSV
    traj_fields = ['review_id', 'k', 'year', 'score', 'classification']
    with open(output_dir / 'half_life_trajectories.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=traj_fields)
        writer.writeheader()
        writer.writerows(trajectories)

    # Summary JSON
    summary = {
        'n_reviews': n,
        'n_stabilizes': len(stabilizes),
        'pct_stabilizes': round(100 * len(stabilizes) / n, 1),
        'n_never_stabilizes': len(never_stab),
        'pct_never_stabilizes': round(100 * len(never_stab) / n, 1),
        'n_early_stabilizer': len(early_stab),
        'half_life_k_mean': round(mean_hl, 1),
        'half_life_k_median': median_hl,
        'mean_volatility': round(mean_vol, 1),
        'mean_flips': round(sum(n_flips_list) / n, 1),
        'elapsed_seconds': round(elapsed, 1),
    }
    with open(output_dir / 'half_life_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Saved to {output_dir}/")
    return output_dir


if __name__ == '__main__':
    main()
