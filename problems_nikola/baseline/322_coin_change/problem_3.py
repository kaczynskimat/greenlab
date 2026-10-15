
# # -------------------------------------------------
# Coin Change Problem - baseline version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 3 (1079ms)  - code smell injected
import math


class Solution:

    def amountCollected(self, i, j, coins):
        if j == 0:
            return 0

        if i >= len(coins):
            return math.inf

        res = self.amountCollected(i + 1, j, coins)

        if j >= coins[i]:
            res = min(res, 1 + self.amountCollected(i, j - coins[i], coins))

        return res

    def coinChange(self, coins: list[int], amount: int) -> int:
        ans = self.amountCollected(0, amount, coins)
        if ans == math.inf:
            return -1
        return ans