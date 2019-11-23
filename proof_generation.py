from proposition_checker import check_proposition
from parsing_functions import normalize, first_part, second_part, main_connective
from Proof_Model import Proof_Model

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

def complete_tableau(model, logic='K'):
    # model.reduce_all_propositions()

    for world in model.worlds:
        for proposition in model.worlds[world]['propositions']:
            main_con = main_connective(proposition)
            if main_con == '/\\' and model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = True
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = True
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'open' or branch_2 == 'open':
                    return 'open'
            
            elif main_con == '\\/' and not model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = False
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = False
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'open' or branch_2 == 'open':
                    return 'open'
            
            elif main_con == '->' and not model.worlds[world]['propositions'][proposition]:
                model.worlds[world]['propositions'].pop(proposition)

                model.worlds[world]['propositions'][first_part(proposition)] = True
                branch_1 = complete_tableau(model, logic)

                model.worlds[world]['propositions'].pop(first_part(proposition))

                model.worlds[world]['propositions'][second_part(proposition)] = False
                branch_2 = complete_tableau(model, logic)

                if branch_1 == 'open' or branch_2 == 'open':
                    return 'open'

def test_initialize_tableau():
    proposition = 'p -> q'
    logic = 'KT'
    print(initialize_tableau(proposition, logic))

def test_complete_tableau():
    proposition = 'p \\/ q'
    logic = 'K'

    model = initialize_tableau(proposition, logic)

    evaluation = complete_tableau(model, logic)

    print(evaluation)

if __name__ == '__main__':
    test_complete_tableau()
