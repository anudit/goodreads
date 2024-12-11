import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Load the JSON file
input_json_file = 'quotes.json'  # Replace with your JSON file path
output_parquet_file = 'quotes.parquet'  # Desired Parquet file path

# Read the JSON data into a pandas DataFrame
df = pd.read_json(input_json_file)

# Save the DataFrame as a Parquet file
df.to_parquet(output_parquet_file, engine='pyarrow', index=False)

print(f"JSON data has been converted and saved to {output_parquet_file}, {df.shape}")
