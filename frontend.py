# frontend.py
# Author: Mark Liffiton
# Date: Sep, 2023
#
# Functions implementing the front-end of the interpreter for CS355 A2
#
import sys


def read():
    """Read an entire file into a string

    Either reads from a file if a filename is given on the commandline
    or from stdin if not.

    Returns:
      A string containing the contents of the file or stdin.
    """
    try:
        fileobj = open(sys.argv[1], 'r')
    except IndexError:
        fileobj = sys.stdin
    with fileobj as f:
        return f.read()


def parse(text):
    """Tokenize and parse a program text into an AST.

    Args:
      text (string): The program text to parse.

    Returns:
      An AST as a recursive list of strings-and-lists.
      Expression nodes in the AST are represented as lists.
      Each component of an expression is a separate element in the list.
    """
    # Ensure parentheses are split from other tokens
    text = text.replace('(', ' ( ')
    text = text.replace(')', ' ) ')
    # Simply split the entire program on any whitespace to get a list of tokens
    tokens = text.split()

    # Iteratively parse the tokens into an AST

    # Set up a top-level list
    top = []
    cur = top

    # Use a stack to store parent nodes as we go
    stack = []
    stack.append(cur)

    for part in tokens:
        if part == '(':
            new = []
            cur.append(new)
            cur = new
            stack.append(cur)
        elif part == ')':
            stack.pop()
            cur = stack[-1]
        else:
            cur.append(part)

    assert len(stack) == 1, "Invalid program.  Probably mismatched parentheses."
    assert len(top) == 1, "Invalid program.  A valid program contains exactly one ( ) expression at the topmost level."

    # return the one expression of the program
    return top[0]
