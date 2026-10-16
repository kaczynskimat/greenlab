# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        for char in set(ransomNote):
            if ransomNote.count(char) > magazine.count(char):
                return False
                
        return True
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
from collections import defaultdict

class SolutionV2:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        mag_dict = defaultdict(int)
        
        for c in magazine:
            mag_dict[c] += 1
        
        for c in ransomNote:
            if mag_dict[c] <= 0:
                return False
            mag_dict[c] -= 1
        
        return True
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        
        counts = [0] * 26
        
        for ch in magazine:
            counts[ord(ch) - 97] += 1
            
        for ch in ransomNote:
            idx = ord(ch) - 97
            if counts[idx] == 0:
                return False
            counts[idx] -= 1
            
        return True