import pandas as pd

# Load the data
data_path = '../../data/raw/raw_data_afternoon.csv'
data = pd.read_csv(data_path)

# Check initial shape before removing duplicates
initial_shape = data.shape
print(initial_shape)

# Remove duplicates
data_cleaned = data.drop_duplicates()

# Check final shape after removing duplicates
final_shape = data_cleaned.shape
print(final_shape)

# Checking for missing values
missing_values = data_cleaned.isnull().sum()
print(missing_values)

# Correcting time values
for index, row in data_cleaned.iterrows():
    try:
        pd.to_datetime(row['Time'])
    except ValueError:
        print(f"Invalid time value detected: {row['Time']}")
        user_input = input("Enter the corrected value, or press 2 to delete this row: ")

        if user_input == "2":
            # If user inputs "2", delete the row
            data_cleaned.drop(index, inplace=True)
        else:
            # Otherwise, update the 'Time' value with the user's corrected input
            data_cleaned.at[index, 'Time'] = user_input

# Save the cleaned data
cleaned_data_path = '../../data/processed/cleaned_afternoon.csv'
data_cleaned.to_csv(cleaned_data_path, index=False)
