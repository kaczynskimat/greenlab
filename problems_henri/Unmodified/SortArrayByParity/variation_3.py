from typing import List

class Solution:
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