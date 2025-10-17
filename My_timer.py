import tkinter as tk
from tkinter import ttk

class MyTimer(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding = (20, 10))
        self.master = master

        self.pack(fill = "both")

        self.timer_running = False
        self.time_left = 25 * 60
        self.timer_id = None

        self.create_widgets()
        self.update_timer_display()

    def create_widgets(self):
        self.timer_Label = ttk.Label(self, text = "", font = ("", 60))
        self.timer_Label.pack(pady = 10)

        button_frame = ttk.Frame(self, padding = (0, 10))
        button_frame.pack(fill = 'x')

        