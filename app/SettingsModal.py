import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
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

        self.container = tk.Frame(self)
        self.notebook = ttk.Notebook(self.container, width = 390, height = 246)

        self.tab_preferences = tk.Frame(self.notebook)

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

        #self.notebook.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.notebook.grid(row = 0, column = 0, padx = 5, sticky = tk.W + tk.E + tk.N + tk.S)
        self.notebook.add(self.tab_preferences, text = 'Preferences')

        # Apply button
        self.cancel_apply_group = tk.Frame(self.container, height = 20, width = 390)
        #self.cancel_apply_group.grid_propagate(0)
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
        self.geometry(f'400x300+{self.master.master.winfo_x() + self.master.master.winfo_width() // 2 - 200}+{self.master.master.winfo_y() + self.master.master.winfo_height() // 2 - 150}')
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

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'w', encoding = 'UTF-8') as settings:
            settings.write(json.dumps(self.settings, indent = 4))
            settings.close()
        
        if close: self.close()
    
    def cancel(self):
        self.close()