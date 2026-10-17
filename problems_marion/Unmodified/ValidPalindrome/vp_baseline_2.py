class Solution:
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