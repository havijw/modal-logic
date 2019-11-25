# determines if an argument has redundant outer parentheses
def has_outer_parens(arg):
    if not (arg[0] == '(' and arg[-1] == ')'):
        return False
    
    arg = arg[1:]
    while not (arg.count('(') == arg.count(')')):
        arg = arg[1:]
    
    if arg == '':
        return True
    return False

# takes redundant outer parentheses off for consistent formatting
def strip_outer_parens(arg):
    # if the argument is nothing, just return it
    if arg == '':
        return arg
    
    arg = arg.strip()

    while has_outer_parens(arg):
        arg = arg[1:-1]
    return arg

# finds the main connective of an argument
def main_connective(proposition):
    proposition = strip_outer_parens(proposition)
    proposition = proposition.replace(' ', '')

    dual_connectives = ['->', '/\\', '\\/']
    single_connectives = ['|=|', '<>', '~']

    if '(' not in proposition:
        for connective in dual_connectives:
            if connective in proposition:
                return connective
        
        if proposition[0:1] == '~':
            return '~'
        elif proposition[0:2] == '<>':
            return '<>'
        elif proposition[0:3] == '|=|':
            return '|=|'
        
        return ''
    
    else:
        part_1 = ''
        while not proposition[0] == '(':
            part_1 += proposition[0]
            proposition = proposition[1:]
        
        # part_1 could be nothing if the first part is in parens
        if part_1 == '':
            part_1 = proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
        
        elif part_1 in single_connectives:
            connective = part_1
            part_1 = proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
            
            if proposition == '':
                return connective
            else:
                part_1 = remove_negation(part_1)
                part_1 = strip_outer_parens(part_1)
        
        if part_1[-2:] in dual_connectives:
            return part_1[-2:]

        elif part_1[-2:] == '<>':
            if not part_1.upper() == part_1.lower():
                return '<>'
            else:
                if part_1[0:2] == '<>':
                    return '<>'
                elif part_1[0:3] == '|=|':
                    return '|=|'
                elif part_1[0:1] == '~':
                    return '~'
        
        elif part_1[-3:] == '|=|':
            if not part_1.upper() == part_1.lower():
                return '|=|'
            else:
                if part_1[0:2] == '<>':
                    return '<>'
                elif part_1[0:3] == '|=|':
                    return '|=|'
                elif part_1[0:1] == '~':
                    return '~'
        
        elif part_1[-1:] == '~':
            if not part_1.upper() == part_1.lower():
                return '~'
            else:
                if part_1[0:2] == '<>':
                    return '<>'
                elif part_1[0:3] == '|=|':
                    return '|=|'
                elif part_1[0:1] == '~':
                    return '~'
        
        if proposition[0:2] in dual_connectives:
            return proposition[0:2]
        elif proposition[0:2] == '<>':
            return '<>'
        elif proposition[0:3] == '|=|':
            return proposition[0:3]
        elif proposition[0:1] == '~':
            return proposition[0:1]

# adds negation to the front of an argument
def add_negation(arg):
    arg = normalize(arg)

    return '(~' + arg + ')'

# removes negation from argument if it exists
# otherwise just returns the argument
def remove_negation(arg):
    arg = normalize(arg)
    
    if not main_connective(arg) == '~':
        return arg
    else:
        return arg[2:-1]

# finds the part of the argument before the main connective
# for example, first_part('A \\/ B') returns 'A'
def first_part(proposition):
    proposition = strip_outer_parens(proposition)
    proposition = proposition.replace(' ', '')

    dual_connectives = ['->', '/\\', '\\/']
    single_connectives = ['|=|', '<>', '~']

    main_con = main_connective(proposition)

    if main_con == '':
        return proposition
    elif main_con == '~' or main_con == '<>' or main_con == '|=|':
        return ''
    
    part_1 = ''

    if '(' not in proposition:
        while not proposition[0:2] == main_con:
            part_1 += proposition[0]
            proposition = proposition[1:]
    
    else:
        part_1 = ''
        while not proposition[0] == '(':
            part_1 += proposition[0]
            proposition = proposition[1:]
        
        # part_1 could be nothing if the first part is in parens
        if part_1 == '':
            part_1 = proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
        
        elif part_1 in single_connectives:
            part_1 += proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
            
            part_1 = strip_outer_parens(part_1)
    
    if part_1[-2:] in dual_connectives:
        part_1 = part_1[0:-2]
    
    return normalize(part_1)

def second_part(proposition):
    proposition = strip_outer_parens(proposition)
    proposition = proposition.replace(' ', '')

    dual_connectives = ['->', '/\\', '\\/']
    single_connectives = ['|=|', '<>', '~']

    main_con = main_connective(proposition)

    if main_con == '':
        return proposition
    elif main_con == '~':
        return proposition[1:]
    elif main_con == '<>':
        return proposition[2:]
    elif main_con == '|=|':
        return proposition[3:]
    
    part_1 = ''

    if '(' not in proposition:
        while not proposition[0:2] == main_con:
            part_1 += proposition[0]
            proposition = proposition[1:]
    
    else:
        part_1 = ''
        while not proposition[0] == '(':
            part_1 += proposition[0]
            proposition = proposition[1:]
        
        # part_1 could be nothing if the first part is in parens
        if part_1 == '':
            part_1 = proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
        
        elif part_1 in single_connectives:
            part_1 += proposition[0]
            proposition = proposition[1:]

            while not part_1.count(')') == part_1.count('('):
                part_1 += proposition[0]
                proposition = proposition[1:]
            
            part_1 = strip_outer_parens(part_1)
    
    if proposition[0:2] in dual_connectives:
        proposition = proposition[2:]
    
    return normalize(proposition)

# normalizes argument to standard form
def normalize(arg):
    arg = strip_outer_parens(arg)

    main_con = main_connective(arg)

    if main_con == '':
        return arg
    
    # store first and second parts of argument
    # use recursion to normalize first and second parts
    # then combine everything back into one piece
    p1 = normalize(first_part(arg))
    p2 = normalize(second_part(arg))

    # reassemble the pieces
    if main_con in ['~', '|=|', '<>']:
        arg = main_con + p2
    else:
        arg = p1 + ' ' + main_con + ' ' + p2

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

def test_main_connective():
    to_test = [
        'A',
        'A -> B',
        'A /\\ B',
        'A \\/ B',
        '~A',
        '(A -> B) /\\ C',
        'C /\\ (A -> B)',
        '((A -> B) /\\ (C -> D))',
        '(A -> B) /\\ (C -> D)',
        '(~A -> B) \\/ ~(A -> C \\/ D)',
        '(A)',
        '((A))',
        '~~(p \\/ ~p)',
        '((~p -> r) /\\ (~q -> r)) -> (~(p /\\ q) -> r)',
        '(~(p /\\ q) -> r)',
        '(~p -> r) /\\ (~q -> r)'
    ]

    proposition = '|=|(A -> B) -> (|=|A -> |=|B)'
    print(main_connective(proposition))
    print(first_part(proposition))
    
    # for proposition in to_test:
        # print(main_connective(proposition))

def test_first_part():
    to_test = [
        'A',
        'A -> B',
        'A /\\ B',
        'A \\/ B',
        '~A',
        '(A -> B) /\\ C',
        'C /\\ (A -> B)',
        '((A -> B) /\\ (C -> D))',
        '(A -> B) /\\ (C -> D)',
        '(~A -> B) \\/ ~(A -> C \\/ D)',
        '(A)',
        '((A))',
        '~~(p \\/ ~p)',
        '((~p -> r) /\\ (~q -> r)) -> (~(p /\\ q) -> r)',
        '(~(p /\\ q) -> r)',
        '(~p -> r) /\\ (~q -> r)'
    ]
    
    for proposition in to_test:
        print(first_part(proposition))
    
    props = ['~P', '|=|P', '<>P', '<>P -> Q', '|=|P -> Q']

    for prop in props:
        print(first_part(prop))

def test_second_part():
    to_test = [
        'A',
        'A -> B',
        'A /\\ B',
        'A \\/ B',
        '~A',
        '(A -> B) /\\ C',
        'C /\\ (A -> B)',
        '((A -> B) /\\ (C -> D))',
        '(A -> B) /\\ (C -> D)',
        '(~A -> B) \\/ ~(A -> C \\/ D)',
        '(A)',
        '((A))',
        '~~(p \\/ ~p)',
        '((~p -> r) /\\ (~q -> r)) -> (~(p /\\ q) -> r)',
        '(~(p /\\ q) -> r)',
        '(~p -> r) /\\ (~q -> r)'
    ]
    correct_answers = [
        'A',
        'B',
        'B',
        'B',
        'A',
        'C',
        'A -> B',
        'C -> D',
        'C -> D',
        '~(A -> C \\/ D)',
        'A',
        'A',
        '~(p \\/ ~p)',
        '~(p /\\ q) -> r',
        'r',
        '~q -> r'
    ]
    
    for i in range(len(to_test)):
        print(correct_answers[i], ':', second_part(to_test[i]))

def test_normalize():
    to_test = [
        # '|=|A',
        # '|=|<>A',
        # '<>|=|A',
        # '|=||=|A',
        # '|=|<>A -> B',
        # '(|=|<>A /\\ |=||=|B) -> |=|<>(A)'# /\\ B)'
        '|=|<>(A)'
    ]

    for proposition in to_test:
        print(main_connective(proposition))
        # print(normalize(proposition))

if __name__ == '__main__':
    test_normalize()
