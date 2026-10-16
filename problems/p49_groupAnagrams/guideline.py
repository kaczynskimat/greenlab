from collections import deque, defaultdict
from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
# G27: Replace group lists with deques to evaluate container efficiency
# Convert groups back to lists to preserve the required return type
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
                # freq[key] = []
                freq[key] = deque()
            freq[key].append(ch)

        # return list(freq.values())
        return [list(group) for group in freq.values()]

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
# G27: Replace group lists with deque containers
class SolutionV2:
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

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
# G27: Replace group lists with deque containers
class SolutionV3:
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