#!/usr/bin/env python3
# interp.py
# Author: Mark Liffiton and Harsh Patel
# Date: Sep, 2023
#
# Implementation of an interpreter for CS355 A2
#

from frontend import read, parse


def is_float(atom):
    """Return True if the given atom represents a floating point number,
    False otherwise.
    """
    try:
        float(atom)
        return True
    except ValueError:
        return False


def is_string(atom):
    """Return True if the given atom represents a string, False otherwise.
    An atom represents a string if it starts and ends with " double quotes.
    """
    # Checks is the atom is a string that begins and ends with a quote
    if isinstance(atom, str) and atom[0] == '"' and atom[-1] == '"':
        return True
    else: 
        return False


def evaluate(node):
    """Evaluate an AST node and return its value.

    Args:
      node: The AST node to evaluate.  Either an expression (list) or atom (string)

    Returns:
      The value of the node.  The type depends on the node.
    """
    if isinstance(node, list):
        return evaluate_expr(node)
    else:
        return evaluate_atom(node)


# Use this global dictionary to store the interpreted program's variables.
variables = {}


def assign_var(name, val):
    """Assign a value to a program variable.

    Args:
      name (string): The variable to assign.
      val (varies): The value to assign to it.
    """
    # Resource: https://www.tutorialspoint.com/How-do-I-assign-a-dictionary
    # -value-to-a-variable-in-Python#:~:text=You%20can%20assign%20a%20dictionary,
    # using%20the%20access%20operator%20%5B%5D. 
    # assigns the key to the value in the dictionary
    # assigns a value to a variable(key) in our george lang.
    variables[name] = val


def lookup_var(name):
    """Get the value of a variable.

    Args:
      name (string): The variable to look up.

    Returns:
      The variable's current value.
    """
    # resource: https://careerkarma.com/blog/python-dictionary-get/#:~:
    # text=get()%20method%20is%20used,a%20key%20is%20not%20found.
    # .get() retrieves the value associated with the key(name),
    # the key of the dict is the variable
    return variables.get(name) 
    

def evaluate_atom(atom):
    """Evaluate an atom (Number, String, or Variable).

    Args:
      atom (string): The string representation of the atom to evaluate.

    Returns:
      The atom's value.
    """
    assert isinstance(atom, str), f"Invalid atom: {atom}"
    # if the variable is present in the dict, return the atom
    # if the atom is a float, return that atom as a float,
    # if it's a string then return that atom
    if is_float(atom) == True:
        return float(atom)
    elif is_string(atom) == True:
        return atom
    elif lookup_var(atom) is not None:
        # returns the value of that var
        return  lookup_var(atom)


def evaluate_expr(expr):
    """Evaluate an expression.

    Args:
      expr (list): The expression to evaluate as an AST node (list).

    Returns:
      The expression's value.
    """
    assert isinstance(expr, list), f"Invalid expression: {expr}"
    # initialize the variable word to the first element in the list
    
    word = expr[0]
    # if we see print, then print everything after that print
    if word == 'print':
      for i in expr[1:]:
        # prints whats being evaluated
        result = evaluate(i)
        print(result)

    # if we find the word run, then
    # for every element in the list after the word run, evaluate it
    # return the expressions
    if word == 'run':
      for i in expr[1:]:
          result = evaluate(i)
      return result
    
    # When '+' is found, evaluate the expressions then add them
    if word == '+':
      # Initialize to store the sum
      add = evaluate(expr[1])
      for i in expr[2:]:
        result = evaluate(i)
        add += result
      return add
    
    # When '-' is found, evaluate the expressions then subtract them
    if word == '-':
      # Evaluates the first expression 
      minus = evaluate(expr[1])
      # starts from the second expression
      for i in expr[2:]:
        result = evaluate(i)
        # subtracts the first expression with the rest of the expressions
        minus = minus - result
      return minus
    
    # Multiplication operation that multiplies two arguments
    if word == '*':
      # Evaluates the first expression
      mult = evaluate(expr[1])
      # starts from the second expression
      for i in expr[2:]:
        result = evaluate(i)
        # multiplies the first expression with the rest of the expressions
        mult = mult * result
      return mult  
    
    # Divide operation that divides two arguments
    if word == '/':
      # Evaluates the first expression 
      divide = evaluate(expr[1])
      # starts from the second expression
      for i in expr[2:]:
        result = evaluate(i)
        # divides the first expression with the rest of the expressions
        divide = divide / result
      return divide
    
    # Checks for the less than operation
    if word == '<':
       # stores teh first expression
       less = evaluate(expr[1])
       # Starts from the next expression
       for i in expr[2:]:
          result = evaluate(i)
          # if the first expression is less than the next expression(s)
          # return true, else false
          if less < result:
             return True
          else:
             return False
          
    # checks for the greater than operation
    if word == '>':
       # stores the first expression
       greater = evaluate(expr[1])
       # Starts from the next expression
       for i in expr[2:]:
          result = evaluate(i)
          # if the first expression is greater than the next expression(s)
          # return true, else false
          if greater > result:
             return True
          else:
             return False
          
    # checks for the equal too operation      
    if word == "==":
      # stores the first expression
      equal = evaluate(expr[1])
      # Starts from the next expression
      for i in expr[2:]:
        result = evaluate(i)
        # if the first expression is equal to the next expressions
        # return true, else return false
        if equal == result:
          return True
        else:
          return False
        
    # Let assigns a variable to a value
    if word == "let":
      # assign the first variable to the first expression
      var1 = expr[1]
      # assign the value to the second expression and evaluate it
      var_val = evaluate(expr[2])
      # assigns the var to the val
      result = assign_var(var1, var_val)
      # gets the value of the expression
      value = lookup_var(result)
      return value
    
    # If function that compares two arguments and returns the proper argument
    if word == 'if':
      # stores the comparison operator
      comparison = evaluate(expr[1])
      # if the comparison is true, then it evaluates to the 2nd argument
      if comparison is True:
        return evaluate(expr[2])
      else:
      # if the comparison is false, then it evaluates to the 3rd argument
        return evaluate(expr[3])
    
    # Lambda function that creates a function
    if word == 'lambda':
       # Evaluates to the ast of its argument
       func_name = expr[1]
       return func_name
   
   # Call function that calls a function
    if word == 'call':
       # Evaluates to an AST
       func_name = expr[1]
       val = lookup_var(func_name)
       #returns its value
       return evaluate(val)
    
    
def main():
    # The main function of our interpreter.
    # Read a program, parse it into its AST, and evaluate that AST.
    instr = read()
    AST = parse(instr)

    # If you want to see the AST for debugging, uncomment this.
    # Do not leave it uncommented in your submission, though!
    #print(AST)
    evaluate(AST)


if __name__ == '__main__':
    main()
