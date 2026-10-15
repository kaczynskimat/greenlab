class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
            
        nums.sort()
        ans = [] 
        for i in range(len(nums)):
            
            if(i==0 or nums[i]!=nums[i-1]):
                
                target = nums[i]
                ptr1 = i+1
                ptr2 = len(nums)-1
                
                while ptr1 < ptr2:
                    sum = target + nums[ptr1] + nums[ptr2]
                    if sum == 0 :
                        ans.append([nums[ptr1] , nums[ptr2] , target])
                        while ptr1 < ptr2 and nums[ptr1] == nums[ptr1+1] : ptr1+=1
                        while ptr1 < ptr2 and nums[ptr2] == nums[ptr2-1] : ptr2-=1
                        ptr1 = ptr1+1
                        ptr2 = ptr2-1
                        continue
                        
                    if sum < 0:
                        ptr1 = ptr1 + 1
                        
                    else:
                        ptr2 = ptr2 - 1
                    
        return ans