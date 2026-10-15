# # -------------------------------------------------
# Fibonacci Number - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 2 (47ms) - guideline modified solution

from functools import cache

class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
                return 0
        n -= 1
        @cache
        def f(x):
            if x <= 1:
                return 1
            return f(x-1) + f(x-2)
        return f(n)