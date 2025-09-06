import pandas as pd
import great_expectations as ge

def test_metadata():

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "age": [25, 30, None],
    })

    gdf = ge.from_pandas(df)

    # Example with metadata
    gdf.expect_column_values_to_not_be_null(
        "age",
        meta={
            "jira_ticket": "DATA-123",
            "owner": "data-quality-team",
            "tags": ["critical", "pii"]
        }
    )

    results = gdf.validate()
    print(results)
    # Check metadata in the results

    failed_critical = []
    for exp in results["results"]:
        meta = exp.get("expectation_config", {}).get("meta", {})
        if not exp["success"] and "critical" in meta.get("tags", []):
            failed_critical.append(exp)

    print(f"Critical failures: {failed_critical}")
    assert len(failed_critical) == 1, "There should be one critical failure"
    assert failed_critical[0]["expectation_config"]["meta"]["jira_ticket"] == "DATA-123", "Jira ticket metadata mismatch"
    assert failed_critical[0]["expectation_config"]["meta"]["owner"] == "data-quality-team", "Owner metadata mismatch"
    assert "critical" in failed_critical[0]["expectation_config"]["meta"]["tags"], "Tags metadata mismatch"
    