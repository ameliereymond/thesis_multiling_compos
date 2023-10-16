import json
import re
from pathlib import Path
import os

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
    os.makedirs(Path(output_json_path).parent.absolute(), exist_ok=True)

    data_list = parse_txt_to_dict(input_file_path)
    convert_dict_to_jsonl(data_list, output_json_path)

if __name__ == "__main__":
    languages = {
        "cmn": {},
        "en": {
            "target_rename": "eng"
        },
        "fr": {
            "target_rename": "fra"
        },
        "hin": {},
        "ru": {
            "target_rename": "rus"
        },
    }
    
    splits = {
        "add_prim_jump": {
            "has_dev": False
        },
        "add_prim_turn_left": {
            "has_dev": False
        },
        "length_split": {
            "has_dev": False,
            "target_rename": "length"
        },
        "mcd1": {
            "has_dev": True
        },
        "mcd2": {
            "has_dev": True
        },
        "mcd3": {
            "has_dev": True
        },
        "simple": {
            "has_dev": False
        },
    }
    for lang, lang_info in languages.items():
        target_lang = lang_info["target_rename"] if "target_rename" in lang_info else lang

        for split, split_info in splits.items():
            files = ["test", "train"]
            if split_info["has_dev"]:
                files.append("dev")

            target_split = split_info["target_rename"] if "target_rename" in split_info else split
            
            for file in files:
                input_file = f"data/output/{lang}/{split}/{file}.txt"
                output_file = f"data/output/upload/{target_lang}/{target_split}/{file}.jsonl"
                print(f"Converting {input_file} -> {output_file}")
                convert_txt_to_json(input_file, output_file)
            
