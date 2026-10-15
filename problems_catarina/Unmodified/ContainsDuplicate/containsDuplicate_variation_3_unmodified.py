from collections import Counter

class Solution:
    def containsDuplicate(self,nums:list[int])->bool:
        counter=Counter(nums)
        for k,v in counter.items():
            if v>=2:
                return True
        return False 