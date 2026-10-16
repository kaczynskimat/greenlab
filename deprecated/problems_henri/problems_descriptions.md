# Problems:

| Guideline ID | Family | Difficulty | LeetCode Number # | Problem Name                 | LeetCode URL                                                |	
|--------------|--------|------------|-------------------|------------------------------|-------------------------------------------------------------|
| G24          | Other  | Medium     | #238              | Product of Array Except Self | https://leetcode.com/problems/product-of-array-except-self/ |
| G27          | Other  | Easy       | #905              | Sort Array By Parity         | https://leetcode.com/problems/sort-array-by-parity/         |
| G27          | Other  | Medium     | #49               | Group Anagrams               | https://leetcode.com/problems/group-anagrams/               |
--------------------------------------


## Product of Array Except Self
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.
#### Example 1:
```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```
#### Example 2:
```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```
### Constraints:
2 <= nums.length <= 105 \
-30 <= nums[i] <= 30 \
The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

--------------------------------------

## Sort Array By Parity
Given an integer array nums, move all the even integers at the beginning of the array followed by all the odd integers. \
Return any array that satisfies this condition.

#### Example 1:
```
Input: nums = [3,1,2,4]
Output: [2,4,3,1]
```
##### Explanation:
The outputs [4,2,3,1], [2,4,1,3], and [4,2,1,3] would also be accepted.
#### Example 2:
```
Input: nums = [0]
Output: [0]
```

### Constraints:
1 <= nums.length <= 5000 \
0 <= nums[i] <= 5000

--------------------------------------

## Group Anagrams
Given an array of strings strs, group the anagrams together. You can return the answer in any order.
#### Example 1:
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```
##### Explanation:
There is no string in strs that can be rearranged to form "bat".
The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.
#### Example 2:
```
Input: strs = [""]
Output: [[""]]
```
#### Example 3:
```
Input: strs = ["a"]
Output: [["a"]]
```
### Constraints:
1 <= strs.length <= 104 \
0 <= strs[i].length <= 100 \
strs[i] consists of lowercase English letters.