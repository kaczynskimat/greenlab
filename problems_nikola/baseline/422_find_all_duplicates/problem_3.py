#  -------------------------------------------------
# Duplicates in Array - baseline version
# -------------------------------------------------
# G6: Avoid storing or saving data that has already been computed, saved, or is unnecessary. For example, don't recompute data that is available in a local variable, or avoid having variables only for debugging purposes.
# -------------------------------------------------

# PROBLEM 3 (25s) - original LeetCode solution
class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        if len(nums) == 1:
            return []

        hash = Counter(nums)

        result = []

        for key, value in hash.items():
            if value > 1:
                result.append(key)

        return result