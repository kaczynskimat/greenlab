class Solution:
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