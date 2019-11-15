from parsing_functions import *
from Model import Model

def check_proposition(proposition, world, model):
    if proposition == '':
        return True
    
    proposition = normalize(proposition)

    main_con = main_connective(proposition)

    part_1 = first_part(proposition)
    part_2 = second_part(proposition)

    # for modal-free connectives, we can reduce to simpler cases
    if main_con == '~':
        return not check_proposition(part_2, world, model)
    elif main_con == '/\\':
        return check_proposition(part_1, world, model) and check_proposition(part_2, world, model)
    elif main_con == '\\/':
        return check_proposition(part_1, world, model) or  check_proposition(part_2, world, model)
    elif main_con == '->':
        return (not check_proposition(part_1, world, model)) or (check_proposition(part_2, world, model))
    
    # logic for diamond
    elif main_con == '<>':
        for accessible_world in model.worlds['access']:
            if check_proposition(part_2, accessible_world, model):
                return True
        
        return False
    
    # logic for box
    elif main_con == '|=|':
        for accessible_world in model.worlds['access']:
            if not check_proposition(part_2, accessible_world, model):
                return False
        
        return True
    
    # logic for single variables
    elif main_con == '':
        if proposition in model.worlds['variables']:
            return True
        return False

