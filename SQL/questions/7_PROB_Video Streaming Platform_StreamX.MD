# SQL Daily Drill — Day 7
### 💀 Level: Brutal — Product-Based Company Interview

**Focus:** Retention & Cohort analysis · Pivoting without PIVOT keyword · Graph-style queries · Tricky aggregation conditions · Date arithmetic traps · Multi-condition ranking  
**Nothing repeated from Days 1–6.**

---

## 🎬 Scenario: Video Streaming Platform — StreamX

Think Netflix / Hotstar / Prime Video analytics backend.

---

## 📦 Tables & Sample Data

**users**
| user_id | name     | country | plan      | joined_date |
|---------|----------|---------|-----------|-------------|
| 1       | Animesh  | India   | premium   | 2023-01-10  |
| 2       | Rohit    | India   | basic     | 2023-01-15  |
| 3       | Sara     | USA     | premium   | 2023-02-01  |
| 4       | Karan    | India   | basic     | 2023-02-10  |
| 5       | Nina     | UK      | premium   | 2023-03-05  |
| 6       | Dev      | India   | basic     | 2023-03-20  |
| 7       | Priya    | India   | premium   | 2023-04-01  |
| 8       | Alex     | USA     | basic     | 2023-04-15  |

**content**
| content_id | title               | genre     | release_date | duration_min | language |
|------------|---------------------|-----------|--------------|--------------|----------|
| C01        | Dark Waters         | Thriller  | 2023-01-01   | 122          | English  |
| C02        | Dil Bechara         | Romance   | 2023-01-05   | 108          | Hindi    |
| C03        | The Crown           | Drama     | 2023-02-10   | 55           | English  |
| C04        | Mirzapur S3         | Crime     | 2023-02-15   | 48           | Hindi    |
| C05        | Cosmos              | Documentary | 2023-03-01 | 60           | English  |
| C06        | Panchayat S2        | Comedy    | 2023-03-10   | 40           | Hindi    |
| C07        | Oppenheimer         | Thriller  | 2023-04-05   | 180          | English  |
| C08        | Lust Stories 2      | Drama     | 2023-04-20   | 90           | Hindi    |

**watch_history**
| watch_id | user_id | content_id | watched_at          | watch_duration_min | completed |
|----------|---------|------------|---------------------|--------------------|-----------|
| W01      | 1       | C01        | 2023-01-15 20:00:00 | 122                | true      |
| W02      | 1       | C02        | 2023-01-20 21:00:00 | 108                | true      |
| W03      | 2       | C01        | 2023-01-16 19:00:00 | 60                 | false     |
| W04      | 2       | C04        | 2023-02-20 20:00:00 | 48                 | true      |
| W05      | 3       | C03        | 2023-02-15 18:00:00 | 55                 | true      |
| W06      | 3       | C05        | 2023-03-05 10:00:00 | 60                 | true      |
| W07      | 4       | C02        | 2023-02-12 21:00:00 | 50                 | false     |
| W08      | 4       | C06        | 2023-03-15 20:00:00 | 40                 | true      |
| W09      | 5       | C07        | 2023-04-10 17:00:00 | 180                | true      |
| W10      | 5       | C08        | 2023-04-25 21:00:00 | 45                 | false     |
| W11      | 6       | C04        | 2023-03-25 20:00:00 | 48                 | true      |
| W12      | 6       | C06        | 2023-04-01 21:00:00 | 40                 | true      |
| W13      | 7       | C07        | 2023-04-10 19:00:00 | 90                 | false     |
| W14      | 7       | C08        | 2023-04-22 20:00:00 | 90                 | true      |
| W15      | 1       | C07        | 2023-04-08 18:00:00 | 180                | true      |
| W16      | 2       | C06        | 2023-04-05 21:00:00 | 40                 | true      |
| W17      | 3       | C07        | 2023-04-12 20:00:00 | 180                | true      |
| W18      | 8       | C01        | 2023-04-16 20:00:00 | 80                 | false     |
| W19      | 8       | C05        | 2023-04-20 10:00:00 | 60                 | true      |
| W20      | 1       | C08        | 2023-04-28 21:00:00 | 90                 | true      |

**ratings**
| rating_id | user_id | content_id | score | rated_at   |
|-----------|---------|------------|-------|------------|
| R01       | 1       | C01        | 5     | 2023-01-16 |
| R02       | 1       | C02        | 4     | 2023-01-21 |
| R03       | 2       | C01        | 3     | 2023-01-17 |
| R04       | 3       | C03        | 5     | 2023-02-16 |
| R05       | 3       | C05        | 4     | 2023-03-06 |
| R06       | 4       | C06        | 5     | 2023-03-16 |
| R07       | 5       | C07        | 5     | 2023-04-11 |
| R08       | 6       | C04        | 4     | 2023-03-26 |
| R09       | 7       | C08        | 3     | 2023-04-23 |
| R10       | 1       | C07        | 5     | 2023-04-09 |
| R11       | 3       | C07        | 4     | 2023-04-13 |
| R12       | 8       | C05        | 5     | 2023-04-21 |

---

## 💀 Problems

---

**Q1 — Cohort Retention Analysis**

A cohort is defined by the month a user joined (`joined_date`).  
For each cohort, compute how many users were still "active" (had at least one watch event) in each subsequent month after joining.

Show cohort month, activity month, users active, and retention rate % (relative to cohort size).

> This is one of the most asked questions at Netflix, Hotstar, and Spotify data interviews. You cannot use LAG here — think about self-joining cohort membership against monthly activity.

| cohort_month | activity_month | cohort_size | active_users | retention_pct |
|--------------|----------------|-------------|--------------|---------------|
| 2023-01      | 2023-01        | 2           | 2            | 100.00        |
| 2023-01      | 2023-02        | 2           | 1            | 50.00         |
| 2023-01      | 2023-04        | 2           | 2            | 100.00        |
| 2023-02      | 2023-02        | 2           | 2            | 100.00        |
| 2023-02      | 2023-03        | 2           | 2            | 100.00        |
| 2023-02      | 2023-04        | 2           | 1            | 50.00         |

*(Cohort Jan: users 1 and 2. Jan activity: both watched. Feb: only user 1 has no Feb watch — user 2 watched C04 in Feb → only user 2 active. Apr: user 1 watched C07,C08. user 2 watched C06 → both active)*
*(Verify all cohorts carefully when solving)*

---

**Q2 — Pivot Without PIVOT: Genre Watch Matrix per Country**

Show total completed watches per genre as separate columns, grouped by country. Do not use the PIVOT keyword — use CASE WHEN only.

| country | Thriller | Romance | Drama | Crime | Documentary | Comedy |
|---------|----------|---------|-------|-------|-------------|--------|
| India   | 2        | 1       | 0     | 2     | 0           | 3      |
| USA     | 2        | 0       | 1     | 0     | 2           | 0      |
| UK      | 1        | 0       | 0     | 0     | 0           | 0      |

*(India users: 1,2,4,6,7. Count completed watches per genre for these users only)*
*(User 1: C01 Thriller✓, C02 Romance✓, C07 Thriller✓, C08 Drama✓)*
*(User 2: C04 Crime✓, C06 Comedy✓)*
*(User 4: C06 Comedy✓)*
*(User 6: C04 Crime✓, C06 Comedy✓)*
*(User 7: C08 Drama✓)*
*(India: Thriller=2, Romance=1, Drama=2, Crime=2, Comedy=3)*
*(USA users: 3,8. User3: C03 Drama✓, C05 Doc✓, C07 Thriller✓. User8: C05 Doc✓)*
*(USA: Thriller=1, Drama=1, Documentary=2)*

| country | Thriller | Romance | Drama | Crime | Documentary | Comedy |
|---------|----------|---------|-------|-------|-------------|--------|
| India   | 2        | 1       | 2     | 2     | 0           | 3      |
| USA     | 1        | 0       | 1     | 0     | 2           | 0      |
| UK      | 1        | 0       | 0     | 0     | 0           | 0      |

---

**Q3 — Graph-style Query: Users Who Watched the Exact Same Set of Content**

Find pairs of users who have watched the **exact same set of content IDs** — not just overlap, but a perfect match (same titles, nothing extra, nothing missing on either side).

> This requires thinking in terms of set equality — count of matches = count of total distinct content per user for both users simultaneously.

| user_1 | user_2 | shared_content_count |
|--------|--------|----------------------|
| *(none in this dataset — all users have unique watch sets. Add users with identical watch history to your local data to test)* |

---

**Q4 — Completion Rate Trap: Content That Performs Differently by Plan**

For each content item, compute completion rate separately for `premium` and `basic` plan users.  
**The trap:** Some content has been watched only by one plan type — the other plan's rate must show as NULL, not 0. Do not use COALESCE to hide this.

| content_id | title       | premium_completion_rate | basic_completion_rate |
|------------|-------------|-------------------------|-----------------------|
| C01        | Dark Waters | 1.00                    | 0.00                  |
| C02        | Dil Bechara | 1.00                    | 0.00                  |
| C03        | The Crown   | 1.00                    | NULL                  |
| C04        | Mirzapur S3 | NULL                    | 1.00                  |
| C05        | Cosmos      | 1.00                    | 1.00                  |
| C06        | Panchayat S2| NULL                    | 1.00                  |
| C07        | Oppenheimer | 0.67                    | NULL                  |
| C08        | Lust Stories| 1.00                    | NULL                  |

*(C07 watched by users 5(premium✓), 7(premium✗), 1(premium✓), 3(premium✓) → 3/4? Check: W09 user5 completed, W13 user7 not completed, W15 user1 completed, W17 user3 completed → 3 completed out of 4 = 0.75)*

| content_id | title        | premium_completion_rate | basic_completion_rate |
|------------|--------------|-------------------------|-----------------------|
| C01        | Dark Waters  | 1.00                    | 0.00                  |
| C02        | Dil Bechara  | 1.00                    | 0.00                  |
| C03        | The Crown    | 1.00                    | NULL                  |
| C04        | Mirzapur S3  | NULL                    | 1.00                  |
| C05        | Cosmos       | 1.00                    | 1.00                  |
| C06        | Panchayat S2 | NULL                    | 1.00                  |
| C07        | Oppenheimer  | 0.75                    | NULL                  |
| C08        | Lust Stories | 0.50                    | NULL                  |

*(C08: W14 user7 premium completed, W10 user5 premium not completed, W20 user1 premium completed → 2/3 = 0.67)*

| content_id | title        | premium_completion_rate | basic_completion_rate |
|------------|--------------|-------------------------|-----------------------|
| C07        | Oppenheimer  | 0.75                    | NULL                  |
| C08        | Lust Stories | 0.67                    | NULL                  |

*(Compute all rows carefully when solving — use the data as ground truth)*

---

**Q5 — Date Arithmetic Trap: Users Who Watched Content Released Before They Joined**

Find users who watched content that was released **strictly before their own joining date**. This catches users who may have used a trial or had data integrity issues.

> The trap: release_date vs joined_date comparison is straightforward but many miss that `watched_at` is irrelevant here — it's the content release vs user join that matters.

| user_id | name    | joined_date | content_id | title       | release_date |
|---------|---------|-------------|------------|-------------|--------------|
| 1       | Animesh | 2023-01-10  | *(none — C01 released Jan 1, Animesh joined Jan 10 → C01 released before join ✓)* |

*(C01 released 2023-01-01, Animesh joined 2023-01-10 → C01 is before join, Animesh watched C01 via W01 → qualifies)*
*(C02 released 2023-01-05, before Animesh join Jan 10 → also qualifies)*
*(Check all users against all their watches)*

| user_id | name    | joined_date | content_id | title       | release_date |
|---------|---------|-------------|------------|-------------|--------------|
| 1       | Animesh | 2023-01-10  | C01        | Dark Waters | 2023-01-01   |
| 1       | Animesh | 2023-01-10  | C02        | Dil Bechara | 2023-01-05   |
| 2       | Rohit   | 2023-01-15  | C01        | Dark Waters | 2023-01-01   |
| 2       | Rohit   | 2023-01-15  | C02        | Dil Bechara | 2023-01-05   |

---

**Q6 — Multi-step CTE: Identify Binge-Watching Sessions**

A "binge session" = a user watches 3 or more content items within any 24-hour rolling window.

Chain your CTEs:
1. Order watches per user by `watched_at`
2. For each watch, count how many other watches by the same user fall within 24 hours after it
3. Flag users who have at least one such window with 3+ watches

> Do not use LAG/LEAD. Think about self-joining watch_history on user_id with a time range condition.

| user_id | name    | binge_session_start     | content_count_in_24h |
|---------|---------|-------------------------|----------------------|
| *(With this dataset gaps between watches are days apart — add same-day watches to test. Structure your query correctly first)* |

---

**Q7 — Brain Teaser: Find Content With Ratings But Zero Completed Watches**

Find content that has received at least one rating but has zero **completed** watches.  
The trap: a user can rate something they didn't finish — this is a data quality red flag.

| content_id | title | total_ratings | completed_watches |
|------------|-------|---------------|-------------------|
| *(check: every rated content in ratings table — does it have a completed watch?)*
*(R03: user2 rated C01, W03 user2 watched C01 but completed=false → C01 has other completed watches from user1 so C01 still has completed=true overall)*
*(Go through each content systematically)* |

*(All rated content in this dataset has at least one completed watch elsewhere — add a rating for content with no completed watch to properly test)*

---

**Q8 — Deduplication Trap: Same User Watched Same Content Twice**

Your pipeline accidentally inserted duplicate watch events — same user, same content, same `watched_at` timestamp, different `watch_id`.

Add this dirty data:
```
W21 | 1 | C01 | 2023-01-15 20:00:00 | 122 | true
W22 | 3 | C07 | 2023-04-12 20:00:00 | 180 | true
```

Write a query that:
1. Deduplicates — keep only the lowest `watch_id` per (user_id, content_id, watched_at)
2. From the clean data, compute total unique content watched per user

| user_id | name    | unique_content_watched |
|---------|---------|------------------------|
| 1       | Animesh | 4                      |
| 2       | Rohit   | 3                      |
| 3       | Sara    | 4                      |
| 4       | Karan   | 2                      |
| 5       | Nina    | 2                      |
| 6       | Dev     | 2                      |
| 7       | Priya   | 2                      |
| 8       | Alex    | 2                      |

---

**Q9 — Multi-step CTE: Content Recommendation Gap**

Find users who have watched content in genre X but have **never** watched any content in genre Y, where genre Y has higher average rating than genre X on the platform.

Steps to chain:
1. Compute avg rating per genre platform-wide
2. Find genre pairs where genre Y avg > genre X avg
3. Find users who watched genre X but have no watch record in genre Y
4. Return user + the genre they're missing + the avg rating gap

> This is a multi-hop reasoning problem. Most candidates freeze on step 3.

| user_id | watched_genre | missing_higher_rated_genre | genre_avg | missing_genre_avg |
|---------|---------------|----------------------------|-----------|-------------------|
| *(compute genre averages first from ratings table, then find the gaps)* |

Genre averages from ratings:
| genre       | avg_rating |
|-------------|------------|
| Thriller    | 4.25       |
| Romance     | 4.00       |
| Drama       | 4.00       |
| Crime       | 4.00       |
| Documentary | 4.50       |
| Comedy      | 5.00       |

*(Comedy avg=5.0 is highest. Documentary=4.5. Then find users who watched non-comedy genres but never watched Comedy)*

---

**Q10 — Brain Teaser: The Loyal Completer**

Find users who satisfy ALL of the following simultaneously:
1. Have watched at least 3 distinct content items
2. Have a completion rate (completed watches / total watches) of 100%
3. Have rated every single content they watched (no unrated watches)
4. All their watches are of content released within 30 days of their own `joined_date`

> Condition 4 is the killer. Most candidates get 1-3 right and miss 4 entirely because it requires joining back to content and doing date math inside an aggregation filter.

| user_id | name | total_watched | completion_rate | all_rated | all_within_30_days |
|---------|------|---------------|-----------------|-----------|---------------------|
| *(go through each user methodically — this likely returns 0 rows with this dataset. Extend data or identify which condition each user fails)* |

---
