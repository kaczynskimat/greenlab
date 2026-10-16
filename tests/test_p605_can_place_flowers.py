from copy import deepcopy

import pytest

from problems.p605_canPlaceFlowers.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p605_canPlaceFlowers.guideline import (
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


class TestCanPlaceFlowers:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "flowerbed, n, expected",
        [
            pytest.param([1, 0, 0, 0, 1], 1, True, id="example-1"),
            pytest.param([1, 0, 0, 0, 1], 2, False, id="example-2"),
            pytest.param([0, 0, 1, 0, 1], 1, True, id="start-zeros"),
            pytest.param([1, 0, 0, 0, 0, 1], 2, False, id="two-consecutive-zeros"),
            pytest.param([0], 1, True, id="single-zero-plant"),
            pytest.param([0], 0, True, id="zero-flowers-needed"),
        ],
    )
    def test_expected_output(self, solution_class, flowerbed, n, expected):
        solution = solution_class()
        actual = solution.canPlaceFlowers(deepcopy(flowerbed), n)

        assert isinstance(actual, bool)
        assert actual == expected
