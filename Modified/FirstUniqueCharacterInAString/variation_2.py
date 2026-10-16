import collections

class Solution:
    def firstUniqChar(self, s: str) -> int:
        seen = {}
        for i in range(0, len(s)):
            if seen.get(s[i]) == None:
                seen[s[i]] = collections.deque()
            seen[s[i]].append(i)
        for i in range(0, len(s)):
            queue = seen.get(s[i])
            if queue != None and len(queue) == 1:
                return i
        return -1
