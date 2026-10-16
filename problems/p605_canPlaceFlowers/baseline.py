# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        count = 0
        length = len(flowerbed)
        
        for i in range(length):
            
            if flowerbed[i] == 0:
                
                left_empty = (i == 0) or (flowerbed[i - 1] == 0)
                
                right_empty = (i == length - 1) or (flowerbed[i + 1] == 0)
                
                if left_empty and right_empty:
                    flowerbed[i] = 1
                    count += 1
                        
        return count >= n
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------    
class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        plantable = 0
        i = 0
        while i < len(flowerbed):
            if flowerbed[i] == 0 and (i == 0 or flowerbed[i - 1] == 0) and (i >= len(flowerbed) - 1 or flowerbed[i + 1] == 0):
                plantable += 1
                i += 2
            else:
                i += 1
        if n > plantable:
            return False
        else:
            return True
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------        
class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:

        if n == 0 : return True 
        m = len(flowerbed)

        for i in range(m):
            if flowerbed[i] == 1: 
                if i > 0 : flowerbed[i-1] = 2
                if i < m-1 :  flowerbed[i+1] = 2 
        count = 0
        for i in range(m):
            if flowerbed[i] == 0:
                count += 1 
                if i > 0 : flowerbed[i-1] = 2
                if i < m-1 :  flowerbed[i+1] = 2 

        return count >= n 