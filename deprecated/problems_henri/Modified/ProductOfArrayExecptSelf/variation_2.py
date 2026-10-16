from typing import List
import numpy as np

# G24: Use NumPy cumulative products instead of Python loops
class Solution:
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