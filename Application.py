import tkinter as tk
import os
from Square import Square
from Grid import Grid
import time

class Application(tk.Frame):
    def __init__(self, master = None, size = 10, fillRandom = True):
        super().__init__(master)
        self.master = master
        self.grid()
        self.size = size
        self.fillRandom = fillRandom
        self.isPlaying = False
        self.create_widgets()

    def create_widgets(self):
        # Help row
        self.help_bar_h = tk.Frame(self, width = 35 * self.size, height = 0)
        self.help_bar_h.grid(row = 0, column = 0, sticky = tk.N + tk.W, columnspan = 2)

        # First row (resolution controls)
        self.resolution_group = tk.Frame(self)
        vcmd = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.height_entry = tk.Entry(self.resolution_group, validate = 'key', validatecommand = vcmd, font = ('Verdana', 20), width = 10)
        self.height_entry.bind('<Return>', self.set_resolution)
        self.x_label = tk.Label(self.resolution_group, text = 'x', font = ('Verdana', 20))
        self.width_entry = tk.Entry(self.resolution_group, validate = 'key', validatecommand = vcmd, font = ('Verdana', 20), width = 10)
        self.width_entry.bind('<Return>', self.set_resolution)
        self.set_resolution = tk.Button(self, text = 'Set resolution', command = self.set_resolution, font = ('Verdana', 8))

        self.resolution_group.grid(row = 1, column = 0, sticky = tk.W)
        self.height_entry.grid(row = 0, column = 2, sticky = tk.E)
        self.x_label.grid(row = 0, column = 1)
        self.width_entry.grid(row = 0, column = 0, sticky = tk.W)
        self.set_resolution.grid(row = 1, column = 1, sticky = tk.E, ipady = 10, ipadx = 10)

        self.height_entry.insert(0, '20')
        self.width_entry.insert(0, '35')

        # Second row (game)
        self.game = tk.Frame(self, width = int(self.width_entry.get()) * self.size, height = int(self.height_entry.get()) * self.size)
        self.game.config(bg = 'black')
        self.game.grid(row = 2, column = 0, columnspan = 2, sticky = tk.N + tk.W)

        # Third row (player controls)
        self.player_group = tk.Frame(self)
        self.play_icon = tk.PhotoImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'play.png'))
        self.pause_icon = tk.PhotoImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pause.png'))
        self.randomize_icon = tk.PhotoImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'randomize.png'))
        self.erase_icon = tk.PhotoImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'erase.png'))
        self.play_btn = tk.Button(self.player_group, image = self.play_icon, command = self.play, width = 50, height = 50)
        self.pause_btn = tk.Button(self.player_group, image = self.pause_icon, command = self.pause, width = 50, height = 50)
        self.randomize_btn = tk.Button(self.player_group, image = self.randomize_icon, command = self.randomize, width = 50, height = 50)
        self.erase_btn = tk.Button(self.player_group, image = self.erase_icon, command = self.erase, width = 50, height = 50)
        
        self.player_group.grid(row = 3, column = 0, sticky = tk.W + tk.S)
        self.play_btn.grid(row = 0, column = 0)
        self.pause_btn.grid(row = 0, column = 1)
        self.randomize_btn.grid(row = 0, column = 2)
        self.erase_btn.grid(row = 0, column = 3)

        # Third row (generation info)
        self.generation_label = tk.Label(self, font = ('Verdana', 10), fg = '#666666', text = 'Generation: 0')
        self.generation_label.grid(row = 3, column = 1, sticky = tk.E + tk.N + tk.S)
    
    def onValidate(self, d, i, P, s, S, v, V, W):
        if P:
            try:
                if str(int(P)) == P:
                    return True
            except:
                return False
        else:
            return True
    
    def set_resolution(self, e = None):   # pylint: disable=E0202
        if self.height_entry.get() == '' or int(self.height_entry.get()) < 1:
            height = int(self.game.winfo_height() / self.size)
        else:
            height = int(self.height_entry.get())
        
        if self.width_entry.get() == '' or int(self.width_entry.get()) < 1:
            width = int(self.game.winfo_width() / self.size)
        else:
            width = int(self.width_entry.get())

        newSize = int(input('Size: '))
        
        self.game.config(height = height * newSize, width = width * newSize)

        winwidth = 495 / newSize if width * newSize < 495 else width
        self.master.geometry(f'{int(winwidth * newSize)}x{height * newSize + 98}')
        self.help_bar_h.config(width = winwidth * newSize)

        self.setGrid(Grid(height, width), size = newSize)

    def setGrid(self, gamegrid, size = 0):
        self.game.destroy()
        self.game = tk.Frame(self, width = int(self.width_entry.get()) * self.size, height = int(self.height_entry.get()) * self.size)
        self.game.config(bg = 'black')
        self.game.grid(row = 2, column = 0, columnspan = 2, sticky = tk.N + tk.W)

        if size == 0: size = self.size
        self.size = size

        self.squares = []
        if self.fillRandom: gamegrid.fillRandom()
        self.gamegrid = gamegrid

        for i in range(len(gamegrid())):
            self.squares.append([])

            for j in range(len(gamegrid()[i])):
                square = Square(self.game, self.gamegrid, i, j, gamegrid()[i][j], self.size)
                square.grid(row = j, column = i)

                self.squares[i].append(square)
    
    def updateGrid(self):
        for i in range(len(self.gamegrid())):
            for j in range(len(self.gamegrid()[0])):
                newState = self.gamegrid()[i][j]
                self.squares[i][j].setState(newState)
                self.generation_label.config(text = f'Generation: {self.gamegrid.generation}')
    
    def play(self):
        self.isPlaying = True
        while self.isPlaying:
            oldGrid = self.gamegrid()
            self.gamegrid.computeNextGen()
            self.updateGrid()
            self.update()
            if oldGrid == self.gamegrid(): self.isPlaying = False

    def pause(self):
        self.isPlaying = False
    
    def randomize(self):
        self.gamegrid.fillRandom()
        self.gamegrid.generation = 0
        self.updateGrid()
        self.update()
    
    def erase(self):
        self.gamegrid.all(0)
        self.gamegrid.generation = 0
        self.updateGrid()
        self.update()