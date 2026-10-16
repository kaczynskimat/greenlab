# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
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
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------    
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        ans = [] 
        
        for i in range(len(nums)):
            if nums[i] > 0:
                break

            if (i == 0 or nums[i] != nums[i - 1]):
                target = nums[i]
                ptr1 = i + 1
                ptr2 = len(nums) - 1
                
                while ptr1 < ptr2:
                    sum = target + nums[ptr1] + nums[ptr2]
                    if sum == 0:
                        ans.append([nums[ptr1], nums[ptr2], target])
                        while ptr1 < ptr2 and nums[ptr1] == nums[ptr1 + 1]:
                            ptr1 += 1
                        while ptr1 < ptr2 and nums[ptr2] == nums[ptr2 - 1]:
                            ptr2 -= 1
                        ptr1 = ptr1 + 1
                        ptr2 = ptr2 - 1
                        continue
                        
                    if sum < 0:
                        ptr1 = ptr1 + 1
                    else:
                        ptr2 = ptr2 - 1
                    
        return ans
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------    
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        
        for i in range(n):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            j = i + 1
            k = n - 1
            while j < k:
                total = nums[i] + nums[j] + nums[k]
                if total > 0:
                    k -= 1
                elif total < 0:
                    j += 1
                else:
                    res.append([nums[i], nums[j], nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1
                        
        return res