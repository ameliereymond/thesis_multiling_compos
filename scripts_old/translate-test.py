And(
    left=Jump(
        modifiers=[Twice>]),
    right=Look(
        modifiers=[Around]))


Und(
    Zweimal(Springen),
    Umgluchen,
)

def translate_en_de(EN.Tree english) -> DE.Tree:
    if tree is And:
        return Und(left=translate_en_de(tree.left), right=translate_en_de(tree.right))
    if tree is Jump:
        if tree.modifiers.contains(Twice):
            return Zweimal(Springen(modifiers=[translate_en_de(mod) for mod in modifiers]))
        else:
            return Springen()

EN.