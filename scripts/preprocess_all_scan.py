
from pathlib import Path
from preprocess_scan import translate_scan_file

INPUT_PATH="/Users/amelietamreymond/projects/Master_thesis/data/en/"

for path in Path(INPUT_PATH).rglob('*.txt'):
    output_path = path.relative_to(INPUT_PATH)
    output_path = "/Users/amelietamreymond/projects/Master_thesis/data/fr/" + str(output_path)

    translate_scan_file(path, output_path)