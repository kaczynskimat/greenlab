"""
Equivalence tests for LeetCode #867 Transpose Matrix, guideline G24.

Each tm_baseline_N is compared with tm_modified_N on the same matrices.
The modified versions use numpy, so the tests also check that plain
Python types are returned (not numpy types).
Passing these tests provides evidence of equivalence for the tested
inputs, but does not prove equivalence for all possible inputs.
"""

import copy

import pytest

from tm_baseline_1 import Solution as Baseline1
from tm_baseline_2 import Solution as Baseline2
from tm_baseline_3 import Solution as Baseline3
from tm_modified_1 import Solution as Modified1
from tm_modified_2 import Solution as Modified2
from tm_modified_3 import Solution as Modified3

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


def check(pair, matrix, expected):
    """Run both implementations on independent copies of the matrix and
    compare values, types and input state."""
    baseline, modified = pair
    matrix_baseline = copy.deepcopy(matrix)
    matrix_modified = copy.deepcopy(matrix)
    result_baseline = baseline.transpose(matrix_baseline)
    result_modified = modified.transpose(matrix_modified)
    assert result_baseline == expected, (
        f"Baseline gave {result_baseline}, expected {expected}"
    )
    assert result_modified == expected, (
        f"Input {matrix}: baseline={result_baseline}, modified={result_modified}"
    )
    for name, result in (("baseline", result_baseline), ("modified", result_modified)):
        assert type(result) is list, f"{name} returned {type(result)}, expected list"
        assert all(type(row) is list for row in result), f"{name} rows are not lists"
        assert all(type(v) is int for row in result for v in row), (
            f"{name} returned non-int values (numpy types?)"
        )
    assert matrix_baseline == matrix and matrix_modified == matrix, (
        "An implementation mutated its input matrix"
    )


def test_typical_rectangular(pair):
    """Typical case: non-square matrix, so the dimensions swap."""
    check(pair, [[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]])


def test_square_matrix(pair):
    """Typical case: square matrix."""
    check(pair, [[1, 2], [3, 4]], [[1, 3], [2, 4]])


def test_single_element(pair):
    """Boundary: smallest valid matrix (1x1) is returned unchanged."""
    check(pair, [[7]], [[7]])


def test_single_row_and_single_column(pair):
    """Boundary: extreme aspect ratios, 1xN becomes Nx1 and the reverse."""
    check(pair, [[1, 2, 3, 4]], [[1], [2], [3], [4]])
    check(pair, [[1], [2], [3]], [[1, 2, 3]])


def test_negative_and_extreme_values(pair):
    """Edge case: values at the constraint limits (+-10^9) and zero must
    survive numpy conversion as plain Python ints."""
    matrix = [[-10**9, 0, 10**9], [10**9, -1, -10**9]]
    expected = [[-10**9, 10**9], [0, -1], [10**9, -10**9]]
    check(pair, matrix, expected)