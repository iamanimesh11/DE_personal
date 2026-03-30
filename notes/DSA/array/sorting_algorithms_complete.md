# 🗂️ Sorting Algorithms — Complete DSA Reference
> **Same array everywhere:** `[64, 34, 25, 12, 22, 11, 90]` → `[11, 12, 22, 25, 34, 64, 90]`  
> Every algo: intuition → diagram → code → trace → use/don't use

---

## ⚡ PICK YOUR SORT IN 10 SECONDS

```
What's your data?
│
├── Integers, small known range (0–1000)?  ──────────────► COUNTING SORT
├── Integers, large range but few digits?  ──────────────► RADIX SORT
├── Floats, uniformly distributed?  ──────────────────────► BUCKET SORT
│
└── General data (strings, objects, mixed)?
    │
    ├── n < 20  OR  nearly sorted?  ──────────────────────► INSERTION SORT
    ├── Need STABLE sort?  ─────────────────────────────────► MERGE SORT
    ├── Need IN-PLACE + guaranteed O(n log n)?  ────────────► HEAP SORT
    ├── General large array, memory tight?  ───────────────► QUICK SORT
    └── Just Python?  ─────────────────────────────────────► sorted() ← Tim Sort
```

---

## 🧠 NAME DECODER

| Name | What it literally means |
|---|---|
| **Bubble** | Biggest element *bubbles up* to the end each pass |
| **Selection** | You *select* the min from unsorted each time |
| **Insertion** | You *insert* each element into the sorted left portion |
| **Merge** | Key operation is *merging* two sorted halves |
| **Quick** | Named for *speed* — pivot partitions in-place, no merging |
| **Heap** | Uses a *heap* tree — root = max always, extract repeatedly |
| **Shell** | Named after Donald *Shell* — insertion sort with a shrinking gap |
| **Counting** | Literally *counts* how many times each value appears |
| **Radix** | *Radix* = Latin for base — sorts digit by digit (base-10) |
| **Bucket** | Throws elements into value-range *buckets*, sorts each bucket |
| **Tim** | Named after *Tim Peters* who wrote it for Python in 2002 |

---

## 📊 COMPLEXITY TABLE

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion | **O(n)** | O(n²) | O(n²) | O(1) | ✅ |
| Merge | O(n log n) | O(n log n) | O(n log n) | **O(n)** | ✅ |
| Quick | O(n log n) | O(n log n) | **O(n²)** | O(log n) | ❌ |
| Heap | O(n log n) | O(n log n) | O(n log n) | **O(1)** | ❌ |
| Shell | O(n log n) | O(n^1.5) | O(n²) | O(1) | ❌ |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ |
| Radix | O(nk) | O(nk) | O(nk) | O(n+k) | ✅ |
| Bucket | O(n+k) | O(n+k) | **O(n²)** | O(n) | ✅ |
| Tim | **O(n)** | O(n log n) | O(n log n) | O(n) | ✅ |

> `k` = range of values &nbsp;|&nbsp; **Bold** = the dangerous part to remember

---

---

## 1. 🫧 BUBBLE SORT

### Intuition
> Biggest element **bubbles to the right** end each pass.  
> After pass k, the last k elements are permanently sorted.  
> **KEY CLICK:** Each pass locks one more element at the end. Window shrinks.

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]

Pass 1:  compare neighbors → swap if left > right
  64>34 ✦  34>25 ✦  25>12 ✦  22>11 ✦  rest ok
  [34, 25, 12, 22, 11, 64, 90]  ← 90 locked ✓

Pass 2:  [25, 12, 22, 11, 34, 64, 90]  ← 64 locked ✓
Pass 3:  [12, 22, 11, 25, 34, 64, 90]  ← 34 locked ✓
Pass 4:  [12, 11, 22, 25, 34, 64, 90]  ← 22 locked ✓
Pass 5:  [11, 12, 22, 25, 34, 64, 90]  ← done ✓

SHRINKING WINDOW:
  [unsorted region    ] [■ sorted ■]
  [unsorted region  ] [■■ sorted ■■]
  [unsorted region] [■■■ sorted ■■■]
   ← shrinks           → grows
```

### Code
```python
def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):                        # i = pass number
        swapped = False
        for j in range(0, n - i - 1):        # window shrinks each pass
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:                       # early exit if already sorted
            break
    return arr
```

### Iteration Trace
```
i=0, pass 1: (64,34)→swap (64,25)→swap (64,12)→swap (64,22)→swap (64,11)→swap → [34,25,12,22,11,64,90]
i=1, pass 2: (34,25)→swap (34,12)→swap (34,22)→swap (34,11)→swap           → [25,12,22,11,34,64,90]
i=2, pass 3: (25,12)→swap (25,22)→swap (25,11)→swap                        → [12,22,11,25,34,64,90]
i=3, pass 4: (12,22)→ok   (22,11)→swap                                     → [12,11,22,25,34,64,90]
i=4, pass 5: (12,11)→swap                                                   → [11,12,22,25,34,64,90] ✓
```

✅ **USE:** Nearly sorted (early exit = O(n)), tiny n, teaching  
❌ **DON'T USE:** Large n — always O(n²) in practice  
⚠️ **TRAP:** Most people's default. Signals you only know one sort.

---

## 2. 🎯 SELECTION SORT

### Intuition
> Scan everything, **pick the minimum**, place it at the front.  
> One scan → one swap. Left portion grows one at a time.  
> **KEY CLICK:** Unlike Bubble, doesn't swap constantly — just ONE swap per pass. Good when writes are expensive.

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]

i=0: [✓] [scan all →→→→→→→→→→] min=11 → swap(64,11) → [11, 34, 25, 12, 22, 64, 90]
i=1: [✓✓] [scan →→→→→→→→→→→]  min=12 → swap(34,12) → [11, 12, 25, 34, 22, 64, 90]
i=2: [✓✓✓] [scan →→→→→→→→→]  min=22 → swap(25,22) → [11, 12, 22, 34, 25, 64, 90]
i=3: [✓✓✓✓] [scan →→→→→→→]  min=25 → swap(34,25) → [11, 12, 22, 25, 34, 64, 90]
i=4: [✓✓✓✓✓] [scan →→→→→]  min=34 (in place)     → no swap
i=5: [✓✓✓✓✓✓] [scan →→→]  min=64 (in place)     → no swap

[locked ✓] [scanning for min ————————————→]
 grows →              always full scan
```

### Code
```python
def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        min_idx = i                           # assume current is min
        for j in range(i + 1, n):            # scan rest for true min
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]   # ONE swap per pass
    return arr
```

### Iteration Trace
```
i=0: scan[0..6] → min=11@idx5 → swap(64↔11) → [11, 34, 25, 12, 22, 64, 90]
i=1: scan[1..6] → min=12@idx3 → swap(34↔12) → [11, 12, 25, 34, 22, 64, 90]
i=2: scan[2..6] → min=22@idx4 → swap(25↔22) → [11, 12, 22, 34, 25, 64, 90]
i=3: scan[3..6] → min=25@idx4 → swap(34↔25) → [11, 12, 22, 25, 34, 64, 90]
i=4: scan[4..6] → min=34@idx4 → in place     → [11, 12, 22, 25, 34, 64, 90]
i=5: scan[5..6] → min=64@idx5 → in place     → [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** Write-expensive storage (flash/EEPROM) — only n swaps total, finding k-mins  
❌ **DON'T USE:** Nearly sorted data (still O(n²)), stability needed  
⚠️ **TRAP:** Always scans everything regardless. Doesn't improve on sorted input.

---

## 3. 🃏 INSERTION SORT

### Intuition
> Sorting playing cards in your hand. Pick the next card, **slide it left** until it's in the right spot.  
> Left side is always sorted. You're just inserting into it.  
> **KEY CLICK:** Element walks ← one step at a time. If nearly sorted, barely walks at all → O(n).

### Diagram
```
[64 | 34  25  12  22  11  90]   sorted=1, pick key=34
      ↑key
  64>34 → slide 64 right, insert 34
[34  64 | 25  12  22  11  90]   sorted=2, pick key=25
          ↑key
  64>25, 34>25 → slide both, insert 25
[25  34  64 | 12  22  11  90]   sorted=3, pick key=12
              ↑key
  slide 64,34,25 → insert 12
[12  25  34  64 | 22  11  90]   sorted=4, pick key=22
                  ↑key
  slide 64,34,25 → insert 22
[12  22  25  34  64 | 11  90]   ...
[11  12  22  25  34  64 | 90]   key=90, 64<90 → no slide, stays
[11  12  22  25  34  64  90] ✓
```

### Code
```python
def insertion_sort(arr):
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]                          # card being inserted
        j = i - 1
        while j >= 0 and arr[j] > key:       # slide bigger elements right
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key                     # drop key in correct spot
    return arr
```

### Iteration Trace
```
i=1: key=34 | 64>34→slide | insert → [34, 64, 25, 12, 22, 11, 90]
i=2: key=25 | 64>25→slide, 34>25→slide | insert → [25, 34, 64, 12, 22, 11, 90]
i=3: key=12 | 64,34,25 all slide | insert → [12, 25, 34, 64, 22, 11, 90]
i=4: key=22 | 64,34,25 slide | insert → [12, 22, 25, 34, 64, 11, 90]
i=5: key=11 | 64,34,25,22,12 slide | insert → [11, 12, 22, 25, 34, 64, 90]
i=6: key=90 | 64<90 → no slide → stays → [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** Nearly sorted, online/streaming data, small n (<20), inner sort in Tim Sort  
❌ **DON'T USE:** Large random arrays — too many shifts  
⚠️ **TRAP:** Don't underestimate it. Python's Tim Sort uses it for small chunks.

---

## 4. ✂️ MERGE SORT

### Intuition
> **Split** the array in half until you have single elements (trivially sorted).  
> **Merge** two sorted halves — always pick the smaller top element.  
> **KEY CLICK:** Splitting is trivial. The MERGE step is where the sorting happens. Two sorted arrays → one sorted in O(n). Do this log(n) levels.

### Diagram
```
SPLIT (divide until atoms):
         [64, 34, 25, 12, 22, 11, 90]
                /                \
        [64, 34, 25]          [12, 22, 11, 90]
          /       \              /           \
       [64]     [34, 25]     [12, 22]      [11, 90]
                 /    \       /    \         /    \
               [34]  [25]  [12]  [22]     [11]  [90]

MERGE (combine sorted pairs back up):
               [34]+[25] → [25, 34]
            [64]+[25,34] → [25, 34, 64]
               [12]+[22] → [12, 22]
               [11]+[90] → [11, 90]
          [12,22]+[11,90] → [11, 12, 22, 90]
  [25,34,64]+[11,12,22,90] → [11, 12, 22, 25, 34, 64, 90] ✓

MERGE STEP (always pick smaller head):
  L: [25, 34, 64]    R: [11, 12, 22, 90]
      ↑                   ↑
  25 vs 11 → take 11  → [11]
  25 vs 12 → take 12  → [11, 12]
  25 vs 22 → take 22  → [11, 12, 22]
  25 vs 90 → take 25  → [11, 12, 22, 25]
  34 vs 90 → take 34  → [11, 12, 22, 25, 34]
  64 vs 90 → take 64  → [11, 12, 22, 25, 34, 64]
             take 90  → [11, 12, 22, 25, 34, 64, 90] ✓
```

### Code
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])             # sort left half
    right = merge_sort(arr[mid:])             # sort right half
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:               # pick smaller (≤ keeps it stable)
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])                   # dump leftovers
    result.extend(right[j:])
    return result
```

### Iteration Trace
```
merge_sort([64,34,25,12,22,11,90])
  merge_sort([64,34,25])
    merge_sort([64]) → [64]
    merge_sort([34,25])
      merge_sort([34]) → [34]
      merge_sort([25]) → [25]
      _merge([34],[25]) → [25,34]
    _merge([64],[25,34]) → [25,34,64]
  merge_sort([12,22,11,90])
    merge_sort([12,22]) → [12,22]
    merge_sort([11,90]) → [11,90]
    _merge([12,22],[11,90]) → [11,12,22,90]
  _merge([25,34,64],[11,12,22,90]) → [11,12,22,25,34,64,90] ✓
```

✅ **USE:** Guaranteed O(n log n), stability needed, linked lists, external sort (data > RAM)  
❌ **DON'T USE:** Memory tight — needs O(n) extra space  
⚠️ **TRAP:** Always mention O(n) space cost in interviews. Most forget it.

---

## 5. ⚡ QUICK SORT

### Intuition
> Pick a **pivot**. Rearrange: smaller-left, larger-right. Pivot is now in its **FINAL position**.  
> Recurse both sides. No merging needed — sorting is done during partitioning.  
> **KEY CLICK:** After each partition, ONE element is in its permanent correct spot. You're not sorting — you're placing elements one at a time.

### Diagram
```
[64, 34, 25, 12, 22, 11, | 90]  pivot=90 (last)
 all < 90 → no swaps → pivot stays at end
 90 is in FINAL position ✓

Recurse on [64, 34, 25, 12, 22, 11]:
[64, 34, 25, 12, 22, | 11]  pivot=11
 all > 11 → 11 goes to front
 11 is in FINAL position ✓

Recurse on [34, 25, 12, 22, 64]:
[34, 25, 12, 22, | 64]  pivot=64
 all < 64 → stays at end. 64 in FINAL position ✓

...continues until fully sorted

PARTITION STEP (i tracks "smaller than pivot" boundary):
arr: [64  34  25  12  22  11  90]   pivot=90
      i=-1  j→→→→→→→→→→→→→→→→

j=0: 64≤90? yes → i=0, swap(arr[0],arr[0]) → no change
j=1: 34≤90? yes → i=1, swap(arr[1],arr[1]) → no change
... all ≤ 90, so i ends at 5
swap(arr[i+1], arr[high]) → swap(arr[6], arr[6]) → 90 stays
pivot 90 placed at index 6 ✓

PIVOT CHOICES:
  Last element    →  simple but O(n²) on sorted arrays ⚠️
  Random element  →  statistically safe ✅
  Median of 3     →  best for real data ✅✅
```

### Code
```python
def quick_sort(arr, low=0, high=None):
    arr = arr[:] if high is None else arr
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = _partition(arr, low, high)
        quick_sort(arr, low, pi - 1)          # recurse left of pivot
        quick_sort(arr, pi + 1, high)         # recurse right of pivot
    return arr

def _partition(arr, low, high):
    pivot = arr[high]                         # last element as pivot
    i = low - 1                               # boundary of "smaller" region
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # expand smaller region
    arr[i + 1], arr[high] = arr[high], arr[i + 1]   # place pivot
    return i + 1
```

### Iteration Trace
```
call(0,6): pivot=90 → partition → pi=6, 90 at final pos ✓
  call(0,5): pivot=11 → partition → pi=0, 11 at final pos ✓
    call(0,-1): base case
    call(1,5): pivot=64 → partition → pi=5, 64 at final pos ✓
      call(1,4): pivot=22 → partition → pi=2, 22 at final pos ✓
        call(1,1): [34] base case
        call(3,4): pivot=25 → partition → pi=3, 25 at final pos ✓
          call(3,2): base case
          call(4,4): [34] base case
      call(6,5): base case
Final: [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** General large arrays, in-place, cache-friendly, fastest in practice  
❌ **DON'T USE:** Stability needed, can't risk O(n²) worst case  
⚠️ **TRAP:** Always use random pivot. Sorted input + last-element pivot = O(n²) catastrophe.

---

## 6. 🏔️ HEAP SORT

### Intuition
> Build a **Max-Heap** (parent always > children, root = max).  
> Extract max → put at end → shrink heap → re-heapify. Repeat.  
> **KEY CLICK:** Selection Sort finds max in O(n). Heap Sort finds max in O(log n) using the heap. That's the only difference — but it changes O(n²) to O(n log n).

### Diagram
```
WHAT IS A MAX-HEAP?
  Array:  [90, 34, 64, 12, 22, 11, 25]
  As tree:
              90          ← root = ALWAYS the maximum
            /    \
          34      64
         /  \    /  \
        12  22  11  25
  Rule: parent > both children (everywhere in tree)

BUILD MAX-HEAP from [64, 34, 25, 12, 22, 11, 90]:
  Start from last non-leaf (idx = n//2-1 = 2), heapify up:
  idx=2: children=11,90 → 90>25 → swap → [64,34,90,12,22,11,25]
  idx=1: children=12,22 → 22<34 → ok
  idx=0: children=34,90 → 90>64 → swap → [90,34,64,12,22,11,25]
  Max-Heap: [90, 34, 64, 12, 22, 11, 25]

EXTRACT PHASE:
  swap(root, last) → shrink → heapify root
  [90,34,64,12,22,11,25] → swap(90,25) → [25,34,64,12,22,11,|90✓]
                         → heapify    → [64,34,25,12,22,11,|90✓]
  [64,34,25,12,22,11]    → swap(64,11) → [11,34,25,12,22,|64✓,90✓]
                         → heapify    → [34,22,25,12,11,|64✓,90✓]
  ... repeat → sorted portion grows from right ←

  [heap shrinks ←] [■ sorted grows → ■]
```

### Code
```python
def heap_sort(arr):
    arr = arr[:]
    n = len(arr)
    # Step 1: build max-heap
    for i in range(n // 2 - 1, -1, -1):      # last non-leaf down to root
        _heapify(arr, n, i)
    # Step 2: extract max one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]       # move max to end
        _heapify(arr, i, 0)                   # fix reduced heap
    return arr

def _heapify(arr, n, i):
    largest = i
    left  = 2 * i + 1
    right = 2 * i + 2
    if left  < n and arr[left]  > arr[largest]: largest = left
    if right < n and arr[right] > arr[largest]: largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)             # sift down recursively
```

### Iteration Trace
```
Build heap: [64,34,25,12,22,11,90] → [90,34,64,12,22,11,25]

Extract 90: swap→[25,34,64,12,22,11,|90] heapify→[64,34,25,12,22,11,|90]
Extract 64: swap→[11,34,25,12,22,|64,90] heapify→[34,22,25,12,11,|64,90]
Extract 34: swap→[11,22,25,12,|34,64,90] heapify→[25,22,11,12,|34,64,90]
Extract 25: swap→[12,22,11,|25,34,64,90] heapify→[22,12,11,|25,34,64,90]
Extract 22: swap→[11,12,|22,25,34,64,90] heapify→[12,11,|22,25,34,64,90]
Extract 12: swap→[11,|12,22,25,34,64,90]
Final: [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** In-place + guaranteed O(n log n), k-largest/smallest elements, priority queues  
❌ **DON'T USE:** Cache-sensitive (jumps around memory), stability needed  
⚠️ **TRAP:** Same O() as Quick Sort but slower in practice — poor cache locality.

---

## 7. 🐚 SHELL SORT

### Intuition
> Insertion Sort moves elements ONE step at a time — slow for large gaps.  
> Shell Sort uses a **big gap** first → elements leap to roughly correct region.  
> Gap shrinks → fine-tune. Final gap=1 = regular insertion sort, but now nearly sorted = O(n).  
> **KEY CLICK:** Large gap = coarse sort (big moves, fast). Small gap = fine-tune. Pre-sorting makes the final pass trivial.

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]   gap=3

Compare elements 3 apart:
  64 vs 12: 64>12 → swap → [12, 34, 25, 64, 22, 11, 90]
  34 vs 22: 34>22 → swap → [12, 22, 25, 64, 34, 11, 90]
  25 vs 11: 25>11 → swap → then 12 vs 11 → swap
    → [11, 22, 12, 64, 34, 25, 90]

  gap=3 connects:
  [64  34  25  12  22  11  90]
   |___________|           (64 vs 12)
       |___________|       (34 vs 22)
           |___________|   (25 vs 11)

After gap=3: [11, 22, 12, 64, 34, 25, 90]  ← rough sort done

gap=1: regular insertion sort — nearly sorted already → very fast!
→ [11, 12, 22, 25, 34, 64, 90] ✓

GAP SEQUENCE:  n//2 → n//4 → ... → 1
   gap=3:  coarse  ████████████░░░░░
   gap=1:  fine    ████████████████░  (nearly done, cheap)
```

### Code
```python
def shell_sort(arr):
    arr = arr[:]
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:   # insertion with gap step
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2                                      # shrink gap
    return arr
```

### Iteration Trace
```
gap=3:
  i=3: temp=12, arr[0]=64>12 → slide → arr[3]=64, insert at 0 → [12,34,25,64,22,11,90]
  i=4: temp=22, arr[1]=34>22 → slide → arr[4]=34, insert at 1 → [12,22,25,64,34,11,90]
  i=5: temp=11, arr[2]=25>11 → slide, arr[-1]=12>11 → slide → insert at 0 → [11,22,12,64,34,25,90]
  i=6: temp=90, arr[3]=64<90 → no slide → stays

gap=1: insertion sort on [11,22,12,64,34,25,90] — nearly sorted, fast
Final: [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** Embedded systems (no recursion, O(1) space), medium n, memory constrained  
❌ **DON'T USE:** Need guaranteed O(n log n) or stability  
⚠️ **TRAP:** Often forgotten in interviews. Valid answer for "in-place, no recursion" constraints.

---

## 8. 🔢 COUNTING SORT

### Intuition
> Don't compare — just **COUNT** how many times each value appears.  
> Rebuild sorted array directly from counts. Zero comparisons.  
> **KEY CLICK:** Breaks the O(n log n) comparison barrier by NOT comparing. Only works for integers in a bounded range. `count[v]` tells you exactly where value `v` belongs.

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]

Step 1: tally each value
  count[11]++ count[12]++ count[22]++ count[25]++
  count[34]++ count[64]++ count[90]++

  count array (indices 0..90):
  idx:  0  ...  11  12  ...  22  ...  25  ...  34  ...  64  ...  90
  val:  0  ...   1   1  ...   1  ...   1  ...   1  ...   1  ...   1

Step 2: rebuild — read count array left→right
  idx=11 (×1) → output: [11]
  idx=12 (×1) → output: [11, 12]
  idx=22 (×1) → output: [11, 12, 22]
  idx=25 (×1) → output: [11, 12, 22, 25]
  idx=34 (×1) → output: [11, 12, 22, 25, 34]
  idx=64 (×1) → output: [11, 12, 22, 25, 34, 64]
  idx=90 (×1) → output: [11, 12, 22, 25, 34, 64, 90] ✓

No comparisons at all — O(n+k) beats O(n log n) when k is small!

WHEN k IS A PROBLEM:
  k=100       → fine (count array size 100)
  k=1,000,000 → still ok-ish
  k=2^32      → 4 billion slots → 16GB memory → NOT ok ❌  → use Radix
```

### Code
```python
def counting_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1                       # tally each value
    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)           # rebuild from counts
    return result
```

### Iteration Trace
```
max_val = 90 → count array size = 91

Tallying:
  count[64]+=1, count[34]+=1, count[25]+=1, count[12]+=1
  count[22]+=1, count[11]+=1, count[90]+=1

Rebuild (skip zeros):
  val=11: freq=1 → [11]
  val=12: freq=1 → [11,12]
  val=22: freq=1 → [11,12,22]
  val=25: freq=1 → [11,12,22,25]
  val=34: freq=1 → [11,12,22,25,34]
  val=64: freq=1 → [11,12,22,25,34,64]
  val=90: freq=1 → [11,12,22,25,34,64,90] ✓
```

✅ **USE:** Integers with small known range (ages, grades, scores), subroutine in Radix Sort  
❌ **DON'T USE:** Range k >> n (huge memory), floats, strings, negative numbers (need offset)  
⚠️ **TRAP:** Always check k first. If k = range of values is massive, use Radix Sort instead.

---

## 9. 🔡 RADIX SORT

### Intuition
> Sort digit by digit, **least significant to most significant**.  
> Use a stable sort (counting sort) at each digit pass.  
> **KEY CLICK:** Later passes (more significant digits) override earlier ones — so the most significant digit wins in the end. Like sorting by last name first, then first name: first-name order is preserved within same last names.

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]

Pass 1 — sort by UNITS digit (exp=1):
  64→4   34→4   25→5   12→2   22→2   11→1   90→0
  Bucket by units:
    [0]: 90
    [1]: 11
    [2]: 12, 22   ← 12 before 22 (original order, stable)
    [4]: 64, 34   ← 64 before 34 (original order, stable)
    [5]: 25
  After pass 1: [90, 11, 12, 22, 64, 34, 25]

Pass 2 — sort by TENS digit (exp=10):
  90→9   11→1   12→1   22→2   64→6   34→3   25→2
  Bucket by tens:
    [1]: 11, 12   ← kept order from pass 1 (stable!)
    [2]: 22, 25   ← kept order
    [3]: 34
    [6]: 64
    [9]: 90
  After pass 2: [11, 12, 22, 25, 34, 64, 90] ✓

WHY LEAST→MOST SIGNIFICANT?
  most→least:  last pass (units) would scramble the order ❌
  least→most:  last pass (tens) is the final tiebreaker   ✅
```

### Code
```python
def radix_sort(arr):
    if not arr:
        return arr
    arr = arr[:]
    max_val = max(arr)
    exp = 1                                   # start from units digit
    while max_val // exp > 0:
        arr = _counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr

def _counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count  = [0] * 10                         # digits 0–9

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):                    # prefix sums → positions
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):           # right-to-left keeps it stable
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    return output
```

### Iteration Trace
```
max=90 → 2 passes (exp=1, exp=10)

exp=1 (units):
  digits: 64→4, 34→4, 25→5, 12→2, 22→2, 11→1, 90→0
  count:  [1,1,2,0,2,1,0,0,0,0] → prefix: [1,2,4,4,6,7,7,7,7,7]
  fill right→left (stable): output = [90, 11, 12, 22, 64, 34, 25]

exp=10 (tens):
  digits: 90→9, 11→1, 12→1, 22→2, 64→6, 34→3, 25→2
  output = [11, 12, 22, 25, 34, 64, 90] ✓
```

✅ **USE:** Large list of integers/fixed-length strings, d (digits) is small  
❌ **DON'T USE:** Variable-length strings, floats (needs adaptation), d > log n  
⚠️ **TRAP:** Inner sort MUST be stable. Unstable inner sort = Radix Sort breaks silently.

---

## 10. 🪣 BUCKET SORT

### Intuition
> Distribute elements into **value-range buckets**. Sort each bucket (small → insertion sort is fast). Concatenate.  
> **KEY CLICK:** Like sorting mail by zip code range first, then sorting within each bundle. Only works well when data is **uniformly spread** — otherwise all data falls into one bucket → O(n²).

### Diagram
```
[64, 34, 25, 12, 22, 11, 90]   min=11, max=90, 7 buckets

bucket_range = (90-11)/7 + 1 ≈ 12.3

Distribute:
  bucket 0 [11.0–23.3):  11, 12, 22
  bucket 1 [23.3–35.6):  25, 34
  bucket 2 [35.6–47.9):  (empty)
  bucket 3 [47.9–60.2):  (empty)
  bucket 4 [60.2–72.5):  64
  bucket 5 [72.5–84.8):  (empty)
  bucket 6 [84.8–97.1):  90

Sort each bucket:
  [11,12,22] → sorted ✓
  [25,34]    → sorted ✓

Concatenate:
  [11,12,22] + [25,34] + [64] + [90] = [11,12,22,25,34,64,90] ✓

UNIFORM vs SKEWED:
  Good (uniform): |■■■|■■ |   |■  |■  |   |■  |  ← balanced buckets
  Bad  (skewed):  |■■■■■■■|   |   |   |   |   |  ← all in one = O(n²) ❌
```

### Code
```python
def bucket_sort(arr):
    if not arr:
        return arr
    arr = arr[:]
    min_val, max_val = min(arr), max(arr)
    n = len(arr)
    bucket_range = (max_val - min_val) / n + 1

    buckets = [[] for _ in range(n)]
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        idx = min(idx, n - 1)                # guard: edge values → last bucket
        buckets[idx].append(num)

    for bucket in buckets:
        bucket.sort()                        # insertion sort for small buckets

    return [num for bucket in buckets for num in bucket]
```

### Iteration Trace
```
min=11, max=90, n=7, range_per_bucket≈12.3

Distributing:
  64 → idx=(64-11)/12.3=4 → bucket[4]
  34 → idx=(34-11)/12.3=1 → bucket[1]
  25 → idx=(25-11)/12.3=1 → bucket[1]
  12 → idx=(12-11)/12.3=0 → bucket[0]
  22 → idx=(22-11)/12.3=0 → bucket[0]
  11 → idx=(11-11)/12.3=0 → bucket[0]
  90 → idx=(90-11)/12.3=6 → bucket[6]

Buckets: [0]=[11,12,22], [1]=[34,25], [4]=[64], [6]=[90]
Sort: [11,12,22], [25,34], [64], [90]
Concat: [11,12,22,25,34,64,90] ✓
```

✅ **USE:** Floats in [0,1], uniformly distributed data, parallel sorting  
❌ **DON'T USE:** Skewed/clustered data, distribution unknown  
⚠️ **TRAP:** Only fast with uniform distribution. Visualize your data before using this.

---

## 11. ⏱️ TIM SORT *(Python's `sorted()` and `list.sort()`)*

### Intuition
> Real-world data has **natural runs** (already-sorted sequences).  
> Tim Sort finds them, extends short ones with insertion sort, then merges runs like merge sort.  
> **KEY CLICK:** Insertion sort is O(n) on sorted data. Merge sort is optimal for combining. Tim Sort picks the best tool for each part of the array.

### Diagram
```
REAL-WORLD DATA HAS PATTERNS:
  [1, 3, 5, 7 | 8, 6, 4, 2 | 10, 11, 12, 13]
   └──run 1──┘  └──run 2──┘   └────run 3────┘
   (sorted)      (reverse)       (sorted)

Step 1: Detect/create runs of min size (MIN_RUN ≈ 32-64)
  run 1: [1,3,5,7]     → already sorted ✓
  run 2: [8,6,4,2]     → reverse → [2,4,6,8] then extend with insertion sort
  run 3: [10,11,12,13] → already sorted ✓

Step 2: Merge runs (merge sort style)
  [run1] + [run2] → merge → [sorted 1-8]
  [sorted 1-8] + [run3] → merge → [1,2,3,4,5,6,7,8,10,11,12,13] ✓

FOR OUR ARRAY [64,34,25,12,22,11,90]:
  n=7 < MIN_RUN=32 → just use insertion sort directly
  → [11, 12, 22, 25, 34, 64, 90] ✓

WHY PYTHON USES TIM SORT:
  ✅ O(n) best case (sorted input — common in real data)
  ✅ O(n log n) worst case
  ✅ Stable
  ✅ Battle-tested since 2002
```

### Code
```python
# Python's built-in — just use this:
def tim_sort_demo(arr):
    return sorted(arr)                        # Tim Sort under the hood

# Simplified implementation to understand the idea:
def simplified_tim_sort(arr):
    arr = arr[:]
    MIN_RUN = 32
    n = len(arr)

    # Step 1: sort each run with insertion sort
    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN, n)
        _insertion_sort_range(arr, start, end)

    # Step 2: merge runs
    size = MIN_RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(start + size, n)
            end = min(start + size * 2, n)
            if mid < end:
                merged = _merge(arr[start:mid], arr[mid:end])
                arr[start:end] = merged
        size *= 2
    return arr

def _insertion_sort_range(arr, start, end):
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

✅ **USE:** Always in Python. For interviews when built-ins allowed, just say Tim Sort.  
❌ **DON'T USE:** "Implement from scratch" interviews — too complex; use Merge Sort instead  
⚠️ **TRAP:** "How does Python sort?" → Tim Sort, NOT Quick Sort. Many people get this wrong.

---

## 🎯 INTERVIEW HINT DECODER

| Interviewer says... | They're hinting → |
|---|---|
| *"array is nearly sorted"* | Insertion Sort or Tim Sort |
| *"memory is limited / in-place"* | Quick Sort or Heap Sort (avoid Merge) |
| *"sort must be stable"* | Merge Sort or Tim Sort |
| *"integers in range 1–1000"* | Counting Sort |
| *"find k largest elements"* | Min-Heap of size k → O(n log k) |
| *"find kth largest element"* | Quick Select → O(n) avg, no full sort needed |
| *"data won't fit in RAM"* | Merge Sort (external sort on file chunks) |
| *"many duplicate values"* | Quick Sort with 3-way partition |
| *"sorting a linked list"* | Merge Sort (no random access needed) |
| *"sort by multiple criteria"* | Stable sort (Merge/Tim) + sort by each key |

---

## ⚖️ STABLE vs UNSTABLE — WHY IT MATTERS

```
Stable = equal elements keep their ORIGINAL relative order

Example: students sorted by name first, then by grade

Original (sorted by name):
  [("Alice",90), ("Bob",85), ("Carol",90), ("Dave",85)]

Stable sort by grade:
  [("Bob",85), ("Dave",85), ("Alice",90), ("Carol",90)]
   Bob before Dave ✓      Alice before Carol ✓
   (original name-order preserved within same grade)

Unstable sort by grade (might give):
  [("Dave",85), ("Bob",85), ("Carol",90), ("Alice",90)]
   ← random order within equal grades ✗

STABLE:    Bubble ✅  Insertion ✅  Merge ✅  Counting ✅  Radix ✅  Bucket ✅  Tim ✅
UNSTABLE:  Selection ❌  Quick ❌  Heap ❌  Shell ❌
```

---

## 🔑 ONE-LINER MEMORY ANCHORS

```
Bubble    →  "biggest floats RIGHT each pass, window shrinks"
Selection →  "scan all, pick min, ONE swap per pass"
Insertion →  "slide LEFT until it fits, like cards in hand"
Merge     →  "split to atoms → merge sorted pairs upward"
Quick     →  "pivot lands in FINAL spot, recurse both sides"
Heap      →  "root=max always, extract→end, re-heapify"
Shell     →  "insertion sort with BIG gap first, shrink to 1"
Counting  →  "count[v]++, no comparisons, rebuild from counts"
Radix     →  "sort digit-by-digit LEAST→MOST significant"
Bucket    →  "spread into range-buckets, sort each bucket"
Tim       →  "find runs + insertion + merge = Python's sort"
```

---

*Array used throughout: `[64, 34, 25, 12, 22, 11, 90]` → `[11, 12, 22, 25, 34, 64, 90]`*
