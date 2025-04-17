to pull date from github with token  :

git clone https://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@github.com/iamanimesh11/Airflow_project.git


# to connect with postgredsel in CLI

sudo -u postgres psql
psql -U airflow_user -d airflow_ETL


# to connec to database:
\c airflow_ETL

# to check total tables:
\dt

# check table structure
airflow_ETL=# \d flipkart_laptops
