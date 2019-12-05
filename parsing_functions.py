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
    proposition = remove_outer_parens(proposition)
    
    if '(' not in proposition:
        for con in BINARY_CONNECTIVES:
            if con in proposition:
                return con
        for con in UNARY_CONNECTIVES:
            if con == proposition[0:2]:
                return con
        return ''
    
    if proposition[0:2] in UNARY_CONNECTIVES:
        connective = proposition[0:2]
        while proposition[0:2] in UNARY_CONNECTIVES:
            proposition = proposition[2:]

        if has_outer_parens(proposition) or main_connective(proposition) == '':
            return connective
    
    while not proposition[0:2] in BINARY_CONNECTIVES:
        proposition = proposition[1:]
    
    while not proposition.count('(') == proposition.count(')'):
        proposition = proposition[1:]
        while not proposition[0:2] in BINARY_CONNECTIVES:
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
    proposition = remove_outer_parens(proposition)
    main_con = main_connective(proposition)

    if main_con == '':
        return proposition

    if main_con in UNARY_CONNECTIVES:
        return ''
    
    part_1 = ''
    while not (proposition[0:2] == main_con and proposition.count('(') == proposition.count(')')):
        part_1 += proposition[0]
        proposition = proposition[1:]
    return normalize(part_1)

def second_part(proposition):
    proposition = remove_outer_parens(proposition)
    main_con = main_connective(proposition)

    if main_con == '':
        return proposition

    if main_con in UNARY_CONNECTIVES:
        return proposition[2:]
    
    while not (proposition[0:2] == main_con and proposition.count('(') == proposition.count(')')):
        proposition = proposition[1:]
    return normalize(proposition[2:])

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
        '--A -> (A /\\ <>B)' : '((--A) -> (A /\\ (<>B)))',
        '[]B' : '([]B)',
        '[]A -> []B' : '(([]A) -> ([]B))'
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
