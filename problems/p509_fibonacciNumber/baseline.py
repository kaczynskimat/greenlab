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
        
        return self.print_num(n-1)+self.print_num(n-2)
    def fib(self, n: int) -> int:
         return self.print_num(n)
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def fib(self, n: int) -> int:
        if n == 0:
                return 0
        n -= 1
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
        if n == 0:
            return 0
        if n <= 2:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)