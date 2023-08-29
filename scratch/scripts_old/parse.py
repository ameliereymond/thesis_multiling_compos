# Let's take a sample sentence for this script
sentence = "jump twice and look around"

## LEXER ##
# Or tokenizer. Converts a string to a sequence of
# tokens, e.g. "jump twice and turn around" to
# List(Jump, Twice, And, Turn, Around)

# Let's first define the tokens
from enum import Enum

class Token(Enum):
    Jump   = 1
    Twice  = 2
    And    = 3
    Look   = 4
    Around = 5

# And let's now write a function translating the string
# to a list of tokens. This will be a straightforward
# translation but is useful nonetheless.
# Usually, the goal of lexing is to standardize the
# representation of the text, i.e.

from typing import List

def lex(sentence: str) -> List[Token]:
    tokens = []
    for word in sentence.split(" "):
        if word == "":
            pass
        elif word == "jump":
            tokens.append(Token.Jump)
        elif word == "twice":
            tokens.append(Token.Twice)
        elif word == "and":
            tokens.append(Token.And)
        elif word == "look":
            tokens.append(Token.Look)
        elif word == "around":
            tokens.append(Token.Around)
        else:
            raise Exception(f"Unrecognised token: {word}")

    return tokens

## PARSER ##
# Now, let's parse this into a tree.

# Let's start by defining the tree.
# This tree is built so that the sentence above can be represented as:
#
#                   And
#                  /   \
#               Jump   Look
#                 |      |
#               Twice  Around

# This dataclass thing is just to cut down on the length of the code for the classes.
# Using @dataclass, Python will auto-generate some __init__() functions so that I don't have
# to write them manually. For instance I can write:
# 
#   @dataclass
#   class Person:
#       first_name: str
#       last_name: str
#
# This generates:
#
#   class Person:
#       def __init___(self, first_name: str, last_name: str):
#           self.first_name = first_name
#           self.last_name = last_name
#
# In both cases we can then initiate it as Person("Taylor", "Swift").
from dataclasses import dataclass

@dataclass
class Tree:
    pass

@dataclass
class Jump(Tree):
    modifiers: List[Tree]

@dataclass
class Look(Tree):
    modifiers: List[Tree]

@dataclass
class And(Tree):
    left: Tree
    right: Tree

@dataclass
class Twice:
    pass

@dataclass
class Around:
    pass

# Now, let's define the parser, i.e. the function converting
# a list of tokens to a tree.
#
# This will be a recursive function. We will also define some
# helper functions, which can recurse as well.
#
# We'll assume the grammar is something like:
#
#  S       = command
#  command = action | action And command
#  action  = verb [modifiers...]
#
# NOTE: we make a choice to tell the parser to recurse right on And (even though original SCAN grammar does not specify)
# 
# The internal parsing functions all return a Tuple[Tree, List[Token]] or Tuple[List[Tree], List[Token]].
# The left element of the Tuple, i.e. the Tree or List[Tree], represents the parsed tree.
# The right element of the Tuple, i.e. the List[Token], represent the remaining tokens that were not yet parsed by the function
from typing import Tuple

def parse(tokens: List[Token]) -> Tree:
    # At the top level (indicated by S in the parsing grammar), we parse a command:
    [tree, remaining] = parseCommand(tokens)

    # If there are tokens remaining after the command, that's unexpected.
    # We do not know how to parse that. Throw an exception.
    if len(remaining) > 0:
        raise Exception(f"Did not expect any tokens to remain. {remaining}")
    
    # If there are no tokens remaining, we parsed everything! Return the Tree.
    return tree

def parseCommand(tokens: List[Token]) -> Tuple[Tree, List[Token]]:
    # A command starts with an action. We'll call parseAction to parse that.
    # The returned tree is the parsed action, and remaining contains all the tokens after that action.
    [tree, remaining] = parseAction(tokens)

    # If there are no tokens after the action, we're done. Return.
    if len(remaining) == 0:
        return [tree, remaining]

    if remaining[0] == Token.And:
        # If there is an And token after the action, we want to return And(left, right),
        # where left is what we've parsed so far (i.e., tree)
        # and right is another command (i.e. parseCommand(remaining[1:]))
        left = tree
        [right, new_remaining] = parseCommand(remaining[1:])
        return [And(left, right), new_remaining]
    else:
        raise Exception(f"Unexpected token {remaining[0]} after an action")

def parseAction(tokens: List[Token]) -> Tuple[Tree, List[Token]]:
    # We want to read the first token, so let's first check that there is one
    if len(tokens) == 0:
        raise Exception("No tokens for parseAction!")

    # Let's now inspect this first token
    if tokens[0] == Token.Look:
        # If it's look, we want to parse the following words to see if there are
        # any modifiers on the action of looking, e.g. look left, look around, etc.
        # If there are no modifiers, parseModifiers will return an empty list.
        [modifiers, remaining] = parseModifiers(tokens[1:])
        return [Look(modifiers), remaining]
    
    elif tokens[0] == Token.Jump:
        # Same thing for jump
        [modifiers, remaining] = parseModifiers(tokens[1:])
        return [Jump(modifiers), remaining]

    else:        
        raise Exception(f"Unexpected token {tokens[0]} for an action")


def parseModifiers(tokens: List[Token]) -> Tuple[List[Tree], List[Token]]:
    # In parseModifiers, we return a List[Tree] and not a Tree. That's because
    # there can be multiple modifiers on an action (e.g. [Around, Twice, ...])
    modifiers = []

    for i, token in enumerate(tokens):
        if token == Token.Around:
            # Translate the Token.Around to the Around tree node (it's a leaf in the parse tree)
            modifiers.append(Around)
        
        elif token == Token.Twice:
            # Translate the Token.Twice to the Twice tree node 
            modifiers.append(Twice)
        
        else:
            # If the current word isn't a modifier, then we're done.
            # Return all the modifiers we've parsed, and let the caller handle how to parse the remaining tokens.
            return [modifiers, tokens[i:]]
    
    return [modifiers, []]


tokens = lex(sentence)
print(f"Tokens: {tokens}")

tree = parse(tokens)
print(f"Tree: {tree}")

