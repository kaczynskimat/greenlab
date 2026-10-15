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