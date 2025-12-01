🚀 **AWS S3 Pocket CLI Cheatsheet (Ultra Short)**

## 🔧 **Setup**

```
aws configure
```

---

## 📂 **Buckets**

```
aws s3 ls                           # List buckets
aws s3 mb s3://bucket               # Create bucket
aws s3 rb s3://bucket --force       # Delete bucket + contents
```

---

## 📁 **Files / Objects**

```
aws s3 cp file s3://bucket/         # Upload
aws s3 cp s3://bucket/file .        # Download
aws s3 mv a b                        # Move / rename
aws s3 rm s3://bucket/file          # Delete
aws s3 ls s3://bucket/              # List objects
```

---

## 🔄 **Sync**

```
aws s3 sync local/ s3://bucket/     # Upload folder
aws s3 sync s3://bucket/ local/     # Download folder
```

---

## 🔐 **Security**

```
aws s3api put-object-acl --acl public-read \
  --bucket bucket --key file              # Make file public
```

---

## 🎯 **Useful Extras**

```
aws s3 presign s3://bucket/file --expires-in 3600
aws s3api head-object --bucket bucket --key file
```

---

## ⭐ **Storage Class (Glacier / IA)**

```
aws s3 cp file s3://bucket/ --storage-class GLACIER
```

---

## 🌐 **Static Website**
```
aws s3 website s3://bucket/ --index-document index.html

Just tell me
