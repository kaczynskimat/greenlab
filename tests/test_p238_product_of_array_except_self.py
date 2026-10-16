from copy import deepcopy

import pytest

from problems.p238_productOfArrayExceptSelf.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3
)

from problems.p238_productOfArrayExceptSelf.guideline import (
    SolutionV1 as GuidelineV1,
    SolutionV2 as GuidelineV2,
    SolutionV3 as GuidelineV3
)

IMPLEMENTATIONS = [
        pytest.param(BaselineV1, id="baseline_v1"),
        pytest.param(BaselineV2, id="baseline_v2"),
        pytest.param(BaselineV3, id="baseline_v3"),

        pytest.param(GuidelineV1, id="guideline_v1"),
        pytest.param(GuidelineV2, id="guideline_v2"),
        pytest.param(GuidelineV3, id="guideline_v3")
    ]

class TestProductOfArrayExceptSelf:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize("nums, expected",
                             [
                                 pytest.param(
                                     [1, 2, 3, 4],
                                     [24, 12, 8, 6],
                                     id="positive-numbers"
                                 ),
                                 pytest.param(
                                     [0, 2, 0, 4],
                                     [0, 0, 0, 0],
                                     id="multiple-zeros"
                                 )
                             ]
                            )

    def test_expected_output(self, solution_class, nums, expected):
        solution = solution_class()

        actual = solution.productExceptSelf(deepcopy(nums))

        assert isinstance(actual, list)
        assert actual == expected
