import pandas as pd
import os
import sys


def fill_missing_data(csv_file_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Fill missing data using forward-fill and backward-fill method
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        # Save the modified DataFrame to a new CSV file in the 'processed' folder
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        processed_folder = os.path.join(backend_dir, 'processed')
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        # Get the file name from the original file path
        file_name = os.path.basename(csv_file_path)

        # Construct the processed file path with the processed folder and file name
        processed_file_path = os.path.join(processed_folder, file_name)

        # Save the DataFrame to the processed file path
        df.to_csv(processed_file_path, index=False)

        # Print the processed file path
        print(processed_file_path)

        return "Success: Data filled and processed file saved successfully!"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Get the CSV file path from the command-line argument
    csv_file_path = sys.argv[1]
    result = fill_missing_data(csv_file_path)
    # print(result)
