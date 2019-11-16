import tkinter as tk
from proposition_checker import check_proposition
from parsing_functions import *
from Model import Model

RADIUS = 50

def draw_node(event):
    background.create_oval(
                           event.x - RADIUS,
                           event.y - RADIUS,
                           event.x + RADIUS,
                           event.y + RADIUS)
    
    name_entry = tk.Entry(root)
    name_entry.place(x=event.x - 20, width=40, y=event.y + 10, height=20)
    name_entry.insert(0, 'Name')

    world_name_entries.append(name_entry)
    
    def delete_name_entry_text(event):
        name_entry.delete(0, 'end')
        name_entry.unbind('<Button 1>')

    name_entry.bind('<Button 1>', delete_name_entry_text)

def draw_arrow(event):
    x, y = background.old_coords
    background.create_line(x, y, event.x, event.y, arrow=tk.LAST)

def draw_arrow_on_click(event):
    background.old_coords = event.x, event.y
    background.bind('<Button 1>', draw_arrow_then_rebind)

def draw_arrow_then_rebind(event):
    draw_arrow(event)
    background.bind('<Button 1>', draw_arrow_on_click)

def delete_prop_entry_text(event):
    prop_entry.delete(0, 'end')
    prop_entry.unbind('<Button 1>')

root = tk.Tk()

canvas = tk.Canvas(root, width=750, height=1000)
canvas.pack()

background = tk.Canvas(bg='#363636')
background.place(relx=0, rely=0, relwidth=1, relheight=0.95)

worlds = ['']
default_world = tk.StringVar(root)
default_world.set(worlds[0])
world_entry = tk.OptionMenu(root, default_world, *worlds)
world_entry.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

def update_worlds_choices(event):
    worlds = []
    for entry_box in world_name_entries:
        worlds.append(entry_box.get())
    
    world_entry = tk.OptionMenu(root, default_world, *worlds)
    world_entry.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)
    world_entry.bind('<Button 1>', update_worlds_choices)

world_entry.bind('<Button 1>', update_worlds_choices)


prop_entry = tk.Entry(root)
prop_entry.place(relx=0.1, rely=0.95, relwidth=0.9, relheight=0.05)
prop_entry.insert(0, 'enter proposition to check')
prop_entry.bind('<Button 1>', delete_prop_entry_text)

# background.create_line(100, 100, 300, 100, fill='blue', width=2)
# background.create_line(300, 100, 200, 300, fill='blue', width=2)
# background.create_line(200, 300, 100, 100, fill='blue', width=2, arrow=tk.LAST)

world_name_entries = []
background.bind("<Button 1>", draw_node)
# background.old_coords = None
# background.bind("<Motion>", draw_arrow)

root.mainloop()
