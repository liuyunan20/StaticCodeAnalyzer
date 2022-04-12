import math


# Modify this function in the shell and copy the new version here
def my_sqrt(value):
    if type(value) is int or type(value) is float:
        return math.sqrt(value)
    if type(value) is str:
        return "The string should be converted into a numeric data type"
    return None
