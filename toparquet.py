import pandas as pd
import re

# File paths
input_json_file = 'quotes.json'
output_json_file = 'quotesclean.json'
output_parquet_file = 'quotes.parquet'

# Read JSON file into a DataFrame
df = pd.read_json(input_json_file)

# Display initial rows
print("Initial DataFrame:")
print(df.head())

# Remove duplicates based on the 'quote' column and count the difference
initial_count = df.shape[0]
df_cleaned = df.drop_duplicates(subset='quote').copy()  # Explicitly create a copy

# Clean up data: Remove trailing commas from authors
df_cleaned.loc[:, 'author'] = df_cleaned['author'].str.rstrip(',')

# Remove "" or “” from quotes
df_cleaned.loc[:, 'quote'] = df_cleaned['quote'].apply(lambda x: re.sub(r'["“”]', '', x))

# Remove quotes with less than 2 words
df_cleaned = df_cleaned[df_cleaned['quote'].apply(lambda x: len(x.split()) >= 4)].copy()  # Create a new copy

duplicates_removed = initial_count - df_cleaned.shape[0]
# Count the final number of entries
final_count = df_cleaned.shape[0]

# Display the number of duplicates and short quotes removed
print(f"Duplicates removed: {duplicates_removed}")
print(f"Total remaining quotes: {final_count}")

# Save the cleaned DataFrame to a JSON file
df_cleaned.to_json(output_json_file, orient='records', indent=4)

# Save the cleaned DataFrame to a Parquet file
df_cleaned.to_parquet(output_parquet_file, engine='pyarrow', index=False)

# Confirm the operation and display the shape of the cleaned DataFrame
print(f"Cleaned JSON data has been saved to {output_json_file}")
print(f"Cleaned Parquet data has been saved to {output_parquet_file}, Shape: {df_cleaned.shape}")

# ~1.7M
