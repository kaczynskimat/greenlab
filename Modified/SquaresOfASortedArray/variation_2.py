class Solution(object):
    def sortedSquares(self, nums):
        result = list(map(lambda x: x * x, nums))
        result.sort()
        return result
