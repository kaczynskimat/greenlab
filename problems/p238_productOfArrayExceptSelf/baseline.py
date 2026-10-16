from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        left = 1
        right = 1
        output = [1] * len(nums)

        for i in range(len(nums)):
            output[i] *= left
            left *= nums[i]

        for i in range(len(nums) - 1, -1, -1):
            output[i] *= right
            right *= nums[i]

        return output

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
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

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
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