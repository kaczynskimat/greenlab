from collections import Counter

class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        counter = Counter()
        for x in nums:
            counter[x] += 1
            if counter[x] >= 2:
                return True 
        return False