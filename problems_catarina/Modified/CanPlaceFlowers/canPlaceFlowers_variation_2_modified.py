class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        if n == 0:
            return True
        plantable = 0
        i = 0
        while i < len(flowerbed):
            if flowerbed[i] == 0 and (i == 0 or flowerbed[i - 1] == 0) and (i >= len(flowerbed) - 1 or flowerbed[i + 1] == 0):
                plantable += 1
                if plantable >= n:
                    return True
                i += 2
            else:
                i += 1
        return plantable >= n
    
    