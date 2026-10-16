# -----------------------------------------------
# Variation 1:
# -----------------------------------------------


class SolutionV1:
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
            prev_idx = seen.get(char, -1)
            if char not in seen or prev_idx <= currMin:
                seen[char] = i
                count += 1
            else:
                results.append(count)
                count = count - (prev_idx - currMin) + 1
                currMin = prev_idx
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
            window_len = right - left + 1
            if window_len > longest:
                longest = window_len
            right += 1

        return longest
