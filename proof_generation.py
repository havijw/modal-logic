from proposition_checker import check_proposition
from parsing_functions import (
    normalize,
    first_part,
    second_part,
    main_connective,
    strip_outer_parens
)
from Proof_Model import Proof_Model
from copy import copy

def get_logic():
    print('Which modal logic would you like to work in?',
          '(1) K',
          '(2) KT',
          '(3) S4',
          '(4) S5', sep='\n', end='\n')
    
    choice = input()
    while not ('1' in choice or
               '2' in choice or
               '3' in choice or
               '4' in choice or
               choice.upper() == 'K' or
               choice.upper() == 'KT' or
               choice.upper() == 'S4' or
               choice.upper() == 'S5'):
        print('Sorry, %s is not a logic I know\nWhich modal logic would you like to work in?' % choice)
        choice = input()
    
    if '1' in choice or choice.upper() == 'K':
        return 'K'
    elif '2' in choice or choice.upper() == 'KT':
        return 'KT'
    elif '3' in choice or choice.upper() == 'S4':
        return 'S4'
    elif '4' in choice or choice.upper() == 'S5':
        return 'S5'

def get_proposition():
    print('Enter the proposition you would like to check')

    proposition = normalize(input())

    return proposition

def initialize_tableau(proposition, logic='K'):
    proposition = normalize(proposition)
    model = Proof_Model()
    model.add_world('1', propositions={proposition : False})
    if logic == 'KT':
        model.add_access('1', '1')
    
    return model

def is_reducible(model):
    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            main_con = main_connective(proposition)

            if main_con == '~':
                return True

            elif main_con == '/\\' and model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '\\/' and not model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '->' and not model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '|=|' and not model.worlds[world]['propositions'][proposition]:
                return True
            
            elif main_con == '<>' and model.worlds[world]['propositions'][proposition]:
                return True
    
    return False

def complete_tableau(model, logic='K'):
    while is_reducible(model):
        worlds_to_add = {}
        for world in model.worlds:
            propositions_to_add = {}
            propositions_to_remove = []
            for proposition in copy(model.worlds[world]['propositions']):
                main_con = main_connective(proposition)

                if main_con == '~':
                    if second_part(proposition) in model.worlds[world]['propositions']:
                        if model.worlds[world]['propositions'][second_part(proposition)] == model.worlds[world]['propositions'][proposition]:
                            return 'closed'
                    elif second_part(proposition) in propositions_to_add:
                        if propositions_to_add[second_part(proposition)] == model.worlds[world]['propositions'][proposition]:
                            return 'closed'

                    propositions_to_add[second_part(proposition)] = not model.worlds[world]['propositions'][proposition]
                    propositions_to_remove.append(proposition)
                
                elif main_con == '/\\' and model.worlds[world]['propositions'][proposition]:
                    if first_part(proposition) in model.worlds[world]['propositions']:
                        if not model.worlds[world]['propositions'][first_part(proposition)]:
                            return 'closed'
                    elif first_part(proposition) in propositions_to_add:
                        if not propositions_to_add[first_part(proposition)]:
                            return 'closed'
                    propositions_to_add[first_part(proposition)]  = True

                    if second_part(proposition) in model.worlds[world]['propositions']:
                        if not model.worlds[world]['propositions'][second_part(proposition)]:
                            return 'closed'
                    elif second_part(proposition) in propositions_to_add:
                        if not propositions_to_add[second_part(proposition)]:
                            return 'closed'
                    propositions_to_add[second_part(proposition)] = True

                    propositions_to_remove.append(proposition)
                
                elif main_con == '\\/' and not model.worlds[world]['propositions'][proposition]:
                    if first_part(proposition) in model.worlds[world]['propositions']:
                        if model.worlds[world]['propositions'][first_part(proposition)]:
                            return 'closed'
                    elif first_part(proposition) in propositions_to_add:
                        if propositions_to_add[first_part(proposition)]:
                            return 'closed'
                    propositions_to_add[first_part(proposition)]  = False

                    if second_part(proposition) in model.worlds[world]['propositions']:
                        if model.worlds[world]['propositions'][second_part(proposition)]:
                            return 'closed'
                    elif second_part(proposition) in propositions_to_add:
                        if propositions_to_add[second_part(proposition)]:
                            return 'closed'
                    propositions_to_add[second_part(proposition)] = False

                    propositions_to_remove.append(proposition)
                
                elif main_con == '->' and not model.worlds[world]['propositions'][proposition]:
                    if first_part(proposition) in model.worlds[world]['propositions']:
                        if not model.worlds[world]['propositions'][first_part(proposition)]:
                            return 'closed'
                    elif first_part(proposition) in propositions_to_add:
                        if not propositions_to_add[first_part(proposition)]:
                            return 'closed'
                    propositions_to_add[first_part(proposition)]  = True

                    if second_part(proposition) in model.worlds[world]['propositions']:
                        if model.worlds[world]['propositions'][second_part(proposition)]:
                            return 'closed'
                    elif second_part(proposition) in propositions_to_add:
                        if propositions_to_add[second_part(proposition)]:
                            return 'closed'
                    propositions_to_add[second_part(proposition)] = False

                    propositions_to_remove.append(proposition)
                
                elif main_con == '|=|' and not model.worlds[world]['propositions'][proposition]:
                    new_world_index = 1
                    while (world + '.' + str(new_world_index) in model.worlds[world]['access'] or
                           world + '.' + str(new_world_index) in worlds_to_add):
                        new_world_index += 1
                    
                    new_world_name = world + '.' + str(new_world_index)
                    worlds_to_add[new_world_name] = {'access' : [], 'variables' : {}, 'propositions' : {second_part(proposition) : False}}
                    model.add_access(world, new_world_name)

                    propositions_to_remove.append(proposition)
                
                elif main_con == '<>' and model.worlds[world]['propositions'][proposition]:
                    new_world_index = 1
                    while (world + '.' + str(new_world_index) in model.worlds[world]['access'] or
                           world + '.' + str(new_world_index) in worlds_to_add):
                        new_world_index += 1
                    
                    new_world_name = world + '.' + str(new_world_index)
                    worlds_to_add[new_world_name] = {'access' : [], 'variables' : {}, 'propositions' : {second_part(proposition) : True}}
                    model.add_access(world, new_world_name)

                    propositions_to_remove.append(proposition)
            
            for proposition in propositions_to_remove:
                model.worlds[world]['propositions'].pop(proposition)

            model.worlds[world]['propositions'].update(propositions_to_add)
        
        for world in worlds_to_add:
            model.add_world(world, worlds_to_add[world]['access'], worlds_to_add[world]['variables'], worlds_to_add[world]['propositions'])
    
    # check for pure variables in model's propositions
    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            if main_connective(proposition) == '':
                variable = strip_outer_parens(proposition)
                if variable not in model.worlds[world]['variables']:
                    model.worlds[world]['variables'][variable] = model.worlds[world]['propositions'][proposition]
                
                else:
                    if not model.worlds[world]['propositions'][proposition] == model.worlds[world]['variables'][variable]:
                        return 'closed'

    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            main_con = main_connective(proposition)

            # branching 'and'
            if main_con == '/\\' and model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = True
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = True
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
            
            # branching 'or'
            elif main_con == '\\/' and not model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = False
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = False
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
            
            # branching 'implies'
            elif main_con == '->' and not model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = True
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = False
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
    
    return 'open'

def test_initialize_tableau():
    proposition = 'p -> q'
    logic = 'KT'
    print(initialize_tableau(proposition, logic))

def test_reduce_propositions():
    model = Proof_Model()
    model.add_world('world 1', propositions={'<>p -> (q \\/ r)' : False})
    print(model)

    reduce_propositions(model, 'K')
    print(model)

def test_complete_tableau():
    examples = [
        'p \\/ ~p',
        '~(p /\\ ~p)',
        'p -> p',
        'p -> (p \\/ p)',
        'p -> (p /\\ p)',
        '(p /\\ q) -> p',
        '(p /\\ (p -> q)) -> q',
        'p -> (p \\/ q)',
        'p \\/ q -> q \\/ p',
        'p /\\ q -> q /\\ p',
        '(p -> q) -> ((p \\/ r) -> (q \\/ r))',
        'p -> q'

    logic = 'K'

    for proposition in examples:
        print('proposition : %s' % proposition)
        model = initialize_tableau(proposition, logic)
        result = complete_tableau(model, logic)
        print(result)

        if result == 'open':
            print('A problem occurred')

def main():
    logic = get_logic()
    proposition = get_proposition()

    model = initialize_tableau(proposition, logic)
    result = complete_tableau(model, logic)

    if result == 'closed':
        print('Proposition is a theorem of %s' % logic)
    elif result == 'open':
        print('Proposition is not a theorem of %s' % logic)
    else:
        print('Something went wrong when processing your proposition. My deepest apologies')

if __name__ == '__main__':
    test_complete_tableau()
