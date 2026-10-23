"""Tests for First Unique Character in a String."""

import pytest

from problems.p387_firstUniqueCharacterInAString.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p387_firstUniqueCharacterInAString.guideline import (
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


class TestFirstUniqueCharacterInAString:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "s, expected",
        [
            pytest.param("leetcode", 0, id="first-character-is-unique"),
            pytest.param("loveleetcode", 2, id="unique-character-after-repeats"),
            pytest.param("aabb", -1, id="no-unique-character"),
            pytest.param("z", 0, id="single-character"),
            pytest.param("", -1, id="empty-string"),
        ],
    )
    def test_expected_output(self, solution_class, s, expected):
        solution = solution_class()
        actual = solution.firstUniqChar(s)

        assert isinstance(actual, int)
        assert actual == expected
