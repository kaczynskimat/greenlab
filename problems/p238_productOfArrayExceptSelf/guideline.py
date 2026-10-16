import numpy as np
from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
# G24: Use NumPy cumulative products instead of Python loops
class SolutionV1:
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


# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
# G24: Use NumPy cumulative products instead of Python loops
class SolutionV2:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # O(1) space
        n = len(nums)
        values = np.asarray(nums, dtype=np.int64)
        # ans = [1 for i in range(n)]
        ans = np.ones(n, dtype=np.int64)
        # for i in range(1, n):
        #    ans[i] = ans[i - 1] * nums[i - 1]
        ans[1:] = np.cumprod(values[:-1])

        #prd = 1
        prd = np.ones(n, dtype=np.int64)
        # for i in range(n - 1, -1, -1):
        #    ans[i] = prd * ans[i]
        #    prd *= nums[i]
        prd[:-1] = np.cumprod(values[:0:-1])[::-1]
        ans *= prd

        # return ans
        return ans.tolist()

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
# G24: Use NumPy cumulative products instead of Python loops
class SolutionV3:
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