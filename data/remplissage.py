import tkinter as tk
from tkinter import simpledialog
import time
import win32clipboard





def input_nom():
    return simpledialog.askstring(title="Input",prompt="Nom du dosssier/edt")

def input_parent():
    return simpledialog.askstring(title="Input",prompt="Nom du parent")


filename="edt.csv"
file=open(filename,"a")
ROOT = tk.Tk()
ROOT.withdraw()
win32clipboard.OpenClipboard()
nom_parent=input_parent()

while True:
    nom=input_nom()
    if nom=='exit' or nom=='EXIT' or nom==None or nom=="":
        break
    time.sleep(0.1)
    win32clipboard.OpenClipboard()
    old_clip = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    new_clip=old_clip

    while(new_clip==old_clip):
        win32clipboard.OpenClipboard()
        new_clip = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        time.sleep(0.1)
    
    file.write(nom+","+nom_parent+","+new_clip+'\n')

file.close()