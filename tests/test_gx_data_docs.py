import json
import os
import pandas as pd
import great_expectations as gx
from great_expectations.data_context import BaseDataContext
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.checkpoint import SimpleCheckpoint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
suite_path = os.path.join(BASE_DIR, "suites", "user_suite.json")

data_docs_dir = os.path.join(BASE_DIR, "data_docs")

# Load JSON suite
with open(suite_path, "r") as f:
    suite_json = json.load(f)

# Sample data
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 35, 45]
})

# Minimal in-memory GX config
config = {
    "config_version": 3.0,
    "datasources": {
        "pandas_datasource": {
            "class_name": "Datasource",
            "execution_engine": {"class_name": "PandasExecutionEngine"},
            "data_connectors": {
                "default_runtime_data_connector": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["batch_id"],
                }
            },
        }
    },
    "expectations_store_name": "expectations_store",
    "validation_results_store_name": "validation_results_store",
    "data_docs_sites": {
        "local_site": {
            "class_name": "SiteBuilder",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": data_docs_dir,
            },
            "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
        }
    },
    "stores": {
        "expectations_store": {"class_name": "ExpectationsStore"},
        "validation_results_store": {"class_name": "ValidationsStore"},
    },
    "anonymous_usage_statistics": {"enabled": False},
}

# Create in-memory GX context
context = BaseDataContext(project_config=config)

# Create batch request
batch_request = {
    "datasource_name": "pandas_datasource",
    "data_connector_name": "default_runtime_data_connector",
    "data_asset_name": "my_data",
    "runtime_parameters": {"batch_data": df},
    "batch_identifiers": {"batch_id": "test_batch"},
}

# Register expectation suite
suite = ExpectationSuite(**suite_json)
context.add_or_update_expectation_suite(expectation_suite=suite)

# ✅ Run validation with checkpoint
checkpoint = SimpleCheckpoint(
    name="my_checkpoint",
    data_context=context,
    validations=[{
        "batch_request": batch_request,
        "expectation_suite_name": suite.expectation_suite_name,
    }],
)
checkpoint_result = checkpoint.run()

# Build and open Data Docs
context.build_data_docs()
context.open_data_docs()

# Assert all expectations passed
assert checkpoint_result["success"], "Validation failed!"
