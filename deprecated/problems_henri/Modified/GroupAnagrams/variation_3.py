# from collections import defaultdict
from collections import defaultdict, deque
from typing import List

# G27: Replace group lists with deque containers
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if not strs:
            return []
        # anagrams = defaultdict(list)
        anagrams = defaultdict(deque)
        for s in strs:
            sorted_str = ''.join(sorted(s))
            anagrams[sorted_str].append(s)
        # return list(anagrams.values())
        return [list(group) for group in anagrams.values()]