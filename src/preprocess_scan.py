import re
import sys
import os
from pathlib import Path
from parse import parser_en
from translate import translate_EN_RU, translate_EN_HIN, translate_EN_FR, translate_EN_ZH

def parse_scan_line(line: str):
    [input, output] = re.split(' OUT: ', line)
    input = input[3:]
    
    # Create generator so that we can have all lines, return tuple of 
    return (input, output)

def tokenize(sentence: str):
    return sentence.strip().split()

def parse(parser, tokens):
    tree = parser.parse(tokens)
    tree = list(tree)

    if len(tree) != 1:
        sentence = " ".join(tokens)
        raise Exception(f"Expected only 1 tree root, but parsed {len(tree)} tree roots in the sentence '{sentence}'")
    
    return tree[0]

def translate(tree_en, target_lang: str):
    if target_lang == "ru":
        return translate_EN_RU(tree_en)
    elif target_lang == "fr":
        return translate_EN_FR(tree_en)
    elif target_lang == "hin":
        return translate_EN_HIN(tree_en)
    elif target_lang == "cmn":
        return translate_EN_ZH(tree_en)
    else:
        raise Exception(f"Language {target_lang} is not supported")

def tree_to_sentence(tree, target_lang: str) -> str:
    if target_lang == "cmn":
        return "".join(tree.leaves()) 
    else:
        return " ".join(tree.leaves()) 

def translate_scan_line(line: str, target_lang: str) -> str:
    (input, output) = parse_scan_line(line)
    tokens = tokenize(input)
    tree_en = parse(parser_en, tokens)
    try:
        tree_target = translate(tree_en, target_lang)
    except AssertionError:
        raise Exception(f"Could not parse tree: {tree_en}")
    sentence = tree_to_sentence(tree_target, target_lang)
    return f"IN: {sentence} OUT: {output}"

def translate_scan_file(input_file: str, output_file: str, target_lang: str):
    print(f"Translating!")
    print(f"input: {input_file}")
    print(f"output: {output_file}")
    print(f"target_lang: {target_lang}")

    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)

    with open(input_file, 'r') as file_in:
        with open(output_file, 'w') as file_out:
            i = 0
            for line in file_in.readlines():
                translated = translate_scan_line(line, target_lang)
                file_out.write(translated)
                i += 1
                if i % 100 == 0:
                    print(f"Parsed {i} lines")

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    target_lang = sys.argv[3]

    translate_scan_file(input_file, output_file, target_lang)