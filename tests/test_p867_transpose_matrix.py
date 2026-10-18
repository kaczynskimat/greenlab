from copy import deepcopy
import pytest
from problems.p867_transposeMatrix.baseline import (
    SolutionV1 as BaselineV1,
    SolutionV2 as BaselineV2,
    SolutionV3 as BaselineV3,
)
from problems.p867_transposeMatrix.guideline import (
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
class TestTransposeMatrix:
    @pytest.mark.parametrize("solution_class", IMPLEMENTATIONS)
    @pytest.mark.parametrize(
        "matrix, expected",
        [
            pytest.param([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]], id="typical-rectangular"),
            pytest.param([[1, 2], [3, 4]], [[1, 3], [2, 4]], id="square-matrix"),
            pytest.param([[7]], [[7]], id="single-element"),
            pytest.param([[1, 2, 3, 4]], [[1], [2], [3], [4]], id="single-row"),
            pytest.param([[1], [2], [3]], [[1, 2, 3]], id="single-column"),
            pytest.param(
                [[-10**9, 0, 10**9], [10**9, -1, -10**9]],
                [[-10**9, 10**9], [0, -1], [10**9, -10**9]],
                id="extreme-values",
            ),
        ],
    )
    def test_expected_output(self, solution_class, matrix, expected):
        solution = solution_class()
        actual = solution.transpose(deepcopy(matrix))
        assert isinstance(actual, list)
        assert all(isinstance(row, list) for row in actual)
        assert all(isinstance(val, int) for row in actual for val in row)
        assert actual == expected