#  -------------------------------------------------
# Duplicates in Array - guideline-adherent version
# -------------------------------------------------
# G6: Avoid storing or saving data that has already been computed, saved, or is unnecessary. For example, don't recompute data that is available in a local variable, or avoid having variables only for debugging purposes.
# -------------------------------------------------


# PROBLEM 1 (43s) - guideline modified solution
class Solution:
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


# PROBLEM 2 (40s) - guideline modified solution
class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        ans = []
        for x in nums:
            x = abs(x)
            if nums[x - 1] < 0:
                ans.append(x)
            nums[x - 1] *= -1
        return ans


# PROBLEM 3 (25s) - guideline modified solution
class Solution:
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
