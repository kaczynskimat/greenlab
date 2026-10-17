class Solution(object):
    def sortedSquares(self, nums):
        nums.sort()
        n = len(nums)
        right = n - 1
        left = 0
        result = n * [0]
        for i in range(n - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                result[i] = nums[left] ** 2
                left += 1
            else:
                result[i] = nums[right] ** 2
                right -= 1
        return result
