import tkinter as tk

class DelayModal(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.output = tk.StringVar()

        self.container = tk.Frame(self)
        self.delay_label = tk.Label(self.container, text = 'Delay:', font = ('Verdana', 20))
        self.delay_entry = tk.Entry(self.container, validate = 'key', validatecommand = self.master.only_digits, font = ('Verdana', 20), width = 5, textvariable = self.output)
        self.delay_ms_label = tk.Label(self.container, text = 'ms', font = ('Verdana', 20))

        self.container.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
        self.delay_label.grid(row = 0, column = 0, sticky = tk.W)
        self.delay_entry.grid(row = 1, column = 0)
        self.delay_ms_label.grid(row = 1, column = 1)

        self.delay_entry.bind('<Return>', self.close)
    
    def close(self, e = None):
        self.master.master.wm_attributes('-disabled', False)
        self.destroy()
        self.master.master.wm_deiconify()
    
    def show(self):
        self.master.master.wm_attributes('-disabled', True)
        self.transient(self.master)
        self.title('Choose delay between 2 generations')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.wm_deiconify()
        self.geometry(f'400x300+{self.master.master.winfo_x() + self.master.master.winfo_width() // 4}+{self.master.master.winfo_y() + self.master.master.winfo_height() // 4}')
        self.delay_entry.focus_force()
        self.wait_window()

        output = 0 if self.output.get() == '' else int(self.output.get()) / 1000
        return output