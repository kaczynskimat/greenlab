from copy import deepcopy

import pytest

from problems.p322_coinChange.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p322_coinChange.guideline import (
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


class TestCoinChange:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "coins, amount, expected",
        [
            pytest.param([1, 2, 5], 11, 3, id="leetcode-example"),
            pytest.param([2], 3, -1, id="impossible-change"),
            pytest.param([1], 0, 0, id="zero-amount"),
            pytest.param([1, 3, 4], 6, 2, id="non-greedy-optimum"),
        ],
    )
    def test_expected_output(self, solution_class, coins, amount, expected):
        solution = solution_class()
        actual = solution.coinChange(deepcopy(coins), amount)
        assert isinstance(actual, int)
        assert actual == expected
