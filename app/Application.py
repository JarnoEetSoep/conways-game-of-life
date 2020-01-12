import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Thread import Thread
import json
import time
import os
from Square import Square
from Grid import Grid
from DelayModal import DelayModal
from HelpModal import HelpModal

class Application(tk.Frame):
    def __init__(self, master = None, width = 40, height = 25, size = 10, fillRandom = True, filepath = None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.size = size
        self.fillRandom = fillRandom
        self.isPlaying = False
        self.delay = 0
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.tk.call('wm', 'iconphoto', self.master._w, ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/icon.png'))))
        
        self.updateGridThread = Thread(self, self.delay, self._playGame)

        self.filepath = filepath
        if filepath: self.loadFile()
        
        self.create_widgets()
        self.width.set(str(width))
        self.height.set(str(height))
        self.sizevar.set(str(size))

        self.master.update()

        self.setResolution()

    def create_widgets(self):
        # Styles
        self.button_style = {'relief': 'raised', 'cursor': 'hand2'}
        self.entry_style = {'relief': 'sunken'}
        self.checkbutton_style = {'font': ('Verdana', 10)}

        # Help row
        self.help_bar_h = tk.Frame(self, width = 35 * self.size, height = 0)
        self.help_bar_h.grid(row = 0, column = 0, sticky = tk.N + tk.W, columnspan = 2)

        # Top menu
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = 'File', menu = self.menu_file)

        self.menu_file.add_command(label = 'New File     (Ctrl+N)', command = self.newFile)
        self.master.bind('<Control-n>', self.newFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Open...      (Ctrl+O)', command = self.openFile)
        self.master.bind('<Control-o>', self.openFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Save         (Ctrl+S)', command = self.saveFile)
        self.master.bind('<Control-s>', self.saveFile)
        self.menu_file.add_command(label = 'Save As...   (Ctrl+Shift+S)', command = self.saveFileAs)
        self.master.bind('<Control-S>', self.saveFileAs)
        self.menu_file.add_separator()

        self.menu_examples = tk.Menu(self.menu_file, tearoff = 0)
        self.menu_file.add_cascade(label = 'Examples', menu = self.menu_examples)

        self.menu_examples.add_command(label = 'Glider', command = lambda: self.loadExample('glider'))
        self.menu_examples.add_command(label = 'Lightweight spaceship', command = lambda: self.loadExample('lightweight-spaceship'))
        self.menu_examples.add_separator()
        self.menu_examples.add_command(label = 'Blinker', command = lambda: self.loadExample('oscillator-blinker'))
        self.menu_examples.add_command(label = 'Toad', command = lambda: self.loadExample('oscillator-toad'))
        self.menu_examples.add_command(label = 'Beacon', command = lambda: self.loadExample('oscillator-beacon'))
        self.menu_examples.add_command(label = 'Traffic light', command = lambda: self.loadExample('oscillator-traffic-light'))
        self.menu_examples.add_command(label = 'Pulsar', command = lambda: self.loadExample('oscillator-pulsar'))
        self.menu_examples.add_command(label = 'Pentadecathlon', command = lambda: self.loadExample('oscillator-pentadecathlon'))
        self.menu_examples.add_separator()
        self.menu_examples.add_command(label = 'Gospers glider gun with eater', command = lambda: self.loadExample('gospers-glider-gun-with-eater'))

        self.master.config(menu = self.menu)

        # First row (resolution controls)
        self.resolution_group = tk.Frame(self)
        self.size_and_set_group = tk.Frame(self)

        self.only_digits = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.width = tk.StringVar()
        self.height = tk.StringVar()
        self.sizevar = tk.StringVar()

        self.width_entry = tk.Entry(self.resolution_group, textvariable = self.width, validate = 'key', validatecommand = self.only_digits, font = ('Verdana', 20), width = 5, cnf = self.entry_style)
        self.width_entry.bind('<Return>', self.setResolution)
        self.x_label = tk.Label(self.resolution_group, text = 'x', font = ('Verdana', 20))
        self.height_entry = tk.Entry(self.resolution_group, textvariable = self.height, validate = 'key', validatecommand = self.only_digits, font = ('Verdana', 20), width = 5, cnf = self.entry_style)
        self.height_entry.bind('<Return>', self.setResolution)
        self.size_label = tk.Label(self.size_and_set_group, text = 'Square size: ', font = ('Verdana', 10))
        self.size_entry = tk.Entry(self.size_and_set_group, textvariable = self.sizevar, validate = 'key', validatecommand = self.only_digits, font = ('Verdana', 20), width = 5, cnf = self.entry_style)
        self.size_entry.bind('<Return>', self.setResolution)
        self.set_resolution = tk.Button(self.size_and_set_group, text = 'Set resolution', command = self.setResolution, font = ('Verdana', 8), cnf = self.button_style)

        self.resolution_group.grid(row = 0, column = 0, sticky = tk.W)
        self.width_entry.grid(row = 0, column = 0, sticky = tk.W)
        self.x_label.grid(row = 0, column = 1, sticky = tk.W)
        self.height_entry.grid(row = 0, column = 2, sticky = tk.W)

        self.size_and_set_group.grid(row = 0, column = 1, sticky = tk.E)
        self.size_label.grid(row = 0, column = 0, sticky = tk.E)
        self.size_entry.grid(row = 0, column = 1, sticky = tk.E)
        self.set_resolution.grid(row = 0, column = 2, sticky = tk.E, ipady = 7, ipadx = 10)

        # Second row (game)
        self.game = tk.Frame(self)
        self.game.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N + tk.W)

        # Third row (player controls)
        self.player_group = tk.Frame(self)
        self.help_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/help.png')).resize((50, 50), Image.ANTIALIAS))
        self.play_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/play.png')).resize((50, 50), Image.ANTIALIAS))
        self.pause_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/pause.png')).resize((50, 50), Image.ANTIALIAS))
        self.randomize_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/randomize.png')).resize((50, 50), Image.ANTIALIAS))
        self.skip_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/skip.png')).resize((50, 50), Image.ANTIALIAS))
        self.erase_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/erase.png')).resize((50, 50), Image.ANTIALIAS))
        self.help_btn = tk.Button(self.player_group, image = self.help_icon, command = self.help, width = 50, cnf = self.button_style)
        self.play_btn = tk.Button(self.player_group, image = self.play_icon, command = self.play, width = 50, cnf = self.button_style)
        self.pause_btn = tk.Button(self.player_group, image = self.pause_icon, command = self.pause, width = 50, cnf = self.button_style)
        self.randomize_btn = tk.Button(self.player_group, image = self.randomize_icon, command = self.randomize, width = 50, cnf = self.button_style)
        self.erase_btn = tk.Button(self.player_group, image = self.erase_icon, command = self.erase, width = 50, cnf = self.button_style)
        self.skip_btn = tk.Button(self.player_group, image = self.skip_icon, command = self.skip, width = 50, cnf = self.button_style)

        self.help_btn.image = self.help_icon
        self.play_btn.image = self.play_icon
        self.pause_btn.image = self.pause_icon
        self.randomize_btn.image = self.randomize_icon
        self.erase_btn.image = self.erase_icon
        self.skip_btn.image = self.skip_icon

        self.connect_group = tk.Frame(self.player_group)
        self.updown = tk.IntVar(value = 1)
        self.leftright = tk.IntVar(value = 1)
        self.connect_up_down = tk.Checkbutton(self.connect_group, text = 'Connect up and down', variable = self.updown, cnf = self.checkbutton_style)
        self.connect_left_right = tk.Checkbutton(self.connect_group, text = 'Connect left and right', variable = self.leftright, cnf = self.checkbutton_style)
        
        self.player_group.grid(row = 2, column = 0, sticky = tk.W + tk.S)
        self.help_btn.grid(row = 0, column = 0)
        self.play_btn.grid(row = 0, column = 1)
        self.pause_btn.grid(row = 0, column = 2)
        self.randomize_btn.grid(row = 0, column = 3)
        self.erase_btn.grid(row = 0, column = 4)
        self.skip_btn.grid(row = 0, column = 5)

        self.connect_group.grid(row = 0, column = 6)
        self.connect_up_down.grid(row = 0, column = 0)
        self.connect_left_right.grid(row = 1, column = 0)

        # Third row (generation info and quit button)
        self.gen_and_quit = tk.Frame(self, height = 50)
        self.generation_label = tk.Label(self.gen_and_quit, font = ('Verdana', 10), fg = '#666666', text = 'Generation: 0')
        self.quit_icon = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/quit.png')).resize((50, 50), Image.ANTIALIAS))
        self.quit_btn = tk.Button(self.gen_and_quit, image = self.quit_icon, command = self.quit, width = 50, cnf = self.button_style)

        self.quit_btn.image = self.quit_icon

        self.gen_and_quit.grid(row = 2, column = 1, sticky = tk.E + tk.N + tk.S)
        self.generation_label.grid(row = 2, column = 0, sticky = tk.E + tk.N + tk.S)
        self.quit_btn.grid(row = 2, column = 1, sticky = tk.E + tk.N + tk.S)

        # Help modal
        self.helpModal = None
    
    def onValidate(self, d, i, P, s, S, v, V, W):
        if P:
            try:
                if str(int(P)) == P and int(P) > -1:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True
    
    def setResolution(self, e = None):   # pylint: disable=E0202
        if self.width.get() == '' or int(self.width.get()) < 1:
            width = int(self.game.winfo_width() / self.size)
            self.width.set(str(width))
        else:
            width = int(self.width_entry.get())

        if self.height.get() == '' or int(self.height.get()) < 1:
            height = int(self.game.winfo_height() / self.size)
            self.height.set(str(height))
        else:
            height = int(self.height_entry.get())
        
        if self.sizevar.get() == '' or int(self.sizevar.get()) < 1:
            self.size.set(str(width))
        else:
            self.size = int(self.size_entry.get())
        
        self.game.config(height = height * self.size, width = width * self.size)

        winwidth = 805 / self.size if width * self.size < 805 else width
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
        self.oldGrid = gamegrid()

        for i in range(len(gamegrid())):
            self.squares.append([])

            for j in range(len(gamegrid()[i])):
                square = Square(self.game, self.gamegrid, i, j, gamegrid()[i][j], self.size)
                square.grid(row = j, column = i)

                self.squares[i].append(square)
    
    def updateGrid(self, compute = True):
        if compute:
            self.oldGrid = self.gamegrid()
            self.gamegrid.computeNextGen(bool(self.updown.get()), bool(self.leftright.get()))
        
        self.generation_label.config(text = f'Generation: {self.gamegrid.generation}')
        for i in range(len(self.gamegrid())):
            for j in range(len(self.gamegrid()[0])):
                if self.oldGrid[i][j] != self.gamegrid()[i][j]:
                    newState = self.gamegrid()[i][j]
                    self.squares[i][j].setState(newState)
        
        if self.oldGrid == self.gamegrid(): self.isPlaying = False
    
    def _playGame(self):
        if self.isPlaying:
            self.updateGrid()
            self.update()
    
    def play(self, e = None):
        self.delay = DelayModal(self).show()

        if self.delay >= 0:
            self.updateGridThread.setDelay(self.delay)
            self.isPlaying = True

            if not self.updateGridThread.is_alive():
                self.updateGridThread.start()

    def pause(self):
        self.isPlaying = False
    
    def randomize(self):
        self.oldGrid = self.gamegrid()
        self.gamegrid.fillRandom()
        self.gamegrid.generation = 0
        self.updateGrid(compute = False)
        self.update()
    
    def erase(self):
        self.oldGrid = self.gamegrid()
        self.gamegrid.all(0, lambda c: c == 1)
        self.gamegrid.generation = 0
        self.updateGrid(compute = False)
        self.update()
    
    def skip(self):
        self.updateGrid()
        self.update()
    
    def quit(self, e = None):
        self.isPlaying = False
        self.updateGridThread.kill()
        self.master.destroy()
    
    def help(self):
        if self.helpModal and self.helpModal.winfo_exists():
            self.helpModal.focus_force()
        else:
            self.helpModal = HelpModal(self)
            self.helpModal.show()
    
    def newFile(self, e = None):
        self.filepath = None
        self.setResolution()

        self.master.title('Conway\'s Game of Life')
    
    def openFile(self, e = None):
        cgol_path = filedialog.askopenfilename(initialdir = os.path.abspath('.'), title = 'Choose GoL board', filetypes = [('Conway\'s Game of Life save', '*.cgol')])

        if cgol_path:   
            cgol_path = os.path.abspath(cgol_path)
            self.filepath = cgol_path
            self.loadFile()
    
    def saveFile(self, e = None):
        if self.filepath:
            save = {}
            save['size'] = self.sizevar.get()
            save['wrapleftright'] = bool(self.leftright.get())
            save['wrapupdown'] = bool(self.updown.get())
            g = self.gamegrid()
            save['board'] = [[g[j][i] for j in range(len(g))] for i in range(len(g[0]))]
            
            with open(self.filepath, 'w', encoding = 'UTF-8') as cgol:
                cgol.write(json.dumps(save, separators = (',', ':')))
                cgol.close()
        else:
            self.saveFileAs()
    
    def saveFileAs(self, e = None):
        cgol_path = filedialog.asksaveasfilename(initialdir = os.path.abspath('.'), title = 'Save GoL board', filetypes = [('Conway\'s Game of Life save', '*.cgol')])
        if not cgol_path.endswith('.cgol'): cgol_path += '.cgol'
        
        if cgol_path:   
            cgol_path = os.path.abspath(cgol_path)
            self.filepath = cgol_path

            self.master.title(f'{os.path.basename(os.path.normpath(self.filepath))} - Conway\'s Game of Life')

            save = {}
            save['size'] = self.sizevar.get()
            save['wrapleftright'] = bool(self.leftright.get())
            save['wrapupdown'] = bool(self.updown.get())
            g = self.gamegrid()
            save['board'] = [[g[j][i] for j in range(len(g))] for i in range(len(g[0]))]
            
            with open(cgol_path, 'w', encoding = 'UTF-8') as cgol:
                cgol.write(json.dumps(save, separators = (',', ':')))
                cgol.close()

    def loadFile(self):
        with open(self.filepath, 'r', encoding = 'UTF-8') as cgol:
            data = json.loads(cgol.read())
            try:
                size = str(int(data['size']))
                board = data['board']
                board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

                self.width.set(len(board))
                self.height.set(len(board[0]))
                self.sizevar.set(size)

                self.leftright.set(int(data['wrapleftright']))
                self.updown.set(int(data['wrapupdown']))

                self.setResolution()

                self.gamegrid.setGrid(board)
                self.updateGrid(compute = False)
                self.master.title(f'{os.path.basename(os.path.normpath(self.filepath))} - Conway\'s Game of Life')
            except Exception as e:
                print(e)
            
            cgol.close()
    
    def loadExample(self, name):
        cgol_path = os.path.normpath(os.path.join(os.path.abspath('.'), f'examples/{name}.cgol'))
        with open(cgol_path, 'r', encoding = 'UTF-8') as cgol:
            data = json.loads(cgol.read())

            size = str(int(data['size']))
            board = data['board']
            board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

            self.width.set(len(board))
            self.height.set(len(board[0]))
            self.sizevar.set(size)

            self.leftright.set(int(data['wrapleftright']))
            self.updown.set(int(data['wrapupdown']))

            self.setResolution()

            self.gamegrid.setGrid(board)
            self.updateGrid(compute = False)