import pytest

from problems.p509_fibonacciNumber.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p509_fibonacciNumber.guideline import (
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


class TestFibonacciNumber:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "n, expected",
        [
            pytest.param(0, 0, id="zero"),
            pytest.param(1, 1, id="one"),
            pytest.param(2, 1, id="two"),
            pytest.param(3, 2, id="three"),
            pytest.param(7, 13, id="medium-input"),
            pytest.param(10, 55, id="larger-input"),
        ],
    )
    def test_expected_output(self, solution_class, n, expected):
        solution = solution_class()
        actual = solution.fib(n)
        assert isinstance(actual, int)
        assert actual == expected
