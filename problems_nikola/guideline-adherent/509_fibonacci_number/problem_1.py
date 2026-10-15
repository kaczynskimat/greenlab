# # -------------------------------------------------
# Fibonacci Number - guideline-adherent version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 1 (47ms) - guideline modified solution
class Solution:
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
