from collections import OrderedDict

class Solution:
    def firstUniqChar(self, s: str) -> int:
        list1 = list(s)
        uniques = list(OrderedDict.fromkeys(list1))
        for val in uniques:
            freq = list1.count(val)
            if freq == 1 and freq != 0:
                return list1.index(val)
        return -1
