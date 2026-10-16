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
        l = []
        for j in d:
            if d[j] == 2:
                l.append(j)
        return l
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
from rpds import List

class SolutionV2:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        ans = []
        for x in nums:
            x = abs(x)
            if nums[x - 1] < 0:
                ans.append(x)
            nums[x - 1] *= -1
        return ans
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        if len(nums) == 1:
            return []

        seen = set()
        result = []

        for key in nums:
            if key in seen:
                result.append(key)
            else:
                seen.add(key)

        return result