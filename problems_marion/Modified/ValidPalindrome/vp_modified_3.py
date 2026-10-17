from collections import deque


class Solution:
    def isPalindrome(self, s: str) -> bool:
        chars = deque()
        for c in s:
            if c.isalnum():
                chars.append(c.lower())

        while len(chars) > 1:
            if chars.popleft() != chars.pop():
                return False
        return True