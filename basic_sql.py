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
