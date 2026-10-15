class Solution:
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