import pandas as pd

# Step 1: Read the .csv data
csv_file_path = './uploads/Mall_Customers.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Categorize the data (example: categorizing based on gender)

# Create an empty dictionary to hold categorized data
categorized_data = {}

# Iterate through the rows and categorize based on gender
for index, row in df.iterrows():
    gender = row['Gender']
    if gender not in categorized_data:
        categorized_data[gender] = []
    categorized_data[gender].append(row)

# Print the categorized data
for gender, data in categorized_data.items():
    print(f"Gender: {gender}")
    for record in data:
        print(record)

# Step 3 (Optional): Save the categorized data to a new .csv file
for gender, data in categorized_data.items():
    gender_csv_file = f"{gender}_data.csv"
    gender_df = pd.DataFrame(data)
    gender_df.to_csv(gender_csv_file, index=False)

