from nltk import CFG
from nltk.parse import RecursiveDescentParser

grammar_en = CFG.fromstring("""
C -> S AND S | S AFTER S | S
S -> V TIMES | V
V -> ACTION VECTOR DIR | TURN VECTOR DIR | D | ACTION
D -> ACTION DIR | TURN DIR

ACTION -> 'walk' | 'look' | 'run' | 'jump'
TURN -> 'turn'
VECTOR -> 'around' | 'opposite'
DIR -> 'left' | 'right'
TIMES -> 'twice' | 'thrice'
AFTER -> 'after'
AND -> 'and'
""")

grammar_fr = CFG.fromstring("""
C -> S AND S | S AFTER S | S
S -> V TIMES | V
V -> ACTION VECTOR DIR | TURN VECTOR DIR | D | ACTION
D -> ACTION DIR | TURN DIR

ACTION -> 'marcher' | 'regarder' | 'courir' | 'sauter'
TURN -> 'tourner'
VECTOR -> 'autour' | 'en' 'face'
DIR -> 'gauche' | 'droite'
TIMES -> 'deux' 'fois' | 'trois' 'fois'
AFTER -> 'après'
AND -> 'et'
""")

parser_en = RecursiveDescentParser(grammar_en)
parser_fr = RecursiveDescentParser(grammar_fr)