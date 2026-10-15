from collections import Counter
from bisect import bisect_left, bisect_right

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        triplets = set()
        counter = Counter(nums)
        ns = sorted(counter.keys())

        for i, ni in enumerate(ns):
            if ni > 0:
                break
            if ni == 0:
                if counter[0] >= 3:
                    triplets.add((0, 0, 0))
            else: 
                if counter[ni] >= 2 and -2 * ni in counter:
                    triplets.add((ni, ni, -2 * ni))
                t = -ni
                left = bisect_left(ns, t - ns[-1], i + 1)
                right = bisect_right(ns, t // 2, left)
                for nj in ns[left:right]:
                    nk = t - nj
                    if nk in counter and (nk != nj or counter[nj] >= 2):
                        triplets.add((ni, nj, nk))

        return [list(t) for t in triplets]