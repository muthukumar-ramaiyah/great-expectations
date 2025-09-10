import pandas as pd
from great_expectations.dataset import PandasDataset
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
import os
import json

def test_gx_profiling():
    # Sample data
    df = pd.read_csv("data/listings.csv")
    dataset = PandasDataset(df)

    # # Run profiler
    profiler = UserConfigurableProfiler(dataset)
    suite = profiler.build_suite()
    # print(suite)
    with open("tests/suites/listings_suite.json", "w") as f:
        json.dump(suite.to_json_dict(), f, indent=2)

    # # Validate dataset against generated suite
    results = dataset.validate(expectation_suite=suite)
    # print(results)
    assert results["success"] == True, "Data validation failed against the generated expectation suite"
    
