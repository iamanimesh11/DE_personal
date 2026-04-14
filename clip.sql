-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    signup_date DATE,
    is_creator BOOLEAN
);

-- POSTS TABLE
CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    post_type VARCHAR(20),
    posted_at TIMESTAMP,
    caption TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- INTERACTIONS TABLE
CREATE TABLE interactions (
    interaction_id INT PRIMARY KEY,
    user_id INT,
    post_id INT,
    type VARCHAR(20),
    interacted_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

-- FOLLOWS TABLE
CREATE TABLE follows (
    follower_id INT,
    followee_id INT,
    followed_at DATE,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (followee_id) REFERENCES users(user_id)
);


-- USERS
INSERT INTO users VALUES
(1, 'animesh_k', 'India', '2021-03-10', TRUE),
(2, 'rohit_v', 'India', '2020-07-15', TRUE),
(3, 'sara_m', 'USA', '2022-01-20', FALSE),
(4, 'jay_p', 'India', '2021-11-05', TRUE),
(5, 'nina_r', 'UK', '2023-05-01', FALSE),
(6, 'karan_s', 'India', '2020-03-22', FALSE);

-- POSTS
INSERT INTO posts VALUES
(201, 1, 'video', '2024-01-05 10:00:00', 'My first vlog'),
(202, 2, 'image', '2024-01-06 12:00:00', 'Sunset vibes'),
(203, 1, 'image', '2024-01-10 09:00:00', 'Morning routine'),
(204, 4, 'video', '2024-01-15 18:00:00', 'Cooking tutorial'),
(205, 2, 'video', '2024-02-01 11:00:00', 'Travel diary'),
(206, 1, 'image', '2024-02-10 08:00:00', 'Gym progress'),
(207, 4, 'image', '2024-03-01 14:00:00', 'Product review'),
(208, 2, 'video', '2024-03-15 16:00:00', 'City guide');

-- INTERACTIONS
INSERT INTO interactions VALUES
(1, 3, 201, 'like', '2024-01-05 10:30:00'),
(2, 5, 201, 'like', '2024-01-05 11:00:00'),
(3, 6, 201, 'comment', '2024-01-05 11:15:00'),
(4, 3, 202, 'like', '2024-01-06 13:00:00'),
(5, 6, 202, 'like', '2024-01-06 14:00:00'),
(6, 5, 203, 'comment', '2024-01-10 09:30:00'),
(7, 3, 204, 'like', '2024-01-15 19:00:00'),
(8, 6, 204, 'comment', '2024-01-15 19:30:00'),
(9, 5, 204, 'like', '2024-01-16 08:00:00'),
(10, 3, 205, 'like', '2024-02-01 12:00:00'),
(11, 6, 205, 'comment', '2024-02-01 12:30:00'),
(12, 5, 206, 'like', '2024-02-10 09:00:00'),
(13, 3, 207, 'comment', '2024-03-01 15:00:00');
-- (14, 6, 208, 'like', '2024-03-15 17:00:00'),
-- (15, 3, 208, 'comment', '2024-03-15 17:30:00');

-- FOLLOWS
INSERT INTO follows VALUES
(3, 1, '2024-01-01'),
(5, 1, '2024-01-02'),
(6, 1, '2024-01-03'),
(3, 2, '2024-01-01'),
(6, 2, '2024-01-04'),
(5, 4, '2024-01-05'),
(3, 4, '2024-01-06');


-- q1

-- select * from posts;

-- with cte as (
-- select i.post_id,count(i.interaction_id) as total_interactions ,p.user_id
-- from interactions i 
-- join posts p 
-- on i.post_id=p.post_id
-- group by i.post_id
-- )

-- select user_id,count(post_id) as total_posts ,sum(total_interactions) as t 
-- from cte 
-- group by user_id
-- having total_posts>2 and t>5;

-- SELECT 
--     p.user_id,
--     COUNT(DISTINCT p.post_id) AS total_posts,
--     COUNT(i.interaction_id) AS total_interactions
-- FROM posts p
-- LEFT JOIN interactions i 
--     ON p.post_id = i.post_id
-- GROUP BY p.user_id
-- HAVING 
--     COUNT(DISTINCT p.post_id) > 2
--     AND COUNT(i.interaction_id) > 5;

-- q2

-- WITH post_interactions AS (
--     SELECT 
--         p.post_id,
--         p.user_id,
--         COUNT(i.interaction_id) AS total_interactions
--     FROM posts p
--     LEFT JOIN interactions i 
--         ON p.post_id = i.post_id
--     GROUP BY p.post_id, p.user_id
-- ),
-- followers_cte AS (
--     SELECT 
--         followee_id,
--         COUNT(*) AS total_followers
--     FROM follows
--     GROUP BY followee_id
-- )

-- SELECT 
--     pi.post_id,
--     pi.user_id,
--     pi.total_interactions,
--     f.total_followers,
--     (pi.total_interactions * 100.0) / NULLIF(f.total_followers, 0) AS engagement
-- FROM post_interactions pi
-- JOIN followers_cte f 
--     ON f.followee_id = pi.user_id;



-- q3 

-- select * from posts ;

-- select user_id,post_id,posted_at,
-- datediff(posted_at,
-- LAG(posted_at) over (partition by user_id order by posted_at) )
-- as days_since_last_post
-- from posts 


-- Q4


-- select * from posts;
-- select * from interactions;


-- select p.user_id,p.post_id ,
-- p.posted_at,
-- count(i.interaction_id) as total_interactions,
-- sum(count(i.interaction_id)) 
--         over (partition by p.user_id order by p.posted_at) as cum_sum
-- from posts p 
-- join interactions i 
-- on p.post_id=i.post_id
-- GROUP by p.user_id,p.post_id,p.posted_at



-- q5 

-- WITH RankedPosts AS (
--     SELECT 
--         p.user_id, 
--         p.post_id, 
--         p.post_type, 
--         COUNT(i.interaction_id) AS total_interactions,
--         -- ROW_NUMBER ensures a unique "1" for every user_id
--         ROW_NUMBER() OVER (
--             PARTITION BY p.user_id 
--             ORDER BY COUNT(i.interaction_id) DESC, p.posted_at ASC
--         ) as rn
--     FROM posts p
--     LEFT JOIN interactions i ON p.post_id = i.post_id
--     GROUP BY p.user_id, p.post_id, p.post_type, p.posted_at
-- )

-- SELECT 
--     user_id, 
--     post_id, 
--     post_type, 
--     total_interactions
-- FROM RankedPosts
-- WHERE rn = 1;



-- q7

-- select p.post_id, p.user_id,u.username,p.posted_at
-- from posts p 
-- left join interactions i 
-- on p.post_id=i.post_id
-- join users u 
-- on p.user_id=u.user_id
-- where i.interaction_id is NULL 



-- SELECT *
-- FROM posts p
-- WHERE NOT EXISTS (
--     SELECT 1 
--     FROM interactions i 
--     WHERE i.post_id = p.post_id
-- );


-- q8
-- SELECT 
--     DATE_FORMAT(signup_date, '%Y-%m') AS month, 
--     COUNT(user_id) AS new_creators
-- FROM users
-- WHERE is_creator = 'true'
-- GROUP BY month
-- ORDER BY new_creators DESC, month ASC





-- q9 

-- SELECT 
--     p.user_id,
--     p.post_id,
--     SUM(CASE WHEN i.type = 'like' THEN 1 ELSE 0 END) AS total_likes,
--     SUM(CASE WHEN i.type = 'comment' THEN 1 ELSE 0 END) AS total_comments
-- FROM posts p
-- LEFT JOIN interactions i ON p.post_id = i.post_id
-- GROUP BY p.user_id, p.post_id
-- ORDER BY p.post_id;


-- q 10

-- with cte as (

-- select post_id,COUNT(interaction_id) as total_intertactions
-- from interactions

-- GROUP by post_id

-- )

-- select post_id,total_intertactions,
-- CASE NTILE(4) OVER (ORDER BY total_intertactions)
--             WHEN 1 THEN 'Cold'
--             WHEN 2 THEN 'Warm'
--             WHEN 3 THEN 'Hot'
--             WHEN 4 THEN 'Viral'

--             ELSE 'High'
--       END AS tier

-- from cte 


-- q11 Find all pairs of users who both interacted with the same post. Each pair once only.

-- select * from interactions;

-- select DISTINCT 
-- u.user_id as user1,v.user_id,u.post_id as user2
-- from interactions u 
-- join interactions v 
-- on u.post_id=v.post_id
-- where u.user_id!=v.user_id
-- and u.user_id<v.user_id


-- q12

-- with cte as (
-- select u.user_id,u.username ,u.country,
-- count(i.interaction_id) as total_intertactions
-- from users u 
-- join posts p 
-- on u.user_id=p.user_id
-- join interactions i 
-- on p.post_id=i.post_id
-- GROUP by u.user_id,u.country
-- )
-- select * from (
-- select *,
-- dense_Rank()  over (PARTITION by country 
-- ORDER by total_intertactions desc  ) as rn 
-- from cte 
-- ) a  
-- where rn=1


-- q13
-- select * from users ;

-- select * from follows ;

-- select u.user_id
-- from users  u 
-- left join follows f  
-- on u.user_id=f.followee_id
-- where f.follower_id is null 
-- AND u.is_creator = 'true'; 




-- select u.user_id from users u 
-- where not EXISTS (
-- select 1 from follows f 
-- where u.user_id=f.followee_id
-- )
-- AND u.is_creator = 'true'


-- Q14  ⚡ — Sessionization: User Interaction Sessions

-- WITH SessionBreaks AS (
--     -- Your exact query here
--     SELECT user_id, interaction_id, interacted_at,
--     CASE WHEN TIMESTAMPDIFF(minute, 
--           LAG(interacted_at) OVER (PARTITION BY user_id ORDER BY interacted_at), 
--           interacted_at) > 60 THEN 1 ELSE 0 END AS is_new_session
--     FROM interactions
-- )
-- SELECT 
--     *,
--     SUM(is_new_session) OVER (PARTITION BY user_id ORDER BY interacted_at) + 1 AS session_id
-- FROM SessionBreaks;


-- q15 ⚡
-- with cte as (

-- SELECT 
--     p.post_id ,p.post_type,
--     count(i.interaction_id) as total_intertactions
-- FROM posts p
-- left JOIN interactions i 
--     ON p.post_id = i.post_id
-- GROUP by p.post_id,p.post_type
-- )

-- select post_id,
-- post_type,
-- total_intertactions,
-- round(
-- percent_rank() over (PARTITION by post_type order by total_intertactions ) 
-- ,2) as r 
-- from cte 
-- order by post_type desc;

-- q16 ⚡
-- select * from interactions;

-- with cte as  (
-- select DISTINCT DATE_FORMAT(interacted_at, '%Y-%m-%d') as "date",
-- count(interaction_id) 
-- over (
-- PARTITION by DATE_FORMAT(interacted_at, '%Y-%m-%d')) as  total_interactions

-- from interactions
-- )

-- SELECT 
--     date,
--     total_interactions,
--     SUM(total_interactions) OVER (
--         ORDER BY date 
--         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
--     ) AS rolling_7_day_sum
-- FROM cte;


-- Q18 — Churn: Creators Who Haven't Posted in 45+ Days⚡
-- SELECT 
--     u.user_id, 
--     u.username, 
--     MAX(p.posted_at) AS last_post_date
-- FROM users u
-- JOIN posts p ON u.user_id = p.user_id
-- GROUP BY u.user_id, u.username
-- HAVING MAX(p.posted_at) < (SELECT MAX(posted_at) FROM posts) - INTERVAL 70 DAY;

-- q19

-- WITH UniqueDates as (
--     -- Step 1: Get unique days per user
--     SELECT DISTINCT user_id, DATE(posted_at) as post_date
--     FROM posts
-- )
-- , StreakGroups  as (
--     SELECT 
--         user_id, 
--         post_date,
--         DATE_SUB(post_date, INTERVAL ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY post_date) DAY) as streak_group
--     FROM UniqueDates
-- )
-- -- select * from StreakGroups;

-- SELECT 
--     user_id, 
--     COUNT(*) as streak_length,
--     MIN(post_date) as streak_start,
--     MAX(post_date) as streak_end
-- FROM StreakGroups
-- GROUP BY user_id,streak_group
-- ORDER BY streak_length DESC;

-- q20 




WITH MonthlyGains AS (
    -- Step 1: Count new followers per creator per month
    SELECT 
        followee_id AS creator_id,
        DATE_FORMAT(followed_at, '%Y-%m') AS month,
        COUNT(follower_id) AS new_followers
    FROM follows
    GROUP BY followee_id, month
),
GrowthCalc AS (
    -- Step 2: Use LAG to find the prior month's new followers
    SELECT 
        creator_id,
        month,
        new_followers,
        LAG(new_followers) OVER (PARTITION BY creator_id ORDER BY month) AS prev_month_gain
    FROM MonthlyGains
)
-- Step 3: Calculate the growth rate percentage
SELECT 
    creator_id,
    month,
    new_followers,
    prev_month_gain,
    ROUND(
        (new_followers - prev_month_gain) * 100.0 / NULLIF(prev_month_gain, 0), 
        2
    ) AS mom_growth_rate
FROM GrowthCalc
ORDER BY creator_id, month;













































































































