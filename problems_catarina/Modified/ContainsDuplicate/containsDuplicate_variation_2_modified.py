class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        nums.sort()
        
        for index in range(len(nums) - 1):
            if nums[index] == nums[index + 1]:
                return True
        return False