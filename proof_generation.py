from check_proposition import check_proposition
from parsing_functions import (
    normalize,
    first_part,
    second_part,
    main_connective,
    remove_outer_parens
)
from Proof_Model import Proof_Model
from copy import copy, deepcopy

def get_logic():
    print('Which axioms would you like your modal logic to satisfy?',
          'Choices are:', ' * T', ' * 4', ' * B', 'Enter selections separated by commas', sep='\n', end='\n')
    choices = input()

    logic = 'K'

    if 't' in choices.lower():
        logic += 'T'
    if 'B' in choices.lower():
        logic += 'B'
    if '4' in choices:
        logic += '4'
    
    return logic

def get_proposition():
    print('Enter the proposition you would like to check')

    proposition = normalize(input())

    return proposition

def initialize_tableau(proposition, logic='K'):
    proposition = normalize(proposition)
    model = Proof_Model({})
    model.add_world('1', propositions={proposition : False})
    if 'T' in logic:
        model.add_access('1', '1')
    
    return model

def is_reducible(model):
    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            main_con = main_connective(proposition)

            if main_con == '--':
                return True

            elif main_con == '/\\' and model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '\\/' and not model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '->' and not model.worlds[world]['propositions'][proposition]:
                return True

            elif main_con == '[]' and not model.worlds[world]['propositions'][proposition]:
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

                if main_con == '--':
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
                
                elif main_con == '[]' and not model.worlds[world]['propositions'][proposition]:
                    new_world_index = 1
                    while (world + '.' + str(new_world_index) in model.worlds[world]['access'] or
                           world + '.' + str(new_world_index) in worlds_to_add):
                        new_world_index += 1
                    
                    new_world_name = world + '.' + str(new_world_index)
                    worlds_to_add[new_world_name] = {'access' : [], 'variables' : {}, 'propositions' : {second_part(proposition) : False}}
                    if 'T' in logic:
                        worlds_to_add[new_world_name]['access'].append(new_world_name)
                    if 'B' in logic:
                        worlds_to_add[new_world_name]['access'].append(world)
                    model.add_access(world, new_world_name)

                    propositions_to_remove.append(proposition)
                
                elif main_con == '<>' and model.worlds[world]['propositions'][proposition]:
                    new_world_index = 1
                    while (world + '.' + str(new_world_index) in model.worlds[world]['access'] or
                           world + '.' + str(new_world_index) in worlds_to_add):
                        new_world_index += 1
                    
                    new_world_name = world + '.' + str(new_world_index)
                    worlds_to_add[new_world_name] = {'access' : [], 'variables' : {}, 'propositions' : {second_part(proposition) : True}}
                    if 'T' in logic:
                        worlds_to_add[new_world_name]['access'].append(new_world_name)
                    if 'B' in logic:
                        worlds_to_add[new_world_name]['access'].append(world)
                    model.add_access(world, new_world_name)

                    propositions_to_remove.append(proposition)
            
            for proposition in propositions_to_remove:
                model.worlds[world]['propositions'].pop(proposition)

            model.worlds[world]['propositions'].update(propositions_to_add)
        
        for world in worlds_to_add:
            model.add_world(world, worlds_to_add[world]['access'], worlds_to_add[world]['variables'], worlds_to_add[world]['propositions'])
        
        # changing things at new worlds that have been created based on True [] or False <>
        for world in model.worlds:
            for accessible_world in model.worlds[world]['access']:
                propositions_to_remove = []
                propositions_to_add = {}

                for proposition in model.worlds[world]['propositions']:
                    if (main_connective(proposition) == '[]' and model.worlds[world]['propositions'][proposition]):
                        part_2 = normalize(second_part(proposition))

                        if part_2 not in model.worlds[accessible_world]['propositions'] and part_2 not in propositions_to_add:
                            propositions_to_add[part_2] = True
                        elif part_2 in model.worlds[accessible_world]['propositions']:
                            if not model.worlds[accessible_world]['propositions'][part_2]:
                                return 'closed'
                        elif part_2 in propositions_to_add:
                            if not propositions_to_add[proposition]:
                                return 'closed'
                    
                    elif (main_connective(proposition) == '<>' and not model.worlds[world]['propositions'][proposition]):
                        part_2 = normalize(second_part(proposition))

                        if part_2 not in model.worlds[accessible_world]['propositions'] and part_2 not in propositions_to_add:
                            propositions_to_add[normalize(second_part(proposition))] = False
                        elif part_2 in model.worlds[accessible_world]['propositions']:
                            if model.worlds[accessible_world]['propositions'][part_2]:
                                return 'closed'
                        elif part_2 in propositions_to_add:
                            if propositions_to_add[part_2]:
                                return 'closed'
                
                for proposition in propositions_to_add:
                    if proposition in model.worlds[accessible_world]['propositions']:
                        if not model.worlds[accessible_world]['propositions'][proposition] == propositions_to_add[proposition]:
                            return 'closed'
                    model.worlds[accessible_world]['propositions'][proposition] = propositions_to_add[proposition]
                
                for proposition in propositions_to_remove:
                    model.worlds[world]['propositions'].pop(proposition)
        
        if len(model.worlds) > 128:
            print('MAXIMUM NUMBER OF WORLDS EXCEEDED (128)')
            return 'open'
    
    for world in model.worlds:
        for accessible_world in model.worlds[world]['access']:
            propositions_to_remove = []
            propositions_to_add = {}

            for proposition in model.worlds[world]['propositions']:
                if (main_connective(proposition) == '[]' and model.worlds[world]['propositions'][proposition]):
                    part_2 = normalize(second_part(proposition))

                    if part_2 not in model.worlds[accessible_world]['propositions'] and part_2 not in propositions_to_add:
                        propositions_to_add[part_2] = True
                    elif part_2 in model.worlds[accessible_world]['propositions']:
                        if not model.worlds[accessible_world]['propositions'][part_2]:
                            return 'closed'
                    elif part_2 in propositions_to_add:
                        if not propositions_to_add[proposition]:
                            return 'closed'
                
                elif (main_connective(proposition) == '<>' and not model.worlds[world]['propositions'][proposition]):
                    part_2 = normalize(second_part(proposition))

                    if part_2 not in model.worlds[accessible_world]['propositions'] and part_2 not in propositions_to_add:
                        propositions_to_add[normalize(second_part(proposition))] = False
                    elif part_2 in model.worlds[accessible_world]['propositions']:
                        if model.worlds[accessible_world]['propositions'][part_2]:
                            return 'closed'
                    elif part_2 in propositions_to_add:
                        if propositions_to_add[part_2]:
                            return 'closed'
            
            for proposition in propositions_to_add:
                if proposition in model.worlds[accessible_world]['propositions']:
                    if not model.worlds[accessible_world]['propositions'][proposition] == propositions_to_add[proposition]:
                        return 'closed'
                model.worlds[accessible_world]['propositions'][proposition] = propositions_to_add[proposition]
            
            for proposition in propositions_to_remove:
                model.worlds[world]['propositions'].pop(proposition)
    
    # check for pure variables in model's propositions
    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            if main_connective(proposition) == '':
                variable = remove_outer_parens(proposition)
                if variable not in model.worlds[world]['variables']:
                    model.worlds[world]['variables'][variable] = model.worlds[world]['propositions'][proposition]
                
                else:
                    if not model.worlds[world]['propositions'][proposition] == model.worlds[world]['variables'][variable]:
                        return 'closed'

    # handles branching cases
    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            main_con = main_connective(proposition)

            # branching 'and'
            if main_con == '/\\' and not model.worlds[world]['propositions'][proposition]:
                branch_1_model = deepcopy(model)
                branch_2_model = deepcopy(model)

                branch_1_model.worlds[world]['propositions'].pop(proposition)
                branch_1_model.worlds[world]['propositions'][first_part(proposition)] = False
                branch_1 = complete_tableau(branch_1_model, logic)

                branch_2_model.worlds[world]['propositions'].pop(proposition)
                branch_2_model.worlds[world]['propositions'][second_part(proposition)] = False
                branch_2 = complete_tableau(branch_2_model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
                else:
                    return 'open'
            
            # branching 'or'
            elif main_con == '\\/' and model.worlds[world]['propositions'][proposition]:
                branch_1_model = deepcopy(model)
                branch_2_model = deepcopy(model)

                branch_1_model.worlds[world]['propositions'].pop(proposition)
                branch_1_model.worlds[world]['propositions'][first_part(proposition)] = True
                branch_1 = complete_tableau(branch_1_model, logic)

                branch_2_model.worlds[world]['propositions'].pop(proposition)
                branch_2_model.worlds[world]['propositions'][second_part(proposition)] = True
                branch_2 = complete_tableau(branch_2_model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
                else:
                    return 'open'
            
            # branching 'implies'
            elif main_con == '->' and model.worlds[world]['propositions'][proposition]:
                branch_1_model = deepcopy(model)
                branch_2_model = deepcopy(model)

                branch_1_model.worlds[world]['propositions'].pop(proposition)
                branch_1_model.worlds[world]['propositions'][first_part(proposition)] = False
                branch_1 = complete_tableau(branch_1_model, logic)

                branch_2_model.worlds[world]['propositions'].pop(proposition)
                branch_2_model.worlds[world]['propositions'][second_part(proposition)] = True
                branch_2 = complete_tableau(branch_2_model, logic)

                if branch_1 == 'closed' and branch_2 == 'closed':
                    return 'closed'
                else:
                    return 'open'
    
    return 'open'

def evaluate_proposition(proposition, logic='K'):
    new_model = initialize_tableau(proposition, logic)
    result = complete_tableau(new_model, logic)
    if result == 'closed':
        return 'valid'
    elif result == 'open':
        return 'not valid'
    else:
        return 'problem occurred'

def test_initialize_tableau():
    proposition = 'p -> q'
    logic = 'KT'
    print(initialize_tableau(proposition, logic))

def test_complete_tableau():
    modal_examples = [
        '[](A \\/ B) -> ([]A \\/ []B)',
        '[](A -> B) -> ([]A -> []B)',
        '([]<>A /\\ [][]B) -> []<>(A /\\ B)'
    ]

    # modal_example_models = [initialize_tableau(prop) for prop in modal_examples]

    logic = 'K'

    # proposition = '[](A -> B) -> ([]A -> []B)'

    # model = initialize_tableau(proposition, logic)
    # print(complete_tableau(model, logic))
    # return

    for proposition in modal_examples:
        model = initialize_tableau(proposition, logic)
        print(model)
        print(complete_tableau(model, logic))
    
    return
    
    examples = [
        'p \\/ --p',
        '--(p /\\ --p)',
        'p -> p',
        'p -> (p \\/ p)',
        'p -> (p /\\ p)',
        '(p /\\ q) -> p',
        '(p /\\ (p -> q)) -> q',
        'p -> (p \\/ q)',
        'p \\/ q -> q \\/ p',
        'p /\\ q -> q /\\ p',
        '(p -> q) -> ((p \\/ r) -> (q \\/ r))',
        'p -> q']

    logic = 'K'

    for proposition in examples:
        print('proposition : %s' % proposition)
        model = initialize_tableau(proposition, logic)
        print(model)
        result = complete_tableau(model, logic)
        print(result)

        if result == 'open':
            print('A problem occurred')

def main():
    logic = get_logic()
    proposition = get_proposition()

    result = evaluate_proposition(proposition, logic)

    if result == 'valid':
        print('Proposition is a theorem of %s' % logic)
    elif result == 'not valid':
        print('Proposition is not a theorem of %s' % logic)
    else:
        print('Something went wrong when processing your proposition. My deepest apologies')

if __name__ == '__main__':
    main()
