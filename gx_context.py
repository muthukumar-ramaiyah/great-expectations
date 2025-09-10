import pandas as pd
import great_expectations as gx
from great_expectations import expectations as gxe

context = gx.get_context(mode="file", project_root_dir="./context")

# print(context)

# Define the Data Source's parameters:
# This path is relative to the `base_directory` of the Data Context.
source_folder = "./data"

data_source_name = "my_filesystem_data_source"

# Create the Data Source:
data_source = context.datasources.add_pandas_filesystem(
    name=data_source_name, base_directory=source_folder
)

# Define the Data Asset's parameters:
asset_name = "listings"

file_csv_asset = data_source.add_csv_asset(name=asset_name)

preset_expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column="summary")

batch_definition_name = "my_batch_definition"
batch_definition = (
    context.data_sources.get(data_source_name)
    .get_asset(asset_name)
    .get_batch_definition(batch_definition_name)
)

batch = batch_definition.get_batch()

print(batch.head())

