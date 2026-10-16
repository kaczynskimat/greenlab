from git import List
from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------


class SolutionV1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        chars = set()
        l = 0
        r = 0
        res=0
        while(r < len(s)):
            while(r < len(s) and s[r] not in chars):
                chars.add(s[r])
                r += 1
            res = max(res, r - l)
            if r == len(s): break
            while(l < r):
                if (s[r] == s[l]):
                    l += 1
                    break
                chars.remove(s[l])
                l += 1
            r += 1
        return res

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        count = 0
        results = []
        currMin = -1
        for i in range(len(s)):
            char = s[i]
            if char not in seen or seen[char] <= currMin:
                seen[char] = i
                count += 1
            else:
                results.append(count)
                count = count - (seen[char] - currMin) + 1
                currMin = seen[char]
                seen[char] = i
        results.append(count)
        return max(results)


# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
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