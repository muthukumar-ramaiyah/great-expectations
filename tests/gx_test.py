import pandas as pd
import great_expectations as ge

def test_user_data_quality():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "email": ["a@test.com", "b@test.com", None],
        "age": [25, 30, 55],
        "salary": [50000, 60000, 70000],
        "status": ["active", "inactive", "unknown"] # 'unknown' is not in the expected set
    })

    gdf = ge.from_pandas(df)
    gdf.expect_column_values_to_not_be_null("email")
    gdf.expect_table_row_count_to_be_between(min_value=3, max_value=1000)
    gdf.expect_column_to_exist("email")
    gdf.expect_column_values_to_be_between("age", min_value=18, max_value=60)
    gdf.expect_column_mean_to_be_between("age", 20, 50)
    gdf.expect_column_median_to_be_between("salary", 30000, 80000)
    gdf.expect_column_values_to_be_in_set("status", ["active", "inactive", "pending"])
    outcome = gdf.validate()

    # print(outcome)
    # print("*" * 20)
    # print(outcome["results"][0])

    assert outcome["results"][0]["success"] == False, f"Expectation success mismatch: {result["success"]}"
    assert outcome["results"][0]["result"]["unexpected_count"] == 1, f"Unexpected count mismatch: {result}"
    assert outcome["results"][0]["result"]["element_count"] == 3, f"Element count mismatch: {result}"
    assert outcome["results"][0]["result"]["unexpected_percent"] == (1/3)*100, f"Unexpected percent mismatch: {result}"
    assert outcome["results"][0]["result"]["unexpected_percent_total"] == (1/3)*100, f"Unexpected percent total mismatch: {result}"
    assert outcome["results"][0]["result"]["partial_unexpected_list"] == [], f"Partial unexpected list mismatch: {result}"
