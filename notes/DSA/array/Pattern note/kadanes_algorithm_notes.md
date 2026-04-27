# Kadane's Algorithm — Complete Revision Notes
> 6 problems | Python | Easy → Hard | Full pattern coverage

---

## What is Kadane's Algorithm?

Kadane's is a dynamic programming technique to find the **maximum sum subarray** in O(n) time.

**Core Idea:** At every index, you make one decision:
```
extend the current subarray  OR  start fresh from here
current = max(nums[i], current + nums[i])
```

If adding the current element makes things worse than starting over → restart.

```
nums    =  [-2,  1, -3,  4, -1,  2,  1, -5,  4]

current =  [-2,  1, -2,  4,  3,  5,  6,  1,  5]
             ↑   ↑        ↑                       
           restart restart restart                

max_sum = 6  (subarray [4,-1,2,1])
```

---

## Quick Reference Table

| # | Problem | LC # | Difficulty | Key Twist |
|---|---------|------|------------|-----------|
| 1 | Maximum Subarray | 53 | Easy | Pure Kadane's — the foundation |
| 2 | Maximum Product Subarray | 152 | Medium | Track both max AND min (negatives flip sign) |
| 3 | Best Time to Buy & Sell Stock | 121 | Medium | Kadane's on daily profit differences |
| 4 | Maximum Sum Circular Subarray | 918 | Medium | `max(kadane, total - min_subarray)` |
| 5 | Maximum Subarray Sum After One Deletion | 1186 | Medium | DP with two states: deleted or not yet |
| 6 | Maximum Absolute Sum of Any Subarray | 1749 | Medium | `max_subarray_sum - min_subarray_sum` |

---
---

## EASY

---

## 1. Maximum Subarray ⭐ The Foundation
**Pattern:** Pure Kadane's
**LC:** 53

**Problem:** Given array `nums`, return the largest sum of any contiguous subarray.

```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6  # subarray [4, -1, 2, 1]
```

**Approach:**
- `current` = best sum ending at current index
- `max_sum` = best seen so far
- At each step: extend or restart

```python
def maxSubArray(nums):
    current = nums[0]
    max_sum = nums[0]

    for i in range(1, len(nums)):
        current = max(nums[i], current + nums[i])   # extend or restart
        max_sum = max(max_sum, current)

    return max_sum

maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])  # 6
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Why start with `nums[0]` not `0`?** All elements could be negative. `0` would be wrong (empty subarray isn't allowed). Always initialize with the first element.

---
---

## MEDIUM

---

## 2. Maximum Product Subarray
**Pattern:** Kadane's — track max AND min simultaneously
**LC:** 152

**Problem:** Given array `nums`, return the largest product of any contiguous subarray.

```
Input:  nums = [2, 3, -2, 4]
Output: 6  # [2, 3]

Input:  nums = [-2, 0, -1]
Output: 0
```

**Core Insight — Why track the minimum too?**
```
A negative × negative = positive
So today's minimum could become tomorrow's maximum if we hit a negative number.
```

**Approach:**
- Track `max_prod` and `min_prod` at each step
- When `nums[i]` is negative → swap max and min before multiplying
- Reset if `nums[i]` alone beats any product (handles zeros)

```python
def maxProduct(nums):
    max_prod = nums[0]
    min_prod = nums[0]
    result   = nums[0]

    for i in range(1, len(nums)):
        # If current num is negative, swap — negative flips max↔min
        if nums[i] < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(nums[i], max_prod * nums[i])
        min_prod = min(nums[i], min_prod * nums[i])

        result = max(result, max_prod)

    return result

maxProduct([2, 3, -2, 4])   # 6
maxProduct([-2, 0, -1])     # 0
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **The swap trick:** when you see a negative number, the current max becomes the future min and vice versa. Swapping before multiplying captures this cleanly.
>
> ⚠️ **Zeros reset everything** — `max(nums[i], max_prod * nums[i])` naturally handles this because `nums[i]` alone restarts.

---

## 3. Best Time to Buy and Sell Stock — Kadane's Lens
**Pattern:** Kadane's on difference array
**LC:** 121

**Problem:** Array `prices`. Return maximum profit from one buy + one sell (buy before sell).

```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5  # buy at 1, sell at 6
```

**The Kadane's Connection:**
- Build a difference array: `diff[i] = prices[i] - prices[i-1]`
- Finding max profit = finding max subarray sum of `diff`
- This IS Kadane's algorithm!

```
prices = [7,  1,  5,  3,  6,  4]
diff   =    [-6,  4, -2,  3, -2]
                  ↑_______↑
         max subarray of diff = 4 + (-2) + 3 = 5  ✓
```

```python
# Standard approach (tracking min price):
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit

# Kadane's approach (on diff array — same result):
def maxProfitKadane(prices):
    current = 0
    max_profit = 0

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        current = max(diff, current + diff)
        max_profit = max(max_profit, current)

    return max_profit

maxProfit([7, 1, 5, 3, 6, 4])        # 5
maxProfitKadane([7, 1, 5, 3, 6, 4])  # 5
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Why revisit this?** The "min price so far" approach and Kadane's on differences are mathematically identical. Seeing both builds intuition for recognizing Kadane's in disguise.

---

## 4. Maximum Sum Circular Subarray
**Pattern:** Kadane's + total - min subarray trick
**LC:** 918

**Problem:** Given a **circular** array `nums`, return the max subarray sum. The subarray can wrap around the end.

```
Input:  nums = [5, -3, 5]
Output: 10  # [5, 5] wrapping around

Input:  nums = [-3, -2, -3]
Output: -2  # all negative — must take one element
```

**Core Insight — Two cases:**
```
Case 1: Max subarray does NOT wrap  →  normal Kadane's
Case 2: Max subarray DOES wrap      →  total_sum - min_subarray_sum
```

```
[5, -3, 5]  total = 7
Case 1 (no wrap):  Kadane = 5
Case 2 (wrap):     7 - (-3) = 10  ✓
Answer = max(5, 10) = 10
```

**Edge case:** If all elements are negative, `min_subarray = total`, so case 2 = 0 (empty). In this case, answer is just case 1.

```python
def maxSubarraySumCircular(nums):
    # Case 1: normal Kadane's (no wrap)
    max_sum = nums[0]
    cur_max = nums[0]

    # Case 2: total - min subarray (wrap)
    min_sum = nums[0]
    cur_min = nums[0]

    total = nums[0]

    for i in range(1, len(nums)):
        cur_max = max(nums[i], cur_max + nums[i])
        max_sum = max(max_sum, cur_max)

        cur_min = min(nums[i], cur_min + nums[i])
        min_sum = min(min_sum, cur_min)

        total += nums[i]

    # If all negative → max_sum is the (least negative) answer
    if max_sum < 0:
        return max_sum

    return max(max_sum, total - min_sum)

maxSubarraySumCircular([5, -3, 5])      # 10
maxSubarraySumCircular([-3, -2, -3])    # -2
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Why does `total - min_sum` give the wrapping answer?**
> The wrapped subarray = everything EXCEPT some middle subarray.
> To maximize the wrapped portion → minimize what's excluded → find the minimum subarray.

---

## 5. Maximum Subarray Sum After One Deletion
**Pattern:** Kadane's with two DP states
**LC:** 1186

**Problem:** Given array `nums`, you may delete at most one element. Return max subarray sum with at least one element remaining.

```
Input:  nums = [1, -2, 0, 3]
Output: 4  # delete -2 → [1, 0, 3] = 4
```

**Approach — Two DP arrays:**
- `no_del[i]` = max subarray sum ending at `i` with **no deletion used**
- `one_del[i]` = max subarray sum ending at `i` with **one deletion used**

```
Transitions:
no_del[i]  = max(nums[i], no_del[i-1] + nums[i])    # extend or restart
one_del[i] = max(no_del[i-1], one_del[i-1] + nums[i])
              ↑ delete nums[i]   ↑ deletion already used, just extend
```

```python
def maximumSum(nums):
    no_del  = nums[0]
    one_del = 0           # deleting nums[0] → empty, but we need ≥1 element
    result  = nums[0]

    for i in range(1, len(nums)):
        one_del = max(no_del, one_del + nums[i])   # delete curr OR extend with prev deletion
        no_del  = max(nums[i], no_del + nums[i])   # normal Kadane's
        result  = max(result, no_del, one_del)

    return result

maximumSum([1, -2, 0, 3])   # 4
maximumSum([-1, -1, -1, -1])  # -1
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Order matters:** update `one_del` BEFORE `no_del` so `no_del` still refers to the previous step when computing `one_del`.

---

## 6. Maximum Absolute Sum of Any Subarray
**Pattern:** Kadane's max + Kadane's min
**LC:** 1749

**Problem:** Array `nums`. Return the maximum absolute sum of any subarray (can be negative subarray with large magnitude).

```
Input:  nums = [1, -3, 2, 3, -4]
Output: 5  # subarray [2,3] has sum 5 OR [-3,2,3,-4] = -2, abs = 2
           # actually max subarray = 5, min subarray = -5 → answer = 5
```

**Core Insight:**
```
max |sum| = max(max_subarray_sum, |min_subarray_sum|)
          = max(max_subarray_sum, -min_subarray_sum)
```

Run Kadane's twice — once for max, once for min.

```python
def maxAbsoluteSum(nums):
    # Kadane's for maximum subarray sum
    max_sum = cur_max = nums[0]
    # Kadane's for minimum subarray sum
    min_sum = cur_min = nums[0]

    for i in range(1, len(nums)):
        cur_max = max(nums[i], cur_max + nums[i])
        max_sum = max(max_sum, cur_max)

        cur_min = min(nums[i], cur_min + nums[i])
        min_sum = min(min_sum, cur_min)

    return max(max_sum, -min_sum)

maxAbsoluteSum([1, -3, 2, 3, -4])   # 5
maxAbsoluteSum([2, -5, 1, -4, 3, -2])  # 8
```
⏱ Time: `O(n)` | Space: `O(1)`

---
---

## Cheat Sheet — Templates

### Template 1: Classic Kadane's (max subarray sum)
```python
current = nums[0]
max_sum = nums[0]

for i in range(1, len(nums)):
    current = max(nums[i], current + nums[i])   # extend or restart
    max_sum = max(max_sum, current)
```

### Template 2: Kadane's — track max AND min (product variant)
```python
max_val = min_val = result = nums[0]

for i in range(1, len(nums)):
    if nums[i] < 0:
        max_val, min_val = min_val, max_val    # swap on negative!
    max_val = max(nums[i], max_val * nums[i])
    min_val = min(nums[i], min_val * nums[i])
    result  = max(result, max_val)
```

### Template 3: Circular Subarray
```python
# Run both max and min Kadane's in one pass
# Answer = max(max_kadane, total - min_kadane)
# Edge case: if all negative → return max_kadane only
```

### Template 4: Kadane's with a State (one deletion allowed)
```python
no_del  = nums[0]
one_del = 0

for i in range(1, len(nums)):
    one_del = max(no_del, one_del + nums[i])   # update one_del FIRST
    no_del  = max(nums[i], no_del + nums[i])
```

---

## Pattern Recognition Guide

| If the problem says... | Reach for |
|------------------------|-----------|
| Max sum contiguous subarray | Classic Kadane's |
| Max **product** subarray | Kadane's tracking max AND min |
| One buy + one sell stock | Min-so-far OR Kadane's on `diff` array |
| Circular array, subarray can wrap | `max(kadane, total - min_subarray)` |
| Max sum after deleting one element | Two-state Kadane's (`no_del`, `one_del`) |
| Max **absolute** sum of any subarray | `max(max_kadane, -min_kadane)` |

---

## Common Mistakes to Avoid

- **Initializing with `0` instead of `nums[0]`** → wrong when all elements are negative (empty subarray not allowed)
- **Forgetting to swap before multiplying** in the product variant → gives wrong answer on negative inputs
- **Circular problem — all-negative edge case:** `total - min_sum = 0` (empty subarray), which is invalid → check `if max_sum < 0: return max_sum`
- **One-deletion problem — update order:** always update `one_del` before `no_del` in the loop
- **Kadane's finds sum, not indices** — if you need the actual subarray, track `start`, `end`, `temp_start` separately

---

## The Big Picture — How Kadane's Fits In

```
┌──────────────────────────────────────────────────────────────┐
│                    Subarray Problems                          │
├─────────────────┬────────────────────┬───────────────────────┤
│  Count/Exists   │  Max/Min Sum        │  Product              │
│                 │                    │                        │
│  Prefix Sum     │  Kadane's          │  Kadane's              │
│  + HashMap      │  O(n) O(1)         │  track max+min        │
│                 │                    │                        │
│  "how many      │  "largest sum"     │  "largest product"     │
│   subarrays     │  "circular max"    │                        │
│   sum to k"     │  "after deletion"  │                        │
└─────────────────┴────────────────────┴───────────────────────┘

Sliding Window → when all nums > 0 and window constraint is given
Prefix Sum     → when you need count, or range queries
Kadane's       → when you need max/min of any subarray, no constraint on size
```
