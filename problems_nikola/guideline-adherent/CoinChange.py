# # -------------------------------------------------
# Coin Change Problem - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------


# PROBLEM 1 (47ms) - guideline modified solution
from math import gcd


class Solution:
    @staticmethod
    def coinChange(coins, target):
        if target == 0:
            return 0

        n = len(coins)
        if n == 1:
            return target // coins[0] if target % coins[0] == 0 else -1

        coins.sort()

        minCoin = coins[0]
        if target == minCoin:
            return 1
        idx = 1
        gcdVal = minCoin
        while idx < n and target >= coins[idx]:
            if target == coins[idx]:
                return 1
            gcdVal = gcd(coins[idx], gcdVal)
            coins[idx] -= minCoin
            idx += 1
        if target % gcdVal != 0:
            return -1

        minVal = (target - 1) // (coins[idx - 1] + minCoin) + 1
        maxVal = target // minCoin

        memo = {}

        for i in range(minVal, maxVal + 1):
            if Solution.findCombination(
                coins, 1, idx - 1, target - i * minCoin, i, memo
            ):
                return i
        return -1

    @staticmethod
    def findCombination(coins, left, right, target, maxCoins, memo):
        key = (left, right, target, maxCoins)

        if key in memo:
            return memo[key]

        if target == 0:
            return True
        if target < coins[left] or target // coins[right] > maxCoins:
            return False
        if target % coins[right] == 0:
            return True
        if left == right:
            return False
        for k in range(target // coins[right] + 1):
            if Solution.findCombination(
                coins, left, right - 1, target - k * coins[right], maxCoins - k, memo
            ):
                memo[key] = True
                return True

        memo[key] = False
        return False


# PROBLEM 2 (735ms) - original LeetCode solution
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:

        @cache
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
