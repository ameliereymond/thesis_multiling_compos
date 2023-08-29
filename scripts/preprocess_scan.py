import re
import sys
import os
from pathlib import Path
from parse import parser_en
from translate import translate_EN_RU

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

def translate_scan_line(line: str) -> str:
    (input, output) = parse_scan_line(line)
    tokens = tokenize(input)
    tree_en = parse(parser_en, tokens)
    try:
        tree_fr = translate_EN_RU(tree_en)
    except AssertionError:
        raise Exception(f"Could not parse tree: {tree_en}")
    
    sentence_fr = "".join(tree_fr.leaves()) # TODO add space here if other lang than zh
    return f"IN: {sentence_fr} OUT: {output}"

def translate_scan_file(input_file, output_file):
    print(f"Translating!")
    print(f"input: {input_file}")
    print(f"output: {output_file}")

    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)

    with open(input_file, 'r') as file_in:
        with open(output_file, 'w') as file_out:
            i = 0
            for line in file_in.readlines():
                translated = translate_scan_line(line)
                file_out.write(translated)
                i += 1
                if i % 100 == 0:
                    print(f"Parsed {i} lines")

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    translate_scan_file(input_file, output_file)