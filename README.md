## The Sun Enjoyers - Green Lab 2026
Replication package for our study on energy-efficient Python code at Vrije Universiteit Amsterdam.

We compare original and guideline-modified solutions for 16 LeetCode problems across 8 energy-efficiency guidelines.
We measure energy consumption, execution time, average power draw, CPU utilization, and memory usage.

### Contents:
- Data: Raw measurements
- Source code: Code implementations, Experiment runner configurations, processing and analysis scripts
- Figures: Exploratory and final figures
- Text: Project report, README, and some experiment notes

### LeetCode Problems:
16 Problems - 8 Easy - 8 Medium

| Guideline ID | Family             | Difficulty | LeetCode # | Problem Name                                    | LeetCode URL |
|--------------|--------------------|------------|------------|-------------------------------------------------|--------------|
| G1           | Code Optimization	 | Easy	      | #387	      | First Unique Character in a String I                      | 	https://leetcode.com/problems/first-unique-character-in-a-string/        |
| G1           | 	Code Optimization | 	Medium    | 	#3        | 	Longest Substring Without Repeating Characters | 	https://leetcode.com/problems/longest-substring-without-repeating-characters/        |
| G2	          | Code Optimization  | 	Easy	     | #977	      | Squares of a Sorted Array	                      | https://leetcode.com/problems/squares-of-a-sorted-array/         |
| G2	          | Code Optimization	 | Medium	    | #240        | 	Merge Intervals	                               | https://leetcode.com/problems/search-a-2d-matrix-ii/        |
| G3	          | Code Optimization	 | Easy	      | #605       | 	Can Place Flowers	                            | https://leetcode.com/problems/can-place-flowers/         |
| G3	          | Code Optimization  | 	Medium	   | #15	       | 3Sum	                                           | https://leetcode.com/problems/3sum/         |
| G6	          | Code Optimization	 | Easy	      | #383	       | Ransom Note	                                    | https://leetcode.com/problems/ransom-note/         |
| G6	          | Code Optimization  | 	Medium	   | #442       | 	Find All Duplicates in an Array                | 	https://leetcode.com/problems/find-all-duplicates-in-an-array/        |
| G18	         | Function Calls	    | Easy	      | #509	      | Fibonacci Number	                       | https://leetcode.com/problems/fibonacci-number/         |
| G18	         | Function Calls     | 	Medium	   | #322	      | Coin Change	                                    | https://leetcode.com/problems/coin-change/         |
| G19	         | Function Calls     | 	Easy	     | #125	      | Valid Palindrome	                               | https://leetcode.com/problems/valid-palindrome/         |
| G19	         | Function Calls	    | Medium	    | #200	      | Number of Islands                               | 	https://leetcode.com/problems/number-of-islands/        |
| G24	         | Other	             | Easy	      | #867	      | Transpose Matrix	                               | https://leetcode.com/problems/transpose-matrix/         |
| G24	         | Other	             | Medium	    | #238	      | Product of Array Except Self	                   | https://leetcode.com/problems/product-of-array-except-self/         |
| G27	         | Other	             | Easy	      | #905	      | Sort Array By Parity                            | 	https://leetcode.com/problems/sort-array-by-parity/        |
| G27	         | Other              | 	Medium	   | #49	       | Group Anagrams                                  | https://leetcode.com/problems/group-anagrams/         |

### Documentation:
See the project report (PDF) for the experimental design, procedure, and analysis.

# Still TODO keep one version and adapt it?:

| Guideline ID | LeetCode # & Name (Difficulty) | Solution Variant | Smell Added By Us? | Description of Modification / Refactoring (Baseline vs. Refactored) |
| :--- | :--- | :--- | :--- | :--- |
| **G1** | #387 (First Unique Character in a String) <br> *(Easy)* | Solution 1 | **No** (Retrieved from LC) | **Baseline:**  <br>**Refactored:**  |
| **G1** | #387 (First Unique Character in a String) <br> *(Easy)* | Solution 2 | **No** (Retrieved from LC) | **Baseline:**  <br>**Refactored:**  |
| **G1** | #387 (First Unique Character in a String) <br> *(Easy)* | Solution 3 | **No** (Retrieved from LC) | **Baseline:**  <br>**Refactored:** |
| **G1** | #3 (Longest Substring Without Repeating Characters) <br> *(Medium)* | Solution 1 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** |
| **G1** | #3 (Longest Substring Without Repeating Characters) <br> *(Medium)* | Solution 2 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** |
| **G1** | #3 (Longest Substring Without Repeating Characters) <br> *(Medium)* | Solution 3 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** |
| **G2** | #977 (Squares of a Sorted Array) <br> *(Easy)* | Solution 1 | **Yes** (Injected) | **Baseline:** <br>**Refactored:** |
| **G2** | #977 (Squares of a Sorted Array) <br> *(Easy)* | Solution 2 | **Yes** (Injected) | **Baseline:** <br>**Refactored:** |
| **G2** | #977 (Squares of a Sorted Array) <br> *(Easy)* | Solution 3 | **Yes** (Injected) | **Baseline:** <br>**Refactored:** |
| **G2** | #240 (Search a 2D Matrix II) <br> *(Medium)* | Solution 1 | **Yes** (Injected) | **Baseline:** <br>**Refactored:** |
| **G2** | #240 (Search a 2D Matrix II) <br> *(Medium)* | Solution 2 | **Yes** (Injected) | **Baseline:** <br>**Refactored:** |
| **G2** | #240 (Search a 2D Matrix II) <br> *(Medium)* | Solution 3 | **Yes** (Injected) | **Baseline:** <br>**Refactored:**  |
| **G3** | #217 (Contains Duplicate) <br> *(Easy)* | Solution 1 | | |
| **G3** | #217 (Contains Duplicate) <br> *(Easy)* | Solution 2 | | |
| **G3** | #217 (Contains Duplicate) <br> *(Easy)* | Solution 3 | | |
| **G3** | #15 (3Sum) <br> *(Medium)* | Solution 1 | | |
| **G3** | #15 (3Sum) <br> *(Medium)* | Solution 2 | | |
| **G3** | #15 (3Sum) <br> *(Medium)* | Solution 3 | | |
| **G6** | #26 (Remove Duplicates from Sorted Array) <br> *(Easy)* | Solution 1 | | |
| **G6** | #26 (Remove Duplicates from Sorted Array) <br> *(Easy)* | Solution 2 | | |
| **G6** | #26 (Remove Duplicates from Sorted Array) <br> *(Easy)* | Solution 3 | | |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 1 | | |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 2 | | |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 3 | | |
| **G18** | #746 (Min Cost Climbing Stairs) <br> *(Easy)* | Solution 1 | | |
| **G18** | #746 (Min Cost Climbing Stairs) <br> *(Easy)* | Solution 2 | | |
| **G18** | #746 (Min Cost Climbing Stairs) <br> *(Easy)* | Solution 3 | | |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 1 | | |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 2 | | |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 3 | | |
| **G19** | #125 (Valid Palindrome) <br> *(Easy)* | Solution 1 | | |
| **G19** | #125 (Valid Palindrome) <br> *(Easy)* | Solution 2 | | |
| **G19** | #125 (Valid Palindrome) <br> *(Easy)* | Solution 3 | | |
| **G19** | #200 (Number of Islands) <br> *(Medium)* | Solution 1 | | |
| **G19** | #200 (Number of Islands) <br> *(Medium)* | Solution 2 | | |
| **G19** | #200 (Number of Islands) <br> *(Medium)* | Solution 3 | | |
| **G24** | #867 (Transpose Matrix) <br> *(Easy)* | Solution 1 | | |
| **G24** | #867 (Transpose Matrix) <br> *(Easy)* | Solution 2 | | |
| **G24** | #867 (Transpose Matrix) <br> *(Easy)* | Solution 3 | | |
| **G24** | #238 (Product of Array Except Self) <br> *(Medium)* | Solution 1 | | |
| **G24** | #238 (Product of Array Except Self) <br> *(Medium)* | Solution 2 | | |
| **G24** | #238 (Product of Array Except Self) <br> *(Medium)* | Solution 3 | | |
| **G28** | #905 (Sort Array By Parity) <br> *(Easy)* | Solution 1 | | |
| **G28** | #905 (Sort Array By Parity) <br> *(Easy)* | Solution 2 | | |
| **G28** | #905 (Sort Array By Parity) <br> *(Easy)* | Solution 3 | | |
| **G28** | #49 (Group Anagrams) <br> *(Medium)* | Solution 1 | | |
| **G28** | #49 (Group Anagrams) <br> *(Medium)* | Solution 2 | | |
| **G28** | #49 (Group Anagrams) <br> *(Medium)* | Solution 3 | | |



| Guideline ID | LeetCode # & Name (Difficulty) | Solution Variant | Smell Added By Us? | Description of Modification / Refactoring (Baseline vs. Refactored) | Link to LeetCode|
| :--- | :--- | :--- | :--- | :--- | :--- |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 1 | **No** (Retrieved from LC) | **Baseline:**  <br>**Refactored:**  | https://leetcode.com/problems/find-all-duplicates-in-an-array/description/ |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 2 | **No** (Retrieved from LC) | **Baseline:**  <br>**Refactored:**  | https://leetcode.com/problems/find-all-duplicates-in-an-array/description/ |
| **G6** | #442 (Find All Duplicates in an Array) <br> *(Medium)* | Solution 3 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/find-all-duplicates-in-an-array/description/ |
| **G18** | #509 (Fibonacci Number) <br> *(Easy)* | Solution 1 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/fibonacci-number/description/ |
| **G18** | #509 (Fibonacci Number) <br> *(Easy)* | Solution 2 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:**  | https://leetcode.com/problems/fibonacci-number/description/ |
| **G18** | #509 (Fibonacci Number) <br> *(Easy)* | Solution 3 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/fibonacci-number/description/ |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 1 | **No** (Retrieved from LC) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/coin-change/description/ |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 2 | **Yes** (Code Smell Injected) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/coin-change/description/ |
| **G18** | #322 (Coin Change) <br> *(Medium)* | Solution 3 | **Yes** (Code Smell Injected) | **Baseline:** <br>**Refactored:** | https://leetcode.com/problems/coin-change/description/ |