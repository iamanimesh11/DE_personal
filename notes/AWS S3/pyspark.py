Here is your **clean, minimal, crystal-clear summary note** — the only steps you ever need to remember to set up and run PySpark correctly on Windows + Anaconda + Jupyter.

---

# 🟩 **PYSPARK SETUP SUMMARY (WINDOWS + ANACONDA)**

### *(Save this — this is your master reference)*

---

# ✅ **1. Create and activate environment**

```bash
conda create -n pyspark_env python=3.11
conda activate pyspark_env
```

---

# ✅ **2. Install PySpark + Jupyter**

```bash
conda install -c conda-forge pyspark
conda install -c conda-forge findspark
conda install -c conda-forge jupyter
```

---

# ✅ **3. Install correct Java (PySpark 4.x needs Java 17)**

```bash
conda install -c conda-forge openjdk=17
```

---

# ✅ **4. Set environment variables (VERY IMPORTANT)**

These make sure Spark uses the correct Python and Java.

Run once:

```bash
setx PYSPARK_PYTHON "D:\conda\envs\pyspark_env\python.exe"
setx PYSPARK_DRIVER_PYTHON "D:\conda\envs\pyspark_env\python.exe"
setx SPARK_HOME "D:\conda\envs\pyspark_env\Lib\site-packages\pyspark"
setx JAVA_HOME "D:\conda\envs\pyspark_env"
```

Restart terminal.

---

# ✅ **5. Register kernel to Jupyter**

```bash
python -m ipykernel install --user --name pyspark_env --display-name "PySpark (conda)"
```

Now you can pick **PySpark (conda)** inside Jupyter.

---

# ✅ **6. Start Jupyter from inside environment**

```bash
conda activate pyspark_env
jupyter notebook
```

Open a notebook → choose **PySpark (conda)**.

---

# ✅ **7. Always run this FIRST cell in every notebook**

```python
import os

os.environ["PYSPARK_PYTHON"] = r"D:\conda\envs\pyspark_env\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"D:\conda\envs\pyspark_env\python.exe"
os.environ["SPARK_HOME"] = r"D:\conda\envs\pyspark_env\Lib\site-packages\pyspark"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("PySpark Notebook") \
    .getOrCreate()

spark
```

---

# 🎉 **8. Test**

```python
df = spark.createDataFrame([(1,"Animesh"), (2,"LG")], ["id", "name"])
df.show()
```

---

# 🟦 **If PySpark ever gives error again**

Check these 3 things:

1️⃣ `java -version` → should show Java 17
2️⃣ Python path → should be conda env
3️⃣ Run `df.show()` → should NOT show “Python was not found”

---

# 📌 Done.

This is everything you ever need to remember.

If you want, I can format this as a **PDF**, **Markdown file**, or **Notebook template**.
