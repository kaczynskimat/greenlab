# # -------------------------------------------------
# Fibonacci Number - baseline version
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# PROBLEM 1 (100ms) - original LeetCode solution
class Solution:
    def print_num(self,n):
        if n==0:
            return 0
        if n==1 or n==2:
            return 1
        if n==3:
            return 2
        
        return self.print_num(n-1)+self.print_num(n-2)
    def fib(self, n: int) -> int:
         return self.print_num(n)

# PROBLEM 2 (92ms) - original LeetCode solution
class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
                return 0
        n -= 1
        def f(x):
            if x <= 1:
                return 1
            return f(x-1) + f(x-2)
        return f(n)

# PROBLEM 3 (120ms) - original LeetCode solution
class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)