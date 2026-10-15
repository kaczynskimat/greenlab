from typing import List

class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        return [[matrix[r][c] for r in range(rows)] for c in range(cols)]