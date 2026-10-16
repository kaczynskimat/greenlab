from typing import List
from collections import defaultdict

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        #Tc -> o(n * k)
        #Sc -> o(n)
        freq = {}

        for ch in strs:
            count = [0] * 26

            for c in ch:
                count[ord(c) - ord('a')] += 1

            key = tuple(count)

            if key not in freq:
                freq[key] = []
            freq[key].append(ch)

        return list(freq.values())

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        result = defaultdict(list)

        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord("a")] += 1

            result[tuple(count)].append(s)

        return list(result.values())

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if not strs:
            return []
        anagrams = defaultdict(list)
        for s in strs:
            sorted_str = ''.join(sorted(s))
            anagrams[sorted_str].append(s)
        return list(anagrams.values())