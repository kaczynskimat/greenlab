class Solution:
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