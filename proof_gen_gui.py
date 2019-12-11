from proof_generation import initialize_tableau, complete_tableau
from parsing_functions import normalize
from Proof_Model import Proof_Model

import tkinter as tk

BACKGROUND= '#d6d6d6'

INSTRUCTIONS = '''Choose properties of a modal logic, then enter a proposition to check.
Connectives to use
------------------
 * negation: --
 * box:      []
 * diamond:  <>
 * and:      /\\
 * or:       \\/
 * implies:  ->
 Please note that for some reason, the checking only works the first time, so
 you should exit and restart the program after checking the first time.
 (I am working on this and hopefully will be able to fix it).'''

def delete_initial_text(event):
    proposition_entry.delete(0, 'end')
    proposition_entry.unbind('<Button 1>')


def check_current_proposition(event):
    logic = ''
    if reflexive_true:
        logic += 'T'
    if transitive_true:
        logic += '4'
    if symmetric_true:
        logic += 'B'
    
    model = initialize_tableau(proposition_entry.get())
    print(model)
    result = complete_tableau(model)
    if result == 'open':
        root.configure(bg='#ff4d4d')
        reflexive_checkbox.configure(bg='#ff4d4d')
        transitive_checkbox.configure(bg='#ff4d4d')
        symmetric_checkbox.configure(bg='#ff4d4d')
        instructions.configure(bg='#ff4d4d')

    elif result == 'closed':
        root.configure(bg='#7aff81')
        reflexive_checkbox.configure(bg='#7aff81')
        transitive_checkbox.configure(bg='#7aff81')
        symmetric_checkbox.configure(bg='#7aff81')
        instructions.configure(bg='#7aff81')
    
    model = Proof_Model()
    print(model)


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(width=500, height=800, bg=BACKGROUND)

    # instructions
    instructions = tk.Label(root)
    instructions.configure(text=INSTRUCTIONS, anchor='w', justify='left')
    instructions.grid(sticky='w')

    # logic check boxes for properties
    reflexive_true  = tk.IntVar()
    transitive_true = tk.IntVar()
    symmetric_true  = tk.IntVar()

    reflexive_checkbox  = tk.Checkbutton(root, text='T (Reflexive)',  variable=reflexive_true , bg=BACKGROUND)
    transitive_checkbox = tk.Checkbutton(root, text='4 (Transitive)', variable=transitive_true, bg=BACKGROUND)
    symmetric_checkbox  = tk.Checkbutton(root, text='B (Symmetric)',  variable=symmetric_true , bg=BACKGROUND)

    reflexive_checkbox.grid(sticky='w')
    transitive_checkbox.grid(sticky='w')
    symmetric_checkbox.grid(sticky='w')

    # proposition entry box
    proposition_entry = tk.Entry(root)#, font=('Courier', 14))
    proposition_entry.grid(sticky='w')

    proposition_entry.insert(0, 'Enter a proposition')
    proposition_entry.bind('<Button 1>', delete_initial_text)

    proposition_entry.bind('<Return>', check_current_proposition)

    root.mainloop()
