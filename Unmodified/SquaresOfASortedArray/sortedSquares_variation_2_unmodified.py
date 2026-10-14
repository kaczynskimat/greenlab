class Solution(object):
    def sortedSquares(self, nums):
        nums.sort()
        result = list(map(lambda x: x * x, nums))
        result.sort()
        return result
