from typing import List
# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        res = [[0] * len(matrix) for _ in range(len(matrix[0]))]
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                res[c][r] = matrix[r][c]
        return res
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        return [[matrix[r][c] for r in range(rows)] for c in range(cols)]
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        res = [[] for _ in range(len(matrix[0]))]
        for row in matrix:
            for c, val in enumerate(row):
                res[c].append(val)
        return res