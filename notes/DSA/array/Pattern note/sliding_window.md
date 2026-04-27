# Sliding Window — Complete Revision Notes
> 14 problems | Python | Easy → Hard | Full pattern coverage

---

## Quick Reference Table

| # | Problem | LC # | Difficulty | Pattern Type | Key Trick |
|---|---------|------|------------|--------------|-----------|
| 1 | Maximum Average Subarray I | 643 | Easy | Fixed window | Basic avg over window of size k |
| 2 | Best Time to Buy and Sell Stock | 121 | Easy | Sliding window on prices | Track min price seen so far |
| 3 | Max Vowels in a Substring | 1456 | Medium | Fixed window | Init first window, then slide |
| 4 | Permutation in String | 567 | Medium | Fixed window + freq | Same as anagrams — check if window matches |
| 5 | Longest Subarray of 1's After Deleting One Element | 1493 | Medium | Variable window | Allow 1 zero, find longest window |
| 6 | Minimum Size Subarray Sum | 209 | Medium | Variable window (shortest) | Shrink when sum >= target, track min length |
| 7 | Longest Substring Without Repeating Characters | 3 | Medium | Variable window + set | Shrink when duplicate enters window |
| 8 | Fruit Into Baskets | 904 | Medium | At most 2 distinct | Shrink when basket count > 2 |
| 9 | Max Consecutive Ones III | 1004 | Medium | Variable window | Track zero count; shrink when > k |
| 10 | Longest Repeating Character Replacement | 424 | Medium | Variable window + freq | `window_size - max_freq > k` → invalid |
| 11 | Subarray Product Less Than K | 713 | Medium | Variable window | Each valid right adds `(right-left+1)` subarrays |
| 12 | Number of Subarrays with Sum = Goal | 930 | Medium | atMost trick | `exactly(k)` = `atMost(k) - atMost(k-1)` |
| 13 | Find All Anagrams in a String | 438 | Medium | Fixed window + freq | Two freq arrays of size 26 |
| 14 | Minimum Window Substring | 76 | Hard | Variable window + freq map | Shrink only when all chars satisfied |

---
---

## EASY

---

## 1. Maximum Average Subarray I
**Pattern:** Fixed-size window — the simplest possible sliding window
**LC:** 643

**Problem:** Given array `nums` and integer `k`, find the subarray of length `k` with the maximum average.

```
Input:  nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75  # subarray [12,-5,-6,50] → avg = 51/4
```

**Approach:**
- Sum up the first window of size `k`
- Slide: add `nums[i]`, subtract `nums[i - k]`
- Track max sum, return `max_sum / k`

```python
def findMaxAverage(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum / k

findMaxAverage([1,12,-5,-6,50,3], 4)  # 12.75
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 2. Best Time to Buy and Sell Stock
**Pattern:** Sliding window on prices — track best buy point
**LC:** 121

**Problem:** Array `prices` where `prices[i]` is stock price on day `i`. Return max profit from one buy + one sell.

```
Input:  prices = [7,1,5,3,6,4]
Output: 5  # buy at 1, sell at 6
```

**Approach:**
- `left = buy day`, `right = sell day`
- If `prices[right] < prices[left]` → move left to right (found cheaper buy)
- Else → update max profit

```python
def maxProfit(prices):
    left = 0
    max_profit = 0

    for right in range(1, len(prices)):
        if prices[right] < prices[left]:
            left = right          # found a cheaper buy day
        else:
            profit = prices[right] - prices[left]
            max_profit = max(max_profit, profit)

    return max_profit

maxProfit([7,1,5,3,6,4])  # 5
```
⏱ Time: `O(n)` | Space: `O(1)`

---
---

## MEDIUM

---

## 3. Max Vowels in a Substring of Given Length
**Pattern:** Fixed-size window
**LC:** 1456

**Problem:** String `s`, integer `k`. Return the max vowels in any substring of length `k`.

```
Input:  s = "leetcode", k = 3
Output: 2  # "lee" and "eet" both have 2 vowels
```

**Approach:**
- Count vowels in first window of size `k`
- Slide: add `s[i]`, remove `s[i - k]`
- Early exit if `max_count == k`

```python
def maxVowels(s, k):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    current = sum(1 for c in s[:k] if c in vowels)
    max_count = current

    for i in range(k, len(s)):
        if s[i] in vowels:
            current += 1
        if s[i - k] in vowels:
            current -= 1
        max_count = max(max_count, current)
        if max_count == k:
            return k

    return max_count

maxVowels("leetcode", 3)  # 2
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 4. Permutation in String
**Pattern:** Fixed-size window + frequency matching
**LC:** 567

**Problem:** Strings `s1` and `s2`. Return `True` if any permutation of `s1` is a substring of `s2`.

```
Input:  s1 = "ab", s2 = "eidbaooo"
Output: True  # "ba" is a permutation of "ab"
```

**Approach:**
- Fixed window of size `len(s1)`, compare freq arrays at each step
- Same idea as Find All Anagrams — just return True/False

```python
def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False

    p_count = [0] * 26
    window  = [0] * 26
    k = len(s1)

    for c in s1:
        p_count[ord(c) - ord('a')] += 1

    for i in range(len(s2)):
        window[ord(s2[i]) - ord('a')] += 1
        if i >= k:
            window[ord(s2[i - k]) - ord('a')] -= 1
        if window == p_count:
            return True

    return False

checkInclusion("ab", "eidbaooo")  # True
```
⏱ Time: `O(n)` | Space: `O(1)` — fixed 26-char arrays

> 💡 Same pattern as Find All Anagrams (#13). If you can solve one, you can solve the other.

---

## 5. Longest Subarray of 1's After Deleting One Element
**Pattern:** Variable-size window — allow exactly 1 zero
**LC:** 1493

**Problem:** Binary array `nums`. Delete exactly one element. Return length of the longest subarray of 1s.

```
Input:  nums = [1,1,0,1]
Output: 3  # delete the 0 → [1,1,1]
```

**Approach:**
- Same as Max Consecutive Ones III with `k = 1`
- Answer is `window_size - 1` because one element must always be deleted

```python
def longestSubarray(nums):
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(len(nums)):
        if nums[right] == 0:
            zero_count += 1
        while zero_count > 1:
            if nums[left] == 0:
                zero_count -= 1
            left += 1
        max_len = max(max_len, right - left)  # -1 for the deleted element

    return max_len

longestSubarray([1,1,0,1])  # 3
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 `right - left` instead of `right - left + 1` because we must delete one element.

---

## 6. Minimum Size Subarray Sum
**Pattern:** Variable-size window — find **shortest** valid window
**LC:** 209

**Problem:** Array of positive integers `nums`, integer `target`. Return length of the shortest subarray with sum ≥ target.

```
Input:  nums = [2,3,1,2,4,3], target = 7
Output: 2  # [4,3]
```

**Approach:**
- Expand right, add to `current_sum`
- When `current_sum >= target` → valid! Shrink from left while still valid
- Track `min_len` every time window is valid

```python
def minSubArrayLen(target, nums):
    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum >= target:          # while valid → shrink
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return 0 if min_len == float('inf') else min_len

minSubArrayLen(7, [2,3,1,2,4,3])  # 2
```
⏱ Time: `O(n)` | Space: `O(1)`

> 💡 **Key difference:** for longest window shrink while **invalid**; for shortest window shrink while **valid**.

---

## 7. Longest Substring Without Repeating Characters
**Pattern:** Variable-size window + set for uniqueness
**LC:** 3

**Problem:** String `s`. Return length of the longest substring with no repeated characters.

```
Input:  s = "abcabcbb"
Output: 3  # "abc"
```

**Approach:**
- Use a `set` to track characters in current window
- When `s[right]` is already in set → shrink from left until duplicate is removed
- Track max window size

```python
def lengthOfLongestSubstring(s):
    left = 0
    char_set = set()
    max_len = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len

lengthOfLongestSubstring("abcabcbb")  # 3
```
⏱ Time: `O(n)` | Space: `O(min(n, 26))`

---

## 8. Fruit Into Baskets
**Pattern:** Variable-size window — at most 2 distinct elements
**LC:** 904

**Problem:** Array `fruits`, each value is a fruit type. You have 2 baskets (each holds 1 type). Return max fruits from a contiguous subarray using at most 2 types.

```
Input:  fruits = [1,2,3,2,2]
Output: 4  # [2,3,2,2] — types 2 and 3
```

**Approach:**
- Use a `dict` to count fruit types in window
- When `len(basket) > 2` → shrink from left until only 2 types remain

```python
def totalFruit(fruits):
    left = 0
    basket = {}
    max_fruits = 0

    for right in range(len(fruits)):
        basket[fruits[right]] = basket.get(fruits[right], 0) + 1

        while len(basket) > 2:
            basket[fruits[left]] -= 1
            if basket[fruits[left]] == 0:
                del basket[fruits[left]]
            left += 1

        max_fruits = max(max_fruits, right - left + 1)

    return max_fruits

totalFruit([1,2,3,2,2])  # 4
```
⏱ Time: `O(n)` | Space: `O(1)` — at most 3 keys in dict at any time

> 💡 **Generalizes to:** "Longest substring with at most K distinct characters" — just change `> 2` to `> k`.

---

## 9. Max Consecutive Ones III
**Pattern:** Variable-size window — flip at most k zeros
**LC:** 1004

**Problem:** Binary array `nums`, integer `k`. Return max consecutive 1s if you can flip at most `k` zeros.

```
Input:  nums = [1,1,0,1,1,0,1], k = 1
Output: 5
```

**Approach:**
- Track `zero_count` as you expand right
- When `zero_count > k` → shrink from left
- Answer is `max(right - left + 1)`

```python
left = 0
zero_count = 0
max_size = 0

for right in range(len(nums)):
    if nums[right] == 0:
        zero_count += 1
    while zero_count > k:
        if nums[left] == 0:
            zero_count -= 1
        left += 1
    max_size = max(max_size, right - left + 1)

print(max_size)  # 5
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 10. Longest Repeating Character Replacement
**Pattern:** Variable-size window + frequency map
**LC:** 424

**Problem:** String `s`, integer `k`. Replace at most `k` characters. Return length of longest uniform substring.

```
Input:  s = "AABABBA", k = 1
Output: 4  # Replace one 'B' → "AAAA"
```

**Approach:**
- Track `max_freq` (count of the most frequent char in window)
- Replacements needed = `window_size - max_freq`
- If > `k` → invalid, shrink left
- `max_freq` never decreases (optimization — we only care about bigger windows)

```python
left = 0
max_freq = 0
freq = {}
max_length = 0

for right in range(len(s)):
    char = s[right]
    freq[char] = freq.get(char, 0) + 1
    max_freq = max(max_freq, freq[char])

    while (right - left + 1) - max_freq > k:
        freq[s[left]] -= 1
        left += 1

    max_length = max(max_length, right - left + 1)

print(max_length)  # 4
```
⏱ Time: `O(n)` | Space: `O(26)` = `O(1)`

---

## 11. Subarray Product Less Than K
**Pattern:** Variable-size window — count subarrays
**LC:** 713

**Problem:** Positive integers `nums`, integer `k`. Count subarrays where product of all elements < k.

```
Input:  nums = [10,5,2,6], k = 100
Output: 8  # [10],[5],[2],[6],[10,5],[5,2],[2,6],[5,2,6]
```

**Approach:**
- Running product; multiply in `nums[right]`
- While `product >= k` → divide out `nums[left]`, shrink
- Every valid `right` contributes `(right - left + 1)` new subarrays ending at `right`

```python
def numSubarrayProductLessThanK(nums, k):
    if k <= 1:
        return 0
    left = 0
    product = 1
    count = 0

    for right in range(len(nums)):
        product *= nums[right]
        while product >= k:
            product //= nums[left]
            left += 1
        count += (right - left + 1)

    return count

numSubarrayProductLessThanK([10,5,2,6], 100)  # 8
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 12. Number of Subarrays with Sum = Goal
**Pattern:** Variable-size window — atMost trick
**LC:** 930

**Problem:** Binary array `nums`, integer `goal`. Count subarrays with sum **exactly** equal to `goal`.

```
Input:  nums = [1,0,1,0,1], goal = 2
Output: 4
```

**Approach:**
- Sliding window naturally counts `sum <= goal`
- `exactly(goal)` = `atMost(goal) - atMost(goal - 1)`

```python
def atMost(nums, goal):
    if goal < 0:
        return 0
    left = 0
    current_sum = 0
    count = 0
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > goal:
            current_sum -= nums[left]
            left += 1
        count += (right - left + 1)
    return count

def numSubarraysWithSum(nums, goal):
    return atMost(nums, goal) - atMost(nums, goal - 1)

numSubarraysWithSum([1,0,1,0,1], 2)  # 4
```
⏱ Time: `O(n)` | Space: `O(1)`

---

## 13. Find All Anagrams in a String
**Pattern:** Fixed-size window + frequency arrays
**LC:** 438

**Problem:** Strings `s` and `p`. Return all start indices where a substring of `s` is an anagram of `p`.

```
Input:  s = "cbaebabacd", p = "abc"
Output: [0, 6]
```

**Approach:**
- Build freq array for `p` (size 26)
- Slide window of `len(p)` over `s`; add right char, remove left char
- If freq arrays match → record start index

```python
def findAnagrams(s, p):
    res = []
    if len(p) > len(s):
        return res

    p_count = [0] * 26
    window  = [0] * 26
    k = len(p)

    for c in p:
        p_count[ord(c) - ord('a')] += 1

    for i in range(len(s)):
        window[ord(s[i]) - ord('a')] += 1
        if i >= k:
            window[ord(s[i - k]) - ord('a')] -= 1
        if window == p_count:
            res.append(i - k + 1)

    return res

findAnagrams("cbaebabacd", "abc")  # [0, 6]
```
⏱ Time: `O(n)` | Space: `O(1)` — fixed 26-char arrays

---
---

## HARD

---

## 14. Minimum Window Substring ⭐ Most Important
**Pattern:** Variable-size window + freq map + need counter
**LC:** 76

**Problem:** Strings `s` and `t`. Return the shortest substring of `s` containing every character of `t` (including duplicates).

```
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

**Approach:**
- `need` dict tracks how many of each char in `t` we still need
- `missing` = total characters still unsatisfied
- Expand right: if char is needed, decrement `missing`
- When `missing == 0` (window valid): record answer, shrink left to minimize

```python
def minWindow(s, t):
    from collections import Counter
    need = Counter(t)
    missing = len(t)
    best = ""
    left = 0

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1

        if missing == 0:                      # valid window found
            while need[s[left]] < 0:          # shrink from left
                need[s[left]] += 1
                left += 1
            window = s[left:right + 1]
            if not best or len(window) < len(best):
                best = window
            need[s[left]] += 1               # break validity to keep searching
            missing += 1
            left += 1

    return best

minWindow("ADOBECODEBANC", "ABC")  # "BANC"
```
⏱ Time: `O(n)` | Space: `O(|t|)`

> 💡 **Why this is the hardest:** you manage two separate states — the freq map AND a `missing` counter. The `missing` variable tells you when the window becomes valid/invalid without re-scanning the whole map.

---
---

## Cheat Sheet — Templates

### Template 1: Fixed-Size Window (window size = k)
```python
# Init first window
for i in range(k):
    # process s[i]

# Slide
for i in range(k, len(s)):
    # add s[i]       → right side coming in
    # remove s[i-k]  → left side going out
    # check condition
```

### Template 2: Variable-Size Window (find LONGEST)
```python
left = 0
for right in range(len(arr)):
    # expand: add arr[right] to state
    while <window is INVALID>:
        # shrink: remove arr[left]
        left += 1
    max_len = max(max_len, right - left + 1)
```

### Template 3: Variable-Size Window (find SHORTEST)
```python
left = 0
min_len = float('inf')
for right in range(len(arr)):
    # expand: add arr[right] to state
    while <window is VALID>:          # opposite of longest!
        min_len = min(min_len, right - left + 1)
        # shrink: remove arr[left]
        left += 1
```

### Template 4: Count Subarrays — atMost trick
```python
# For "exactly k" problems → exactly(k) = atMost(k) - atMost(k-1)

def atMost(arr, k):
    left, count = 0, 0
    for right in range(len(arr)):
        # add arr[right] to state
        while <state exceeds k>:
            # remove arr[left]
            left += 1
        count += (right - left + 1)   # all subarrays ending at right
    return count
```

---

## Pattern Recognition — What to Use When

| If the problem says... | Pattern to reach for |
|------------------------|----------------------|
| Subarray/substring of **fixed length k** | Fixed-size window |
| **Longest** subarray where condition holds | Variable window, shrink while **invalid** |
| **Shortest** subarray where condition holds | Variable window, shrink while **valid** |
| **Count** subarrays with sum/product **exactly k** | `atMost(k) - atMost(k-1)` |
| At most k zeros / k replacements / k distinct | Variable window, shrink when count **> k** |
| Anagram / permutation exists in string | Fixed window (size = pattern) + freq array[26] |
| Contains **all** characters of pattern t | Variable window + `missing` counter (LC 76) |
| At most **2 types** / 2 distinct values | Fruit Into Baskets pattern |

---

## Common Mistakes to Avoid

- **Off by one in fixed window:** remove `s[i - k]` not `s[i - k - 1]`
- **Longest vs Shortest confusion:** longest → shrink while **invalid** | shortest → shrink while **valid**
- **"Exactly k" trap:** almost never directly solvable — always think `atMost(k) - atMost(k-1)`
- **Minimum Window Substring:** `t` can have duplicate chars — freq map handles this, a set won't
- **Product problems:** always handle `k <= 1` edge case (every element's product >= 1)
- **Deleting one element (LC 1493):** answer is `right - left` not `right - left + 1`
