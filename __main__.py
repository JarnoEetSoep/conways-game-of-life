import tkinter as tk
from Grid import Grid
from Application import Application

root = tk.Tk()

root.resizable(0, 0)
root.geometry('525x398')
root.title('Conway\'s Game of Life - by Jarno Romijn')

app = Application(master = root, size = 15, fillRandom = False)

grid = Grid(20, 35)
app.setGrid(grid)

app.mainloop()