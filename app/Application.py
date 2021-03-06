import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from Thread import Thread
import json
import time
import os

from Square import Square
from Grid import Grid
from DelayModal import DelayModal
from HelpModal import HelpModal
from SettingsModal import SettingsModal
from BetterScrollbar import BetterScrollbar

class Application(tk.Frame):
    def __init__(self, master = None, width = 40, height = 25, filepath = None):
        super().__init__(master)
        self.master = master
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'r', encoding = 'UTF-8') as settings:
            self.settings = json.loads(settings.read())
            settings.close()

        self.isPlaying = False
        self.delay = 0
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.tk.call('wm', 'iconphoto', self.master._w, ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/icon.png'))))
        
        self.updateGridThread = Thread(self, self.delay, self._playGame)

        self.is_fullscreen = True
        self.master.bind('<F11>', lambda e: self.fullscreen('toggle'))
        self.master.bind('<Escape>', lambda e: self.fullscreen('off'))
        
        self.createWidgets()
        self.width.set(str(width))
        self.height.set(str(height))

        self.master.update()

        self.filepath = filepath
        if filepath:
            self.loadFile()
        else:
            self.setResolution()

    def createWidgets(self):
        # Styles
        self.button_style = {'relief': 'raised', 'cursor': 'hand2'}
        self.entry_style = {'relief': 'sunken'}
        self.checkbutton_style = {'font': ('Verdana', 10)}

        # Grid configure
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(1, weight = 1)

        # Top menu
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = 'File', menu = self.menu_file)

        self.menu_file.add_command(label = 'New File', accelerator = 'Ctrl+N', command = self.newFile)
        self.master.bind_all('<Control-n>', self.newFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Open...', accelerator = 'Ctrl+O', command = self.openFile)
        self.master.bind_all('<Control-o>', self.openFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Save', accelerator = 'Ctrl+S', command = self.saveFile)
        self.master.bind_all('<Control-s>', self.saveFile)
        self.menu_file.add_command(label = 'Save As...', accelerator = 'Ctrl+Shift+S', command = self.saveFileAs)
        self.master.bind_all('<Control-S>', self.saveFileAs)
        self.menu_file.add_separator()

        self.menu_examples = tk.Menu(self.menu_file, tearoff = 0)
        self.menu_file.add_cascade(label = 'Examples', menu = self.menu_examples)

        self.menu_examples.add_command(label = 'Glider', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'glider.cgol'))))
        self.menu_examples.add_command(label = 'Big glider', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'big-glider.cgol'))))
        self.menu_examples.add_command(label = 'Lightweight spaceship', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'lightweight-spaceship.cgol'))))
        self.menu_examples.add_command(label = 'Middleweight spaceship', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'middleweight-spaceship.cgol'))))
        self.menu_examples.add_command(label = 'Heavyweight spaceship', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'heavyweight-spaceship.cgol'))))
        self.menu_examples.add_command(label = 'Spider', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'spider.cgol'))))
        self.menu_examples.add_command(label = 'Weekender', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'weekender.cgol'))))
        self.menu_examples.add_command(label = 'Photon', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'spaceships', 'photon.cgol'))))

        self.menu_examples.add_separator()

        self.menu_examples.add_command(label = 'Blinker', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'blinker.cgol'))))
        self.menu_examples.add_command(label = 'Toad', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'toad.cgol'))))
        self.menu_examples.add_command(label = 'Beacon', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'beacon.cgol'))))
        self.menu_examples.add_command(label = 'Traffic light', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'traffic-light.cgol'))))
        self.menu_examples.add_command(label = 'Pulsar', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'pulsar.cgol'))))
        self.menu_examples.add_command(label = 'Pentadecathlon', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'oscillators', 'pentadecathlon.cgol'))))

        self.menu_examples.add_separator()

        self.menu_examples.add_command(label = 'R-Pentomino', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'methelusas', 'r-pentomino.cgol'))))

        self.menu_examples.add_separator()

        self.menu_examples.add_command(label = 'Gospers glider gun with eater', command = lambda: self.loadFile(File = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples', 'misc', 'gospers-glider-gun-with-eater.cgol'))))

        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Settings', command = self.openSettings)

        self.menu_help = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = 'Help', menu = self.menu_help)

        self.menu_help.add_command(label = 'Manual', accelerator = 'F1', command = self.help)
        self.master.bind_all('<F1>', self.help)

        self.master.config(menu = self.menu)

        # First row (resolution controls)
        self.resolution_group = tk.Frame(self)

        self.only_digits = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.width = tk.StringVar()
        self.height = tk.StringVar()

        self.width_entry = tk.Entry(self.resolution_group, textvariable = self.width, validate = 'key', validatecommand = self.only_digits, font = ('Verdana', 20), width = 5, cnf = self.entry_style)
        self.width_entry.bind('<Return>', self.setResolution)
        self.x_label = tk.Label(self.resolution_group, text = 'x', font = ('Verdana', 20))
        self.height_entry = tk.Entry(self.resolution_group, textvariable = self.height, validate = 'key', validatecommand = self.only_digits, font = ('Verdana', 20), width = 5, cnf = self.entry_style)
        self.height_entry.bind('<Return>', self.setResolution)
        self.set_resolution = tk.Button(self, text = 'Set resolution', command = self.setResolution, font = ('Verdana', 8), cnf = self.button_style)

        self.resolution_group.grid(row = 0, column = 0, sticky = tk.W)
        self.width_entry.grid(row = 0, column = 0, sticky = tk.W)
        self.x_label.grid(row = 0, column = 1, sticky = tk.W)
        self.height_entry.grid(row = 0, column = 2, sticky = tk.W)

        self.set_resolution.grid(row = 0, column = 1, sticky = tk.E, ipady = 7, ipadx = 10)

        # Second row (game)
        self.game_container = tk.Frame(self)
        self.game_container.grid_rowconfigure(0, weight = 1)
        self.game_container.columnconfigure(0, weight = 1)
        self.game_container.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N + tk.E + tk.S + tk.W)

        self.game_scrollbar_h = BetterScrollbar(self.game_container, orient = tk.HORIZONTAL)
        self.game_scrollbar_h.grid(row = 1, column = 0, sticky = tk.W + tk.E)

        self.game_scrollbar_v = BetterScrollbar(self.game_container, orient = tk.VERTICAL)
        self.game_scrollbar_v.grid(row = 0, column = 1, sticky = tk.N + tk.S)

        self.game = tk.Canvas(self.game_container, cursor = 'hand2', bd = 0, xscrollcommand = self.game_scrollbar_h.set, yscrollcommand = self.game_scrollbar_v.set)
        self.game.grid(row = 0, column = 0, sticky = tk.N + tk.W + tk.E + tk.S)

        self.game.bind('<Shift-MouseWheel>', lambda e: self.game.xview_scroll(-int(e.delta / 120), 'units'))
        self.game.bind('<Shift-Button-4>', lambda e: self.game.xview_scroll(-int(e.delta / 120), 'units'))
        self.game.bind('<Shift-Button-5>', lambda e: self.game.xview_scroll(-int(e.delta / 120), 'units'))

        self.game.bind('<MouseWheel>', lambda e: self.game.yview_scroll(-int(e.delta / 120), 'units'))
        self.game.bind('<Button-4>', lambda e: self.game.yview_scroll(-int(e.delta / 120), 'units'))
        self.game.bind('<Button-5>', lambda e: self.game.yview_scroll(-int(e.delta / 120), 'units'))

        self.game.bind('<Shift-Button-1>', lambda e: self.game.scan_mark(e.x, e.y))
        self.game.bind('<Shift-B1-Motion>', lambda e: self.game.scan_dragto(e.x, e.y, gain = 1))

        self.game.bind('<Control-MouseWheel>', self.zoomGame)
        self.game.bind('<Control-Button-4>', self.zoomGame)
        self.game.bind('<Control-Button-5>', self.zoomGame)

        self.game_scrollbar_h.config(command = self.game.xview)
        self.game_scrollbar_v.config(command = self.game.yview)

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

        self.gen_and_quit.grid(row = 2, column = 1, sticky = tk.E)
        self.generation_label.grid(row = 0, column = 0, sticky = tk.E)
        self.quit_btn.grid(row = 0, column = 1, sticky = tk.E)

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
    
    def setResolution(self, e = None):
        if self.width.get() != '' and int(self.width.get()) > 0:
            if self.height.get() != '' and int(self.height.get()) > 0:
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())

                self.setGrid(Grid(height, width))

                self.game.config(scrollregion = self.game.bbox('all'))

    def setGrid(self, gamegrid):
        self.game.delete('all')

        self.gamegrid = gamegrid
        self.oldGrid = gamegrid()
        self.squares = []

        for i in range(len(gamegrid())):
            self.squares.append([])
            for j in range(len(gamegrid()[i])):
                ID = self.game.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, outline = '#808080', tag = f'{i},{j}')
                square = Square(self.gamegrid, self.game, ID, i, j, self.gamegrid()[i][j], self.settings['alive-color'], self.settings['dead-color'])
                self.squares[i].append(square)
        
        self.update()
    
    def updateGrid(self, compute = True):
        if compute:
            self.oldGrid = self.gamegrid()
            self.gamegrid.computeNextGen(bool(self.updown.get()), bool(self.leftright.get()), self.settings['rule'])
        
        self.generation_label.config(text = f'Generation: {self.gamegrid.generation}')
        for i in range(len(self.gamegrid())):
            for j in range(len(self.gamegrid()[0])):
                if self.oldGrid[i][j] != self.gamegrid()[i][j]:
                    newState = self.gamegrid()[i][j]
                    self.squares[i][j].setState(newState)
        
        if self.oldGrid == self.gamegrid(): self.isPlaying = False
        self.game.update()
    
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
    
    def help(self, e = None):
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
            save['wrapleftright'] = bool(self.leftright.get())
            save['wrapupdown'] = bool(self.updown.get())
            save['rule'] = self.settings['rule']
            g = self.gamegrid()
            save['board'] = [[g[j][i] for j in range(len(g))] for i in range(len(g[0]))]
            
            with open(self.filepath, 'w', encoding = 'UTF-8') as cgol:
                cgol.write(json.dumps(save, separators = (',', ':')))
                cgol.close()
        else:
            self.saveFileAs()
    
    def saveFileAs(self, e = None):
        cgol_path = filedialog.asksaveasfilename(initialdir = os.path.abspath('.'), title = 'Save GoL board', filetypes = [('Conway\'s Game of Life save', '*.cgol')])
        
        if cgol_path:  
            if not cgol_path.endswith('.cgol'): cgol_path += '.cgol' 
            cgol_path = os.path.abspath(cgol_path)
            self.filepath = cgol_path

            self.master.title(f'{os.path.basename(os.path.normpath(self.filepath))} - Conway\'s Game of Life')

            save = {}
            save['wrapleftright'] = bool(self.leftright.get())
            save['wrapupdown'] = bool(self.updown.get())
            save['rule'] = self.settings['rule']
            g = self.gamegrid()
            save['board'] = [[g[j][i] for j in range(len(g))] for i in range(len(g[0]))]
            
            with open(cgol_path, 'w', encoding = 'UTF-8') as cgol:
                cgol.write(json.dumps(save, separators = (',', ':')))
                cgol.close()

    def loadFile(self, File = None):
        path = File if File else self.filepath
        with open(path, 'r', encoding = 'UTF-8') as cgol:
            data = json.loads(cgol.read())
            try:
                board = data['board']

                for i in range(0, len(board)):
                    assert len(board[i]) == len(board[i - 1])

                board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

                self.width.set(len(board))
                self.height.set(len(board[0]))

                self.leftright.set(int(data['wrapleftright']))
                self.updown.set(int(data['wrapupdown']))
                self.settings['rule'] = data['rule']

                self.setResolution()

                self.gamegrid.setGrid(board)
                self.updateGrid(compute = False)

                if File == None: self.master.title(f'{os.path.basename(os.path.normpath(self.filepath))} - Conway\'s Game of Life')

                with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'w', encoding = 'UTF-8') as settings:
                    settings.write(json.dumps(self.settings, indent = 4))
                    settings.close()

            except (TypeError, KeyError, AssertionError):
                messagebox.showerror('Couldn\'t load file', f'File couldn\'t be loaded, bacause the save file is probably corrupted. Make sure it has the following properties: wrapleftright, wrapupdown, rule and board. For more info see the documentation (nice question mark in the left-bottom corner.')
            except Exception as e:
                messagebox.showerror('Couldn\'t load file', f'This is an uncaught exeption. Please send the following to the developer.\n\n{e}\n{e.args}')
            
            cgol.close()
    
    def openSettings(self):
        self.settings = SettingsModal(self).show()

        for i in range(len(self.gamegrid())):
            for j in range(len(self.gamegrid()[0])):
                self.squares[i][j].setColors(self.settings['alive-color'], self.settings['dead-color'])
    
    def fullscreen(self, mode):
        if mode == 'toggle':
            self.is_fullscreen = not self.is_fullscreen
            self.master.attributes('-fullscreen', self.is_fullscreen)
        elif mode == 'off':
            self.is_fullscreen = False
            self.master.attributes('-fullscreen', False)
    
    def zoomGame(self, e):
        if e.num == 4 or e.delta > 0:
            self.game.scale('all', e.x, e.y, 1.1, 1.1)
        elif e.num == 5 or e.delta < 0:
            self.game.scale('all', e.x, e.y, 0.9, 0.9)
        
        self.game.config(scrollregion = self.game.bbox('all'))