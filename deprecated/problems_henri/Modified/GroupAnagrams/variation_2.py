# from collections import defaultdict
from collections import defaultdict, deque


# G27: Replace group lists with deque containers
class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        # result = defaultdict(list)
        result = defaultdict(deque)

        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord("a")] += 1

            result[tuple(count)].append(s)

        #return list(result.values())
        return [list(group) for group in result.values()]