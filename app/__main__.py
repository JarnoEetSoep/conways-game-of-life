import tkinter as tk
import argparse
import json
import sys
import os

from Application import Application

parser = argparse.ArgumentParser(description='Start Conway\'s Game of Life')
parser.add_argument('-f', '--file', help = 'The .cgol file you want to use')
args = parser.parse_args()

cgol_path = None

if args.file:
    try:
        cgol_path = os.path.realpath(os.path.normpath(args.file))

        if not cgol_path.endswith('.cgol'):
            print('File must be a .cgol file')
            sys.exit()

        with open(cgol_path, 'r', encoding = 'UTF-8') as cgol_file:
            json.loads(cgol_file.read())
            cgol_file.close()

    except OSError:
        print('Wrong file path')
        sys.exit()
    except json.decoder.JSONDecodeError:
        print(f'"{cgol_path}" is not a valid .cgol file')
        sys.exit()

try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'r', encoding = 'UTF-8') as settings:
        s = json.loads(settings)
        s['alive-color']
        s['dead-color']
        s['rule']
        s.close()
except:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'w', encoding = 'UTF-8') as settings:
        s = {
            'alive-color': '#000000',
            'dead-color': '#ffffff',
            'rule': 'b3s23'
        }

        settings.write(json.dumps(s, indent = 4))
        settings.close()

root = tk.Tk()

root.resizable(1, 1)
root.attributes("-fullscreen", True)
root.minsize(850, 200)
root.geometry('950x700+50+50')

width = 40
height = 25

root.title('Conway\'s Game of Life')

app = Application(master = root, width = width, height = height, filepath = cgol_path)

app.mainloop()