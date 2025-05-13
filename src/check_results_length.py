import os
import json

def check_json_files_have_100_items(parent_folder):
    number_bad_files = 0
    for root, _, files in os.walk(parent_folder):
        for file in files:
            if file.endswith('results.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    item_count = len(data)
                    if item_count != 100:
                        print(f"{file_path} has {item_count} items")
                        number_bad_files += 1
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")
    
    if number_bad_files > 0:
        print(f"WARNING: {number_bad_files} bad files")
    else:
        print("All files have 100 items")

parent_folder = 'data/output/results/aya-expanse-8b'
check_json_files_have_100_items(parent_folder)
