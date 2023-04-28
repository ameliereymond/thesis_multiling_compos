import re

def parse_file(datafile):
    with open(datafile) as f:
        #for line in f:
        firstNlines = f.readlines()[0:5]
        for line in firstNlines:
            
        
            [input, output] = re.split(' OUT: ', line)
            input = input[3:]
           
            return input, output


def translate(input_sequence):
    input_sequence_translated = []
    for word in input_sequence:

        # Verbs 
        if word == "turn":
            input_sequence_translated.append("tourner")
        if word == "look":
            input_sequence_translated.append("regarder")
        if word == "run":
            input_sequence_translated.append("courir")
        if word == "jump":
            input_sequence_translated.append("sauter")
        if word == "walk":
            input_sequence_translated.append("marcher")

        # Directions 
        if word == "left":
            input_sequence_translated.append("à gauche")
        if word == "right":
            input_sequence_translated.append("à droite")
        if word == "opposite":
            input_sequence_translated.append("en face")
        if word == "around":
            input_sequence_translated.append("autour")

        if word == "twice":
            input_sequence_translated.append("deux fois")
        if word == "thrice":
            input_sequence_translated.append("trois fois")
        
        print(input_sequence_translated)
        
    #return input_sequence_translated
        



if __name__ == '__main__':
    datafile = "/Users/amelietamreymond/projects/Master_thesis/data/SCAN_dataset/tasks.txt"
    input, output = parse_file(datafile)
    translate(input)
    #print(translation)