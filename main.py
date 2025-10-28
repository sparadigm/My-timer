import tkinter as tk
from tkinter import ttk

from My_timer import MyTimer

def main():
    root = tk.Tk()

    root.title("MyTimer")
    root.geometry("450x350")
    #root.resizable(False, False)
    style = ttk.Style()
    style.theme_use('clam')
    app = MyTimer(master = root)

    root.mainloop()

if __name__ == "__main__":
    main()