from nltk import Tree

def translate_EN_FR(tree_en: Tree) -> Tree:
    word_mapping = {
        "walk" : "marcher",
        "look" : "regarder",
        "run"  : "courir",
        "jump" : "sauter",
        "and": "et",
        "after": "ensuite",
        "opposite": "en face", 
        "around": "autour",
        "right": "à droite",
        "left": "à gauche",
        "turn": "tourner",
        "twice": "deux fois",
        "thrice": "trois fois"
    }
    label = tree_en.label()
    if label in set(["C", "S", "V", "D"]):
        return Tree(label, [translate_EN_FR(nt) for nt in tree_en])
    else:
        return Tree(label, [word_mapping[word] for word in tree_en])
