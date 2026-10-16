from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # O(1) space
        n = len(nums)
        ans = [1 for i in range(n)]
        for i in range(1, n):
            ans[i] = ans[i - 1] * nums[i - 1]

        prd = 1
        for i in range(n - 1, -1, -1):
            ans[i] = prd * ans[i]
            prd *= nums[i]

        return ans