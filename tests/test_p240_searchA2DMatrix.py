"""Tests for Search a 2D Matrix II."""

from copy import deepcopy

import pytest

from problems.p240_searchA2DMatrix.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p240_searchA2DMatrix.guideline import (
    SolutionV1 as GuidelineV1,
    SolutionV2 as GuidelineV2,
    SolutionV3 as GuidelineV3,
)

IMPLEMENTATIONS = [
    pytest.param(BaselineV1, id="baseline_v1"),
    pytest.param(BaselineV2, id="baseline_v2"),
    pytest.param(BaselineV3, id="baseline_v3"),
    pytest.param(GuidelineV1, id="guideline_v1"),
    pytest.param(GuidelineV2, id="guideline_v2"),
    pytest.param(GuidelineV3, id="guideline_v3"),
]


class TestSearchA2DMatrix:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "matrix, target, expected",
        [
            pytest.param(
                [
                    [1, 4, 7, 11, 15],
                    [2, 5, 8, 12, 19],
                    [3, 6, 9, 16, 22],
                    [10, 13, 14, 17, 24],
                    [18, 21, 23, 26, 30],
                ],
                5,
                True,
                id="target-present",
            ),
            pytest.param(
                [
                    [1, 4, 7, 11, 15],
                    [2, 5, 8, 12, 19],
                    [3, 6, 9, 16, 22],
                    [10, 13, 14, 17, 24],
                    [18, 21, 23, 26, 30],
                ],
                20,
                False,
                id="target-absent",
            ),
            pytest.param([[1, 3, 5], [2, 4, 6]], 1, True, id="first-element"),
            pytest.param([[1, 3, 5], [2, 4, 6]], 6, True, id="last-element"),
            pytest.param([[1]], 0, False, id="single-element-absent"),
        ],
    )
    def test_expected_output(self, solution_class, matrix, target, expected):
        solution = solution_class()
        actual = solution.searchMatrix(deepcopy(matrix), target)

        assert isinstance(actual, bool)
        assert actual is expected
