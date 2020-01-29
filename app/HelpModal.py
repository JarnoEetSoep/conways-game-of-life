import tkinter as tk
import os

from BetterScrollbar import BetterScrollbar

class HelpModal(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.container = tk.Frame(self)

        self.bind_all('<Configure>', self.resize)

        self.scrollbar = tk.Scrollbar(self.container)
        self.scrollbar.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH)

        self.manual = tk.Text(self.container, font = ('Verdana', 10), wrap = tk.WORD, yscrollcommand = self.scrollbar.set)

        self.scrollbar.config(command = self.manual.yview)

        # Manual
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'manual.txt'), 'r', encoding = 'UTF-8') as manual:
            self.manual.insert(tk.END, manual.read())
            manual.close()

        self.manual.config(state = tk.DISABLED)

        self.container.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER, relwidth = 1, relheight = 1)
        self.manual.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
    
    def close(self, e = None):
        self.destroy()
        self.master.master.focus_force()
    
    def show(self):
        self.title('Manual')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.wm_deiconify()
        self.geometry(f'400x600+{self.master.master.winfo_x() + self.master.master.winfo_width() // 2 - 200}+{self.master.master.winfo_y() + self.master.master.winfo_height() // 2 - 300}')
        self.focus_force()
    
    def resize(self, e):
        pass