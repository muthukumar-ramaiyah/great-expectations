import json
import os
import pandas as pd
from great_expectations.dataset import PandasDataset

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up from tests/
suite_path = os.path.join(BASE_DIR, "tests", "suites", "user_suite.json")

def test_gx_suite_json():
    # Load JSON suite
    with open(suite_path, "r") as f:
        suite_json = json.load(f)

    # Sample data
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 35, 45]
    })
    dataset = PandasDataset(df)

    # # Validate dataset against generated suite
    results = dataset.validate(expectation_suite=suite_json)
    # print(results)
    assert results["statistics"]["success_percent"] == 100.0, "Success rate is below 100"
