import sys
from preprocess_scan import parse_scan_line

def generate_verification_file(english_file, translated_file, output_file):
    with open(english_file, 'r') as enfile:
        with open(translated_file, 'r') as trfile:
            with open(output_file, 'w') as outfile:
                for i in range(40):
                    (text_en, instr_en) = parse_scan_line(enfile.readline())
                    (text_tr, instr_tr) = parse_scan_line(trfile.readline())
                    assert instr_en == instr_tr
                    
                    outfile.write(f"--- EXAMPLE {i} ---\n")
                    outfile.write(f"English:      {text_en}\n")
                    outfile.write(f"Translated:   {text_tr}\n")
                    outfile.write(f"Instructions: {instr_en}\n\n")

if __name__ == '__main__':
    english_file = sys.argv[1]
    translated_file = sys.argv[2]
    output_file = sys.argv[3]

    generate_verification_file(english_file, translated_file, output_file)
