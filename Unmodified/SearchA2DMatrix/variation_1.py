class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            row.sort()

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
