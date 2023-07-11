import re
from parse import parser_en
from translate import translate_EN_FR

SCAN_TEST_FILE = "/Users/amelietamreymond/projects/Master_thesis/data/SCAN_dataset/add_prim_split/tasks_test_addprim_jump.txt"
TRANSLATED_FILE = "/Users/amelietamreymond/projects/Master_thesis/outputs/test.txt"

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
        raise Exception(f"wow wow wow too fast you got {len(tree)} items in the sentence '{sentence}'")
    
    return tree[0]

def translate_scan_line(line: str) -> str:
    (input, output) = parse_scan_line(line)
    tokens = tokenize(input)
    tree_en = parse(parser_en, tokens)        
    tree_fr = translate_EN_FR(tree_en)
    sentence_fr = " ".join(tree_fr.leaves())
    return f"IN: {sentence_fr} OUT: {output}"

def main():
    with open(SCAN_TEST_FILE, 'r') as file_in:
        with open(TRANSLATED_FILE, 'w') as file_out:
            i = 0
            for line in file_in.readlines():
                translated = translate_scan_line(line)
                file_out.write(translated)
                i += 1
                if i % 100 == 0:
                    print(f"Parsed {i} lines")

if __name__ == '__main__':
    main()