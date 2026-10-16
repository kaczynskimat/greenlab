from copy import deepcopy

import pytest

from problems.p49_groupAnagrams.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3
)

from problems.p49_groupAnagrams.guideline import (
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

class TestGroupAnagrams:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize("nums, expected",
                             [
                                 pytest.param(
                                     [""],
                                     [[""]],
                                     id="empty-string"
                                 ),
                                 pytest.param(
                                     ["a"],
                                     [["a"]],
                                     id="single-string"
                                 ),
                                 pytest.param(
                                     ["ab", "ab", "ba"],
                                     [["ab", "ab", "ba"]],
                                     id="duplicates"
                                 ),
                                 pytest.param(
                                     ["eat", "tea", "tan", "ate", "nat", "bat"],
                                     [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]],
                                     id="multiple-groups"
                                 ),
                                 pytest.param(
                                     ["a", "b", "c"],
                                     [["a"], ["b"], ["c"]],
                                     id="no-anagrams"
                                 )
                             ]
                            )

    def test_expected_output(self, solution_class, nums, expected):
        solution = solution_class()

        actual = solution.groupAnagrams(deepcopy(nums))

        assert isinstance(actual, list)
        assert all(isinstance(group, list) for group in actual)
        assert sorted(sorted(group) for group in actual) == sorted(
            sorted(group) for group in expected
        )
