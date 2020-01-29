class Square:
    def __init__(self, gamegrid, canvas, ID, x, y, state, alive_color, dead_color):
        self.canvas = canvas
        self.gamegrid = gamegrid
        self.x = x
        self.y = y
        self.id = ID
        self.state = state
        self.alive_color = alive_color
        self.dead_color = dead_color
        self._setColor()
        self.canvas.tag_bind(f'{x},{y}', '<Button-1>', self.switchState)

    def _setColor(self):
        self.canvas.itemconfig(f'{self.x},{self.y}', fill = self.alive_color if self.state == 1 else self.dead_color)
    
    def switchState(self, e = None):
        if e.state:
            if e.state == 1:
                return None

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