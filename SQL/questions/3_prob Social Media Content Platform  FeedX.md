# SQL Daily Drill — Day 3
### 🔥 Level: FAANG Interview

---

## 🏢 Scenario: Social Media Content Platform — FeedX

Think Instagram / YouTube analytics backend.

---

## 📦 Tables & Sample Data

**users**
| user_id | username  | country | signup_date | is_creator |
|---------|-----------|---------|-------------|------------|
| 1       | animesh_k | India   | 2021-03-10  | true       |
| 2       | rohit_v   | India   | 2020-07-15  | true       |
| 3       | sara_m    | USA     | 2022-01-20  | false      |
| 4       | jay_p     | India   | 2021-11-05  | true       |
| 5       | nina_r    | UK      | 2023-05-01  | false      |
| 6       | karan_s   | India   | 2020-03-22  | false      |

**posts**
| post_id | user_id | post_type | posted_at           | caption                  |
|---------|---------|-----------|---------------------|--------------------------|
| 201     | 1       | video     | 2024-01-05 10:00:00 | My first vlog            |
| 202     | 2       | image     | 2024-01-06 12:00:00 | Sunset vibes             |
| 203     | 1       | image     | 2024-01-10 09:00:00 | Morning routine          |
| 204     | 4       | video     | 2024-01-15 18:00:00 | Cooking tutorial         |
| 205     | 2       | video     | 2024-02-01 11:00:00 | Travel diary             |
| 206     | 1       | image     | 2024-02-10 08:00:00 | Gym progress             |
| 207     | 4       | image     | 2024-03-01 14:00:00 | Product review           |
| 208     | 2       | video     | 2024-03-15 16:00:00 | City guide               |

**interactions**
| interaction_id | user_id | post_id | type    | interacted_at       |
|----------------|---------|---------|---------|---------------------|
| 1              | 3       | 201     | like    | 2024-01-05 10:30:00 |
| 2              | 5       | 201     | like    | 2024-01-05 11:00:00 |
| 3              | 6       | 201     | comment | 2024-01-05 11:15:00 |
| 4              | 3       | 202     | like    | 2024-01-06 13:00:00 |
| 5              | 6       | 202     | like    | 2024-01-06 14:00:00 |
| 6              | 5       | 203     | comment | 2024-01-10 09:30:00 |
| 7              | 3       | 204     | like    | 2024-01-15 19:00:00 |
| 8              | 6       | 204     | comment | 2024-01-15 19:30:00 |
| 9              | 5       | 204     | like    | 2024-01-16 08:00:00 |
| 10             | 3       | 205     | like    | 2024-02-01 12:00:00 |
| 11             | 6       | 205     | comment | 2024-02-01 12:30:00 |
| 12             | 5       | 206     | like    | 2024-02-10 09:00:00 |
| 13             | 3       | 207     | comment | 2024-03-01 15:00:00 |
| 14             | 6       | 208     | like    | 2024-03-15 17:00:00 |
| 15             | 3       | 208     | comment | 2024-03-15 17:30:00 |

**follows**
| follower_id | followee_id | followed_at |
|-------------|-------------|-------------|
| 3           | 1           | 2024-01-01  |
| 5           | 1           | 2024-01-02  |
| 6           | 1           | 2024-01-03  |
| 3           | 2           | 2024-01-01  |
| 6           | 2           | 2024-01-04  |
| 5           | 4           | 2024-01-05  |
| 3           | 4           | 2024-01-06  |

---

## 📋 Problems

---

**Q1 — GROUP BY + HAVING**

Find creators who have posted more than 2 times AND received more than 5 total interactions across all their posts. Show creator user_id, total posts, total interactions.

| user_id | total_posts | total_interactions |
|---------|-------------|---------------------|
| 1       | 3           | 6                   |
| 2       | 3           | 6                   |

---

**Q2 — Engagement Rate per Post**

For each post compute engagement rate = `total interactions / total followers of that creator * 100`. Show post_id, creator, engagement_rate. Sort descending.

| post_id | user_id | total_interactions | creator_followers | engagement_rate |
|---------|---------|--------------------|-------------------|-----------------|
| 204     | 4       | 3                  | 2                 | 150.00          |
| 201     | 1       | 3                  | 3                 | 100.00          |

---

**Q3 — LAG: Days Between Consecutive Posts per Creator**

For each creator, list posts chronologically with the number of days since their previous post. NULL for first post.

| user_id | post_id | posted_at           | days_since_last_post |
|---------|---------|---------------------|----------------------|
| 1       | 201     | 2024-01-05 10:00:00 | NULL                 |
| 1       | 203     | 2024-01-10 09:00:00 | 5                    |
| 1       | 206     | 2024-02-10 08:00:00 | 31                   |

---

**Q4 — Running Total of Interactions per Creator Over Time**

For each creator, show cumulative total interactions received across their posts in chronological order.

| user_id | post_id | posted_at           | post_interactions | cumulative_interactions |
|---------|---------|---------------------|-------------------|--------------------------|
| 1       | 201     | 2024-01-05 10:00:00 | 3                 | 3                        |
| 1       | 203     | 2024-01-10 09:00:00 | 1                 | 4                        |
| 1       | 206     | 2024-02-10 08:00:00 | 1                 | 5                        |

---

**Q5 — CTE: Top Performing Post per Creator**

Using a CTE, find the single post with highest interactions for each creator. Show ties.

| user_id | post_id | post_type | total_interactions |
|---------|---------|-----------|--------------------|
| 1       | 201     | video     | 3                  |
| 2       | 205     | video     | 2                  |
| 4       | 204     | video     | 3                  |

---

**Q6 — Recursive CTE: Follow Chain Depth**

Follows can be chained: if A follows B and B follows C, A is indirectly 2 hops from C. For user_id = 3, find all users reachable within 2 follow hops and the hop depth.

| start_user | reached_user | depth |
|------------|--------------|-------|
| 3          | 1            | 1     |
| 3          | 2            | 1     |
| 3          | 4            | 1     |

*(At depth 2, extend: who do 1, 2, 4 follow? Add follow data to test deeper)*

---

**Q7 — Correlated Subquery: Creators Whose Latest Post Got Zero Interactions**

Find creators whose most recently posted content received no interactions at all.

| user_id | username | latest_post_id | posted_at           |
|---------|----------|----------------|---------------------|
| 4       | jay_p    | 207            | 2024-03-01 14:00:00 |

*(post 207 has interaction 13 — adjust data or verify your logic)*

---

**Q8 — Subquery in FROM: Month with Highest New Creator Signups**

Find the month with the highest number of new creator accounts created.

| month   | new_creators |
|---------|--------------|
| 2021-03 | 1            |

---

**Q9 — CASE WHEN Pivot: Interaction Breakdown per Post**

For each post show likes and comments as separate columns.

| post_id | user_id | likes | comments |
|---------|---------|-------|----------|
| 201     | 1       | 2     | 1        |
| 202     | 2       | 2     | 0        |
| 203     | 1       | 0     | 1        |
| 204     | 4       | 2     | 1        |
| 205     | 2       | 1     | 1        |

---

**Q10 — NTILE: Classify Posts by Interaction Volume**

Divide all posts into 4 quartiles by total interactions. Label: Cold / Warm / Hot / Viral.

| post_id | total_interactions | quartile | label  |
|---------|--------------------|----------|--------|
| 203     | 1                  | 1        | Cold   |
| 206     | 1                  | 1        | Cold   |
| 202     | 2                  | 2        | Warm   |
| 205     | 2                  | 2        | Warm   |
| 201     | 3                  | 3        | Hot    |
| 204     | 3                  | 4        | Viral  |

---

**Q11 — Self JOIN: Users Who Interacted with the Same Post**

Find all pairs of users who both interacted with the same post. Each pair once only.

| user_1 | user_2 | post_id |
|--------|--------|---------|
| 3      | 5      | 201     |
| 3      | 6      | 201     |
| 5      | 6      | 201     |
| 3      | 6      | 202     |

---

**Q12 — DENSE_RANK: Rank Creators by Total Interactions Received per Country**

Rank creators by total interactions within their country. Show top 1 per country.

| country | user_id | username  | total_interactions | rnk |
|---------|---------|-----------|--------------------|-----|
| India   | 1       | animesh_k | 5                  | 1   |

---

**Q13 — EXISTS: Creators with No Followers**

Find creators who have never been followed by anyone.

| user_id | username |
|---------|----------|
| *(add a creator with no follows to test)* |

---

**Q14 — Sessionization: User Interaction Sessions**

Group each user's interactions into sessions where gap between consecutive interactions is under 1 hour. Assign session_id per user.

| user_id | interaction_id | interacted_at       | session_id |
|---------|----------------|---------------------|------------|
| 3       | 1              | 2024-01-05 10:30:00 | 1          |
| 3       | 4              | 2024-01-06 13:00:00 | 2          |
| 3       | 7              | 2024-01-15 19:00:00 | 3          |
| 3       | 10             | 2024-02-01 12:00:00 | 4          |

---

**Q15 — PERCENT_RANK: Post Engagement Percentile within Post Type**

For each post compute its engagement percentile among posts of the same type (video vs image).

| post_id | post_type | total_interactions | pct_rank |
|---------|-----------|--------------------|----------|
| 201     | video     | 3                  | 1.0      |
| 204     | video     | 3                  | 1.0      |
| 205     | video     | 2                  | 0.0      |
| 202     | image     | 2                  | 1.0      |
| 207     | image     | 1                  | 0.0      |

---

**Q16 — 7-Day Rolling Interaction Count Platform-Wide**

Compute total interactions per day and 7-day rolling sum across the platform.

| date       | daily_interactions | rolling_7day |
|------------|--------------------|--------------|
| 2024-01-05 | 3                  | 3            |
| 2024-01-06 | 2                  | 5            |
| 2024-01-10 | 1                  | 6            |
| 2024-01-15 | 3                  | 9            |

---

**Q17 — Median Interactions per Creator Without MEDIAN()**

Compute median interaction count per post for each creator using only window functions.

| user_id | username  | median_interactions |
|---------|-----------|---------------------|
| 1       | animesh_k | 1.0                 |
| 2       | rohit_v   | 2.0                 |
| 4       | jay_p     | 2.0                 |

---

**Q18 — Churn: Creators Who Haven't Posted in 45+ Days**

Relative to latest date in dataset, find creators whose last post was more than 45 days ago.

| user_id | username | last_posted_at      |
|---------|----------|---------------------|
| 1       | animesh_k| 2024-02-10 08:00:00 |
| 4       | jay_p    | 2024-03-01 14:00:00 |

---

**Q19 — Gaps & Islands: Creator Posting Streaks**

A creator has a "posting streak" if they post on consecutive days. Find each creator's longest streak of consecutive posting days.

| user_id | username  | longest_streak_days |
|---------|-----------|---------------------|
| 1       | animesh_k | 1                   |
| 2       | rohit_v   | 1                   |

*(Add daily posts in data to properly test streak logic)*

---

**Q20 — Follower Growth Rate per Creator Month over Month**

For each creator, compute how many new followers they gained each month and the month-over-month growth rate compared to previous month.

| user_id | month   | new_followers | prev_month_followers | growth_rate_pct |
|---------|---------|---------------|----------------------|-----------------|
| 1       | 2024-01 | 3             | NULL                 | NULL            |
| 2       | 2024-01 | 2             | NULL                 | NULL            |
| 4       | 2024-01 | 2             | NULL                 | NULL            |

---
