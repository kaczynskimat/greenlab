class Solution:
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
