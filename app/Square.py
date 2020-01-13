import tkinter as tk

class Square(tk.Frame):
    def __init__(self, master, gamegrid, x, y, state, size, alive_color, dead_color):
        super().__init__(master)
        self.gamegrid = gamegrid
        self.x = x
        self.y = y
        self.state = state
        self.alive_color = alive_color
        self.dead_color = dead_color
        self._setColor()
        self.size = size
        self.config(height = self.size, width = self.size, bd = 1, relief = 'ridge', cursor = 'hand2')
        self.bind('<Button-1>', self.switchState)

    def _setColor(self):
        self.config(bg = self.alive_color if self.state == 1 else self.dead_color)
    
    def switchState(self, e = None):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
        
        self._setColor()
        self.gamegrid.change(self.x, self.y, self.state)
    
    def setState(self, state):
        self.state = state
        self._setColor()
        self.gamegrid.change(self.x, self.y, self.state)
    
    def setColors(self, a, d):
        self.alive_color = a
        self.dead_color = d
        self._setColor()