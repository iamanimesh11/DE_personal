# Two Pointers — Complete Revision Notes
> 8 problems | Python | Easy → Hard | Full pattern coverage

---

## Quick Reference Table

| # | Problem | LC # | Difficulty | Pattern Type | Key Trick |
|---|---------|------|------------|--------------|-----------|
| 1 | Valid Palindrome | 125 | Easy | Opposite ends | Skip non-alphanumeric, compare inward |
| 2 | Squares of a Sorted Array | 977 | Easy | Opposite ends | Largest square always at one of the ends |
| 3 | Move Zeroes | 283 | Easy | Slow + Fast (same direction) | Slow = next write pos; fast scans ahead |
| 4 | Two Sum II - Input Array Is Sorted | 167 | Medium | Opposite ends | Sorted → shrink search space by comparing sum |
| 5 | 3Sum | 15 | Medium | Fix one + opposite ends | Sort first; fix `i`, two-pointer on rest |
| 6 | Container With Most Water | 11 | Medium | Opposite ends | Move the shorter wall inward |
| 7 | Remove Duplicates from Sorted Array II | 80 | Medium | Slow + Fast (same direction) | Allow at most 2 → compare with `nums[slow - 2]` |
| 8 | Trapping Rain Water | 42 | Hard | Opposite ends + prefix max | Water at `i` = `min(max_left, max_right) - height[i]` |

---
---

## EASY

---

## 1. Valid Palindrome
**Pattern:** Opposite-ends — skip non-alphanumeric characters
**LC:** 125

**Problem:** String `s`. Return `True` if it reads the same forwards and backwards, ignoring non-alphanumeric characters and case.

```
Input:  s = "A man, a plan, a canal: Panama"
Output: True

Input:  s = "race a car"
Output: False
```

**Approach:**
- `left` starts at 0, `right` at end
- Skip non-alphanumeric on both sides
- Compare `s[left].lower()` and `s[right].lower()`
- Mismatch → return False; match → move both inward

```python
def isPalindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True

isPalindrome("A man, a plan, a canal: Panama")  # True
isPalindrome("race a car")                       # False
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 Always handle the skip-loop guard: `left < right` must appear in BOTH inner while conditions, otherwise you'll go out of bounds.

---

## 2. Squares of a Sorted Array
**Pattern:** Opposite-ends — fill result from back to front
**LC:** 977

**Problem:** Integer array `nums` sorted in non-decreasing order. Return array of squares sorted in non-decreasing order.

```
Input:  nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]

Input:  nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]
```

**Approach:**
- Largest square is always at one of the two ends (most negative or most positive)
- Use `left` and `right`; compare `abs(nums[left])` vs `abs(nums[right])`
- Place the larger square at the back of result array, move that pointer inward

```python
def sortedSquares(nums):
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    pos = n - 1                       # fill result from back

    while left <= right:
        left_sq  = nums[left]  ** 2
        right_sq = nums[right] ** 2

        if left_sq > right_sq:
            result[pos] = left_sq
            left += 1
        else:
            result[pos] = right_sq
            right -= 1

        pos -= 1

    return result

sortedSquares([-4,-1,0,3,10])  # [0,1,9,16,100]
```
⏱ Time: `O(n)` | Space: `O(n)` — output array

> 💡 **Why from the back?** We know the largest square, but not the smallest. It's easier to place the biggest value first.

---

## 3. Move Zeroes
**Pattern:** Slow + Fast pointers (same direction) — in-place overwrite
**LC:** 283

**Problem:** Integer array `nums`. Move all 0s to the end while maintaining the relative order of non-zero elements. Do it in-place.

```
Input:  nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Input:  nums = [0,0,1]
Output: [1,0,0]
```

**Approach:**
- `slow` = next position to write a non-zero value
- `fast` scans ahead; when it finds a non-zero, write it at `slow`, advance `slow`
- After loop, fill from `slow` to end with 0s

```python
def moveZeroes(nums):
    slow = 0

    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1

    while slow < len(nums):
        nums[slow] = 0
        slow += 1

    # nums modified in-place

moveZeroes([0,1,0,3,12])  # [1,3,12,0,0]
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 `slow` always points to where the NEXT valid element should go. Think of it as a write cursor.

---
---

## MEDIUM

---

## 4. Two Sum II — Input Array Is Sorted
**Pattern:** Opposite-ends — binary eliminate using sorted property
**LC:** 167

**Problem:** 1-indexed sorted array `numbers`. Find two numbers that add up to `target`. Return their 1-indexed positions.

```
Input:  numbers = [2,7,11,15], target = 9
Output: [1, 2]

Input:  numbers = [2,3,4], target = 6
Output: [1, 3]
```

**Approach:**
- `left = 0`, `right = len - 1`
- `sum < target` → need bigger → move `left` right
- `sum > target` → need smaller → move `right` left
- `sum == target` → found it

```python
def twoSum(numbers, target):
    left, right = 0, len(numbers) - 1

    while left < right:
        current = numbers[left] + numbers[right]

        if current == target:
            return [left + 1, right + 1]      # 1-indexed
        elif current < target:
            left += 1
        else:
            right -= 1

    return []

twoSum([2,7,11,15], 9)  # [1, 2]
twoSum([2,3,4], 6)      # [1, 3]
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 This only works because the array is SORTED. For unsorted → use HashMap (Two Sum I). Sorted = two pointers. Unsorted = HashMap.

---

## 5. 3Sum
**Pattern:** Fix one element + opposite-ends on the rest
**LC:** 15

**Problem:** Array `nums`. Return all unique triplets `[nums[i], nums[j], nums[k]]` such that they sum to 0.

```
Input:  nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]

Input:  nums = [0,0,0]
Output: [[0,0,0]]
```

**Approach:**
- Sort first (enables two pointers + easy dedup)
- Fix `i` from 0 to n-3; run two pointers on `nums[i+1:]`
- Skip duplicates for `i` (same value as previous)
- When sum found, skip duplicates for `left` and `right` too

```python
def threeSum(nums):
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if nums[i] > 0:                      # sorted → no triplet can sum to 0
            break
        if i > 0 and nums[i] == nums[i - 1]: # skip duplicate i
            continue

        left, right = i + 1, len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left]  == nums[left  + 1]: left  += 1
                while left < right and nums[right] == nums[right - 1]: right -= 1
                left  += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result

threeSum([-1,0,1,2,-1,-4])  # [[-1,-1,2],[-1,0,1]]
threeSum([0,0,0])            # [[0,0,0]]
```
⏱ Time: `O(n²)` | Space: `O(1)` excluding output

> 💡 **Most common mistake:** forgetting to skip duplicates after finding a valid triplet. Without that, `[0,0,0,0]` gives duplicate results.

---

## 6. Container With Most Water
**Pattern:** Opposite-ends — always move the shorter wall
**LC:** 11

**Problem:** Array `height` of length `n`. Each index is a vertical line of that height. Find two lines that together form a container holding the most water.

```
Input:  height = [1,8,6,2,5,4,8,3,7]
Output: 49

Input:  height = [1,1]
Output: 1
```

**Approach:**
- `left = 0`, `right = n - 1`
- Area = `min(height[left], height[right]) * (right - left)`
- Move the **shorter** wall inward (moving the taller wall can only decrease or maintain width, but can never increase the limiting height)
- Track `max_water`

```python
def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        h = min(height[left], height[right])
        max_water = max(max_water, h * (right - left))

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water

maxArea([1,8,6,2,5,4,8,3,7])  # 49
maxArea([1,1])                  # 1
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Why move the shorter wall?** Water is limited by the shorter side. Moving the taller wall can never give us more water (width decreases, height stays limited by the same shorter wall). Moving the shorter wall *might* find a taller one.

---

## 7. Remove Duplicates from Sorted Array II
**Pattern:** Slow + Fast pointers — allow at most k occurrences
**LC:** 80

**Problem:** Sorted array `nums` in-place. Allow each unique element at most **twice**. Return new length.

```
Input:  nums = [1,1,1,2,2,3]
Output: 5  →  nums = [1,1,2,2,3,_]

Input:  nums = [0,0,1,1,1,1,2,3,3]
Output: 7  →  nums = [0,0,1,1,2,3,3,_,_]
```

**Approach:**
- `slow` = next write position (starts at 2, first 2 elements always valid)
- `fast` scans from index 2 onward
- Write `nums[fast]` only if it's different from `nums[slow - 2]` (the element 2 spots back in the written portion)

```python
def removeDuplicates(nums):
    slow = 2                              # first 2 always kept

    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]: # not a third duplicate
            nums[slow] = nums[fast]
            slow += 1

    return slow

removeDuplicates([1,1,1,2,2,3])       # 5
removeDuplicates([0,0,1,1,1,1,2,3,3]) # 7
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Generalise to allow k duplicates:** replace `slow = 2` with `slow = k` and `nums[slow - 2]` with `nums[slow - k]`. Works for any k.

---
---

## HARD

---

## 8. Trapping Rain Water ⭐ Most Important
**Pattern:** Opposite-ends + running max from both sides
**LC:** 42

**Problem:** Array `height` representing an elevation map. Compute how much water it can trap after raining.

```
Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6

Input:  height = [4,2,0,3,2,5]
Output: 9
```

**Approach:**
- Water trapped at index `i` = `min(max_left, max_right) - height[i]`
- Brute force precomputes prefix/suffix max arrays → O(n) space
- Two-pointer version avoids that: process from the side with the **smaller max**
  - If `max_left <= max_right`: water at left is determined → add `max_left - height[left]`, move left
  - Else: water at right is determined → add `max_right - height[right]`, move right

```python
def trap(height):
    left, right = 0, len(height) - 1
    max_left, max_right = 0, 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            if height[left] >= max_left:
                max_left = height[left]           # new max, no water trapped
            else:
                water += max_left - height[left]  # water fills up to max_left
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                water += max_right - height[right]
            right -= 1

    return water

trap([0,1,0,2,1,0,1,3,2,1,2,1])  # 6
trap([4,2,0,3,2,5])               # 9
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Why process the smaller side?** The water level at any index is bounded by the MINIMUM of max_left and max_right. When `max_left <= max_right`, we know the left side's bound is `max_left` for certain — the right side can only be equal or taller. So we can safely compute water on the left. Same logic flipped for the right.

---
---

## Cheat Sheet — Templates

### Template 1: Opposite-Ends (Sorted Array / Symmetric)
```python
left, right = 0, len(arr) - 1

while left < right:
    if condition_met(arr[left], arr[right]):
        # record result
        left += 1
        right -= 1
    elif need_larger:
        left += 1
    else:
        right -= 1
```

### Template 2: Slow + Fast (Same Direction — In-Place Write)
```python
slow = 0   # write cursor

for fast in range(len(arr)):
    if arr[fast] meets condition:
        arr[slow] = arr[fast]
        slow += 1

# slow = new valid length
return slow
```

### Template 3: Fix One + Opposite-Ends (k-Sum pattern)
```python
arr.sort()

for i in range(len(arr) - 2):
    if i > 0 and arr[i] == arr[i - 1]:    # skip duplicate fixed element
        continue

    left, right = i + 1, len(arr) - 1

    while left < right:
        total = arr[i] + arr[left] + arr[right]
        if total == 0:
            # record, then skip duplicates
            ...
        elif total < 0:
            left += 1
        else:
            right -= 1
```

### Template 4: Opposite-Ends with Running Max (Trapping Water style)
```python
left, right = 0, len(arr) - 1
max_left = max_right = 0

while left < right:
    if arr[left] <= arr[right]:
        max_left = max(max_left, arr[left])
        # use max_left to compute answer at left
        left += 1
    else:
        max_right = max(max_right, arr[right])
        # use max_right to compute answer at right
        right -= 1
```

---

## Pattern Recognition — What to Use When

| If the problem says... | Pattern to reach for |
|------------------------|----------------------|
| Sorted array + find pair summing to target | Opposite-ends (Two Sum II style) |
| Palindrome / symmetric check | Opposite-ends, skip invalid chars |
| Squares / merge from largest end | Opposite-ends, fill result from back |
| Move / remove elements in-place | Slow + Fast (same direction) |
| Allow at most k duplicates in sorted array | Slow + Fast, compare `arr[slow - k]` |
| Triplets / k-sum | Sort + fix one + opposite-ends on rest |
| Maximize area / container | Opposite-ends, move the smaller side |
| Trapped water / min of two maxes | Opposite-ends + running max both sides |

---

## Common Mistakes to Avoid

- **3Sum duplicates:** skip dupes for `i` AND for `left`/`right` after recording a triplet — forgetting either causes duplicates in output
- **Valid Palindrome:** always guard inner skip-loops with `left < right`, or you'll compare out-of-bounds indices
- **Squares of Sorted Array:** fill `result` from the **back**, not front — you know the largest square, not the smallest
- **Container With Most Water:** always move the **shorter** wall; moving the taller one can never improve the answer
- **Remove Duplicates II generalisation:** `slow` starts at `k` (not 0), comparison is `nums[slow - k]` — `k=1` gives LC 26, `k=2` gives LC 80
- **Trapping Rain Water:** water = `min(max_left, max_right) - height[i]` only when that value is positive — the two-pointer approach handles this automatically via the running max logic
- **Two Sum II vs Two Sum I:** sorted → two pointers; unsorted → HashMap. Don't mix them up.
