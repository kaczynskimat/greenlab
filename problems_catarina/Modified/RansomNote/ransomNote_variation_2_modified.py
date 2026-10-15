from collections import defaultdict

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        mag_dict = defaultdict(int)
        
        for c in magazine:
            mag_dict[c] += 1
        
        for c in ransomNote:
            if mag_dict[c] <= 0:
                return False
            mag_dict[c] -= 1
        
        return True