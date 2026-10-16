class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        suffix = 1
        for i in range(n):
            result[i] *= prefix
            prefix *= nums[i]

            j = n - 1 - i
            result[j] *= suffix
            suffix *= nums[j]

        return result