# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def print_num(self,n):
        if n==0:
            return 0
        if n==1 or n==2:
            return 1
        if n==3:
            return 2

        if n in self.memo:
            return self.memo[n]

        self.memo[n] = self.print_num(n-1)+self.print_num(n-2)
        return self.memo[n]

    def fib(self, n: int) -> int:
         self.memo = {}
         return self.print_num(n)
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
from functools import cache

class SolutionV2:
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
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------

class SolutionV3:
    def fib(self, n: int) -> int:
        @cache
        def calculate(n):
            if n == 0:
                return 0
            if n <= 2:
                return 1
            return calculate(n - 1) + calculate(n - 2)
        return calculate(n)