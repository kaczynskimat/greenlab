class Solution(object):
    def sortedSquares(self, nums):
        nums.sort()
        n = len(nums)
        result = [0] * n
        left = 0
        right = n - 1
        for p in range(n - 1, -1, -1):
            left_square = nums[left] * nums[left]
            right_square = nums[right] * nums[right]
            if left_square > right_square:
                result[p] = left_square
                left += 1
            else:
                result[p] = right_square
                right -= 1
        return result
