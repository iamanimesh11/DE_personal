CSV TO PAQRUET USING ATHENA : 

CREATE TABLE sales_parquet
WITH (
    format = 'PARQUET',
    external_location = 's3://my-de-lake-animesh11/sales_parquet/year=2025/month=1/',
    parquet_compression = 'SNAPPY'
) AS
SELECT *
FROM sales_raw
WHERE year = 2025 AND month = 1
