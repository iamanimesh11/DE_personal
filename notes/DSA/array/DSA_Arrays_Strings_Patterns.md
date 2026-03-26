# 🧠 DSA Pattern Notes — Arrays & Strings
### *For Data Engineer Interviews | Revise Daily*

> **How to use:** When a problem appears → first ask yourself *"Which pattern is this?"* → then code.  
> Don't jump to code. Pattern first. Always.

---

## 📌 Pattern Index

| # | Pattern | When to think of it |
|---|---------|-------------------|
| 1 | Two Pointers | Sorted array, pairs, palindrome |
| 2 | Sliding Window | Subarray/substring with constraint |
| 3 | Prefix Sum | Range sum queries, cumulative count |
| 4 | Hash Map / Frequency Count | Duplicates, anagram, count occurrences |
| 5 | Kadane's Algorithm | Max/min subarray sum |
| 6 | Binary Search on Array | Sorted array, "find position/threshold" |
| 7 | Merge Intervals | Overlapping ranges, scheduling |
| 8 | Monotonic Stack | Next greater/smaller element |
| 9 | Matrix Traversal | 2D grid, island problems |
| 10 | String Manipulation | Parsing, reversing, pattern matching |

---

## 1. 🔁 Two Pointers

### 🧩 What is it?
Use **two index variables** (left, right) moving toward each other or in same direction.  
Avoids nested loops → reduces O(n²) to O(n).

### 🚨 Trigger Words
- "sorted array"
- "find pair with target sum"
- "palindrome"
- "remove duplicates in-place"
- "container with most water"

### 📐 Template
```python
left, right = 0, len(arr) - 1
while left < right:
    if condition_met:
        # process
        left += 1
        right -= 1
    elif need_more:
        left += 1
    else:
        right -= 1
```

---

### 🔹 Example 1 — Two Sum II (Sorted Array)
**Problem:** Given a sorted array, find two numbers that add up to target. Return 1-indexed positions.

```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return [left + 1, right + 1]   # 1-indexed
        elif current < target:
            left += 1      # need bigger sum → move left up
        else:
            right -= 1     # need smaller sum → move right down
    
    return []

# numbers = [2, 7, 11, 15], target = 9  →  [1, 2]
```
**Why two pointers?** Array is sorted → we can intelligently shrink search space.

---

### 🔹 Example 2 — Valid Palindrome
**Problem:** Check if a string is a palindrome ignoring non-alphanumeric chars.

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        # skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    
    return True

# "A man, a plan, a canal: Panama"  →  True
```

---

## 2. 🪟 Sliding Window

### 🧩 What is it?
Maintain a **window [left, right]** over an array/string. Expand right, shrink left based on constraint.  
Key insight: you don't restart from scratch — you *slide*.

### 🚨 Trigger Words
- "longest/shortest subarray/substring with condition"
- "maximum sum of k elements"
- "contains at most k distinct characters"
- "minimum window containing all chars"

### 📐 Template — Variable Size Window
```python
left = 0
window_state = {}   # or a counter / sum

for right in range(len(arr)):
    # --- EXPAND: add arr[right] to window ---
    window_state[arr[right]] = window_state.get(arr[right], 0) + 1
    
    # --- SHRINK: while window is invalid ---
    while window_is_invalid(window_state):
        window_state[arr[left]] -= 1
        if window_state[arr[left]] == 0:
            del window_state[arr[left]]
        left += 1
    
    # --- RECORD: window [left..right] is valid here ---
    result = max(result, right - left + 1)
```

### 📐 Template — Fixed Size Window (size k)
```python
window_sum = sum(arr[:k])
max_sum = window_sum

for i in range(k, len(arr)):
    window_sum += arr[i] - arr[i - k]   # slide: add new, remove old
    max_sum = max(max_sum, window_sum)
```

---

### 🔹 Example 1 — Longest Substring Without Repeating Characters
**Problem:** Find the length of the longest substring with all unique characters.

```python
def length_of_longest_substring(s):
    char_index = {}   # char → last seen index
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        # if char seen and it's inside our window → shrink
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# "abcabcbb"  →  3  ("abc")
# "pwwkew"    →  3  ("wke")
```

---

### 🔹 Example 2 — Minimum Window Substring
**Problem:** Given strings s and t, find the minimum window in s that contains all chars of t.

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)        # chars we need
    have = {}                # chars in current window
    formed = 0               # how many unique chars of t are satisfied
    required = len(need)
    
    left = 0
    result = ""
    min_len = float('inf')
    
    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        
        # check if this char's count satisfies requirement
        if char in need and have[char] == need[char]:
            formed += 1
        
        # try to shrink window when all chars are satisfied
        while formed == required:
            # record result
            if (right - left + 1) < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            
            # remove left char from window
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1
    
    return result

# s = "ADOBECODEBANC", t = "ABC"  →  "BANC"
```

---

## 3. ➕ Prefix Sum

### 🧩 What is it?
Precompute cumulative sums so any **range sum [i, j]** = prefix[j+1] - prefix[i] in O(1).  
Eliminates repeated summation over subarrays.

### 🚨 Trigger Words
- "sum of elements between index i and j"
- "subarray sum equals k"
- "number of subarrays with sum divisible by k"
- "running total / cumulative"

### 📐 Template
```python
prefix = [0] * (len(arr) + 1)
for i in range(len(arr)):
    prefix[i + 1] = prefix[i] + arr[i]

# Sum from index l to r (inclusive):
range_sum = prefix[r + 1] - prefix[l]
```

---

### 🔹 Example 1 — Subarray Sum Equals K
**Problem:** Count the number of subarrays that sum to k.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    running_sum = 0
    prefix_count = defaultdict(int)
    prefix_count[0] = 1   # empty prefix
    
    for num in nums:
        running_sum += num
        
        # if (running_sum - k) was seen before → subarray exists
        count += prefix_count[running_sum - k]
        prefix_count[running_sum] += 1
    
    return count

# nums = [1, 1, 1], k = 2  →  2
# nums = [1, 2, 3], k = 3  →  2
```
**Key insight:** If prefix[j] - prefix[i] = k, then subarray [i..j-1] sums to k.

---

### 🔹 Example 2 — Product of Array Except Self
**Problem:** Return array where each element is product of all others. No division. O(n).

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # left pass: result[i] = product of all elements to the LEFT of i
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # right pass: multiply by product of all elements to the RIGHT of i
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# [1, 2, 3, 4]  →  [24, 12, 8, 6]
```

---

## 4. 🗂️ Hash Map / Frequency Count

### 🧩 What is it?
Use a dictionary to store **counts, last-seen index, or groupings**.  
Trades space for time — turns O(n²) lookups into O(1).

### 🚨 Trigger Words
- "find duplicates"
- "two sum (unsorted)"
- "group anagrams"
- "first unique character"
- "count frequency of..."
- "check if arrays are equal ignoring order"

### 📐 Template
```python
freq = {}
for item in arr:
    freq[item] = freq.get(item, 0) + 1

# or with Counter:
from collections import Counter
freq = Counter(arr)
```

---

### 🔹 Example 1 — Two Sum (Unsorted)
**Problem:** Find indices of two numbers that add to target.

```python
def two_sum(nums, target):
    seen = {}   # value → index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []

# [2, 7, 11, 15], target=9  →  [0, 1]
```

---

### 🔹 Example 2 — Group Anagrams
**Problem:** Group strings that are anagrams of each other.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    
    for s in strs:
        key = tuple(sorted(s))   # anagrams share same sorted key
        groups[key].append(s)
    
    return list(groups.values())

# ["eat","tea","tan","ate","nat","bat"]
# → [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

## 5. 📈 Kadane's Algorithm

### 🧩 What is it?
Find the **maximum sum contiguous subarray** in O(n).  
At each element: either extend existing subarray or start fresh.

### 🚨 Trigger Words
- "maximum subarray sum"
- "largest sum contiguous subarray"
- "best time to buy/sell stock" (variant)

### 📐 Template
```python
max_sum = nums[0]
current_sum = nums[0]

for num in nums[1:]:
    current_sum = max(num, current_sum + num)   # extend OR restart
    max_sum = max(max_sum, current_sum)
```

---

### 🔹 Example 1 — Maximum Subarray
**Problem:** Find the contiguous subarray with the largest sum.

```python
def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    for num in nums[1:]:
        # restart if current sum dragging us down
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# [-2,1,-3,4,-1,2,1,-5,4]  →  6  (subarray: [4,-1,2,1])
```

---

### 🔹 Example 2 — Maximum Product Subarray
**Problem:** Find the contiguous subarray with the largest product. (Negative × Negative = Positive!)

```python
def max_product(nums):
    max_prod = nums[0]
    min_p = max_p = nums[0]   # track both: negatives can flip
    
    for num in nums[1:]:
        candidates = (num, max_p * num, min_p * num)
        max_p = max(candidates)
        min_p = min(candidates)
        max_prod = max(max_prod, max_p)
    
    return max_prod

# [2, 3, -2, 4]  →  6
# [-2, 0, -1]    →  0
```

---

## 6. 🔍 Binary Search on Array

### 🧩 What is it?
Eliminate half the search space each step on a **sorted (or logically sorted) array**.  
If you can ask "is the answer ≥ mid?" → binary search applies.

### 🚨 Trigger Words
- "sorted array, find target"
- "find first/last position"
- "search in rotated sorted array"
- "minimum in rotated array"
- "find peak element"

### 📐 Template
```python
left, right = 0, len(arr) - 1

while left <= right:
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

return -1   # not found
```

---

### 🔹 Example 1 — Search in Rotated Sorted Array
**Problem:** Array was sorted then rotated. Find target. Return index or -1.

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1   # target in left half
            else:
                left = mid + 1    # target in right half
        else:
            # right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1    # target in right half
            else:
                right = mid - 1   # target in left half
    
    return -1

# [4,5,6,7,0,1,2], target=0  →  4
```

---

### 🔹 Example 2 — Find First and Last Position
**Problem:** Find starting and ending position of target in sorted array.

```python
def search_range(nums, target):
    def find_boundary(is_first):
        left, right = 0, len(nums) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                result = mid
                if is_first:
                    right = mid - 1   # keep going left
                else:
                    left = mid + 1    # keep going right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    return [find_boundary(True), find_boundary(False)]

# [5,7,7,8,8,10], target=8  →  [3, 4]
```

---

## 7. 📅 Merge Intervals

### 🧩 What is it?
Sort intervals by start time, then merge overlapping ones by comparing end times.

### 🚨 Trigger Words
- "merge overlapping intervals"
- "meeting rooms / can attend all meetings"
- "insert interval"
- "find free time / gaps"
- anything with **[start, end]** pairs

### 📐 Template
```python
intervals.sort(key=lambda x: x[0])   # sort by start
merged = [intervals[0]]

for start, end in intervals[1:]:
    if start <= merged[-1][1]:        # overlapping
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])   # no overlap, add new
```

---

### 🔹 Example 1 — Merge Intervals
**Problem:** Given a list of intervals, merge all overlapping intervals.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

# [[1,3],[2,6],[8,10],[15,18]]  →  [[1,6],[8,10],[15,18]]
```

---

### 🔹 Example 2 — Meeting Rooms II (Min Rooms Needed)
**Problem:** Find the minimum number of meeting rooms needed.

```python
import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[0])
    heap = []   # min-heap of end times
    
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)   # reuse room
        else:
            heapq.heappush(heap, end)      # new room needed
    
    return len(heap)

# [[0,30],[5,10],[15,20]]  →  2
```

---

## 8. 📚 Monotonic Stack

### 🧩 What is it?
Stack that maintains elements in **increasing or decreasing order**.  
Used to find next/previous greater or smaller elements efficiently.

### 🚨 Trigger Words
- "next greater element"
- "daily temperatures / how many days until warmer"
- "largest rectangle in histogram"
- "trapping rain water"
- "stock span problem"

### 📐 Template — Next Greater Element
```python
stack = []   # stores indices
result = [-1] * len(nums)

for i, num in enumerate(nums):
    # pop elements smaller than current (current is their "next greater")
    while stack and nums[stack[-1]] < num:
        idx = stack.pop()
        result[idx] = num
    stack.append(i)
```

---

### 🔹 Example 1 — Daily Temperatures
**Problem:** For each day, find how many days until a warmer temperature. Return 0 if none.

```python
def daily_temperatures(temperatures):
    stack = []   # stores indices of unresolved days
    result = [0] * len(temperatures)
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day   # days to wait
        stack.append(i)
    
    return result

# [73,74,75,71,69,72,76,73]  →  [1,1,4,2,1,1,0,0]
```

---

### 🔹 Example 2 — Largest Rectangle in Histogram
**Problem:** Find the largest rectangle area in a histogram.

```python
def largest_rectangle(heights):
    stack = []   # monotonic increasing stack of indices
    max_area = 0
    heights.append(0)   # sentinel to flush stack at end
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    return max_area

# [2,1,5,6,2,3]  →  10
```

---

## 9. 🗺️ Matrix Traversal

### 🧩 What is it?
Traverse a 2D grid using **BFS** (level-by-level) or **DFS** (depth-first, mark visited).  
BFS → shortest path. DFS → connected regions / islands.

### 🚨 Trigger Words
- "number of islands"
- "flood fill"
- "shortest path in grid"
- "connected components in matrix"
- "0/1 matrix — distance to nearest 0"

### 📐 Template — DFS (Islands)
```python
def dfs(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if grid[r][c] != '1':
        return
    grid[r][c] = '#'   # mark visited
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        dfs(grid, r + dr, c + dc)
```

### 📐 Template — BFS (Shortest Path)
```python
from collections import deque

queue = deque([(start_r, start_c, 0)])   # row, col, distance
visited = set()
visited.add((start_r, start_c))

while queue:
    r, c, dist = queue.popleft()
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if valid(nr, nc) and (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append((nr, nc, dist + 1))
```

---

### 🔹 Example 1 — Number of Islands
**Problem:** Count connected components of '1's in a grid.

```python
def num_islands(grid):
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return
        if grid[r][c] != '1':
            return
        grid[r][c] = '#'   # sink the island
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    
    return count

# grid with 3 islands  →  3
```

---

### 🔹 Example 2 — Spiral Matrix (Traversal)
**Problem:** Return all elements of an m×n matrix in spiral order.

```python
def spiral_order(matrix):
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for c in range(left, right + 1):       # →
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):       # ↓
            result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):   # ←
                result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):   # ↑
                result.append(matrix[r][left])
            left += 1
    
    return result
```

---

## 10. 🔤 String Manipulation

### 🧩 What is it?
Direct string operations: **reversal, parsing, pattern matching, character counting**.  
Often combined with hash map or two pointers.

### 🚨 Trigger Words
- "reverse words in string"
- "check if valid parentheses"
- "longest common prefix"
- "roman to integer / integer to roman"
- "decode string (e.g., 3[abc])"
- "implement strStr / find needle in haystack"

---

### 🔹 Example 1 — Valid Parentheses
**Problem:** Check if string of brackets is valid (properly opened and closed).

```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:   # closing bracket
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)   # opening bracket
    
    return not stack   # valid if nothing left

# "()[]{}"  →  True
# "([)]"    →  False
```

---

### 🔹 Example 2 — Longest Common Prefix
**Problem:** Find the longest common prefix string among an array of strings.

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    
    prefix = strs[0]
    
    for s in strs[1:]:
        # shrink prefix until s starts with it
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

# ["flower","flow","flight"]  →  "fl"
# ["dog","racecar","car"]     →  ""
```

---

## ⚡ Quick Pattern Recognition Cheat Sheet

```
Problem mentions...              →  Think...
─────────────────────────────────────────────────────
sorted array + pair/target       →  Two Pointers
substring/subarray + constraint  →  Sliding Window
range sum / subarray sum = k     →  Prefix Sum
duplicates / counts / lookup     →  Hash Map
max/min subarray sum             →  Kadane's
sorted + find position           →  Binary Search
[start, end] intervals           →  Merge Intervals
next greater / temperatures      →  Monotonic Stack
2D grid / connected regions      →  DFS/BFS Matrix
brackets / parsing / reversal    →  String + Stack
```

---

## 📅 Daily Revision Checklist

- [ ] Can I name all 10 patterns from memory?
- [ ] Can I write the template for each without looking?
- [ ] For each pattern, can I name 2 problems that use it?
- [ ] Do I ask "which pattern?" BEFORE writing any code?

---

*Built for DE interview prep | Animesh Singh | iamanimesh.dev*
