from typing import List

class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        res = [[] for _ in range(len(matrix[0]))]

        for row in matrix:
            for c, val in enumerate(row):
                res[c].append(val)

        return res