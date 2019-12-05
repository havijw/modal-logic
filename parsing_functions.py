UNARY_CONNECTIVES = ['--', '[]', '<>']
BINARY_CONNECTIVES = ['->', '/\\', '\\/']

class ParensError(Exception):
    pass

# determines if an argument has redundant outer parentheses
def has_outer_parens(proposition):
    if proposition == '' or len(proposition) == 1:
        return False

    if not proposition[0] == '(' and proposition[-1] == ')':
        return False
    
    proposition = proposition[1:]
    while not (proposition.count('(') == proposition.count(')')):
        proposition = proposition[1:]
    
    if proposition == '':
        return True
    return False

# takes redundant outer parentheses off for consistent formatting
def remove_outer_parens(proposition):
    proposition = proposition.replace(' ', '')
    if proposition == '':
        return ''
    
    while has_outer_parens(proposition):
        proposition = proposition[1:-1]
    return proposition

# finds the main connective of an argument
def main_connective(proposition):
    if not proposition.count('(') == proposition.count(')'):
        raise ParensError('Mismatched parentheses in proposition %s' % proposition)

    proposition = remove_outer_parens(proposition).replace(' ', '')

    # check if there is any connective in the proposition
    connected = False
    for connective in UNARY_CONNECTIVES:
        if connective in proposition:
            connected = True
            break
    if not connected:
        for connective in BINARY_CONNECTIVES:
            if connective in proposition:
                connected = True
                break
    if not connected:
        return ''

    while not ((   proposition[0:2] in BINARY_CONNECTIVES
                or proposition[0:2] in UNARY_CONNECTIVES  and has_outer_parens(proposition[2:]))
               and proposition.count('(') == proposition.count(')')):
        if proposition == '':
            raise ParensError
        proposition = proposition[1:]
    
    return proposition[0:2]

# adds negation to the front of an argument
def add_negation(arg):
    arg = normalize(arg)

    return '(--' + arg + ')'

# removes negation from argument if it exists
# otherwise just returns the argument
def remove_negation(arg):
    arg = normalize(arg)
    
    if not main_connective(arg) == '--':
        return arg
    else:
        return arg[3:-1]

# finds the part of the argument before the main connective
# for example, first_part('A \\/ B') returns 'A'
def first_part(proposition):
    if not proposition.count('(') == proposition.count(')'):
        raise ParensError('Mismatched parentheses in proposition %s' % proposition)

    proposition = remove_outer_parens(proposition).replace(' ', '')

    unary = False
    binary = False
    # check for binary connective
    for connective in BINARY_CONNECTIVES:
        if connective in proposition:
            binary = True
            break
    
    # check for unary connective
    for connective in UNARY_CONNECTIVES:
        if connective in proposition:
            unary = True
            break
    
    # unary but not binary has no first part
    if unary and not binary:
        return ''
    # neither unary nor binary is just a letter
    elif not (unary or binary):
        return proposition
    
    first_part = ''

    while not ((   proposition[0:2] in BINARY_CONNECTIVES
                or proposition[0:2] in UNARY_CONNECTIVES  and has_outer_parens(proposition[2:]))
               and proposition.count('(') == proposition.count(')')):
        if proposition == '':
            raise ParensError
        first_part += proposition[0]
        proposition = proposition[1:]
    
    return first_part

def second_part(proposition):
    if not proposition.count('(') == proposition.count(')'):
        raise ParensError('Mismatched parentheses in proposition %s' % proposition)

    proposition = remove_outer_parens(proposition).replace(' ', '')

    binary = False
    for connective in BINARY_CONNECTIVES:
        if connective in proposition:
            binary = True
            break

    unary = False
    for connective in UNARY_CONNECTIVES:
        if connective in proposition:
            unary = True
            break
    
    if not binary:
        if unary:
            proposition = proposition.replace('(', '')
            proposition = proposition.replace(')', '')
            return proposition[2:]
        
        else:
            return proposition

    while not (proposition[0:2] in BINARY_CONNECTIVES and proposition.count('(') == proposition.count(')')):
        if proposition == '':
            raise ParensError
        proposition = proposition[1:]
    
    return proposition[2:]

# normalizes argument to standard form
def normalize(proposition):
    main_con = main_connective(proposition)
    
    if main_con == '':
        proposition = proposition.replace('(', '').replace(')', '')
        return proposition
    elif main_con in UNARY_CONNECTIVES:
        return ''.join(['(', main_con, normalize(second_part(proposition)), ')'])
    elif main_con in BINARY_CONNECTIVES:
        return ''.join(['(', normalize(first_part(proposition)), ' ', main_con, ' ', normalize(second_part(proposition)), ')'])

def test_main_connective():
    test_cases = {
        'A' : '',
        '--A' : '--',
        '<>A' : '<>',
        '[]A' : '[]',
        'A -> B' : '->',
        'A /\\ B' : '/\\',
        'A \\/ B' : '\\/',
        '(A)' : '',
        '(--A)' : '--',
        '--(A)' : '--',
        'A -> --B' : '->',
        '--A -> B' : '->',
        '--A -> (B)' : '->',
        '--A -> --B' : '->',
        '(--A) -> (B /\\ A)' : '->',
        '--<>[]--A' : '--',
        '<><>[]<>A' : '<>',
        '<>[]A -> <><>(A -> []B)' : '->',
        '((A -> B) \\/ (C /\\ D)) -> E': '->',
        '--A -> (A /\\ <>B)' : '->',
        '(A /\\ <>B)' : '/\\',
        '[](A -> B)' : '[]'
        # '(A -> B' : '->', # should throw a ParensError
        # 'A -> B)' : '->'  # should throw a ParensError
    }

    failed = False
    for proposition in test_cases:
        main_con = main_connective(proposition)
        if not main_con == test_cases[proposition]:
            failed = True
            print('FAILURE:\nProposition %s returned %s should be %s' % (proposition, main_con, test_cases[proposition]))
    
    if not failed:
        print('Looks good. Nice.')

def test_first_part():
    test_cases = {
        'A' : 'A',
        '--A' : '',
        '<>A' : '',
        '[]A' : '',
        'A -> B' : 'A',
        'A /\\ B' : 'A',
        'A \\/ B' : 'A',
        '(A)' : 'A',
        '(--A)' : '',
        '--(A)' : '',
        'A -> --B' : 'A',
        '--A -> B' : '--A',
        '--A -> (B)' : '--A',
        '--A -> --B' : '--A',
        '(--A) -> (B /\\ A)' : '(--A)',
        '--<>[]--A' : '',
        '<><>[]<>A' : '',
        '<>[]A -> <><>(A -> []B)' : '<>[]A',
        '[](A -> B)' : ''
        # 'A -> B)' : 'A', # should throw a ParensError
        # '(A -> B' : '(A' # should throw a ParensError
    }

    failed = False
    for proposition in test_cases:
        part_1 = first_part(proposition)
        if part_1 == test_cases[proposition]:
            pass
        else:
            failed = True
            print('FAILURE:\nProposition %s returned .%s. should be .%s.' % (proposition, part_1, test_cases[proposition]))
    
    if not failed:
        print('Looks good. Nice.')

def test_second_part():
    test_cases = {
        'A' : 'A',
        '--A' : 'A',
        '<>A' : 'A',
        '[]A' : 'A',
        'A -> B' : 'B',
        'A /\\ B' : 'B',
        'A \\/ B' : 'B',
        '(A)' : 'A',
        '(--A)' : 'A',
        '--(A)' : 'A',
        'A -> --B' : '--B',
        '--A -> B' : 'B',
        '--A -> (B)' : '(B)',
        '--A -> --B' : '--B',
        '(--A) -> (B /\\ A)' : '(B/\\A)',
        '--<>[]--A' : '<>[]--A',
        '<><>[]<>A' : '<>[]<>A',
        '<>[]A -> <><>(A -> []B)' : '<><>(A->[]B)',
        '[](A -> B)' : 'A -> B'
        # 'A -> B)' : 'B)', # shouldn't throw a ParensError
        # '(A -> B' : '(A' # should throw a ParensError
    }

    failed = False
    for proposition in test_cases:
        part_2 = second_part(proposition)
        if not part_2 == test_cases[proposition]:
            failed = True
            print('FAILURE:\nProposition %s returned .%s. should be .%s.' % (proposition, part_2, test_cases[proposition]))
    
    if not failed:
        print('Looks good. Nice.')

def test_normalize():
    test_cases = {
        'A /\\ B /\\ C' : '(A /\\ (B /\\ C))',
        'A -> B' : '(A -> B)',
        '--A' : '(--A)',
        '--<>A' : '(--(<>A))',
        '--A -> (A /\\ <>B)' : '((--A) -> (A /\\ (<>B)))'
    }

    failed = False
    for proposition in test_cases:
        normed = normalize(proposition)
        if not normed == test_cases[proposition]:
            failed = True
            print('FAILURE:\nProposition %s returned .%s. should be .%s.' % (proposition, normed, test_cases[proposition]))
    
    if not failed:
        print('Looks good. Nice.')

if __name__ == '__main__':
    test_second_part()
