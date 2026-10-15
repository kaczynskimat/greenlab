#  -------------------------------------------------
# Duplicates in Array - guideline-adherent version
# -------------------------------------------------
# G6: Avoid storing or saving data that has already been computed, saved, or is unnecessary. For example, don't recompute data that is available in a local variable, or avoid having variables only for debugging purposes.
# -------------------------------------------------

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