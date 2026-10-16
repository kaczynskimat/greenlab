from typing import List

class Solution:
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