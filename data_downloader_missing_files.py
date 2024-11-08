import os
import requests
import sys

# get missing names
with open("text_files/files.txt", "r") as f:
    CSVs = f.read()

CSVs = CSVs.replace("\n    ", " ").replace("%20", "_")[2:-2].split("', '")
# print(CSVs)

local_file_path = f"data/tfl_CSVs/"
os.makedirs(local_file_path, exist_ok=True)
downloaded_files = set(os.listdir(local_file_path))
missing_files = [csv for csv in CSVs if csv not in downloaded_files]
print(f"downloading {len(missing_files)} files: {missing_files}")

# Base URL
base_url = "https://cycling.data.tfl.gov.uk/usage-stats/"

# Download each CSV file
for file_name in missing_files:
    file_url = base_url + file_name
    # if flag==False:
    #     print(f"Downloaded {file_name}")
    #     break
    response = requests.get(file_url)

    
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the CSV file
        file_path = os.path.join(local_file_path, file_name.replace("%20", "_"))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}, Status code: {response.status_code}")

print(f"All ({len(missing_files)}) files downloaded.")
