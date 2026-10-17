from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------


class SolutionV1:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        row = 0
        column = len(matrix[0]) - 1
        while row < len(matrix) and column >= 0:
            element = matrix[row][column]
            if target == element:
                return True
            elif target < element:
                column -= 1
            else:
                row += 1
        return False


# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
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


# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        for i in range(len(matrix)):
            l = 0
            r = len(matrix[0])
            while l < r:
                mid = (l + r) // 2
                if matrix[i][mid] == target:
                    return True
                elif matrix[i][mid] > target:
                    r = mid
                else:
                    l = mid + 1
        return False
