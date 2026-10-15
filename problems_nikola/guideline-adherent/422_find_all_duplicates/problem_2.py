#  -------------------------------------------------
# Duplicates in Array - guideline-adherent version
# -------------------------------------------------
# G6: Avoid storing or saving data that has already been computed, saved, or is unnecessary. For example, don't recompute data that is available in a local variable, or avoid having variables only for debugging purposes.
# -------------------------------------------------

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