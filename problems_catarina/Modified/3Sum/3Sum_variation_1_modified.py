class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        if len(nums) < 3:
            return []
            
        nums.sort()
        ans = []

        for k in range(0, len(nums) - 2):
            if nums[k] > 0:
                break

            if k > 0 and nums[k] == nums[k - 1]:
                continue
                
            a = nums[k]
            left = k + 1
            right = len(nums) - 1

            while left < right:
                current_sum = a + nums[left] + nums[right]
                if current_sum < 0:
                    left += 1
                elif current_sum > 0:
                    right -= 1
                else:
                    ans.append([a, nums[left], nums[right]])
                    left += 1
                    right -= 1
                
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return ans