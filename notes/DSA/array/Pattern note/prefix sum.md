# Prefix Sum — Complete Revision Notes
> 9 problems | Python | Easy → Medium | Full pattern coverage

---

## What is Prefix Sum?

A **prefix sum array** stores the cumulative sum up to each index.

```
nums   =  [1,  2,  3,  4,  5]
prefix =  [0,  1,  3,  6, 10, 15]   ← prefix[i] = sum of nums[0..i-1]
```

**Core formula:**
```
prefix[i] = prefix[i-1] + nums[i-1]

Sum of subarray nums[l..r] = prefix[r+1] - prefix[l]
```

> 💡 **Why add a leading 0?** So you can query any range `[l, r]` without an `if l == 0` edge case.

---

## Quick Reference Table

| # | Problem | LC # | Difficulty | Key Idea |
|---|---------|------|------------|----------|
| 1 | Running Sum of 1D Array | 1480 | Easy | Build prefix in-place |
| 2 | Find Pivot Index | 724 | Easy | `left_sum == total - left_sum - nums[i]` |
| 3 | Range Sum Query - Immutable | 303 | Easy | Precompute once, answer in O(1) |
| 4 | Subarray Sum Equals K | 560 | Medium | `prefix[j] - prefix[i] == k` → use hashmap |
| 5 | Product of Array Except Self | 238 | Medium | Prefix products + suffix products |
| 6 | Number of Ways to Split Array | 2270 | Medium | Left prefix vs right suffix comparison |
| 7 | Contiguous Array (equal 0s and 1s) | 525 | Medium | Map 0→-1, find longest subarray with sum 0 |
| 8 | Minimum Average Difference | 2256 | Medium | Prefix sum for left avg, suffix for right avg |
| 9 | Sum of Absolute Differences in Sorted Array | 1685 | Medium | Use prefix to compute left/right contributions |

---
---

## EASY

---

## 1. Running Sum of 1D Array
**Pattern:** Basic prefix sum build
**LC:** 1480

**Problem:** Given array `nums`, return running sum where `result[i] = sum(nums[0..i])`.

```
Input:  nums = [1, 2, 3, 4]
Output:        [1, 3, 6, 10]
```

**Approach:**
- Each element becomes itself + the element before it
- Can be done in-place

```python
def runningSum(nums):
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]
    return nums

runningSum([1, 2, 3, 4])  # [1, 3, 6, 10]
```
⏱ Time: `O(n)` | Space: `O(1)` in-place

---

## 2. Find Pivot Index
**Pattern:** Left sum vs right sum using prefix
**LC:** 724

**Problem:** Return the index where the sum of elements to its left equals the sum to its right. Return `-1` if none.

```
Input:  nums = [1, 7, 3, 6, 5, 6]
Output: 3  # left_sum = 1+7+3 = 11, right_sum = 5+6 = 11
```

**Approach:**
- `total = sum(nums)`
- For each index: `right_sum = total - left_sum - nums[i]`
- If `left_sum == right_sum` → found pivot

```python
def pivotIndex(nums):
    total = sum(nums)
    left_sum = 0

    for i in range(len(nums)):
        right_sum = total - left_sum - nums[i]
        if left_sum == right_sum:
            return i
        left_sum += nums[i]

    return -1

pivotIndex([1, 7, 3, 6, 5, 6])  # 3
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 No need to build a prefix array — just track `left_sum` as you go and derive `right_sum` from `total`.

---

## 3. Range Sum Query - Immutable
**Pattern:** Classic prefix sum — precompute once, query many times
**LC:** 303

**Problem:** Given array `nums`, implement `sumRange(left, right)` that returns sum of elements between indices `left` and `right` inclusive. Will be called multiple times.

```
Input:  nums = [-2, 0, 3, -5, 2, -1]
        sumRange(0, 2) → 1    # -2+0+3
        sumRange(2, 5) → -1   # 3-5+2-1
```

**Approach:**
- Precompute prefix array where `prefix[i]` = sum of first `i` elements
- Any range query: `prefix[right+1] - prefix[left]`

```python
class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]

obj = NumArray([-2, 0, 3, -5, 2, -1])
obj.sumRange(0, 2)   # 1
obj.sumRange(2, 5)   # -1
```
⏱ Build: `O(n)` | Query: `O(1)` | Space: `O(n)`

> 💡 **Why this pattern matters:** precompute once, answer infinite queries in O(1). This is the core promise of prefix sum.

---
---

## MEDIUM

---

## 4. Subarray Sum Equals K ⭐ Most Important
**Pattern:** Prefix sum + hashmap
**LC:** 560

**Problem:** Array `nums`, integer `k`. Return the number of subarrays whose sum equals `k`.

```
Input:  nums = [1, 1, 1], k = 2
Output: 2  # [1,1] at indices (0,1) and (1,2)
```

**Core Insight:**
```
sum(i..j) = prefix[j] - prefix[i-1] = k
→ we need: prefix[i-1] = prefix[j] - k
```
So at each step, check how many previous prefix sums equal `current_sum - k`.

**Approach:**
- Use a hashmap `{prefix_sum: count}`, initialized with `{0: 1}` (empty prefix)
- At each element, update `current_sum` then look up `current_sum - k`

```python
def subarraySum(nums, k):
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1       # empty prefix (sum = 0 seen once)
    current_sum = 0
    count = 0

    for num in nums:
        current_sum += num
        count += prefix_count[current_sum - k]   # how many valid left boundaries exist
        prefix_count[current_sum] += 1

    return count

subarraySum([1, 1, 1], 2)  # 2
```
⏱ Time: `O(n)` | Space: `O(n)`

> 💡 **Why `{0: 1}` in the hashmap?** If the entire prefix from index 0 to j sums to k, `current_sum - k = 0` needs to be in the map. Seeding with `{0: 1}` handles this cleanly.
>
> ⚠️ **Can't use sliding window here** because `nums` can have negative numbers. Prefix sum + hashmap is the only reliable approach.

---

## 5. Product of Array Except Self
**Pattern:** Prefix products + suffix products
**LC:** 238

**Problem:** Return array `output` where `output[i]` is the product of all elements except `nums[i]`. No division allowed.

```
Input:  nums = [1, 2, 3, 4]
Output:        [24, 12, 8, 6]
```

**Approach:**
- First pass (left to right): `prefix[i]` = product of all elements to the LEFT of `i`
- Second pass (right to left): multiply in suffix product (product of all elements to the RIGHT)
- Combine in-place — no extra array needed

```python
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n

    # Pass 1: result[i] = product of everything to the LEFT
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply in product of everything to the RIGHT
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result

productExceptSelf([1, 2, 3, 4])  # [24, 12, 8, 6]
```
⏱ Time: `O(n)` | Space: `O(1)` extra (output array doesn't count)

> 💡 Trace through example:
> ```
> After pass 1: result = [1,  1,  2,  6]   ← left products
> After pass 2: result = [24, 12, 8,  6]   ← multiplied by right products
> ```

---

## 6. Number of Ways to Split Array
**Pattern:** Prefix sum for left/right comparison
**LC:** 2270

**Problem:** Array `nums`. Count valid splits at index `i` where sum of `nums[0..i]` ≥ sum of `nums[i+1..n-1]`.

```
Input:  nums = [10, 4, -8, 7]
Output: 2  # splits at i=0 and i=2 are valid
```

**Approach:**
- Precompute `total` sum
- Iterate, maintaining `left_sum`; derive `right_sum = total - left_sum`
- Last index is never a valid split (nothing on the right)

```python
def waysToSplitArray(nums):
    total = sum(nums)
    left_sum = 0
    count = 0

    for i in range(len(nums) - 1):    # don't include last index
        left_sum += nums[i]
        right_sum = total - left_sum
        if left_sum >= right_sum:
            count += 1

    return count

waysToSplitArray([10, 4, -8, 7])  # 2
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 7. Contiguous Array (Equal 0s and 1s)
**Pattern:** Prefix sum + hashmap — longest subarray with sum 0
**LC:** 525

**Problem:** Binary array `nums`. Return length of the longest subarray with equal number of 0s and 1s.

```
Input:  nums = [0, 1, 0, 1, 1, 0]
Output: 4  # [0,1,0,1] or [1,0,1,1,0] — wait, [0,1,0,1] = indices 0-3
```

**Core Trick — map 0 → -1:**
- Replace every `0` with `-1`; now "equal 0s and 1s" becomes "subarray sum = 0"
- Find longest subarray with sum 0 using prefix sum + hashmap

```python
def findMaxLength(nums):
    prefix_index = {0: -1}    # prefix_sum: first index it appeared
    current_sum = 0
    max_len = 0

    for i, num in enumerate(nums):
        current_sum += 1 if num == 1 else -1

        if current_sum in prefix_index:
            max_len = max(max_len, i - prefix_index[current_sum])
        else:
            prefix_index[current_sum] = i   # only store FIRST occurrence

    return max_len

findMaxLength([0, 1, 0, 1, 1, 0])  # 4
```
⏱ Time: `O(n)` | Space: `O(n)`

> 💡 **Why only store first occurrence?** We want the LONGEST subarray, so we want the earliest left boundary. Never overwrite an existing entry in the map.
>
> 💡 **Why `{0: -1}`?** If `current_sum` returns to 0 at index `i`, the entire subarray `0..i` is valid. Length = `i - (-1) = i + 1`.

---

## 8. Minimum Average Difference
**Pattern:** Prefix sum for left avg, suffix for right avg
**LC:** 2256

**Problem:** Array `nums`. For each index `i`, compute `|avg(nums[0..i]) - avg(nums[i+1..n-1])|`. Return the index with minimum average difference (leftmost if tie).

```
Input:  nums = [2, 5, 3, 9, 5, 3]
Output: 3
```

**Approach:**
- Build prefix sum array
- At each `i`: `left_avg = prefix[i+1] // (i+1)`, `right_avg = (total - prefix[i+1]) // (n-i-1)`
- Handle edge case: when `i == n-1`, right avg = 0

```python
def minimumAverageDifference(nums):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    total = prefix[n]
    min_diff = float('inf')
    result = 0

    for i in range(n):
        left_avg = prefix[i + 1] // (i + 1)
        right_sum = total - prefix[i + 1]
        right_avg = right_sum // (n - i - 1) if i < n - 1 else 0
        diff = abs(left_avg - right_avg)
        if diff < min_diff:
            min_diff = diff
            result = i

    return result

minimumAverageDifference([2, 5, 3, 9, 5, 3])  # 3
```
⏱ Time: `O(n)` | Space: `O(n)`

---

## 9. Sum of Absolute Differences in Sorted Array
**Pattern:** Prefix sum for left and right contributions
**LC:** 1685

**Problem:** Sorted array `nums`. Return array `result` where `result[i]` = sum of absolute differences between `nums[i]` and all other elements.

```
Input:  nums = [2, 3, 5]
Output:        [4, 3, 5]
# result[0] = |2-3| + |2-5| = 1+3 = 4
```

**Core Insight:**
- Elements to the **left** of `i` are smaller → contribution = `nums[i] * i - prefix[i]`
- Elements to the **right** of `i` are larger → contribution = `(suffix_sum) - nums[i] * (n - i - 1)`

```python
def getSumAbsoluteDifferences(nums):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    result = []
    for i in range(n):
        left_contribution  = nums[i] * i - prefix[i]
        right_contribution = (prefix[n] - prefix[i + 1]) - nums[i] * (n - i - 1)
        result.append(left_contribution + right_contribution)

    return result

getSumAbsoluteDifferences([2, 3, 5])  # [4, 3, 5]
```
⏱ Time: `O(n)` | Space: `O(n)`

> 💡 **Why this works (sorted array):** since array is sorted, all left elements ≤ `nums[i]` and all right elements ≥ `nums[i]`, so we don't need `abs()` — the signs are guaranteed.

---
---

## Cheat Sheet — Templates

### Template 1: Build Prefix Sum Array
```python
prefix = [0] * (len(nums) + 1)
for i in range(len(nums)):
    prefix[i + 1] = prefix[i] + nums[i]

# Range sum [l, r] (0-indexed, inclusive):
range_sum = prefix[r + 1] - prefix[l]
```

### Template 2: Prefix Sum + Hashmap (count subarrays)
```python
# For "count subarrays with sum = k"
from collections import defaultdict
seen = defaultdict(int)
seen[0] = 1         # ← always seed with {0: 1}
current_sum = 0
count = 0

for num in nums:
    current_sum += num
    count += seen[current_sum - k]
    seen[current_sum] += 1
```

### Template 3: Prefix Sum + Hashmap (longest subarray)
```python
# For "longest subarray with sum = 0" or "equal 0s and 1s"
first_seen = {0: -1}    # ← seed with {0: -1} (before array starts)
current_sum = 0
max_len = 0

for i, num in enumerate(nums):
    current_sum += num
    if current_sum in first_seen:
        max_len = max(max_len, i - first_seen[current_sum])
    else:
        first_seen[current_sum] = i   # only store FIRST occurrence!
```

### Template 4: Left/Right Split
```python
# For "compare left half vs right half" problems
total = sum(nums)
left_sum = 0

for i in range(len(nums) - 1):   # exclude last index
    left_sum += nums[i]
    right_sum = total - left_sum
    # compare left_sum and right_sum
```

---

## Pattern Recognition Guide

| If the problem says... | Use this |
|------------------------|----------|
| Running cumulative sum | Build prefix in-place (LC 1480) |
| Left sum == right sum at some index | Track `left_sum`, derive `right_sum = total - left_sum - nums[i]` |
| Multiple range sum queries on static array | Precompute prefix, answer each in O(1) |
| Count subarrays with **sum = k** (may have negatives) | Prefix + hashmap, seed `{0:1}` |
| **Longest** subarray with sum = 0 or equal 0s/1s | Prefix + hashmap, seed `{0:-1}`, store first occurrence only |
| Product of array except self | Two-pass: prefix products then suffix products |
| Left avg vs right avg at each split | Prefix sum array + iterate |
| Absolute differences in sorted array | Prefix for left/right contribution formula |

---

## Key Distinctions to Remember

```
COUNT subarrays  →  seen[0] = 1   (count empty prefix as 1 way)
LONGEST subarray →  seen[0] = -1  (empty prefix starts at index -1)

Sliding Window works when all nums > 0 (no negatives)
Prefix + Hashmap works even with negative numbers ← use this for sum = k
```

---

## How Prefix Sum, Sliding Window & HashMap Relate

```
┌─────────────────────────────────────────────────────────┐
│              Subarray / Substring Problems               │
├───────────────────┬─────────────────────────────────────┤
│  All nums > 0     │  Can have negatives / any values    │
│  (or fixed size)  │                                     │
│                   │                                     │
│  Sliding Window   │  Prefix Sum + HashMap               │
│  O(n), O(1)       │  O(n), O(n)                        │
└───────────────────┴─────────────────────────────────────┘
```

Both solve subarray problems — know when to reach for which.