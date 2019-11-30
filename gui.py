import tkinter as tk
from tkinter import font
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

        self.variables_entry = tk.Entry(master)
        self.variables_entry.place(x=x - 35, width=70, y=y - 20, height=20)
        self.variables_entry.insert(0, 'True Vars')
        self.variables_entry.bind('<Button 1>', self.clear_variables_entry)
        self.variables_entry.bind('<Key>', self.update_variables)

        self.name_entry = tk.Entry(master)
        self.name_entry.place(x=x - 35, width=70, y=y + 10, height=20)
        self.name_entry.insert(0, 'Name')
        self.name_entry.bind('<Button 1>', self.clear_name_entry)

        self.name = self.name_entry.get() + str(len(worlds))
        model.add_world(self.name)
        update_world_selection()
        self.name_entry.bind('<Key>', self.update_name)

        self.delete_button = tk.Button(master, text='x', command=self.delete)
        self.delete_button['font'] = delete_button_font
        self.delete_button.place(x=x - 12, y=y - RADIUS - 4, width=24, height=20)

        self.arrows = {}
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
        for arrow in self.arrows:
            self.master.delete(arrow)
        
        for world in worlds:
            to_delete = []
            for arrow in world.arrows:
                if world.arrows[arrow][0] == self.x and world.arrows[arrow][1] == self.y:
                    self.master.delete(arrow)
                    to_delete.append(arrow)
            world.arrows = {key:world.arrows[key] for key in world.arrows if key not in to_delete}
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
        for world in model.worlds:
            if old_name in model.worlds[world]['access']:
                model.add_access(world, self.name)
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
                if distance(event.x, event.y, world.x, world.y) <= RADIUS and world.name not in model.worlds[self.name]['access']:
                    if distance(x, y, world.x, world.y) <= RADIUS:
                        arc_to_self = self.master.create_arc(
                            world.x - 40,
                            world.y,
                            world.x + 40,
                            world.y - 100,
                            start=340, extent=220, style='arc', width=3
                        )
                        arrow_tip = self.master.create_line(
                            world.x - 35,
                            world.y - 29,
                            world.x - 34,
                            world.y - 27,
                            arrow=tk.LAST, width=3
                        )
                        self.arrows[arc_to_self] = (-1, -1)
                        self.arrows[arrow_tip]   = (-1, -1)
                        self.master.tag_bind(arc_to_self, '<Button 1>', lambda event, name = arc_to_self: self.delete_arrow(name))
                        self.master.tag_bind(arc_to_self, '<Button 1>', lambda event, name = arrow_tip:   self.delete_arrow(name))
                        self.master.tag_bind(arrow_tip,   '<Button 1>', lambda event, name = arc_to_self: self.delete_arrow(name))
                        self.master.tag_bind(arrow_tip,   '<Button 1>', lambda event, name = arrow_tip:   self.delete_arrow(name))
                    else:
                        new_arrow = self.master.create_line(x, y, event.x, event.y, arrow=tk.LAST, width=3)
                        self.arrows[new_arrow] = (world.x, world.y)
                        self.master.tag_bind(new_arrow, '<Button 1>', lambda event, name = new_arrow: self.delete_arrow(name))
                    
                    model.add_access(self.name, world.name)
            
            self.master.unbind('<ButtonRelease-1>')
        
        canvas.bind('<ButtonRelease-1>', draw_arrow)
    
    def delete_arrow(self, arrow):
        self.master.delete(arrow)
        for world in worlds:
            if world.x == self.arrows[arrow][0] and world.y == self.arrows[arrow][1]:
                model.remove_access(self.name, world.name)

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def toggle_world_addition():
    global can_add_worlds
    if can_add_worlds:
        can_add_worlds = False
        canvas.unbind('<Button 1>')
        world_add_button.configure(text='Enable world adding')
    else:
        can_add_worlds = True
        canvas.bind('<Button 1>', create_world)
        world_add_button.configure(text='Disable world adding')

def create_world(event):
    for world in worlds:
        if (distance(event.x, event.y, world.x, world.y) <= RADIUS * 2 or
            event.y >= canvas.winfo_height() - world_selection.winfo_height() - RADIUS):
            return
    world = World(canvas, event.x, event.y)
    worlds.append(world)

def update_world_selection():
    world_options = list(model.worlds.keys())
    world_options.sort()
    if world_options == []:
        world_options = ['']
    world_selection = tk.OptionMenu(canvas, menu_message, *world_options)
    world_selection.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

def check_current_proposition():
    proposition = proposition_entry.get()
    world = menu_message.get()
    value = check_proposition(proposition, world, model)

    if value:
        canvas.configure(bg='#7aff81')
    else:
        canvas.configure(bg='#ff4d4d')

def check_current_proposition_event(event):
    proposition = proposition_entry.get()
    world = menu_message.get()
    value = check_proposition(proposition, world, model)

    if value:
        canvas.configure(bg='#7aff81')
    else:
        canvas.configure(bg='#ff4d4d')

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(width=1200, height=800)
    delete_button_font = tk.font.Font(family='Helvetica', size=10, weight='normal')
    canvas = tk.Canvas(root, bg=BACKGROUND, bd=0)
    canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    can_add_worlds = True
    world_add_button = tk.Button(canvas, text='Disable World Adding', command=toggle_world_addition, borderwidth=0)
    world_add_button.place(x=0, y=0, height=20, width=250)

    worlds = []
    model = Model()
    canvas.bind('<Button 1>', create_world)

    menu_message = tk.StringVar(root)
    menu_message.set('select world')
    world_selection = tk.OptionMenu(canvas, menu_message, list(model.worlds.keys()))
    world_selection.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    proposition_entry = tk.Entry(canvas)
    proposition_entry.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.05)
    proposition_entry.bind('<Return>', check_current_proposition_event)

    check_proposition_button = tk.Button(canvas, text='Check', command=check_current_proposition)
    check_proposition_button.place(relx=0.9, rely=0.95, relwidth=0.1, relheight=0.05)

    root.mainloop()
