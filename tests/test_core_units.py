"""Direct unit coverage for the core half-life / trajectory / RDA-parse logic.

The existing suite exercises compute_robustness and resolve_paths, and the
main() integration test monkeypatches load_review to a synthetic dict, so
compute_half_life, compute_trajectory and load_review were never run against
their real logic. These tests close that gap (finding F3).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import pipeline
from pipeline import compute_half_life, compute_trajectory, load_review


def _traj(scores, ks=None):
    """Build a minimal trajectory list from a list of scores."""
    if ks is None:
        ks = list(range(3, 3 + len(scores)))
    return [
        {'k': k, 'year': 2000 + i, 'score': s, 'classification': 'x', 'n_specs': 8}
        for i, (k, s) in enumerate(zip(ks, scores))
    ]


class TestComputeHalfLife:
    def test_monotone_stabilize_returns_first_sustained_k(self):
        # 72 at k=4 is the first score >=70 that then stays >=70.
        traj = _traj([60, 72, 80, 90])  # k = 3,4,5,6
        k, year = compute_half_life(traj, threshold=70.0)
        assert k == 4

    def test_dip_then_recover_returns_sustained_not_transient(self):
        # 75 at k=3 is transient (drops to 60 at k=4); the sustained run
        # starts at k=5. Half-life must be 5, NOT 3.
        traj = _traj([75, 60, 80, 85])  # k = 3,4,5,6
        k, year = compute_half_life(traj, threshold=70.0)
        assert k == 5

    def test_never_stabilizes_returns_none(self):
        traj = _traj([60, 50, 40])
        assert compute_half_life(traj, threshold=70.0) == (None, None)

    def test_empty_trajectory_returns_none(self):
        assert compute_half_life([], threshold=70.0) == (None, None)

    def test_last_step_only_above_threshold(self):
        # Only the final step clears the bar -> sustained trivially from there.
        traj = _traj([50, 60, 65, 71])  # k=3,4,5,6
        k, _ = compute_half_life(traj, threshold=70.0)
        assert k == 6


class TestComputeTrajectory:
    def test_k5_review_yields_steps_t3_to_t5(self):
        review = {
            'yi': np.array([-0.5, -0.5, -0.5, -0.5, -0.5]),
            'sei': np.array([0.1, 0.1, 0.1, 0.1, 0.1]),
            'years': np.array([2001, 2002, 2003, 2004, 2005]),
            'cochrane_direction': -1,
            'k': 5,
        }
        traj = compute_trajectory(review)
        assert [s['k'] for s in traj] == [3, 4, 5]
        for step in traj:
            assert set(step) >= {'k', 'year', 'score', 'classification', 'n_specs'}
            assert 0 <= step['score'] <= 100
        # Homogeneous strongly significant -> robust throughout.
        assert traj[-1]['score'] >= 90


def _make_df(rows, binary=True):
    """Build a Pairwise70-shaped DataFrame for load_review."""
    n = len(rows['Mean'])
    data = {
        'Analysis.group': ['G1'] * n,
        'Analysis.number': [1] * n,
        'Analysis.name': ['Primary outcome'] * n,
        'Study.year': rows.get('Study.year', list(range(2001, 2001 + n))),
        'Mean': rows['Mean'],
        'CI.start': rows['CI.start'],
        'CI.end': rows['CI.end'],
        'Experimental.cases': ([5] * n if binary else [np.nan] * n),
    }
    return pd.DataFrame(data)


class TestLoadReview:
    def test_ratio_scale_binary(self, monkeypatch):
        df = _make_df({
            'Mean': [0.5, 0.6, 0.55, 0.5],
            'CI.start': [0.3, 0.4, 0.35, 0.3],
            'CI.end': [0.8, 0.9, 0.85, 0.8],
        }, binary=True)
        monkeypatch.setattr(pipeline.pyreadr, 'read_r', lambda _p: {'d': df})
        review = load_review(Path('CD123456_x.rda'))
        assert review is not None
        assert review['scale'] == 'ratio'
        assert review['k'] == 4
        assert review['review_id'] == 'CD123456'
        # yi should be log of the ratio Means.
        assert np.allclose(np.sort(review['yi']), np.sort(np.log([0.5, 0.6, 0.55, 0.5])))

    def test_difference_scale_continuous(self, monkeypatch):
        df = _make_df({
            'Mean': [-0.5, -0.3, -0.4],
            'CI.start': [-0.9, -0.7, -0.8],
            'CI.end': [-0.1, 0.1, 0.0],
        }, binary=False)
        monkeypatch.setattr(pipeline.pyreadr, 'read_r', lambda _p: {'d': df})
        review = load_review(Path('CD999999_y.rda'))
        assert review is not None
        assert review['scale'] == 'difference'
        assert review['k'] == 3
        # difference scale keeps Mean as-is (no log transform).
        assert np.allclose(np.sort(review['yi']), np.sort([-0.5, -0.3, -0.4]))

    def test_fewer_than_three_valid_rows_returns_none(self, monkeypatch):
        df = _make_df({
            'Mean': [0.5, 0.6],
            'CI.start': [0.3, 0.4],
            'CI.end': [0.8, 0.9],
        }, binary=True)
        monkeypatch.setattr(pipeline.pyreadr, 'read_r', lambda _p: {'d': df})
        assert load_review(Path('CD000002_z.rda')) is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
