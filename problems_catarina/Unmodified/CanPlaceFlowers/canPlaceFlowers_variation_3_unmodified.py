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