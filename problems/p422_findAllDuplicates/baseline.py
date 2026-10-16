# -----------------------------------------------
# Variation 1:
# -----------------------------------------------

class SolutionV1:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        d = {}
        for i in nums:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        k = list(d.keys())
        v = list(d.values())
        l = []
        for j in d:
            if d[j] == 2:
                l.append(j)
        return l
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        ans = []
        n = len(nums)
        for x in nums:
            x = abs(x)
            if nums[x - 1] < 0:
                ans.append(x)
            nums[x - 1] *= -1
        return ans
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
from collections import Counter


class SolutionV3:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        if len(nums) == 1:
            return []

        hash = Counter(nums)

        result = []

        for key, value in hash.items():
            if value > 1:
                result.append(key)

        return result