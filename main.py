import tkinter as tk
from tkinter import ttk

from My_timer import MyTimer

def main():
    root = tk.Tk()

    root.title("集中用タイマー")
    root.geometry("350x250")
    root.resizable(False, False)
    style = ttk.Style()
    style.theme_use('clam')
    app = MyTimer(master = root)

    root.mainloop()

if __name__ == "__main__":
    main()