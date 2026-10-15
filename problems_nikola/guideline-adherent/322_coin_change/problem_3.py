# # -------------------------------------------------
# Coin Change Problem - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 3 (1079ms)  - original LeetCode solution
import math


class Solution:

    def amountCollected(self, i, j, coins, dp):
        if j == 0:
            return 0

        if i >= len(coins):
            return math.inf

        if dp[i][j] != -2:
            return dp[i][j]

        dp[i][j] = self.amountCollected(i + 1, j, coins, dp)
        res = dp[i][j]

        if j >= coins[i]:
            dp[i][j] = min(res, 1 + self.amountCollected(i, j - coins[i], coins, dp))
            res = dp[i][j]

        return res

    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [[-2 for _ in range(amount + 1)] for _ in range(len(coins))]
        ans = self.amountCollected(0, amount, coins, dp)
        if ans == math.inf:
            return -1
        return ans