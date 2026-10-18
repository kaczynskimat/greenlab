from copy import deepcopy
import pytest
from problems.p200_numberOfIslands.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p200_numberOfIslands.guideline import (
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
class TestNumberOfIslands:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "grid, expected",
        [
            pytest.param(
                [
                    ["1", "1", "0", "0", "0"],
                    ["1", "1", "0", "0", "0"],
                    ["0", "0", "1", "0", "0"],
                    ["0", "0", "0", "1", "1"],
                ],
                3,
                id="typical-multiple-islands",
            ),
            pytest.param([["1"]], 1, id="single-cell-land"),
            pytest.param([["0"]], 0, id="single-cell-water"),
            pytest.param([["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]], 0, id="all-water"),
            pytest.param([["1", "1", "1"], ["1", "1", "1"]], 1, id="all-land"),
            pytest.param(
                [
                    ["1", "0", "0", "1"],
                    ["0", "0", "0", "0"],
                    ["1", "0", "0", "1"],
                ],
                4,
                id="islands-touching-edges",
            ),
            pytest.param(
                [
                    ["1", "0", "1"],
                    ["0", "1", "0"],
                    ["1", "0", "1"],
                ],
                5,
                id="diagonal-islands",
            ),
        ],
    )
    def test_expected_output(self, solution_class, grid, expected):
        solution = solution_class()
        actual = solution.numIslands(deepcopy(grid))
        assert isinstance(actual, int)
        assert actual == expected