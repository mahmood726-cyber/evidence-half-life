"""Tests for Evidence Half-Life pipeline."""
import sys, json, csv, pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import compute_robustness, main, resolve_paths
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / 'data' / 'output'


class TestRobustness:
    def test_homogeneous_significant(self):
        """Homogeneous significant data should be robust."""
        yi = np.array([-0.5, -0.5, -0.5, -0.5, -0.5])
        sei = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
        r = compute_robustness(yi, sei, cochrane_direction=-1)
        assert r is not None
        assert r['score'] >= 90

    def test_heterogeneous_unstable(self):
        """Very heterogeneous data should be unstable."""
        yi = np.array([-1.5, -0.5, 0.5, 1.5, 0.0])
        sei = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        r = compute_robustness(yi, sei, cochrane_direction=-1)
        assert r is not None
        assert r['score'] < 70

    def test_k2_returns_none(self):
        yi = np.array([-0.5, -0.3])
        sei = np.array([0.2, 0.2])
        assert compute_robustness(yi, sei, -1) is None

    def test_score_range(self):
        yi = np.array([-0.3, -0.2, -0.1, 0.0, 0.1])
        sei = np.array([0.15, 0.15, 0.15, 0.15, 0.15])
        r = compute_robustness(yi, sei, -1)
        assert r is not None
        assert 0 <= r['score'] <= 100

    def test_n_specs_correct(self):
        """Should have 4 estimators x 2 CI methods = 8 specs."""
        yi = np.array([-0.5, -0.3, -0.1])
        sei = np.array([0.2, 0.2, 0.2])
        r = compute_robustness(yi, sei, -1)
        assert r is not None
        assert r['n_specs'] == 8


class TestResults:
    @pytest.fixture
    def summary(self):
        path = OUTPUT_DIR / 'half_life_summary.json'
        if not path.exists():
            pytest.skip('Run pipeline.py first')
        with open(path) as f:
            return json.load(f)

    @pytest.fixture
    def results(self):
        path = OUTPUT_DIR / 'half_life_results.csv'
        if not path.exists():
            pytest.skip('Run pipeline.py first')
        rows = []
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows

    def test_review_count_matches_results(self, summary, results):
        assert summary['n_reviews'] == len(results)
        assert summary['n_reviews'] >= 300

    def test_stabilizes_plus_never_equals_total(self, summary):
        assert summary['n_stabilizes'] + summary['n_never_stabilizes'] == summary['n_reviews']

    def test_majority_never_stabilize(self, summary):
        assert summary['pct_never_stabilizes'] > 50

    def test_median_half_life(self, summary):
        assert 3 <= summary['half_life_k_median'] <= 30

    def test_all_have_k(self, results):
        for r in results:
            assert int(r['k']) >= 5

    def test_stabilizers_have_half_life(self, results):
        for r in results:
            if r['stabilizes'] == 'Yes':
                assert r['half_life_k'] != '', f"{r['review_id']} stabilizes but no half_life_k"

    def test_volatility_non_negative(self, results):
        for r in results:
            assert float(r['volatility']) >= 0


class TestTrajectories:
    @pytest.fixture
    def trajectories(self):
        path = OUTPUT_DIR / 'half_life_trajectories.csv'
        if not path.exists():
            pytest.skip('Run pipeline.py first')
        rows = []
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows

    def test_trajectories_exist(self, trajectories):
        assert len(trajectories) > 1000  # 307 reviews x ~10 steps avg

    def test_scores_in_range(self, trajectories):
        for t in trajectories[:500]:
            s = float(t['score'])
            assert 0 <= s <= 100, f"{t['review_id']} k={t['k']}: score={s}"

    def test_k_minimum(self, trajectories):
        for t in trajectories:
            assert int(t['k']) >= 3


def test_main_uses_repo_relative_sibling_projects(tmp_path, monkeypatch):
    projects_root = tmp_path / 'projects'
    project_root = projects_root / 'EvidenceHalfLife'
    project_root.mkdir(parents=True)

    paths = resolve_paths(project_root=project_root, projects_root=projects_root)
    rda_path = paths['pairwise_dir'] / 'CD000001_analysis.rda'
    rda_path.parent.mkdir(parents=True, exist_ok=True)
    rda_path.write_text('', encoding='utf-8')

    synthetic_review = {
        'review_id': 'CD000001',
        'analysis_name': 'Synthetic review',
        'yi': np.array([-0.5, -0.5, -0.5, -0.5, -0.5]),
        'sei': np.array([0.1, 0.1, 0.1, 0.1, 0.1]),
        'years': np.array([2001, 2002, 2003, 2004, 2005]),
        'k': 5,
        'scale': 'ratio',
        'cochrane_direction': -1,
    }
    monkeypatch.setattr('pipeline.load_review', lambda _: synthetic_review)

    output_dir = main(project_root=project_root, projects_root=projects_root)

    summary = json.loads((output_dir / 'half_life_summary.json').read_text(encoding='utf-8'))
    assert output_dir == project_root / 'data' / 'output'
    assert summary['n_reviews'] == 1
    assert summary['n_stabilizes'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
