class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        longest = 0
        left, right = 0, 0
        while left <= right < len(s):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            if (right - left + 1) > longest:
                longest = right - left + 1
            right += 1

        return longest
