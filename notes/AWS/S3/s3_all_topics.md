## AWS S3 Topics — Complete Mastery List

1️⃣ Core Concepts

What is S3 (Simple Storage Service)

Object storage vs Block storage vs File storage

Buckets, Objects, Keys, Prefixes

Regions, Availability Zones

Strong vs Eventual consistency

Durability (11 nines) & high availability

---

2️⃣ Buckets & Objects

Creating and deleting buckets

Bucket naming rules

Uploading objects (single file, multiple files, folders)

Object metadata (system & custom metadata)

Copying and moving objects

Deleting objects and empty folders

Versioning (enable, suspend, retrieve versions)

Object tagging

---

3️⃣ Storage Classes & Lifecycle

S3 Standard

S3 Intelligent-Tiering

S3 Standard-IA (Infrequent Access)

S3 One Zone-IA

S3 Glacier & Glacier Deep Archive

Lifecycle policies (transition, expiration)

Intelligent-tiering automation

---

4️⃣ Data Management

Multipart upload (for large files)

Upload concurrency

Object locking / WORM (Write Once Read Many)

S3 Inventory (reporting on objects)

S3 Batch Operations
---


5️⃣ Access & Security

IAM policies vs Bucket policies

ACLs (Access Control Lists)

Block Public Access

Encryption at rest

SSE-S3, SSE-KMS, SSE-C

Encryption in transit (HTTPS)

AWS KMS integration

CloudTrail logging for S3

Access logs

---

6️⃣ Networking & Endpoints

S3 URL formats (virtual-hosted vs path-style)

S3 endpoints (VPC endpoints, Gateway endpoints)

Cross-region replication (CRR)

Cross-account access

Pre-signed URLs (temporary access)


7️⃣ Advanced Features

Event notifications (Lambda, SQS, SNS triggers)

S3 Select (querying CSV/JSON/Parquet files)

S3 Object Lambda

Glacier retrieval types (Expedited, Standard, Bulk)

Requester pays buckets


8️⃣ Integration with AWS Services

AWS Glue (Data catalog)

Athena (query S3 data directly)

Redshift Spectrum

Lambda triggers

CloudWatch & EventBridge integration

Data pipelines & Airflow / Step Functions

SageMaker (ML datasets from S3)

---

9️⃣ Performance & Optimization

Multipart upload & download

Transfer Acceleration

Data compression strategies

Caching (CloudFront with S3)

Monitoring with CloudWatch metrics

Cost optimization using Storage Class Analysis
---

🔟 Best Practices

Bucket naming and structure for data lakes

Data lifecycle and cost efficiency

Security & compliance

Disaster recovery & replication strategies

Monitoring and auditing access


