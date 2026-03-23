# TCS NQT Prime – Advanced Section Notes (Non-SQL)
> Exam: 1 April | Target: TCS Prime | SQL = already covered

---

## 📌 Exam Structure (Advanced Section Only)

| Sub-section | Questions | Time | Difficulty |
|---|---|---|---|
| Advanced Quantitative Ability | 10 Qs | shared 25 min | Hard |
| Advanced Reasoning Ability | 5 Qs | shared 25 min | Hard |
| Advanced Coding | 3 problems | 90 min | Hard |
| **Total** | **~18 Qs** | **115 min** | — |

> ⚠️ Quant + Reasoning share the 25 minutes. 15 questions in 25 mins = ~100 sec per question. Speed matters more than perfection here.
> No negative marking. Attempt everything.

---

# PART 1 – ADVANCED QUANTITATIVE ABILITY

---

## Topic 1: Number System

### Divisibility Rules (memorize cold)
```
÷ 2   → last digit even
÷ 3   → sum of digits ÷ 3
÷ 4   → last 2 digits ÷ 4
÷ 5   → last digit 0 or 5
÷ 6   → divisible by 2 AND 3
÷ 8   → last 3 digits ÷ 8
÷ 9   → sum of digits ÷ 9
÷ 11  → (sum of odd-position digits) - (sum of even-position digits) = 0 or ÷ 11
```

### HCF and LCM
```
HCF × LCM = Product of two numbers (only for 2 numbers)

HCF by Euclid: HCF(a, b) = HCF(b, a mod b) until remainder = 0
LCM = (a × b) / HCF(a, b)
```

**Example:** HCF(48, 18)?
→ 48 = 2×18 + 12 → HCF(18,12) → 18 = 1×12 + 6 → HCF(12,6) = **6**

### Remainders
```
(a × b) mod n = [(a mod n) × (b mod n)] mod n
(a + b) mod n = [(a mod n) + (b mod n)] mod n
```

**Example:** 37 × 43 mod 5?
→ 37 mod 5 = 2, 43 mod 5 = 3 → 2×3 = 6 → 6 mod 5 = **1**

### Powers and Cyclicity (last digit patterns)
```
2: 2,4,8,6 → cycle 4
3: 3,9,7,1 → cycle 4
4: 4,6 → cycle 2
7: 7,9,3,1 → cycle 4
8: 8,4,2,6 → cycle 4
9: 9,1 → cycle 2
```
**Example:** Last digit of 7^53?
→ 53 mod 4 = 1 → first in cycle → **7**

---

## Topic 2: Percentages, Profit & Loss

### Key Formulas
```
% change = (New - Old) / Old × 100

Profit% = Profit / CP × 100
SP = CP × (1 + Profit%/100)
CP = SP / (1 + Profit%/100)

Loss% = Loss / CP × 100
SP = CP × (1 - Loss%/100)

Discount% = Discount / MP × 100
SP = MP × (1 - Discount%/100)
```

### Successive % change trick
If price increases by a% then b%:
```
Net change = a + b + (a×b)/100
```
**Example:** 20% increase then 10% decrease:
→ 20 + (-10) + (20×-10)/100 = 10 - 2 = **8% net increase**

### Marked Price problems
```
If profit% on CP = p% and discount% on MP = d%:
MP/CP = (100 + p) / (100 - d)
```

---

## Topic 3: Time, Speed, Distance

```
Speed = Distance / Time
Average Speed (two equal distances at s1 and s2) = 2s1s2 / (s1+s2)   ← NOT (s1+s2)/2
```

### Relative Speed
- Same direction: |s1 - s2|
- Opposite direction: s1 + s2

### Trains
```
Train crossing a pole/person: time = Length of train / Speed
Train crossing a platform: time = (Length of train + Length of platform) / Speed
Two trains crossing: time = (L1 + L2) / relative speed
```

### Boats and Streams
```
Speed downstream = boat + stream
Speed upstream   = boat - stream
Boat speed = (downstream + upstream) / 2
Stream speed = (downstream - upstream) / 2
```

---

## Topic 4: Time and Work

```
If A does work in 'a' days → A's 1-day work = 1/a
A + B together: 1/a + 1/b = (a+b)/(ab) → Days = ab/(a+b)
```

### Pipes and Cisterns
Same concept — fill (+), drain (-)
```
Net work/hour = 1/a - 1/b (one fills, one drains)
```

**Example:** A fills in 12hrs, B drains in 20hrs. Net = 1/12 - 1/20 = (5-3)/60 = 2/60 = 1/30 → fills in **30 hrs**

### Work with efficiency
If A is 3x as efficient as B:
→ A takes 1/3 the time B takes

---

## Topic 5: Simple & Compound Interest

```
SI = P × R × T / 100
CI = P × (1 + R/100)^T - P

Effective annual rate for half-yearly compounding at R%:
= (1 + R/200)^2 - 1
```

**Common trap:** "8% compounded half-yearly" means 4% per 6 months.

### Difference between CI and SI for 2 years:
```
CI - SI = P × (R/100)^2
```

---

## Topic 6: Permutation & Combination + Probability

### Formulas
```
nPr = n! / (n-r)!         ← ordered selection
nCr = n! / [r! × (n-r)!]  ← unordered selection

nC0 = nCn = 1
nC1 = n
nCr = nC(n-r)
```

### Probability
```
P(A) = Favorable outcomes / Total outcomes
P(A or B) = P(A) + P(B) - P(A and B)
P(A and B) = P(A) × P(B)  [if independent]
P(not A) = 1 - P(A)
```

### Common setups
**Cards:** 52 total | 4 suits × 13 cards | 12 face cards | 4 aces
**Dice:** 6 faces | sample space for 2 dice = 36
**Coins:** 2^n outcomes for n coins

**Example:** Probability of getting sum 7 from 2 dice?
→ Pairs: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6 → 6/36 = **1/6**

---

## Topic 7: Averages, Ratio, Mixtures

### Averages
```
Average = Sum / Count
If one element changes by x, average changes by x/n
Weighted average = (w1×a1 + w2×a2) / (w1+w2)
```

### Alligation / Mixtures (cross method)
```
Cheaper : Costlier = (Costlier - Mean) : (Mean - Cheaper)
```
**Example:** Mix milk at ₹20/L and ₹30/L to get ₹24/L. Ratio?
→ (30-24) : (24-20) = 6:4 = **3:2**

---

## Topic 8: Geometry & Mensuration (quick ref)

```
Circle:   Area = πr²  |  Circumference = 2πr
Triangle: Area = ½ × base × height  |  Heron's: √[s(s-a)(s-b)(s-c)], s=(a+b+c)/2
Rectangle: Area = l×b  |  Perimeter = 2(l+b)
Cuboid: Volume = l×b×h  |  Surface Area = 2(lb+bh+lh)
Cylinder: Volume = πr²h  |  CSA = 2πrh
Sphere: Volume = (4/3)πr³  |  SA = 4πr²
Cone: Volume = (1/3)πr²h  |  Slant height l = √(r²+h²)
```

---

## Topic 9: Progressions & Logarithms

### AP (Arithmetic Progression)
```
nth term = a + (n-1)d
Sum = n/2 × [2a + (n-1)d]  or  n/2 × (first + last)
```

### GP (Geometric Progression)
```
nth term = a × r^(n-1)
Sum = a(r^n - 1) / (r - 1)  [r ≠ 1]
Sum to infinity = a / (1-r)  [|r| < 1]
```

### Logarithm Rules
```
log(ab) = log a + log b
log(a/b) = log a - log b
log(a^n) = n log a
log_b(a) = log a / log b   ← change of base
log_a(a) = 1
log(1) = 0
```

---

# PART 2 – ADVANCED REASONING ABILITY

---

## Topic 1: Seating Arrangements (Complex)

Two types: Linear and Circular.

**Circular — key rule:**
- Fix one person, arrange rest → (n-1)! ways
- "Facing center" vs "facing outside" matters in circular puzzles

**Approach for puzzle-type:**
1. List all constraints
2. Start with most specific (X sits exactly 3 places from Y)
3. Use elimination for remaining

**Common clue types:**
- "Immediate neighbor" → adjacent
- "Second to the left" → exactly 2 seats left
- "Facing" in circle → directly opposite

---

## Topic 2: Blood Relations

**Key relationships to know:**
```
Parent's sibling         = Uncle / Aunt
Parent's sibling's child = Cousin
Spouse's parent          = Father/Mother-in-law
Child's spouse           = Son/Daughter-in-law
Sibling's child          = Nephew / Niece
```

**Approach:** Draw a tree. Never try to solve blood relation in your head.

**Classic trick questions:**
- "Pointing to a photo: He is the son of my father's only son" → that's YOUR son
- "She is the daughter of the only son of my grandfather" → your sister/cousin

---

## Topic 3: Syllogisms

**Rules (Venn Diagram logic):**
```
All A are B   → A circle fully inside B
Some A are B  → A and B circles overlap
No A are B    → A and B circles don't overlap
Some A are not B → Part of A outside B
```

**Valid conclusions:**
- All A→B + All B→C = All A→C ✅
- All A→B + Some B→C = Some A→C? ❌ (not necessarily)
- Some A→B + All B→C = Some A→C ✅
- No A→B + All C→A = No C→B ✅

**Tip:** For "Either/Or" conclusions — check if both individually fail but together they cover all cases.

---

## Topic 4: Data Sufficiency

Format: A question is given + Statement I + Statement II.
Options are always:
- (A) Statement I alone sufficient
- (B) Statement II alone sufficient
- (C) Both together sufficient
- (D) Either alone sufficient
- (E) Neither sufficient

**Approach:**
1. Try Statement I alone → sufficient? → A or D
2. Try Statement II alone → sufficient? → B, D, or not E
3. If both needed → C
4. If neither → E

---

## Topic 5: Number & Letter Series

**Common patterns:**
```
+1, +2, +3...  (incrementing diff)
×2, ×3, ×4...  (multiplying)
Prime numbers: 2,3,5,7,11,13...
Squares: 1,4,9,16,25...
Cubes: 1,8,27,64,125...
Fibonacci: 1,1,2,3,5,8,13...
Alternating: two interleaved series
```

**Letter series:** A=1, B=2 ... Z=26. Often the same numeric patterns applied to positions.

**Example:** Z, X, V, T, _
→ every letter skips one (Z=26, X=24, V=22, T=20) → **R**

---

## Topic 6: Statement-Assumption / Conclusion

**Assumption = unstated premise required for the statement to hold**
**Conclusion = what logically follows from the statement**

**Tips:**
- Assumption can't contradict the statement
- Conclusion must be directly inferable — no extra jumps
- "Strong argument" = logically relevant + factually sound
- "Weak argument" = emotional, vague, or not directly related

---

# PART 3 – ADVANCED CODING (90 mins, 3 problems)

> You've chosen SQL — so for the 3 coding problems, **at least 1–2 may be solvable in SQL**.
> But TCS Prime coding is algorithmic in nature. Know DSA concepts cold even if you write SQL.

---

## Coding Section Reality Check

Topics expected: Arrays, Strings, Linked Lists, Stacks, Queues, Trees, Graphs, Recursion, Sorting, Searching, Time & Space Complexity, Matrix operations, Number series, Shortest Path logic.

Difficulty: **Hard**. Think LeetCode medium-hard.

---

## Topic 1: Arrays & Strings

### Must-Know Patterns

**Find duplicates:**
```
Brute: O(n²) nested loop
Better: Sort + check adjacent O(n log n)
Best: Hash map / frequency array O(n)
```

**Two Sum (find pair with given sum):**
```
Sort + two pointers (left, right) O(n log n)
OR Hash set — for each element check if (target - element) in set O(n)
```

**Sliding Window (subarray of size k):**
```
Max/min sum subarray of size k:
- Compute sum of first k elements
- Slide: add next, remove first, track max
Time: O(n)
```

**Kadane's Algorithm (max subarray sum):**
```
max_so_far = max_ending_here = arr[0]
for i in 1..n:
    max_ending_here = max(arr[i], max_ending_here + arr[i])
    max_so_far = max(max_so_far, max_ending_here)
```

**String reversal, palindrome check, anagram check:**
```
Palindrome: two pointers from both ends
Anagram: sort both strings and compare OR frequency count
```

---

## Topic 2: Recursion & Backtracking

### Recursion Template
```
function solve(params):
    if base_case:
        return result
    # recursive call
    return f(solve(smaller_problem))
```

### Key Recursion Problems
**Factorial:**
```
fact(n) = n × fact(n-1)
fact(0) = 1
```

**Fibonacci:**
```
fib(n) = fib(n-1) + fib(n-2)
fib(0)=0, fib(1)=1
```

**Power (fast exponentiation):**
```
power(base, exp):
    if exp == 0: return 1
    if exp is even: return power(base, exp/2)^2
    else: return base × power(base, exp-1)
Time: O(log n)
```

---

## Topic 3: Sorting Algorithms

| Algorithm | Best | Avg | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |

> **Quick Sort worst case** = already sorted array with first element as pivot
> **Merge Sort** = always O(n log n), best for linked lists
> **Counting Sort** = O(n+k), only for integers in a range

---

## Topic 4: Searching

**Binary Search** (array must be sorted):
```
left=0, right=n-1
while left <= right:
    mid = (left+right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid+1
    else: right = mid-1
return -1
Time: O(log n)
```

---

## Topic 5: Linked Lists

**Key operations:**
```
Reverse: prev=None, curr=head
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev

Detect cycle: Floyd's (slow pointer moves 1, fast moves 2)
    if they meet → cycle exists

Find middle: slow/fast pointers
    when fast reaches end, slow is at middle
```

---

## Topic 6: Stacks and Queues

**Stack (LIFO):** Push/Pop from top
**Queue (FIFO):** Enqueue at rear, Dequeue from front

**Stack problems:**
- Balanced parentheses check
- Next greater element
- Evaluate postfix expression
- Reverse a string using stack

**Queue problems:**
- BFS traversal
- First non-repeating character in stream

**Monotonic Stack pattern (Next Greater Element):**
```
for each element from right to left:
    while stack not empty and stack.top <= element:
        stack.pop()
    NGE[i] = stack.top if stack not empty else -1
    stack.push(element)
```

---

## Topic 7: Trees

**Traversals (memorize output order):**
```
Inorder   : Left → Root → Right  (BST inorder = sorted)
Preorder  : Root → Left → Right  (used to copy tree)
Postorder : Left → Right → Root  (used to delete tree)
Level-order: BFS using a queue
```

**BST Properties:**
```
Left child < Parent < Right child
Search, Insert, Delete: O(log n) avg, O(n) worst (skewed)
```

**Height of tree:**
```
height(node) = 1 + max(height(left), height(right))
height(null) = 0
```

---

## Topic 8: Graphs

**Representations:**
- Adjacency Matrix: O(V²) space, O(1) edge check
- Adjacency List: O(V+E) space, better for sparse graphs

**BFS (Breadth First Search):**
```
Use Queue. Start from source.
Mark visited before enqueuing.
Used for: shortest path (unweighted), level order
Time: O(V+E)
```

**DFS (Depth First Search):**
```
Use Stack (or recursion).
Used for: cycle detection, topological sort, connected components
Time: O(V+E)
```

**Shortest Path:**
```
Unweighted graph → BFS
Weighted (no negative) → Dijkstra's O((V+E) log V)
Negative weights → Bellman-Ford O(VE)
All pairs → Floyd-Warshall O(V³)
```

---

## Topic 9: Dynamic Programming (DP)

**Core idea:** Break problem into overlapping subproblems, store results.

**Template:**
```
1. Define state: dp[i] means "answer for problem of size i"
2. Write recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
3. Set base cases
4. Fill table bottom-up (or memoize top-down)
```

**Must-know DP problems:**

**Fibonacci (DP):**
```
dp[0]=0, dp[1]=1
dp[i] = dp[i-1] + dp[i-2]
```

**0/1 Knapsack:**
```
dp[i][w] = max value using first i items with capacity w
if weight[i] > w: dp[i][w] = dp[i-1][w]
else: dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])
```

**Longest Common Subsequence (LCS):**
```
if s1[i]==s2[j]: dp[i][j] = 1 + dp[i-1][j-1]
else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Longest Increasing Subsequence (LIS):**
```
dp[i] = max(dp[j]+1) for all j<i where arr[j]<arr[i]
LIS length = max(dp[i])
Time: O(n²)  or  O(n log n) with patience sorting
```

**Coin Change (min coins):**
```
dp[0] = 0
dp[i] = min(dp[i - coin] + 1) for each coin
```

---

## Topic 10: Time & Space Complexity (must for Prime)

```
O(1)       < O(log n) < O(n) < O(n log n) < O(n²) < O(2^n) < O(n!)

Common complexities:
Binary search       → O(log n)
Linear search       → O(n)
Merge/Quick/Heap sort → O(n log n)
Bubble/Selection/Insertion sort → O(n²)
BFS / DFS           → O(V+E)
DP Knapsack         → O(n×W)
Floyd-Warshall      → O(V³)
```

**Space complexity:**
```
Recursive calls use stack space — depth of recursion = space
Iterative with auxiliary array → O(n)
In-place algorithms → O(1)
```

**Master Theorem (for divide-and-conquer):**
```
T(n) = aT(n/b) + f(n)
Merge Sort: T(n) = 2T(n/2) + O(n) → O(n log n)
Binary Search: T(n) = T(n/2) + O(1) → O(log n)
```

---

# PART 4 – TECHNICAL INTERVIEW (Post-NQT for Prime)

> Prime interview is significantly harder. Expect live coding + system design.

---

## OOPS Concepts (language-agnostic)

```
Encapsulation  → Bundle data + methods, hide internals (private/public)
Abstraction    → Expose only what's necessary (interfaces, abstract classes)
Inheritance    → Child class gets parent's properties/methods
Polymorphism   → Same method name, different behavior
               → Compile-time: method overloading (same name, diff params)
               → Runtime: method overriding (child redefines parent method)
```

**Key terms:**
- Constructor: special method called on object creation
- Destructor: called on object destruction
- Abstract class: can't be instantiated, has abstract methods
- Interface: pure abstraction, all methods are abstract
- Virtual function: enables runtime polymorphism

---

## OS Concepts

```
Process vs Thread:
Process = independent execution, own memory
Thread = lightweight, shares memory with parent process

Scheduling algorithms:
FCFS (First Come First Serve) → simple, convoy effect
SJF (Shortest Job First) → optimal avg wait, starvation possible
Round Robin → time quantum, fair, used in real systems
Priority Scheduling → highest priority runs first

Deadlock conditions (ALL 4 must hold):
1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait

Page replacement:
FIFO, LRU (Least Recently Used), Optimal
```

---

## DBMS Beyond SQL

```
ER Diagram → Entity, Attribute, Relationship
Normalization → 1NF, 2NF, 3NF, BCNF (covered in SQL notes)
ACID → Atomicity, Consistency, Isolation, Durability
Indexing → B-tree, Hash index
Transactions → BEGIN, COMMIT, ROLLBACK
Concurrency problems → Dirty read, Non-repeatable read, Phantom read
Isolation levels → READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE
```

---

## CN (Computer Networks)

```
OSI 7 Layers (top to bottom):
7. Application  (HTTP, FTP, SMTP)
6. Presentation (encryption, compression)
5. Session      (session management)
4. Transport    (TCP, UDP)
3. Network      (IP, routing)
2. Data Link    (MAC address, switches)
1. Physical     (cables, bits)

TCP vs UDP:
TCP → reliable, ordered, connection-oriented, slower
UDP → unreliable, no order, connectionless, faster

IP addresses:
IPv4 = 32-bit, IPv6 = 128-bit
Subnet mask: 255.255.255.0 → /24

HTTP methods: GET, POST, PUT, DELETE, PATCH
Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error
```

---

# 📋 7-Day Schedule

| Day | Focus |
|---|---|
| Day 1 | Quant: Number System, %, Profit & Loss |
| Day 2 | Quant: TSD, Time & Work, SI/CI |
| Day 3 | Quant: P&C, Probability, Mixtures, Progressions |
| Day 4 | Reasoning: Seating, Blood Relations, Syllogisms, Series |
| Day 5 | Coding: Arrays, Strings, Recursion, Sorting |
| Day 6 | Coding: Linked Lists, Trees, Graphs, DP basics |
| Day 7 | Full mock + Revision of Complexity, OOPS, DBMS, OS, CN |

---

# ⚡ Last-Minute Cheatsheet

```
QUANT:
  Average speed (equal distance) = 2v1v2/(v1+v2) — NOT simple average
  Successive % = a + b + ab/100
  CI - SI (2 yrs) = P(R/100)²
  Alligation ratio = (high-mean):(mean-low)
  HCF × LCM = product of 2 numbers (only for 2)

REASONING:
  Circular arrangement — fix 1 person, arrange (n-1)!
  Syllogism — draw Venn, don't assume
  Data Sufficiency — test each statement independently first

CODING:
  Two pointers → sorted array, pair problems
  Sliding window → subarray/substring problems
  DP → overlapping subproblems + optimal substructure
  BFS → shortest path (unweighted)
  DFS → cycle detection, topological sort
  Quick Sort worst case → O(n²) on sorted input
  Binary Search → O(log n), array must be sorted
```
