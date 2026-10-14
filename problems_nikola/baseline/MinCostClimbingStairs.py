# # -------------------------------------------------
# Min Cost Climbing Stairs - baseline version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------


# PROBLEM 1 (5ms) - code smell injected
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:

        def helper(i):
            if i >= len(cost):
                return 0

            return cost[i] + min(helper(i + 1), helper(i + 2))

        return min(helper(0), helper(1))


# PROBLEM 2 (6ms) - code smell injected
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        def dp(i):
            if i <= 1:
                return 0

            return min(dp(i - 1) + cost[i - 1], dp(i - 2) + cost[i - 2])

        return dp(len(cost))


# PROBLEM 3 (3ms) - code smell injected
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        n = len(cost)

        def solve(i):
            if i >= n:
                return 0
            return cost[i] + min(solve(i + 1), solve(i + 2))

        return min(solve(0), solve(1))
