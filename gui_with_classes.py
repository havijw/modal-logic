from tkinter import *
from parsing_functions import *
from proposition_checker import check_proposition
from Model import Model
from math import sin, cos

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
        self.variables_entry.bind('<Key>', self.update_variables)

        self.name_entry = Entry(master)
        self.name_entry.place(x=x - 35, width=70, y=y + 10, height=20)
        self.name_entry.insert(0, 'Name')
        self.name_entry.bind('<Button 1>', self.clear_name_entry)

        self.name = self.name_entry.get() + str(len(worlds))
        model.add_world(self.name)
        update_world_selection()
        self.name_entry.bind('<Key>', self.update_name)

        self.delete_button = Button(master, text='x', command=self.delete)
        self.delete_button.place(x=x - 5, y=y - RADIUS - 5, width=10, height=10)

        self.master.tag_bind(self.outline_tag, '<Enter>', self.bind_B1_Motion_to_start_draw_arrow)
        self.master.tag_bind(self.outline_tag, '<Leave>', self.unbind_B1_Motion)
    
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
        model.remove_world(self.name)
        update_world_selection()
    
    def update_name(self, event):
        old_name = self.name
        self.name = self.name_entry.get() + event.char
        if event.keysym == "BackSpace":
            self.name = self.name[:-2]
        i = 0
        while self.name in model.worlds:
            i += 1
            if i == 1:
                self.name += '_' + str(i) + '_'
            else:
                self.name = self.name[:-2] + str(i) + '_'
        
        model.add_world(self.name, model.worlds[old_name]['access'], model.worlds[old_name]['variables'])
        model.remove_world(old_name)
        update_world_selection()
    
    def update_variables(self, event):
        raw_string = self.variables_entry.get() + event.char
        if event.keysym == "BackSpace":
            raw_string = raw_string[:-2]
        
        variables = raw_string.split(',')
        variables = [v.replace(' ', '') for v in variables]
        variables = [v for v in variables if not v == '']

        model.worlds[self.name]['variables'] = variables
    
    def bind_B1_Motion_to_start_draw_arrow(self, event):
        self.master.bind('<B1-Motion>', self.start_arrow_to)
    
    def unbind_B1_Motion(self, event):
        self.master.unbind('<B1-Motion>')
    
    def start_arrow_to(self, event):
        x = event.x
        y = event.y

        def draw_arrow(event):
            for world in worlds:
                if distance(event.x, event.y, world.x, world.y) <= RADIUS * 2:
                    self.master.create_line(x, y, event.x, event.y, arrow=LAST)
                    if world.name not in model.worlds[self.name]['access']:
                        model.add_access(self.name, world.name)
            
            self.master.unbind('<ButtonRelease-1>')
        
        canvas.bind('<ButtonRelease-1>', draw_arrow)

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def create_world(event):
    for world in worlds:
        if (distance(event.x, event.y, world.x, world.y) <= RADIUS * 2 or
            event.y >= canvas.winfo_height() - world_selection.winfo_height() - RADIUS):
            return
    world = World(canvas, event.x, event.y)
    worlds.append(world)

def start_draw_arrow(event):
    x = event.x
    y = event.y

    def draw_arrow(event):
        for world in worlds:
            if distance(event.x, event.y, world.x, world.y) <= RADIUS * 2:
                canvas.create_line(x, y, event.x, event.y, arrow=LAST)
        canvas.unbind('<ButtonRelease-1>')
    
    canvas.bind('<ButtonRelease-1>', draw_arrow)

def update_world_selection():
    world_options = list(model.worlds.keys())
    world_options.sort()
    world_selection = OptionMenu(canvas, menu_message, *world_options)
    world_selection.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

def check_current_proposition():
    print(model)
    proposition = proposition_entry.get()
    world = menu_message.get()
    value = check_proposition(proposition, world, model)

    if value:
        canvas.configure(bg='#7aff81')
    else:
        canvas.configure(bg='#ff4d4d')

if __name__ == '__main__':
    root = Tk()
    root.configure(width=600, height=800)
    canvas = Canvas(root, bg=BACKGROUND)
    canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    worlds = []
    model = Model()
    canvas.bind('<Button 1>', create_world)

    menu_message = StringVar(root)
    menu_message.set('select world')
    world_selection = OptionMenu(canvas, menu_message, list(model.worlds.keys()))
    world_selection.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    proposition_entry = Entry(canvas)
    proposition_entry.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.05)

    check_proposition_button = Button(canvas, text='Check', command=check_current_proposition)
    check_proposition_button.place(relx=0.9, rely=0.95, relwidth=0.1, relheight=0.05)

    root.mainloop()
