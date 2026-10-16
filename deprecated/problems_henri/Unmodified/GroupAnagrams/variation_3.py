from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if not strs:
            return []
        anagrams = defaultdict(list)
        for s in strs:
            sorted_str = ''.join(sorted(s))
            anagrams[sorted_str].append(s)
        return list(anagrams.values())