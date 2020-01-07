import tkinter as tk
from Grid import Grid
from Application import Application

root = tk.Tk()

root.resizable(0, 0)

width = 40
height = 25
size = 20

root.geometry(f'{width * size}x{height * size + 93}')
root.title('Conway\'s Game of Life - by Jarno Romijn')

app = Application(master = root, size = 15, fillRandom = False)

grid = Grid(height, width)
app.setGrid(grid, size = size)

app.mainloop()