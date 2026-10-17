class Solution:
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
