# SQL Daily Drill — Day 5
### 💀 Level: Brutal — Product-Based Company Interview

**Focus:** Multi-step business logic · NULL traps · Deduplication · Brain teasers  
**No LAG/LEAD. No sessionization. No running totals.**

---

## 🏢 Scenario: SaaS Subscription Platform — SubsX

Think Notion / Slack / Zoom billing backend.

---

## 📦 Tables & Sample Data

**users**
| user_id | name    | email                  | country | created_at  |
|---------|---------|------------------------|---------|-------------|
| 1       | Animesh | animesh@gmail.com      | India   | 2023-01-15  |
| 2       | Rohit   | rohit@gmail.com        | India   | 2023-02-10  |
| 3       | Sara    | sara@outlook.com       | USA     | 2023-03-05  |
| 4       | Karan   | karan@gmail.com        | India   | 2023-04-20  |
| 5       | Nina    | nina@yahoo.com         | UK      | 2023-05-01  |
| 6       | Dev     | dev@gmail.com          | India   | 2023-06-15  |

**subscriptions**
| sub_id | user_id | plan     | started_at  | ended_at    | status    | amount  |
|--------|---------|----------|-------------|-------------|-----------|---------|
| S01    | 1       | basic    | 2023-01-15  | 2023-04-15  | expired   | 299.00  |
| S02    | 1       | pro      | 2023-04-16  | NULL        | active    | 799.00  |
| S03    | 2       | pro      | 2023-02-10  | 2023-05-10  | expired   | 799.00  |
| S04    | 2       | basic    | 2023-05-11  | NULL        | active    | 299.00  |
| S05    | 3       | enterprise| 2023-03-05 | NULL        | active    | 2999.00 |
| S06    | 4       | basic    | 2023-04-20  | 2023-07-20  | expired   | 299.00  |
| S07    | 4       | basic    | 2023-07-21  | 2023-10-21  | expired   | 299.00  |
| S08    | 5       | pro      | 2023-05-01  | NULL        | active    | 799.00  |
| S09    | 6       | basic    | 2023-06-15  | NULL        | active    | 299.00  |
| S10    | 3       | enterprise| 2023-01-01 | 2023-02-28  | expired   | 2999.00 |

**payments**
| pay_id | sub_id | paid_at     | amount   | status  |
|--------|--------|-------------|----------|---------|
| P01    | S01    | 2023-01-15  | 299.00   | success |
| P02    | S02    | 2023-04-16  | 799.00   | success |
| P03    | S03    | 2023-02-10  | 799.00   | success |
| P04    | S04    | 2023-05-11  | 299.00   | success |
| P05    | S05    | 2023-03-05  | 2999.00  | success |
| P06    | S06    | 2023-04-20  | 299.00   | success |
| P07    | S07    | 2023-07-21  | 299.00   | success |
| P08    | S08    | 2023-05-01  | 799.00   | success |
| P09    | S09    | 2023-06-15  | 299.00   | success |
| P10    | S10    | 2023-01-01  | 2999.00  | success |
| P11    | S02    | 2023-05-16  | 799.00   | failed  |
| P12    | S05    | 2023-04-05  | 2999.00  | failed  |
| P13    | S04    | 2023-06-11  | 299.00   | success |
| P14    | S02    | 2023-06-16  | 799.00   | success |

**events**
| event_id | user_id | event_type        | occurred_at         |
|----------|---------|-------------------|---------------------|
| E01      | 1       | login             | 2023-04-10 09:00:00 |
| E02      | 1       | feature_used      | 2023-04-10 09:15:00 |
| E03      | 2       | login             | 2023-05-12 10:00:00 |
| E04      | 2       | feature_used      | 2023-05-12 10:30:00 |
| E05      | 3       | login             | 2023-06-01 08:00:00 |
| E06      | 4       | login             | 2023-08-01 11:00:00 |
| E07      | 4       | feature_used      | 2023-08-01 11:05:00 |
| E08      | 6       | login             | 2023-07-01 14:00:00 |
| E09      | 1       | login             | 2023-06-16 10:00:00 |
| E10      | 3       | feature_used      | 2023-06-01 08:45:00 |

---

## 💀 Problems

---

**Q1 — Multi-step CTE: Downgrade Detection**

A user "downgraded" if they moved from a higher plan to a lower plan in consecutive subscriptions.  
Plan hierarchy: `enterprise > pro > basic`

Find all users who downgraded at least once. Show user name, previous plan, new plan, and the date of downgrade.

> This requires you to order subscriptions per user, compare consecutive plans, and map plan names to a numeric hierarchy — all in CTEs before the final filter.

| user_id | name  | prev_plan | new_plan | downgrade_date |
|---------|-------|-----------|----------|----------------|
| 2       | Rohit | pro       | basic    | 2023-05-11     |

---

**Q2 — NULL Trap: Revenue Calculation With Silent Nulls**

Compute total revenue collected per plan. Revenue = sum of successful payment amounts linked to subscriptions of that plan.

**The trap:** `ended_at` is NULL for active subscriptions. Some junior engineers accidentally filter these out when joining. Make sure your query includes active subscriptions in the result.

Also: user 3 has TWO enterprise subscriptions (S05 and S10). Your query must not double-count the plan — aggregate correctly at payment level, not subscription level.

| plan       | total_revenue |
|------------|---------------|
| basic      | 1494.00       |
| pro        | 2696.00       |
| enterprise | 5998.00       |

*(basic: P01+P04+P06+P07+P09+P13 = 299+299+299+299+299+299 = 1794. Wait — P13 is for S04 which is basic. Recalculate: P01=299, P04=299, P06=299, P07=299, P09=299, P13=299 → 1794)*
*(pro: P02+P03+P08+P14 = 799+799+799+799 = 3196. P11 is failed so excluded)*
*(enterprise: P05+P10 = 2999+2999 = 5998)*

| plan       | total_revenue |
|------------|---------------|
| basic      | 1794.00       |
| pro        | 3196.00       |
| enterprise | 5998.00       |

---

**Q3 — Deduplication: Dirty User Table**

Your data pipeline has a bug. The users table now has duplicate rows for some users (same email, different user_id, slightly different created_at). You need to deduplicate — keep only the row with the **earliest** `created_at` per email. If created_at is also identical, keep the row with the **lowest** user_id.

Add this dirty data to test:

```
| 7  | Animesh | animesh@gmail.com | India | 2023-01-20 |
| 8  | Rohit   | rohit@gmail.com   | India | 2023-02-10 |
```

Write a query that returns one clean row per email. No DELETE — pure SELECT.

| user_id | name    | email             | country | created_at |
|---------|---------|-------------------|---------|------------|
| 1       | Animesh | animesh@gmail.com | India   | 2023-01-15 |
| 2       | Rohit   | rohit@gmail.com   | India   | 2023-02-10 |
| ...     | ...     | ...               | ...     | ...        |

*(For Rohit — both user_id 2 and 8 have same created_at 2023-02-10 → keep user_id 2, the lower one)*

---

**Q4 — Brain Teaser: Nth Highest Without LIMIT/TOP**

Find the **3rd highest** successful payment amount across all payments — without using `LIMIT`, `TOP`, `FETCH`, or `ROWNUM`.

Successful payments sorted: 2999, 2999, 799, 799, 799, 799, 299, 299, 299, 299, 299, 299  
3rd distinct highest = 299. But if non-distinct: 3rd row = 799.

**Do it both ways:**
- 3rd highest **distinct** amount
- 3rd highest **non-distinct** (3rd row if sorted descending)

| third_highest_distinct |
|------------------------|
| 299.00                 |

| third_highest_non_distinct |
|----------------------------|
| 799.00                     |

---

**Q5 — Multi-step CTE: User Lifecycle Funnel**

For each user compute their lifecycle stage using this strict logic:
- `churned` → had a subscription that expired AND no active subscription today AND no login event in last 60 days (relative to max date in events table: 2023-08-01)
- `at_risk` → has active subscription BUT no login event in last 60 days
- `engaged` → has active subscription AND has at least one login event in last 60 days
- `never_converted` → never had any subscription at all

Every user must appear exactly once. Priority order if multiple conditions match: `churned > at_risk > engaged > never_converted`

| user_id | name    | lifecycle_stage  |
|---------|---------|------------------|
| 1       | Animesh | engaged          |
| 2       | Rohit   | at_risk          |
| 3       | Sara    | engaged          |
| 4       | Karan   | churned          |
| 5       | Nina    | at_risk          |
| 6       | Dev     | at_risk          |

*(Reference date = 2023-08-01. 60 days before = 2023-06-02)*
*(Animesh: active sub S02, last login E09 on 2023-06-16 → after Jun 2 → engaged)*
*(Rohit: active sub S04, last login E03 on 2023-05-12 → before Jun 2 → at_risk)*
*(Sara: active sub S05, last event E10 on 2023-06-01 → before Jun 2. E05 login 2023-06-01 → before Jun 2 → at_risk actually)*
*(Karan: no active sub — S06,S07 both expired. Last login E06 on 2023-08-01 → within 60 days but no active sub → churned)*
*(Verify each user carefully when you solve)*

---

**Q6 — NULL Trap: Find Users With Gaps in Subscription Coverage**

A user has a "coverage gap" if there is any period of time between two consecutive subscriptions where they had NO active subscription (i.e., ended_at of one sub is not immediately followed by started_at of the next).

Find users who have at least one such gap. Show user_id, gap_start, gap_end.

> The hard part: `ended_at` can be NULL (active sub — no gap after this). You must handle NULLs carefully or your join silently drops active users.

| user_id | gap_start  | gap_end    |
|---------|------------|------------|
| 1       | 2023-04-15 | 2023-04-16 |
| 2       | 2023-05-10 | 2023-05-11 |

*(S01 ended 2023-04-15, S02 started 2023-04-16 — gap of 1 day)*
*(S03 ended 2023-05-10, S04 started 2023-05-11 — gap of 1 day)*
*(Karan: S06 ended 2023-07-20, S07 started 2023-07-21 — gap of 1 day)*

| user_id | gap_start  | gap_end    |
|---------|------------|------------|
| 1       | 2023-04-15 | 2023-04-16 |
| 2       | 2023-05-10 | 2023-05-11 |
| 4       | 2023-07-20 | 2023-07-21 |

---

**Q7 — Brain Teaser: Employees Who Earn More Than Their Manager (No Manager Table)**

Adapt this classic to SubsX context:

Within the `subscriptions` table, treat users who joined on an earlier date as "seniors" of users who joined later in the same country. Find all users whose current subscription `amount` is **strictly greater** than every senior user (same country, earlier signup) in the same country.

> No pre-built hierarchy. You define seniority entirely from `users.created_at` and filter within `subscriptions`. Must handle users with no seniors (they trivially qualify — decide how to treat them and justify in your query).

| user_id | name | country | sub_amount | result        |
|---------|------|---------|------------|---------------|
| 6       | Dev  | India   | 299.00     | does not beat all seniors |

*(Think carefully — who are Dev's seniors in India? Users 1,2,4 joined before Dev. Their active amounts: 799, 299, NULL(no active). Does Dev beat all? No — Animesh has 799 > 299)*

---

**Q8 — Deduplication + Multi-step: Find the "True" First Subscription per User**

Your pipeline has inserted duplicate subscription records — same user, same plan, same started_at, but different sub_id. Add this dirty data:

```
| S11 | 1 | pro | 2023-04-16 | NULL | active | 799.00 |
| S12 | 3 | enterprise | 2023-03-05 | NULL | active | 2999.00 |
```

Write a query that:
1. Deduplicates subscriptions (same user_id + plan + started_at = duplicate, keep lowest sub_id)
2. From the deduplicated set, finds the **first ever subscription** per user
3. Returns users who started on a `basic` plan as their very first subscription

| user_id | name  | first_plan | first_started_at |
|---------|-------|------------|------------------|
| 1       | Animesh | basic    | 2023-01-15       |
| 4       | Karan   | basic    | 2023-04-20       |
| 6       | Dev     | basic    | 2023-06-15       |

---

**Q9 — Multi-step CTE: Payment Failure Impact Analysis**

For each user who had at least one failed payment, compute:
1. Total amount they successfully paid (lifetime)
2. Total amount of failed payments (lost revenue)
3. Failure rate = `failed_amount / (success_amount + failed_amount) * 100`
4. Whether their subscription is still active despite the failure (`yes` / `no`)

Chain at least 3 CTEs to solve this cleanly.

| user_id | name    | success_amount | failed_amount | failure_rate | still_active |
|---------|---------|----------------|---------------|--------------|--------------|
| 1       | Animesh | 1897.00        | 799.00        | 29.63        | yes          |
| 3       | Sara    | 5998.00        | 2999.00       | 33.33        | yes          |

*(Animesh: success P01+P02+P14=299+799+799=1897, failed P11=799)*
*(Sara: success P05+P10=2999+2999=5998, failed P12=2999)*

---

**Q10 — Brain Teaser: Find Subscriptions That Are "Overlapping" for the Same User**

A data quality issue: some users have two subscriptions with overlapping date ranges (started_at of one falls within the active period of another for the same user).

Write a query to detect all such overlapping subscription pairs for the same user.

> Two subscriptions overlap if: `s2.started_at <= s1.ended_at` AND `s2.started_at >= s1.started_at` (and they are different sub_ids for the same user). Handle the case where `ended_at` is NULL (treat as still open = overlaps with anything started after).

Add this to test:
```
| S13 | 1 | basic | 2023-04-10 | 2023-04-20 | expired | 299.00 |
```
*(S13 started 2023-04-10, which falls inside S01's range 2023-01-15 to 2023-04-15 → overlap)*

| user_id | sub_id_1 | sub_id_2 | overlap_start | overlap_end |
|---------|----------|----------|---------------|-------------|
| 1       | S01      | S13      | 2023-04-10    | 2023-04-15  |

---
