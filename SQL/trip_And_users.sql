-- Create the Trips table
CREATE TABLE Trips (
    id INT PRIMARY KEY,client_id INT,driver_id INT,city_id INT,status VARCHAR(255),request_at DATE
);

-- Insert sample records into the Trips table
INSERT INTO Trips (id, client_id, driver_id, city_id, status, request_at)
VALUES
    (1, 1, 10, 1, 'completed', '2013-10-01'),(2, 2, 11, 1, 'cancelled_by_driver', '2013-10-01'),
    (3, 3, 12, 6, 'completed', '2013-10-01'),(4, 4, 13, 6, 'cancelled_by_client', '2013-10-01'),
    (5, 1, 10, 1, 'completed', '2013-10-02'),(6, 2, 11, 6, 'completed', '2013-10-02'),
    (7, 3, 12, 6, 'completed', '2013-10-02'),(8, 2, 12, 12, 'completed', '2013-10-03'),
    (9, 3, 10, 12, 'completed', '2013-10-03'),(10, 4, 13, 12, 'cancelled_by_driver', '2013-10-03');

-- Create the Users table
CREATE TABLE Users (
    users_id INT PRIMARY KEY,banned VARCHAR(3),role VARCHAR(255) );
-- Insert sample records into the Users table
INSERT INTO Users (users_id, banned, role)
VALUES
    (1, 'No', 'client'),(2, 'Yes', 'client'),(3, 'No', 'client'),(4, 'No', 'client'),(10, 'No', 'driver'),
    (11, 'No', 'driver'),(12, 'No', 'driver'),(13, 'No', 'driver');
    
WITH ValidTrips AS (
    SELECT T.ID,T.client_id,T.driver_id,t.city_id,t.status,t.request_at
    FROM Trips t
    JOIN Users c ON t.client_id = c.users_id AND c.banned = 'No'
    JOIN Users d ON t.driver_id = d.users_id AND d.banned = 'No'
    WHERE t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
)
SELECT 
   request_at as Day,
   round(sum(
   
   case when status!='completed' then 1 else 0 end)*1.0 /count(*),2)
   as 'Cancellation Rate'
   from ValidTrips
   group by request_at
   order by 'Cancellation Rate' desc 
