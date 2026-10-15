#https://leetcode.com/problems/fibonacci-number/description/
# # -------------------------------------------------
# Fibonacci Number
# -------------------------------------------------
# G18: Use memoization to avoid repeated execution of expensive pure functions
# -------------------------------------------------

# Problem 1 (100ms) - 5
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

# Problem 2 (92ms) - 6
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

# Problem 3 (120ms) - 12
class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)

