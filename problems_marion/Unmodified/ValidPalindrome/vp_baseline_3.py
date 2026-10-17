from collections import deque


class Solution:
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
            