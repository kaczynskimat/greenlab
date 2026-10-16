# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        list_magazine = list(magazine)

        for letter in ransomNote:
            if letter in list_magazine:
                flag  = True
                list_magazine.remove(letter)
            else:
                flag = False
                break

        return flag
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
from collections import defaultdict

class SolutionV2:
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
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------    
class SolutionV3:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        counts_mag = [0] * 26
        for ch in magazine:
            counts_mag[ord(ch) - 97] += 1
        counts_ransom = [0] * 26
        for ch in ransomNote:
            counts_ransom[ord(ch) - 97] += 1
        for i in range(26):
            if counts_ransom[i] > counts_mag[i]:
                return False
        return True