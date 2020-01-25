import tkinter as tk
from Application import Application
import sys

root = tk.Tk()

root.resizable(1, 1)
root.attributes("-fullscreen", True)
root.minsize(850, 200)
root.geometry('950x700+50+50')

width = 40
height = 25
size = 30

root.title('Conway\'s Game of Life')

app = Application(master = root, width = width, height = height, size = size)

app.mainloop()