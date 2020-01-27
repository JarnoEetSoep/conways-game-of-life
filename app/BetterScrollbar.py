import tkinter as tk

class BetterScrollbar(tk.Scrollbar):
    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.tk.call('grid', 'remove', self)
        else:
            self.grid()

        tk.Scrollbar.set(self, first, last)