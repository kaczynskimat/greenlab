import pytest

from problems.p125_validPalindrome.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p125_validPalindrome.guideline import (
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


class TestValidPalindrome:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "s, expected",
        [
            pytest.param("A man, a plan, a canal: Panama", True, id="typical-palindrome"),
            pytest.param("race a car", False, id="typical-non-palindrome"),
            pytest.param(".,  :;!?", True, id="only-non-alphanumeric"),
            pytest.param("a", True, id="single-character"),
            pytest.param("0P", False, id="digits-and-letters"),
        ],
    )
    def test_expected_output(self, solution_class, s, expected):
        solution = solution_class()
        actual = solution.isPalindrome(s)
        assert isinstance(actual, bool)
        assert actual == expected