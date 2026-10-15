from collections import defaultdict

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        
        mag_dict = defaultdict(int)
        ransom_dict = defaultdict(int)
        
        
        for c in magazine:
            mag_dict[c] += 1
        
        for c in ransomNote:
            ransom_dict[c] += 1
            if c not in mag_dict:
                return False
        
        for c, val in ransom_dict.items():
            if mag_dict[c] < val:
                return False
        
        return True