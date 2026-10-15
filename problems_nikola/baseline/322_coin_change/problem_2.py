# # -------------------------------------------------
# Coin Change Problem - baseline version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 2 (735ms) - code smell injected
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:

        def recurse(n):

            if n == 0:
                return 0
            if n < 0:
                return float("inf")

            best = float("inf")

            for c in coins:
                best = min(best, recurse(n - c) + 1)

            return best

        result = recurse(amount)
        return -1 if result == float("inf") else result