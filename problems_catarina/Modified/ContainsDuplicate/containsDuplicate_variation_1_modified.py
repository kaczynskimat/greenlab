class Solution(object):
    def containsDuplicate(self, nums):
        x = {}
        for p in nums:
            if p in x:
                return True
            x[p] = 1
            
        return False