import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$') #avalia se tem um ponto ou não
#^ - > começa com $-> termina com (logo só pode 1 caracter)

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def converToNumber(string:str):
    number = float(string)

    if number.is_integer():
        number = int(number)
        
    return number

def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True

    except ValueError:
        valid = False
    return valid

def isEmpty(string: str):
    #return string == ''
    return len(string) == 0
