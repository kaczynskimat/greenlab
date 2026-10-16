import pytest

from problems.p3_longestSubstringWithoutRepeatingCharacters.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p3_longestSubstringWithoutRepeatingCharacters.guideline import (
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


class TestLongestSubstringWithoutRepeatingCharacters:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "s, expected",
        [
            pytest.param("", 0, id="empty-string"),
            pytest.param("a", 1, id="single-character"),
            pytest.param("abcabcbb", 3, id="repeated-substring"),
            pytest.param("bbbbb", 1, id="all-characters-repeat"),
            pytest.param("pwwkew", 3, id="repeated-character-in-middle"),
            pytest.param("dvdf", 3, id="overlapping-repeat"),
            pytest.param("abba", 2, id="repeat-before-window-start"),
        ],
    )
    def test_expected_output(self, solution_class, s, expected):
        solution = solution_class()

        actual = solution.lengthOfLongestSubstring(s)

        assert isinstance(actual, int)
        assert actual == expected
