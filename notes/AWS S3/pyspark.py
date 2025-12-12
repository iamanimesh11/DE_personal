Here is your **short, clean, future-ready summary note** for setting up PySpark on Ubuntu (WSL) + accessing Windows drives + running CSV → Parquet.

---

# ✅ **PySpark Setup Summary (Ubuntu + Conda + Java 17 + Jupyter)**

### **1. Create and activate conda environment**

```bash
conda create -n pyspark_env python=3.10 -y
conda activate pyspark_env
```

### **2. Install Java 17 (required for PySpark 4.x)**

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
```

### **3. Set JAVA_HOME**

Add to `~/.bashrc`:

```bash
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"
```

Reload:

```bash
source ~/.bashrc
```

### **4. Install PySpark + Jupyter**

```bash
pip install pyspark ipykernel
python -m ipykernel install --user --name pyspark_env --display-name "PySpark (Conda)"
```

### **5. Start Jupyter**

```bash
jupyter notebook
```

Select kernel → **PySpark (Conda)**

---

# 📂 **Accessing Windows D drive from Ubuntu**

Windows `D:\folder\file.csv` becomes:

```
/mnt/d/folder/file.csv
```

Use **forward slashes**, never backslashes.

---

# 🔄 **CSV → Parquet Conversion (working version)**

### **Read CSV**

```python
df = spark.read.csv("/mnt/d/AWS_DE/data.csv", header=True, inferSchema=True)
```

### **Write Parquet**

```python
df.write.mode("overwrite").parquet("/mnt/d/AWS_DE/parquet_output")
```

### **Verify**

```python
df2 = spark.read.parquet("/mnt/d/AWS_DE/parquet_output")
df2.show()
```

---

# ⭐ **This is all you need to remember.

Following these points = Spark always works.**

If you want, I can also write a **one-click script** to automate the environment setup.
