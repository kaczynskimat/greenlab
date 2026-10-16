import pytest

from problems.p383_ransomNote.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p383_ransomNote.guideline import (
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


class TestRansomNote:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "ransom_note, magazine, expected",
        [
            pytest.param("a", "b", False, id="cannot-construct"),
            pytest.param("aa", "ab", False, id="insufficient-characters"),
            pytest.param("aa", "aab", True, id="exact-construction"),
            pytest.param("bg", "efjbdfg", True, id="longer-magazine"),
        ],
    )
    def test_expected_output(self, solution_class, ransom_note, magazine, expected):
        solution = solution_class()
        actual = solution.canConstruct(ransom_note, magazine)

        assert isinstance(actual, bool)
        assert actual == expected
