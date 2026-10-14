from collections import OrderedDict


class Solution:
    def firstUniqChar(self, s: str) -> int:
        list1 = list(s)
        uniques = list(OrderedDict.fromkeys(list1))
        for val in uniques:
            if list1.count(val) == 1 and list1.count(val) != 0:
                return list1.index(val)
        return -1
