class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        nums.sort()
        has_duplicate = False

        for index in range(len(nums) - 1):
            if nums[index] == nums[index + 1]:
                has_duplicate = True
        return has_duplicate
