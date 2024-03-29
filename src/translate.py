from nltk import Tree

def translate_EN_FR(tree_en: Tree) -> Tree:
    word_mapping = {
        "walk" : "marcher",
        "look" : "regarder",
        "run"  : "courir",
        "jump" : "sauter",
        "and": "et",
        "after": "après",
        "opposite": "à l'opposé", 
        "around": "autour",
        "right": "par la droite",
        "left": "par la gauche",
        "turn": "tourner",
        "twice": "deux fois",
        "thrice": "trois fois"
    }
    label = tree_en.label()
    if label in set(["C", "S", "V"]):
        return Tree(label, [translate_EN_FR(nt) for nt in tree_en])
    elif label == "D":
        dir_mapping = {
            "left": "à gauche",
            "right": "à droite"
        }
        return Tree(label, [translate_EN_FR(tree_en[0]), dir_mapping[tree_en[1][0]]])
    else:
        return Tree(label, [word_mapping[word] for word in tree_en])


def translate_EN_RU(tree_en: Tree) -> Tree:
    word_mapping = {
        "walk" : "идть",
        "look" : "смотреть",
        "run"  : "бегать",
        "jump" : "прыгать",
        "and": "и",
        "after": "после",
        "opposite": "напротив", 
        "around": "вокруг",
        "right": "на право",
        "left": "на лево" ,
        "turn": "повернуть",
        "twice": "дважды",
        "thrice": "трижды", 
    }
    label = tree_en.label()
    if label in set(["C", "S", "V", "D"]):
        return Tree(label, [translate_EN_RU(nt) for nt in tree_en])
    else:
        return Tree(label, [word_mapping[word] for word in tree_en])


def translate_EN_ZH(tree_en: Tree) -> Tree:
    word_mapping = {
        # AND
        "and": "然后", # "ran hou"

        # AFTER
        "after": "，之前先", # ", zhi qian xian " 

        # TIMES
        "twice": "两次", # "liang ci"
        "thrice": "三次", # "san ci"

        # TURN
        "turn": "转", # "zhuan"

        # DIR
        "left": "向左", # xiang zuo
        "right": "向右", # xiang you
        
        # ACTION
        "walk": "走", # "zou"
        "look": "看", # "kan"
        "run": "跑", #pao
        "jump": "跳", #tiao
    }
    label = tree_en.label()
    if label in set(["C", "S"]):
        return Tree(label, [translate_EN_ZH(nt) for nt in tree_en])
    elif label == "D":
        action_or_turn = tree_en[0]
        dir = tree_en[1]
        return Tree(label, [translate_EN_ZH(dir), translate_EN_ZH(action_or_turn)])
    elif label == "V":
        if len(tree_en) != 3:
            return Tree(label, [translate_EN_ZH(nt) for nt in tree_en])

        assert tree_en[1].label() == "VECTOR"
        assert len(tree_en[1]) == 1
        vector = tree_en[1][0]

        assert tree_en[2].label() == "DIR"
        assert len(tree_en[2]) == 1
        dir = tree_en[2][0]

        cong = "从" # "from/via"
        xiang = "向" # "toward"
        hou = "后" # "behind/opposite"
        zhuan = "转" # "turn[V]"
        yi = "一" # "one"
        quan = "圈" # "loop/round"
        zuo = "左" # "left"
        you = "右" # "right"

        dir_zn = zuo if dir == "left" else you

        if tree_en[0].label() == "TURN":
            if vector == "opposite":
                return Tree("?", [cong, dir_zn, xiang, hou, zhuan])
            
            elif vector == "around":
                return Tree("?", [xiang, dir_zn, zhuan, yi, quan])
            else:
                raise Exception(f"Unexpected value '{vector}' for VECTOR")
            
        elif tree_en[0].label() == "ACTION":
            action = tree_en[0]
            if vector == "opposite":
                return Tree("?", [cong, dir_zn, zhuan, xiang, hou, translate_EN_ZH(action)])
            elif vector == "around":
                return Tree("?", [xiang, dir_zn, translate_EN_ZH(action), yi, quan])
            else:
                raise Exception(f"Unexpected value '{vector}' for VECTOR")
        
        else:
            raise Exception(f"Unexpected subtree '{tree_en[0]}' for VECTOR")
    else:
        return Tree(label, [word_mapping[word] for word in tree_en])
    

def translate_EN_HIN(tree_en: Tree) -> Tree:
    word_mapping = {
         # AND
        "and": "और तब", # "aur tab"

        # AFTER
        "after": "जिसके पहले", # "jiske pehle" 

        # TIMES
        "twice": "दोबार", # "do baar"
        "thrice": "तीनबार", # "teen baar"

        # TURN
        "turn": "मोड़", # "mod"

        # DIR
        "left": "बाएं", # "baai"
        "right": "दांए", # "daai"

        # VECTOR
        "opposite": "पीछे", # "peeche"
        "around": "इद-गद", # "irad girad"
        
        # ACTION
        "walk": "चलना", # "chalna"
        "look": "दे खना", # "dekhna"
        "run": "दौड़ना", # "daudana"
        "jump": "कू दना", # "koodana"
    }

    label = tree_en.label()

    if label == "C":
        return Tree(label, [translate_EN_HIN(nt) for nt in tree_en])
    elif label == "S":
        # V twice -> do baar V 
        if tree_en[-1].label() == "TIMES":
            return Tree(label, [translate_EN_HIN(tree_en[1]), translate_EN_HIN(tree_en[0])])
        else:
            return Tree(label, [translate_EN_HIN(nt) for nt in tree_en])
    elif label == "V":
        # English rule   V -> ACTION VECTOR DIR | TURN VECTOR DIR | D | ACTION
        # Hindin rule    V -> DIR VECTOR ACTION | DIR VECTOR TURN | D | ACTION
        if tree_en[-1].label() == "DIR":
            return Tree(label, [translate_EN_HIN(tree_en[2]), translate_EN_HIN(tree_en[1]), translate_EN_HIN(tree_en[0])])
        else:
            return Tree(label,[translate_EN_HIN(nt) for nt in tree_en])
    elif label == "D":
        return Tree(label, [translate_EN_HIN(tree_en[1]), translate_EN_HIN(tree_en[0])])
    else:
        return Tree(label, [word_mapping[word] for word in tree_en])