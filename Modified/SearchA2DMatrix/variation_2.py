class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        if not matrix or not matrix[0]:
            return False
        m, n = len(matrix), len(matrix[0])
        i, j = 0, n - 1
        while i < m and j >= 0:
            current = matrix[i][j]
            if current == target:
                return True
            elif current < target:
                i += 1
            else:
                j -= 1
        return False
