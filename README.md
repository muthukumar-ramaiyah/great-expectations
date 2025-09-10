```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Got it 👍 — **Great Expectations (GX)** is a Python library for validating and documenting your data. Think of it as "pytest for data." You write *expectations* (rules) about your data, and GX checks whether your data meets them.

Here are some **practical samples** 👇

---

## 🔹 Install Great Expectations

```bash
pip install great-expectations
```

---

## 🔹 1. Quick Start with a Pandas DataFrame

```python
import pandas as pd
import great_expectations as ge

# Create sample data
df = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "age": [25, 30, 45, 22, 40],
    "email": ["a@test.com", "b@test.com", "c@test.com", "d@test.com", "e@test.com"]
})

# Convert to GX dataset
gdf = ge.from_pandas(df)

# Expectations
gdf.expect_column_values_to_not_be_null("id")
gdf.expect_column_values_to_be_unique("id")
gdf.expect_column_values_to_be_between("age", min_value=18, max_value=60)
gdf.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")

# Show results
results = gdf.validate()
print(results)
```

✅ This validates your data against rules:

* `id` is not null and unique
* `age` is between 18–60
* `email` matches an email regex

---

## 🔹 2. Using a SQL Database Table

```python
import great_expectations as ge
from sqlalchemy import create_engine

# Connect to SQLite (or Postgres/MySQL/etc.)
engine = create_engine("sqlite:///mydb.sqlite")
conn = engine.connect()

# Load table into GX
gdf = ge.from_sql("users", conn)

# Expectations
gdf.expect_column_values_to_not_be_null("user_id")
gdf.expect_column_values_to_be_unique("user_id")
gdf.expect_column_values_to_be_between("age", 18, 100)

# Validate
results = gdf.validate()
print(results)
```

---

## 🔹 3. Pytest + GX Integration

You can use GX expectations inside your test suite:

```python
import pandas as pd
import great_expectations as ge

def test_user_data_quality():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "email": ["a@test.com", "b@test.com", None]
    })

    gdf = ge.from_pandas(df)
    result = gdf.expect_column_values_to_not_be_null("email")

    assert result["success"], f"Failed: {result}"
```

👉 If an email is null, the pytest test will fail.

---

## 🔹 4. More Common Expectations

```python
gdf.expect_table_row_count_to_be_between(min_value=5, max_value=1000)
gdf.expect_column_to_exist("email")
gdf.expect_column_mean_to_be_between("age", 20, 50)
gdf.expect_column_median_to_be_between("salary", 30000, 80000)
gdf.expect_column_values_to_be_in_set("status", ["active", "inactive", "pending"])
```

---

## 🔹 5. Generate Data Docs (HTML Report)

```bash
great_expectations init
```

Then run validation:

```bash
great_expectations checkpoint run my_checkpoint
```

GX will generate an **HTML data quality report** you can open in a browser.

---

✅ So in summary:

* **Great Expectations = data quality testing framework**.
* Works with **Pandas, Spark, SQL**.
* You define expectations → run validations → get JSON or HTML reports.

---

Would you like me to put together a **real-world example** where GX validates an **API response (JSON)** by first converting it into a DataFrame?

---

Great Expectations is a Python library for validating, documenting, and profiling data. Here are some samples:

## 🔹 Sample 1: Basic Expectation

Suppose we have a dataset of users with columns "name" and "age". We expect the "age" column to be between 18 and 100.
```Python
import pandas as pd
from great_expectations.dataset import PandasDataset

# Create a sample dataset
data = pd.DataFrame({
    "name": ["John", "Jane", "Bob"],
    "age": [25, 30, 101]
})

# Create a Great Expectations dataset
dataset = PandasDataset(data)

# Define an expectation
dataset.expect_column_values_to_be_between("age", 18, 100)

# Validate the expectation
result = dataset.validate()

print(result)
```
## 🔹 Sample 2: Expectation Suite

We can define multiple expectations and group them into an expectation suite.
```Python
import pandas as pd
from great_expectations.dataset import PandasDataset
from great_expectations.core import ExpectationSuite, ExpectationConfiguration

data = pd.DataFrame({
    "name": ["John", "Jane", "Bob"],
    "age": [25, 30, 101]
})

dataset = PandasDataset(data)

# Define a suite
suite = ExpectationSuite("user_suite")

# Add expectations properly
suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_to_exist",
        kwargs={"column": "name"}
    )
)
suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "age", "min_value": 18, "max_value": 100}
    )
)

# Validate against the suite
result = dataset.validate(expectation_suite=suite)
print(result)

```
## 🔹 3. Sample 3: Data Profiling
Great Expectations can also profile your data to automatically generate expectations.

```Python
import pandas as pd
from great_expectations.dataset import PandasDataset
from great_expectations.profile import BasicSuiteBuilderProfiler

# Create a sample dataset
data = pd.DataFrame({
    "name": ["John", "Jane", "Bob"],
    "age": [25, 30, 35]
})

# Create a Great Expectations dataset
dataset = PandasDataset(data)

# Profile the dataset
profiler = BasicSuiteBuilderProfiler(dataset)
suite = profiler.build_suite()

# Print the generated expectations
print(suite)
```
These samples demonstrate basic usage of Great Expectations for data validation and profiling. You can customize expectations and suites to fit your specific use case.

https://medium.com/@mostsignificant/python-data-validation-made-easy-with-the-great-expectations-package-8d1be266fd3f

https://www.kaggle.com/datasets/airbnb/boston?resource=download

