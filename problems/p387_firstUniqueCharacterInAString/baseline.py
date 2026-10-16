from collections import OrderedDict
import collections

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------


class SolutionV1:
    def firstUniqChar(self, s: str) -> int:
        L = [[-1, -1] for _ in range(26)]
        for i in range(0, len(s)):
            if L[ord(s[i]) - ord('a')][0] == -1:
                L[ord(s[i]) - ord('a')][0] = 1
                L[ord(s[i]) - ord('a')][1] = i
            else:
                L[ord(s[i]) - ord('a')][0] += 1
        res = 100001
        for i in range(0, 26):
            if L[i][0] == 1:
                res = min(res, L[i][1])
        return res if res != 100001 else -1



# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def firstUniqChar(self, s: str) -> int:
        seen = {}
        for i in range(0, len(s)):
            if seen.get(s[i]) == None:
                seen[s[i]] = collections.deque()
            seen[s[i]].append(i)
        for i in range(0, len(s)):
            if seen.get(s[i]) != None and len(seen.get(s[i])) == 1:
                return i
        return -1



# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def firstUniqChar(self, s: str) -> int:
        list1 = list(s)
        uniques = list(OrderedDict.fromkeys(list1))
        for val in uniques:
            if list1.count(val) == 1 and list1.count(val) != 0:
                return list1.index(val)
        return -1

