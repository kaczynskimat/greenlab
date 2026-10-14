# # -------------------------------------------------
# Min Cost Climbing Stairs - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------


# PROBLEM 1 (5ms) - original LeetCode solution
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:

        cache = {}

        def helper(i):
            if i >= len(cost):
                return 0
            if i in cache:
                return cache[i]

            cache[i] = cost[i] + min(helper(i + 1), helper(i + 2))
            return cache[i]

        return min(helper(0), helper(1))


# PROBLEM 2 (6ms) - original LeetCode solution
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        def dp(i):
            if i <= 1:
                return 0

            if i in memo:
                return memo[i]

            memo[i] = min(dp(i - 1) + cost[i - 1], dp(i - 2) + cost[i - 2])
            return memo[i]

        memo = {}
        return dp(len(cost))


# PROBLEM 3 (3ms) - original LeetCode solution
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        n = len(cost)
        cache = [-1] * n

        def solve(i):
            if i >= n:
                return 0
            if cache[i] == -1:
                cache[i] = cost[i] + min(solve(i + 1), solve(i + 2))
            return cache[i]

        return min(solve(0), solve(1))
