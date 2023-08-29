import json
import re

def parse_scan_line(line: str):
    [input, output] = re.split(' OUT: ', line)
    output = output.strip()
    input = input[4:]
    
    # Create generator so that we can have all lines, return tuple of (input,output)
    return (input, output)

def parse_txt_to_dict(input_file_path):
    data_list = []

    with open(input_file_path, 'r') as f:
        for line in f.readlines():
            in_key, out_value = parse_scan_line(line)
            data_dict = {
                "input": in_key,
                "target": out_value
            }
            
            #yield data_dict
            data_list.append(data_dict)

    return data_list

def convert_dict_to_jsonl(data_list, output_file_path):
    with open(output_file_path, 'w', encoding="utf8") as output_file:
        for line in data_list:
            json.dump(line, output_file, ensure_ascii=False)
            output_file.write("\n")


def convert_txt_to_json(input_file_path, output_json_path):
    data_list = parse_txt_to_dict(input_file_path)

    # Convert to JSON file
    convert_dict_to_jsonl(data_list, output_json_path)


# Example usage:
input_file_path = "/Users/amelietamreymond/projects/Master_thesis/data/en/SCAN_dataset/tasks_sample.txt"
output_json_path = "/Users/amelietamreymond/projects/Master_thesis/outputs/tasks_sample_en.jsonl"
convert_txt_to_json(input_file_path, output_json_path)
