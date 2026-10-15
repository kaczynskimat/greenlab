class Solution:
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