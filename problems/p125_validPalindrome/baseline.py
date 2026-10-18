from collections import deque
# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def isPalindrome(self, s: str) -> bool:
        s = "".join(c.lower() for c in s if c.isalnum())
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def isPalindrome(self, s: str) -> bool:
        def is_valid(c):
            return c.isalnum()
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not is_valid(s[left]):
                left += 1
            while left < right and not is_valid(s[right]):
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def isPalindrome(self, s: str) -> bool:
        def is_valid(c):
            return c.isalnum()
        chars = deque()
        for c in s:
            if is_valid(c):
                chars.append(c.lower())
        while len(chars) > 1:
            if chars.popleft() != chars.pop():
                return False
        return True