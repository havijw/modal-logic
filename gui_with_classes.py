from tkinter import *
from parsing_functions import *
from proposition_checker import check_proposition
from Model import Model

RADIUS = 50
BACKGROUND = '#363636'

class World:
    def __init__(self, master, x, y):
        self.x = x
        self.y = y

        self.outline_tag = str(self.x) + ',' + str(self.y) + '-outline'

        self.master = master
        self.outline = master.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill='#399ced', tag=self.outline_tag)

        self.variables_entry = Entry(master)
        self.variables_entry.place(x=x - 35, width=70, y=y - 20, height=20)
        self.variables_entry.insert(0, 'True Vars')
        self.variables_entry.bind('<Button 1>', self.clear_variables_entry)

        self.name_entry = Entry(master)
        self.name_entry.place(x=x - 35, width=70, y=y + 10, height=20)
        self.name_entry.insert(0, 'Name')
        self.name_entry.bind('<Button 1>', self.clear_name_entry)

        self.name = self.name_entry.get()
        self.name_entry.bind('<Key>', self.update_name)

        self.delete_button = Button(master, text='x', command=self.delete)
        self.delete_button.place(x=x - 5, y=y - RADIUS - 5, width=10, height=10)

        self.master.tag_bind(self.outline_tag, '<Enter>', self.bind_B1_motion_to_arrow)
        self.master.tag_bind(self.outline_tag, '<Button 1>', do_nothing)
    
    def clear_variables_entry(self, event):
        self.variables_entry.delete(0, 'end')
        self.variables_entry.unbind('<Button 1>')
    
    def clear_name_entry(self, event):
        self.name_entry.delete(0, 'end')
        self.name_entry.unbind('<Button 1>')
    
    def delete(self):
        self.master.delete(self.outline)
        self.name_entry.destroy()
        self.variables_entry.destroy()
        self.delete_button.destroy()
        worlds.remove(self)
    
    def update_name(self, event):
        self.name = self.name_entry.get()
        print(self.name)
    
    def bind_B1_motion_to_arrow(self, event):
        self.master.bind('<B1-Motion>', draw_arrow)

def create_world(event):
    world = World(canvas, event.x, event.y)
    worlds.append(world)

def draw_arrow(event):
    print('draw arrow')

def do_nothing(event):
    print('I dont want to do anything')

root = Tk()
canvas = Canvas(root, width=750, height=1000, bg=BACKGROUND)
canvas.pack()

worlds = []
world_names = []
canvas.bind('<Button 1>', create_world)

root.mainloop()
