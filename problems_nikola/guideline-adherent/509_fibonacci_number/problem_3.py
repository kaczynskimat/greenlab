# # -------------------------------------------------
# Fibonacci Number - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 3 (47ms) - guideline modified solution

from functools import cache

class Solution:
    def fib(self, n: int) -> int:
        @cache
        def calculate(n):
            if n == 0:
                return 0
            if n <= 2:
                return 1
            return calculate(n - 1) + calculate(n - 2)
        return calculate(n)