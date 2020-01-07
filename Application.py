import tkinter as tk
import os
from Square import Square
from Grid import Grid
import time
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master = None, size = 10, fillRandom = True):
        super().__init__(master)
        self.master = master
        self.grid()
        self.size = size
        self.fillRandom = fillRandom
        self.isPlaying = False
        self.master.tk.call('wm', 'iconphoto', self.master._w, ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.png'))))
        self.create_widgets()

    def create_widgets(self):
        # Help row
        self.help_bar_h = tk.Frame(self, width = 35 * self.size, height = 0)
        self.help_bar_h.grid(row = 0, column = 0, sticky = tk.N + tk.W, columnspan = 2)

        # First row (resolution controls)
        self.resolution_group = tk.Frame(self)
        self.size_and_set_group = tk.Frame(self)
        vcmd = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.height_entry = tk.Entry(self.resolution_group, validate = 'key', validatecommand = vcmd, font = ('Verdana', 20), width = 5)
        self.height_entry.bind('<Return>', self.set_resolution)
        self.x_label = tk.Label(self.resolution_group, text = 'x', font = ('Verdana', 20))
        self.width_entry = tk.Entry(self.resolution_group, validate = 'key', validatecommand = vcmd, font = ('Verdana', 20), width = 5)
        self.width_entry.bind('<Return>', self.set_resolution)
        self.size_label = tk.Label(self.size_and_set_group, text = 'Square size: ', font = ('Verdana', 10))
        self.size_entry = tk.Entry(self.size_and_set_group, validate = 'key', validatecommand = vcmd, font = ('Verdana', 20), width = 5)
        self.size_entry.bind('<Return>', self.set_resolution)
        self.set_resolution = tk.Button(self.size_and_set_group, text = 'Set resolution', command = self.set_resolution, font = ('Verdana', 8))

        self.resolution_group.grid(row = 0, column = 0, sticky = tk.W)
        self.width_entry.grid(row = 0, column = 0, sticky = tk.W)
        self.x_label.grid(row = 0, column = 1, sticky = tk.W)
        self.height_entry.grid(row = 0, column = 2, sticky = tk.W)

        self.size_and_set_group.grid(row = 0, column = 1, sticky = tk.E)
        self.size_label.grid(row = 0, column = 0, sticky = tk.E)
        self.size_entry.grid(row = 0, column = 1, sticky = tk.E)
        self.set_resolution.grid(row = 0, column = 2, sticky = tk.E, ipady = 7, ipadx = 10)

        self.height_entry.insert(0, '25')
        self.width_entry.insert(0, '40')
        self.size_entry.insert(0, '20')

        # Second row (game)
        self.game = tk.Frame(self, width = int(self.width_entry.get()) * self.size, height = int(self.height_entry.get()) * self.size)
        self.game.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N + tk.W)

        # Third row (player controls)
        self.player_group = tk.Frame(self)
        self.play_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'play.png')).resize((50, 50), Image.ANTIALIAS))
        self.pause_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pause.png')).resize((50, 50), Image.ANTIALIAS))
        self.randomize_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'randomize.png')).resize((50, 50), Image.ANTIALIAS))
        self.skip_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'skip.png')).resize((50, 50), Image.ANTIALIAS))
        self.erase_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'erase.png')).resize((50, 50), Image.ANTIALIAS))
        self.play_btn = tk.Button(self.player_group, image = self.play_icon, command = self.play, width = 50, height = 50)
        self.pause_btn = tk.Button(self.player_group, image = self.pause_icon, command = self.pause, width = 50, height = 50)
        self.randomize_btn = tk.Button(self.player_group, image = self.randomize_icon, command = self.randomize, width = 50, height = 50)
        self.erase_btn = tk.Button(self.player_group, image = self.erase_icon, command = self.erase, width = 50, height = 50)
        self.skip_btn = tk.Button(self.player_group, image = self.skip_icon, command = self.skip, width = 50, height = 50)

        self.play_btn.image = self.play_icon
        self.pause_btn.image = self.pause_icon
        self.randomize_btn.image = self.randomize_icon
        self.erase_btn.image = self.erase_icon
        self.skip_btn.image = self.skip_icon
        
        self.player_group.grid(row = 2, column = 0, sticky = tk.W + tk.S)
        self.play_btn.grid(row = 0, column = 0)
        self.pause_btn.grid(row = 0, column = 1)
        self.randomize_btn.grid(row = 0, column = 2)
        self.erase_btn.grid(row = 0, column = 3)
        self.skip_btn.grid(row = 0, column = 4)

        # Third row (generation info)
        self.generation_label = tk.Label(self, font = ('Verdana', 10), fg = '#666666', text = 'Generation: 0')
        self.generation_label.grid(row = 2, column = 1, sticky = tk.E + tk.N + tk.S)
    
    def onValidate(self, d, i, P, s, S, v, V, W):
        if P:
            try:
                if str(int(P)) == P and int(P) > 0:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True
    
    def set_resolution(self, e = None):   # pylint: disable=E0202
        if self.height_entry.get() == '' or int(self.height_entry.get()) < 1:
            height = int(self.game.winfo_height() / self.size)
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(height))
        else:
            height = int(self.height_entry.get())
        
        if self.width_entry.get() == '' or int(self.width_entry.get()) < 1:
            width = int(self.game.winfo_width() / self.size)
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(width))
        else:
            width = int(self.width_entry.get())
        
        if self.size_entry.get() == '' or int(self.size_entry.get()) < 1:
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(width))
        else:
            self.size = int(self.size_entry.get())
        
        self.game.config(height = height * self.size, width = width * self.size)

        winwidth = 40 * 15 / self.size if width * self.size < 40 * 15 else width
        self.master.geometry(f'{int(winwidth * self.size)}x{height * self.size + 93}')
        self.help_bar_h.config(width = winwidth * self.size)

        self.setGrid(Grid(height, width), size = self.size)

    def setGrid(self, gamegrid, size = 0):
        self.game.destroy()
        self.game = tk.Frame(self, width = int(self.width_entry.get()) * self.size, height = int(self.height_entry.get()) * self.size)
        self.game.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N + tk.W)

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
        self.generation_label.config(text = f'Generation: {self.gamegrid.generation}')
        for i in range(len(self.gamegrid())):
            for j in range(len(self.gamegrid()[0])):
                if self.oldGrid[i][j] != self.gamegrid()[i][j]:
                    newState = self.gamegrid()[i][j]
                    self.squares[i][j].setState(newState)
    
    def play(self):
        self.isPlaying = True
        while self.isPlaying:
            self.oldGrid = self.gamegrid()
            self.gamegrid.computeNextGen()
            self.updateGrid()
            self.update()
            if self.oldGrid == self.gamegrid(): self.isPlaying = False

    def pause(self):
        self.isPlaying = False
    
    def randomize(self):
        self.oldGrid = self.gamegrid()
        self.gamegrid.fillRandom()
        self.gamegrid.generation = 0
        self.updateGrid()
        self.update()
    
    def erase(self):
        self.oldGrid = self.gamegrid()
        self.gamegrid.all(0, lambda c: c == 1)
        self.gamegrid.generation = 0
        self.updateGrid()
        self.update()
    
    def skip(self):
        self.oldGrid = self.gamegrid()
        self.gamegrid.computeNextGen()
        self.updateGrid()
        self.update()