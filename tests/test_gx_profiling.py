import pandas as pd
from great_expectations.dataset import PandasDataset
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

def test_gx_profiling():
    # Sample data
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 35, 45]
    })
    dataset = PandasDataset(df)

    # # Run profiler
    profiler = UserConfigurableProfiler(dataset)
    suite = profiler.build_suite()
    # print(suite)

    # # Validate dataset against generated suite
    results = dataset.validate(expectation_suite=suite)
    # print(results)
    assert results["success"] == True, "Data validation failed against the generated expectation suite"
    
