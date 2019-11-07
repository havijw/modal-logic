# determines if an argument has redundant outer parentheses
def hasOuterParens(arg):
    if not (arg[0] == '(' and arg[-1] == ')'):
        return False
    
    arg = arg[1:]
    while not (arg.count('(') == arg.count(')')):
        arg = arg[1:]
    
    if arg == '':
        return True
    return False

# takes redundant outer parentheses off for consistent formatting
def stripOuterParens(arg):
    # if the argument is nothing, just return it
    if arg == '':
        return arg
    
    arg = arg.strip()

    # while there are redundant parentheses, remove them
    while hasOuterParens(arg):
        arg = arg[1:-1]
    return arg

# finds the main connective of an argument
def mainConnective(arg):
    arg = stripOuterParens(arg)
    
    connectives = ['->', '/\\', '\\/', '~', '|=|', '<>']
    
    if '(' not in arg:
        for con in connectives:
            if con in arg:
                return con
        return ''
    
    else:
        if arg[0] == '~':
            while arg[0] == '~':
                arg = arg[1:]
            
            argDupe = arg[1:] # duplicate argument to modify and remove initial '('
            while not argDupe.count('(') == argDupe.count(')'):
                argDupe = argDupe[1:]
            
            if argDupe == '':
                return '~'
        
        elif arg[0:3] == '|=|':
            while arg[0:3] == '|=|':
                arg = arg[3:]
            
            argDupe = arg[1:]
            while not argDupe.count('(') == argDupe.count(')'):
                argDupe = argDupe[1:]
            
            if argDupe == '':
                return '|=|'
        
        elif arg[0:2] == '<>':
            while arg[0:2] == '<>':
                arg = arg[2:]
            
            argDupe = arg[1:]
            while not argDupe.count('(') == argDupe.count(')'):
                argDupe = argDupe[1:]
            
            if argDupe == '':
                return '<>'

        while not arg[0:2] in connectives:
            arg = arg[1:]
        
        while not arg.count('(') == arg.count(')'):
            arg = arg[1:]
            while not arg[0:2] in connectives:
                arg = arg[1:]
        
        return arg[0:2]

# adds negation to the front of an argument
def addNeg(arg):
    arg = normalize(arg)

    return '(~' + arg + ')'

# removes negation from argument if it exists
# otherwise just returns the argument
def removeNeg(arg):
    arg = normalize(arg)
    
    if not mainConnective(arg) == '~':
        return arg
    else:
        return arg[2:-1]

# finds the part of the argument before the main connective
# for example, firstPart('A \\/ B') returns 'A'
def firstPart(arg):
    arg = stripOuterParens(arg)
    
    # store main connecitve of argument
    con = mainConnective(arg)
    
    # for single sentence connectivess, return nothing
    if con == '~' or con == '|=|' or con == '<>':
        return ''

    # build first part of argument
    # essentially just add the beginning of the
    # string until the main connective is reached
    p1 = ''
    if '(' in arg:
        # move beginning of arg to p1 until the main connective is reached
        while not arg[0:2] == con:
            p1 += arg[0]
            arg = arg[1:]
        
        # if parentheses are unbalanced, keep going until they are
        # balanced and the main connective is reached
        while not p1.count('(') == p1.count(')'):
            p1 += con
            arg = arg[2:]
            while not arg[0:2] == con:
                p1 += arg[0]
                arg = arg[1:]
        
        return normalize(p1)
    
    # if no parentheses in the argument, just
    # take everything before the main connective
    else:
        while not arg[0:2] == con:
            p1 += arg[0]
            arg = arg[1:]
        return normalize(p1)

# finds the part of the argument after the main connective
# for example, secondPart('A \\/ B') returns 'B'
def secondPart(arg):
    arg = stripOuterParens(arg)
    
    # store main connective of argument
    con = mainConnective(arg)
    
    # for single sentence symbol, return nothing
    if con == '':
        return ''

    # build second part of argument
    # essentially just add the end of the string
    # until the main connective is reached
    p2 = ''
    if '(' in arg:
        # handle |=| separately because it's longer than all the others
        if con == '|=|':
            while not arg[-2:] == con:
                p2 = arg[-1] + p2
                arg = arg[:-1]
            
            while not p2.count('(') == p2.count(')'):
                p2 = con + p2
                arg = arg[:-2]
                while not arg[-3:] == con:
                    p2 = arg[-1] + p2
                    arg = arg[:-1]
            
            return normalize(p2)

        # move end of arg to p2 until the main connective is reached
        while not arg[-2:] == con:
            p2 = arg[-1] + p2
            arg = arg[:-1]
        
        # if parentheses are unbalanced, keep going until they are
        # balanced and the main connective is reached
        while not p2.count('(') == p2.count(')'):
            p2 = con + p2
            arg = arg[:-2]
            while not arg[-2:] == con:
                p2 = arg[-1] + p2
                arg = arg[:-1]
        
        return normalize(p2)
    
    # if no parentheses in the argument, just
    # take everything after the main connective
    else:
        if con == '|=|':
            while not arg[-3:] == con:
                p2 = arg[-1] + p2
                arg = arg[:-1]
            return normalize(p2)
        
        while not arg[-2:] == con:
            p2 = arg[-1] + p2
            arg = arg[:-1]
        return normalize(p2)

# normalizes argument to standard form
def normalize(arg):
    arg = stripOuterParens(arg)

    mainCon = mainConnective(arg)

    # nothing needs to be done for single sentence symbol
    if mainCon == '':
        return arg
    
    # store first and second parts of argument
    # use recursion to normalize first and second parts
    # then combine everything back into one piece
    p1 = normalize(firstPart(arg))
    p2 = normalize(secondPart(arg))

    # reassemble the pieces
    # negation doesn't need any spacing
    if mainCon == '~' or mainCon == '|=|' or mainCon == '<>':
        arg = mainCon + p2
    # otherwise add spaces in between pieces
    else:
        arg = p1 + ' ' + mainCon + ' ' + p2

    # ensure argument is enclosed in outer parentheses
    if not (arg[0] == '(' and arg[-1] == ')'):
        arg = '(' + arg + ')'
    else:
        argDupe = arg[1:]
        while not argDupe.count('(') == argDupe.count(')'):
            argDupe = argDupe[1:]
        
        if not argDupe == '':
            arg = '(' + arg + ')'
    
    return arg

def test_mainConnective():
    props = ['|=|P', '<>P', '|=|P -> Q', '<>P -> Q']

    for prop in props:
        print(mainConnective(prop))

def test_firstPart():
    props = ['~P', '|=|P', '<>P', '<>P -> Q', '|=|P -> Q']

    for prop in props:
        print(prop, firstPart(prop))

def test_secondPart():
    props = ['~P', '|=|P', '<>P', '<>P -> Q', '|=|P -> Q']

    for prop in props:
        print(prop, secondPart(prop))

if __name__ == '__main__':
    test_secondPart()