class Solution(object):
    def containsDuplicate(self, nums):
        x = {}
        for p in nums:
            if p in x:
                x[p] = 2
            else:
                x[p] = 1
        y = next((True for key, value in x.items() if value == 2), False)
        return y