
import os
import pandas as pd

def preprocess_data(input_path, output_path):
    """
    Reads raw heart disease data, performs basic preprocessing,
    and saves the processed data.
    """
    # Read the raw data
    print(f"Reading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    
    # Display basic info about the dataset
    print("Initial data shape:", df.shape)
    print("Data preview:")
    print(df.head())
    
    # Example preprocessing:
    # 1. Drop rows with missing values
    df.dropna(inplace=True)
    print("Data shape after dropping missing values:", df.shape)
    
    # 2. Optional: Convert columns to appropriate types (if needed)
    # For example, if some categorical columns are stored as numbers:
    # df['some_column'] = df['some_column'].astype('category')
    
    # 3. Optional: Rename columns or perform feature engineering
    # For demonstration, we assume the data is ready after dropping missing values.
    
    # Save the processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to: {output_path}")

if __name__ == "__main__":
    # Define paths for raw and processed data
    raw_data_path = os.path.join("data", "raw", "heart.csv")
    processed_data_path = os.path.join("data", "processed", "heart_processed.csv")
    
    # Run the preprocessing function
    preprocess_data(raw_data_path, processed_data_path)
