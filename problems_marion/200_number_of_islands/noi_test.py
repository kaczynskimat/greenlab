"""
Equivalence tests for LeetCode #200 Number of Islands, guideline G19.

Each noi_baseline_N is compared with noi_modified_N on the same grids.
Passing these tests provides evidence of equivalence for the tested
inputs, but does not prove equivalence for all possible inputs.
"""

import copy

import pytest

from noi_baseline_1 import Solution as Baseline1
from noi_baseline_2 import Solution as Baseline2
from noi_baseline_3 import Solution as Baseline3
from noi_modified_1 import Solution as Modified1
from noi_modified_2 import Solution as Modified2
from noi_modified_3 import Solution as Modified3

PAIRS = [
    (Baseline1, Modified1),
    (Baseline2, Modified2),
    (Baseline3, Modified3),
]


@pytest.fixture(params=PAIRS, ids=["pair1", "pair2", "pair3"])
def pair(request):
    baseline_cls, modified_cls = request.param
    # Fresh instances per test so no state is shared
    return baseline_cls(), modified_cls()


def check(pair, grid, expected):
    """Run both implementations on independent copies of the grid and
    compare the results and the input state."""
    baseline, modified = pair
    grid_baseline = copy.deepcopy(grid)
    grid_modified = copy.deepcopy(grid)
    result_baseline = baseline.numIslands(grid_baseline)
    result_modified = modified.numIslands(grid_modified)
    assert result_baseline == result_modified == expected, (
        f"Grid {grid}: baseline={result_baseline}, "
        f"modified={result_modified}, expected={expected}"
    )
    assert grid_baseline == grid and grid_modified == grid, (
        "An implementation mutated its input grid"
    )


def test_typical_multiple_islands(pair):
    """Typical case: several separate islands of different shapes."""
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    check(pair, grid, 3)


def test_single_cell_grids(pair):
    """Boundary: smallest valid grid (1x1), both land and water."""
    check(pair, [["1"]], 1)
    check(pair, [["0"]], 0)


def test_all_water(pair):
    """Edge case: no land at all gives zero islands."""
    check(pair, [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]], 0)


def test_all_land(pair):
    """Edge case: a grid of only land is exactly one island."""
    check(pair, [["1", "1", "1"], ["1", "1", "1"]], 1)


def test_islands_touching_edges_and_diagonals(pair):
    """Problem-specific edge case: islands on all four borders exercise the
    bounds check, and diagonal neighbours must NOT be connected."""
    edges = [
        ["1", "0", "0", "1"],
        ["0", "0", "0", "0"],
        ["1", "0", "0", "1"],
    ]
    check(pair, edges, 4)
    diagonal = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"],
    ]
    check(pair, diagonal, 5)