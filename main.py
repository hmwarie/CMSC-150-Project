from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from app import App

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    root.title("CMSC 150 Project")
    root.geometry("1080x720")
    app = App(root)
    root.mainloop()
