from copy import deepcopy

import pytest

from problems.p442_findAllDuplicates.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p442_findAllDuplicates.guideline import (
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


class TestFindAllDuplicates:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "nums, expected",
        [
            pytest.param([4, 3, 2, 7, 8, 2, 3, 1], [2, 3], id="leetcode-example"),
            pytest.param([1, 1, 2], [1], id="one-duplicate"),
            pytest.param([1, 2, 3, 4], [], id="no-duplicates"),
            pytest.param([1, 1], [1], id="minimum-array"),
        ],
    )
    def test_expected_output(self, solution_class, nums, expected):
        solution = solution_class()
        actual = solution.findDuplicates(deepcopy(nums))
        assert isinstance(actual, list)
        assert sorted(actual) == sorted(expected)
