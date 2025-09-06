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
