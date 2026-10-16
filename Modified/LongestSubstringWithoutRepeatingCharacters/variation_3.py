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
            window_len = right - left + 1
            if window_len > longest:
                longest = window_len
            right += 1

        return longest
