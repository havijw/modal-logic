from proposition_checker.py import check_proposition

def get_logic():
    print('Which modal logic would you like to work in?',
          '(1) K',
          '(2) KT',
          '(3) S4',
          '(4) S5', sep='\n', end='\n')
    
    choice = input()
    while ('1' not in choice and
           '2' not in choice and
           '3' not in choice and
           '4' not in choice):
        print('Sorry, %s is not a logic I know\nWhich modal logic would you like to work in?' % choice)
        choice = input()
    
    if '1' in choice:
        return 'K'
    elif '2' in choice:
        return 'KT'
    elif '3' in choice:
        return 'S4'
    elif '4' in choice:
        return 'S5'

if __name__ == '__main__':
    logic = get_logic()
    print("Thanks for choosing %s. Unfortunately, I don't know how to do anything yet." % logic)
