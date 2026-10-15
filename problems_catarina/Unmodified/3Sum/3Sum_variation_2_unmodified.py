class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        if len(nums) < 3:
            return []
        if all(num == 0 for num in nums):
            return [[0, 0, 0]]
        
        nums.sort()
        res = set()

        for i in range(len(nums)):
            target = 0 - nums[i]

            map = {}
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in map:
                    sol = tuple(sorted((nums[i], nums[j], complement)))
                    res.add(sol)
                map[nums[j]] = j
        return [list(sol) for sol in res]