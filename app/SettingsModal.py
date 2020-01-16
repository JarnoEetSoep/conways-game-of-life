import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageTk
import json
import os

class SettingsModal(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'r', encoding = 'UTF-8') as settings:
            self.settings = json.loads(settings.read())
            settings.close()

        self.alive_color = tk.StringVar(value = self.settings['alive-color'])
        self.dead_color = tk.StringVar(value = self.settings['dead-color'])
        self.rules = tk.StringVar(value = ';'.join(self.settings['rules']))

        self.container = tk.Frame(self)
        self.notebook = ttk.Notebook(self.container, width = 540, height = 246)

        self.tab_preferences = tk.Frame(self.notebook)
        self.tab_rules = tk.Frame(self.notebook)

        # Preferences tab
        self.alive_color_label = tk.Label(self.tab_preferences, text = 'Color for alive cells: ', font = ('Verdana', 12))
        self.alive_color_input = tk.Frame(self.tab_preferences, bg = self.alive_color.get(), relief = tk.RIDGE, bd = 1, width = 20, height = 20)
        self.alive_color_input.bind('<Button-1>', lambda e: self.chooseColor(self.alive_color, self.alive_color_input))

        self.dead_color_label = tk.Label(self.tab_preferences, text = 'Color for dead cells: ', font = ('Verdana', 12))
        self.dead_color_input = tk.Frame(self.tab_preferences, bg = self.dead_color.get(), relief = tk.RIDGE, bd = 1, width = 20, height = 20)
        self.dead_color_input.bind('<Button-1>', lambda e: self.chooseColor(self.dead_color, self.dead_color_input))

        self.alive_color_label.grid(row = 0, column = 0)
        self.alive_color_input.grid(row = 0, column = 1)
        self.dead_color_label.grid(row = 1, column = 0)
        self.dead_color_input.grid(row = 1, column = 1)

        # Rules tab
        self.tab_rules.grid_rowconfigure(1, weight = 1)

        self.rules_frame = ttk.Frame(self.tab_rules)
        self.rules_frames = []

        for i, rule in enumerate(self.rules.get().split(';')):
            r = Rule(self.rules_frame, rule)
            r.grid(row = i, column = 0, sticky = tk.W + tk.E)
            self.rules_frames.append({
                'id': id(r),
                'rule': r
            })
        
        self.rules_frame.grid(row = 0, column = 0)

        self.controls = tk.Frame(self.tab_rules)
        self.controls.grid_columnconfigure(1, weight = 1)

        self.reset_button = tk.Button(self.controls, text = 'Reset', width = 10, command = self.resetRules, relief = tk.RAISED, cursor = 'hand2')
        self.reset_button.grid(row = 0, column = 0, sticky = tk.W + tk.S)

        self.add_rule_image = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/add.png')).resize((30, 30), Image.ANTIALIAS))
        self.add_rule = tk.Button(self.controls, width = 30, image = self.add_rule_image, command = self.addRule, relief = tk.RAISED, cursor = 'hand2')
        self.add_rule.grid(row = 0, column = 1, sticky = tk.E + tk.S)

        self.controls.grid(row = 1, column = 0, sticky = tk.S + tk.E + tk.W)

        self.notebook.grid(row = 0, column = 0, padx = 5, sticky = tk.W + tk.E + tk.N + tk.S)
        self.notebook.add(self.tab_preferences, text = 'Preferences')
        self.notebook.add(self.tab_rules, text = 'Rules')

        # Apply button
        self.cancel_apply_group = tk.Frame(self.container, width = 540, height = 20)
        self.cancel_button = tk.Button(self.cancel_apply_group, text = 'Cancel', command = self.cancel)
        self.apply_button = tk.Button(self.cancel_apply_group, text = 'Apply', command = self.apply)
        self.apply_and_close_button  = tk.Button(self.cancel_apply_group, text = 'Apply and Close', command = lambda: self.apply(close = True))

        self.cancel_apply_group.grid(row = 1, column = 0, ipadx = 3, sticky = tk.E)
        self.cancel_button.grid(row = 0, column = 0)
        self.apply_button.grid(row = 0, column = 1)
        self.apply_and_close_button.grid(row = 0, column = 2)

        self.container.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    
    def close(self, e = None):
        self.grab_release()
        self.destroy()
        self.master.master.wm_deiconify()
    
    def show(self):
        self.wait_visibility()
        self.grab_set()
        self.transient(self.master)
        self.title('Settings')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.wm_deiconify()
        self.geometry(f'550x300+{self.master.master.winfo_x() + self.master.master.winfo_width() // 2 - 275}+{self.master.master.winfo_y() + self.master.master.winfo_height() // 2 - 150}')
        self.resizable(0, 0)
        self.wait_window()

        return self.settings
    
    def chooseColor(self, var, widget):
        color = colorchooser.askcolor()[1]
        var.set(color)
        widget.config(bg = color)
    
    def apply(self, close = False):
        self.settings['alive-color'] = self.alive_color.get()
        self.settings['dead-color'] = self.dead_color.get()

        rules = ''
        for r in self.rules_frames:
            rules += r['rule'].export() + ';'
        
        self.settings['rules'] = rules[:-1].split(';')
        self.rules.set(rules)

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'w', encoding = 'UTF-8') as settings:
            settings.write(json.dumps(self.settings, indent = 4))
            settings.close()
        
        if close: self.close()
    
    def cancel(self):
        self.close()

    def addRule(self):
        i = len(self.rules_frames)
        rule = Rule(self.rules_frame, 'cell lives if cell is alive and neighborsalive is 0')
        self.rules_frames.append({
            'id': id(rule),
            'rule': rule
        })
        rule.grid(row = i, column = 0, sticky = tk.W + tk.E)
        self.update()
    
    def resetRules(self):
        rules = [
            'cell dies if cell is alive and neighborsalive < 2',
            'cell dies if cell is alive and neighborsalive > 2',
            'cell lives if cell is alive and neighborsalive between 2 and 3',
            'cell lives if cell is dead and neighborsalive = 3'
        ]

        for r in self.rules_frames:
            r['rule'].removeRule()

        self.rules_frames = []        
        self.rules.set(';'.join(rules))
        
        for i, rule in enumerate(self.rules.get().split(';')):
            r = Rule(self.rules_frame, rule)
            r.grid(row = i, column = 0, sticky = tk.W + tk.E)
            self.rules_frames.append({
                'id': id(r),
                'rule': r
            })
        

class Rule(tk.Frame):
    def __init__(self, master, string):
        super().__init__(master)
        self.help_bar_h = tk.Frame(self, width = 540, height = 0)
        self.help_bar_h.grid(row = 0, column = 0, sticky = tk.N + tk.W, columnspan = 2)

        self.frame = tk.Frame(self)
                
        self.lives_or_dies = tk.StringVar(value = string.split(' ')[1])
        self.alive_or_dead = tk.StringVar(value = string.split(' ')[5])
        self.operator = tk.StringVar()
        self.condition_number = tk.StringVar(value = string.split(' ')[9])
        self.condition_number2 = tk.StringVar(value = 0)
        if len(string.split(' ')) > 11:
            self.condition_number2.set(string.split(' ')[11])
        
        self.cell_label = tk.Label(self.frame, text = 'Cell', font = ('Verdana', 10))
        self.lives_or_dies_combobox = ttk.Combobox(self.frame, values = ('lives', 'dies'), textvariable = self.lives_or_dies, state = 'readonly', width = 5)
        self.if_label = tk.Label(self.frame, text = 'if cell is', font = ('Verdana', 10))
        self.alive_or_dead_combobox = ttk.Combobox(self.frame, values = ('alive', 'dead'), textvariable = self.alive_or_dead, state = 'readonly', width = 5)
        self.condition_label = tk.Label(self.frame, text = 'and neighbors alive', font = ('Verdana', 10))
        self.operator_combobox = ttk.Combobox(self.frame, values = ('=', '>', '<', 'between'), textvariable = self.operator, state = 'readonly', width = 8)
        self.condition_number_spinbox = ttk.Spinbox(self.frame, from_ = 0, to = 8, textvariable = self.condition_number, state = 'readonly', width = 4)
        self.and_label = tk.Label(self.frame, text = 'and', font = ('Verdana', 10))
        self.condition_number2_spinbox = ttk.Spinbox(self.frame, from_ = 0, to = 8, textvariable = self.condition_number2, state = 'readonly', width = 4)

        self.operator.trace_add('write', self.checkOperator)
        self.operator.set(string.split(' ')[8])

        self.frame.grid(row = 0, column = 0, sticky = tk.W)

        self.cell_label.grid(row = 0, column = 0)
        self.lives_or_dies_combobox.grid(row = 0, column = 1)
        self.if_label.grid(row = 0, column = 2)
        self.alive_or_dead_combobox.grid(row = 0, column = 3)
        self.condition_label.grid(row = 0, column = 4)
        self.operator_combobox.grid(row = 0, column = 5)
        self.condition_number_spinbox.grid(row = 0, column = 6)

        # Remove button
        self.remove_frame = tk.Frame(self, height = 20)
        self.remove_frame.grid(row = 0, column = 1, sticky = tk.E)

        self.remove_rule_image = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/remove.png')).resize((20, 20), Image.ANTIALIAS))
        self.remove_rule = tk.Button(self.remove_frame, width = 20, image = self.remove_rule_image, command = self.removeRule, relief = tk.RAISED, cursor = 'hand2')
        self.remove_rule.grid(row = 0, column = 0, sticky = tk.E)
    
    def checkOperator(self, *args):
        if self.operator.get() == 'between':
            self.and_label.grid(row = 0, column = 7)
            self.condition_number2_spinbox.grid(row = 0, column = 8)
        else:
            self.and_label.grid_remove()
            self.condition_number2_spinbox.grid_remove()
        
    def removeRule(self):
        for i, v in enumerate(self.master.master.master.master.master.rules_frames):
            if v['id'] == id(self):
                del self.master.master.master.master.master.rules_frames[i]

        self.destroy()
    
    def export(self):
        out = f'cell {self.lives_or_dies.get()} if cell is {self.alive_or_dead.get()} and neighborsalive {self.operator.get()} {self.condition_number.get()}'
        if self.operator.get() == 'between': out += f' and {self.condition_number2.get()}'
        
        return out

if __name__ == "__main__":
    Tk = tk.Tk()
    frm = tk.Frame(Tk)
    x = SettingsModal(frm).show()