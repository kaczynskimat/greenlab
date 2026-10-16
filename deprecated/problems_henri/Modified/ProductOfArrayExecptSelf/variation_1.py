import numpy as np

# G24: Use NumPy instead cumulative products instead of Python loops
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        # left = 1
        # right = 1
        # output = [1] * len(nums)
        values = np.asarray(nums, dtype=np.int64)
        left = np.ones(len(values), dtype=np.int64)
        right = np.ones(len(values), dtype=np.int64)

        # for i in range(len(nums)):
        #    output[i] *= left
        #    left *= nums[i]

        # for i in range(len(nums) - 1, -1, -1):
        #    output[i] *= right
        #    right *= nums[i]

        left[1:] = np.cumprod(values[:-1])
        right[:-1] = np.cumprod(values[:0:-1])[::-1]
        output = left * right
        #return output
        return output.tolist()