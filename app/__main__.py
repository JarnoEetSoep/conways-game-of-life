import tkinter as tk
from Application import Application

root = tk.Tk()

root.resizable(0, 0)

width = 8       # 40
height = 5      # 25
size = 110      # 20

root.title('Conway\'s Game of Life')

app = Application(master = root, width = width, height = height, size = size, fillRandom = False)

app.mainloop()