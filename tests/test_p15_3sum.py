from copy import deepcopy

import pytest

from problems.p15_3sum.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p15_3sum.guideline import (
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


class TestThreeSum:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "nums, expected",
        [
            pytest.param(
                [-1, 0, 1, 2, -1, -4],
                [[-1, -1, 2], [-1, 0, 1]],
                id="standard-example",
            ),
            pytest.param([0, 1, 1], [], id="no-triplets"),
            pytest.param([0, 0, 0], [[0, 0, 0]], id="all-zeros"),
            pytest.param(
                [-2, 0, 1, 1, 2],
                [[-2, 0, 2], [-2, 1, 1]],
                id="multiple-triplets",
            ),
        ],
    )
    def test_expected_output(self, solution_class, nums, expected):
        solution = solution_class()
        actual = solution.threeSum(deepcopy(nums))

        assert isinstance(actual, list)
        assert sorted([sorted(t) for t in actual]) == sorted([sorted(t) for t in expected])
