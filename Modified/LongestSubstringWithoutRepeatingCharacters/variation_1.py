class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        chars = set()
        l = 0
        r = 0
        res = 0
        n = len(s)
        while(r < n):
            while(r < n and s[r] not in chars):
                chars.add(s[r])
                r += 1
            res = max(res, r - l)
            if r == n: break
            while(l < r):
                if (s[r] == s[l]):
                    l += 1
                    break
                chars.remove(s[l])
                l += 1
            r += 1
        return res
