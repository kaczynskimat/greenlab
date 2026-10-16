import numpy as np

# G24: Use NumPy cumulative products instead of Python loops
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        # result = [1] * n
        values = np.asarray(nums, dtype=np.int64)
        # prefix = 1
        prefix = np.ones(n, dtype=np.int64)
        # suffix = 1
        suffix = np.ones(n, dtype=np.int64)
        # for i in range(n):
        #    result[i] *= prefix
        #    prefix *= nums[i]

        #    j = n - 1 - i
        #    result[j] *= suffix
        #    suffix *= nums[j]
        prefix[1:] = np.cumprod(values[:-1])
        suffix[:-1] = np.cumprod(values[:0:-1])[::-1]
        result = prefix * suffix

        # return result
        return result.tolist()