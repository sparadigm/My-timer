import tkinter as tk
from tkinter import ttk

class MyTimer(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding = (20, 10))
        # INFO: super() 
        # INFO: main.pyでapp = MyTimer(master = root)としているので
        # （rootはトップレベルウィンドウ）MyTimerというFrameがrootを親として作成される
        self.master = master

        self.pack(fill = "both")

        self.timer_running = False # False: 止まっている, True: 起動中
        self.time_left = 25 * 60
        self.timer_id = None # after関数の返り値（文字列、予約を識別するためのID）を格納。予約のキャンセルのために使用

        self.create_widgets()
        self.update_timer_display()

    def create_widgets(self):
        self.timer_label = ttk.Label(
            self, 
            text = "", 
            font = ("", 60))
        self.timer_label.pack(pady = 10)

        button_frame = ttk.Frame(
            self, 
            padding = (0, 10))
        button_frame.pack(fill = 'x')

        self.start_pause_button = ttk.Button(
            button_frame,
            text = "start",
            command = self.start_pause
        )
        self.start_pause_button.pack(side = "left", fill = "x", expand = True, padx = 5)

        self.reset_button = ttk.Button(
            button_frame,
            text = "reset",
            command = self.reset_timer
        )
        self.reset_button.pack(side = "left", fill = "x", expand = True, padx = 5)

    def update_timer_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text = f"{minutes:02}:{seconds:02}")
        # INFO: configメソッド -> 実行したウィジェットの設定を変更 （config = configure）
        # INFO: f-strings 0埋め ex){minutes:02} -> 表示する桁数を2桁（右）、0で残りを埋める（左）

    def start_pause(self):
        print("タイマー開始")
        # TODO: ボタンの状態変更、カウントダウンの開始
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.start_pause_button.config(text = "start")
        else:
            self.timer_running = True
            self.start_pause_button.config(text = "pause")
            self.countdown()

    def reset_timer(self):
        # TODO: ボタンの状態変更、リセット、表示の更新
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        self.time_left = 25 * 60
        self.update_timer_display()
        self.start_pause_button.config(text = "start")
        print("タイマーリセット")

    def countdown(self):
        # TODO: 1秒減らす、表示更新
        self.time_left -= 1
        if self.time_left > 0:
            self.update_timer_display()
            self.timer_id = self.after(1000, self.countdown)
        else:
            self.update_timer_display()