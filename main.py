import tkinter as tk
from tkinter import ttk

from My_timer import MyTimer
from app_state import load_state, save_state

def main():
    root = tk.Tk()

    root.title("MyTimer")
    #root.resizable(False, False)
    style = ttk.Style()
    style.theme_use('clam')
    app = MyTimer(master = root)

    load_state(root, app)

    def on_close():
        save_state(root, app)
        root.destroy()
        #INFO: destroy -> ウィンドウやウィジェットの破棄
        # root.destroy()なら全ウィジェットが破棄され、mainloop()は終了

    root.protocol("WM_DELETE_WINDOW", on_close)
    #INFO: protocol("WM_DELETE_WINDOW") -> 閉じる要求を受けた時に何をするか登録する
    root.mainloop()

if __name__ == "__main__":
    main()