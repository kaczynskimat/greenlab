"""Tests for Squares of a Sorted Array."""

from copy import deepcopy

import pytest

from problems.p977_squaresOfASortedArray.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p977_squaresOfASortedArray.guideline import (
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


class TestSquaresOfASortedArray:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "nums, expected",
        [
            pytest.param([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100], id="mixed-signs"),
            pytest.param([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121], id="multiple-negatives"),
            pytest.param([0, 1, 2], [0, 1, 4], id="non-negative"),
            pytest.param([-2], [4], id="single-negative"),
            pytest.param([], [], id="empty-array"),
        ],
    )
    def test_expected_output(self, solution_class, nums, expected):
        solution = solution_class()
        actual = solution.sortedSquares(deepcopy(nums))

        assert isinstance(actual, list)
        assert actual == expected
