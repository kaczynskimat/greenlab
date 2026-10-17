class Solution:
    def firstUniqChar(self, s: str) -> int:
        L = [[-1, -1] for _ in range(26)]
        for i in range(0, len(s)):
            temp = s[i]
            x = ord(temp) - ord('a')
            if L[x][0] == -1:
                L[x][0] = 1
                L[x][1] = i
            else:
                L[x][0] += 1
        res = 100001
        for i in range(0, 26):
            if L[i][0] == 1:
                res = min(res, L[i][1])
        return res if res != 100001 else -1
