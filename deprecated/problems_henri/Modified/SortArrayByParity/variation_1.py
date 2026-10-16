from array import array

# G27: Use a typed numeric array as the working container
class Solution:
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