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