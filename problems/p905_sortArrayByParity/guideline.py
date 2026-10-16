from array import array
from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
# G27: Use a typed numeric array as the working container
class SolutionV1:
    def sortArrayByParity(self, nums: list[int]) -> list[int]:
        nums = array("I", nums)

        i = 0
        for j in range(0,len(nums)):
            if nums[j]%2==0:
                temp = nums[i]
                nums[i]=nums[j]
                nums[j]=temp
                i+=1
        # return nums
        return nums.tolist()

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
# G27: Use a typed numeric array as the working containers
class SolutionV2:
    def sortArrayByParity(self, nums):
        nums = array("I", nums)
        ans = array("I")
        ans1 = array("I")
        ans2 = array("I")
        for i in range(len(nums)):
            if nums[i] % 2==0 :
                ans1.append(nums[i])

        for j in range(len(nums)):
            if nums[j] % 2 !=0 :
                ans2.append(nums[j])

        ans.extend(ans1)
        ans.extend(ans2)
        return ans.tolist()

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
# G27: Use a typed numeric array as the working container
class SolutionV3:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        nums = array("I", nums)
        # 2 Pointers + Swap
        # Time: O(n) - Space: O(1)
        left = 0
        right = len(nums) - 1
        while left < right:
            if nums[left] % 2 == 0:
                left += 1
            else: # nums[left] % 2 != 0: --> Swap
                temp = nums[left]
                nums[left] = nums[right]
                nums[right] = temp
                right -= 1
        # return nums
        return nums.tolist()