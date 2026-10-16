from typing import List

# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def sortArrayByParity(self, nums: list[int]) -> list[int]:
        i = 0
        for j in range(0,len(nums)):
            if nums[j]%2==0:
                temp = nums[i]
                nums[i]=nums[j]
                nums[j]=temp
                i+=1
        return nums

# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def sortArrayByParity(self, nums):
        ans=[]
        ans1=[]
        ans2=[]
        for i in range(len(nums)):
            if nums[i] % 2==0 :
                ans1.append(nums[i])

        for j in range(len(nums)):
            if nums[j] % 2 !=0 :
                ans2.append(nums[j])

        ans.extend(ans1)
        ans.extend(ans2)
        return ans

# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
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
        return nums