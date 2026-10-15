# # -------------------------------------------------
# Fibonacci Number - baseline version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 3 (120ms) - original LeetCode solution
class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)