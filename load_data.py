import os
import csv
import json

"""
This  script is used to process different file formats and iterate through them one by one and save the responses
"""
DATA_FOLDER = "data"

def load_data():
    files_data = []

    for filename in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, filename)
        file_content = []

        # TXT files
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                file_content.append(f.read())

        # CSV files
        elif filename.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                headers = next(reader)
                for row in reader:
                    file_content.append(", ".join(row))

        # JSON files
        elif filename.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, dict):
                    for key, value in data.items():
                        file_content.append(f"{key}: {value}")

                elif isinstance(data, list):
                    for item in data:
                        file_content.append(str(item))

        
        if file_content:
            files_data.append({
                "filename": filename,
                "content": "\n".join(file_content)
            })

    return files_data