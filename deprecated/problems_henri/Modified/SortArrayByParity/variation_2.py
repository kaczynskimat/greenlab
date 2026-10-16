from array import array

# G27: Use a typed numeric array as the working containers
class Solution:
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