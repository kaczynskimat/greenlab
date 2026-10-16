# -----------------------------------------------
# Variation 1:
# -----------------------------------------------


class SolutionV1(object):
    def sortedSquares(self, nums):
        nums.sort()
        n = len(nums)
        result = [0] * n
        left = 0
        right = n - 1
        for p in range(n - 1, -1, -1):
            left_square = nums[left] * nums[left]
            right_square = nums[right] * nums[right]
            if left_square > right_square:
                result[p] = left_square
                left += 1
            else:
                result[p] = right_square
                right -= 1
        return result



# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2(object):
    def sortedSquares(self, nums):
        nums.sort()
        result = list(map(lambda x: x * x, nums))
        result.sort()
        return result



# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3(object):
    def sortedSquares(self, nums):
        nums.sort()
        n = len(nums)
        right = n - 1
        left = 0
        result = n * [0]
        for i in range(n - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                result[i] = nums[left] ** 2
                left += 1
            else:
                result[i] = nums[right] ** 2
                right -= 1
        return result
