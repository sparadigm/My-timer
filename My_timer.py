import tkinter as tk
from tkinter import ttk
import time
from db import insert_session

class MyTimer(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding = (20, 10))
        #INFO: super() 
        #INFO: main.pyでapp = MyTimer(master = root)としているので
        # （rootはトップレベルウィンドウ）MyTimerというFrameがrootを親として作成される
        self.master = master
        self.pack(fill = "both", expand = True)

        self.current_mode = "work" # 作業時: work, 休憩時: break

        self.timer_running = False # False: 停止, True: 動作中
        self.timer_id = None # after関数の返り値（文字列、予約を識別するためのID）を格納。予約のキャンセルのために使用

        self.var_scaleminute = tk.IntVar(value = 25) # 時間設定を変更する際に使うウィジェット変数（分）
        self.var_breakminute = tk.IntVar(value = 5) # 休憩時間（分）
        self.var_scaleminute.trace_add("write", self.scale_change) # 変数の値が変更されたとき、自動でscale_change

        self.var_ismuted = tk.BooleanVar(value = False) # ミュート用
        self.var_isfront = tk.BooleanVar(value = False) # 前面表示用
        self.apply_front()

        self.time_left = self.var_scaleminute.get() * 60 # 作業時間（秒）

        self.session_start = None # 記録用の開始時間
        self.session_mode = None

        self.style = ttk.Style()
        self.style.configure(
            "inorde.TButton",
            font = ("", 12, "bold"),
            padding = [-32, -2]
        )
        self.style.configure(
            "vlmbar.Horizontal.TScale",
        )
        self.style.configure(
            "Status.TLabel",
            font = ("", 25, "bold")
        )
        self.create_widgets()
        self.update_timer_display()

    def create_widgets(self):
        self.center_frame = ttk.Frame(self) # ウィジェットを中央に配置するためのframe
        self.center_frame.pack(expand = True)

        self.status_label = ttk.Label( # 作業中 - 休憩中を表示するlabel
            self.center_frame,
            text = "work",
            style = "Status.TLabel"
        )
        self.status_label.pack(pady = (0, 12)) # pady = (上, 下)

        self.timer_label = ttk.Label( # 残り時間表示
            self.center_frame, 
            text = "", 
            font = ("", 60))
        self.timer_label.pack()

        button_frame = ttk.Frame(
            self.center_frame, 
            padding = (0, 10)
        )
        button_frame.pack()

        time_setting = ttk.Frame( # 時間設定用をtime_settingにまとめる
            self.center_frame,
            padding = (0, 10)
        )
        time_setting.pack()

        self.time_decrease = ttk.Button(
            time_setting,
            text = '-',
            style = "inorde.TButton", # ttkではheight, widthを持てないので、styleで指定
            command = self.decrement_time
        )
        self.time_decrease.pack(side = "left")

        self.time_scale = ttk.Scale(
            time_setting,
            orient = tk.HORIZONTAL,
            from_ = 1,
            to = 60,
            style = "vlmbar.Horizontal.TScale",
            length = 150,
            variable = self.var_scaleminute
        )
        self.time_scale.pack(side = "left", padx = 10)

        self.time_increase = ttk.Button(
            time_setting,
            text = "+",
            style = "inorde.TButton",
            command = self.increment_time
        )
        self.time_increase.pack(side = "left")

        self.start_pause_button = ttk.Button(
            button_frame,
            text = "start",
            command = self.start_pause
        )
        self.start_pause_button.pack(side = "left", fill = "x", padx = 5)

        self.reset_button = ttk.Button(
            button_frame,
            text = "reset",
            command = self.reset_timer
        )
        self.reset_button.pack(side = "left", fill = "x", expand = True, padx = 5)

        self.mute_button = ttk.Checkbutton(
            button_frame,
            text = "Mute",
            variable = self.var_ismuted
        )
        self.mute_button.pack()

        self.front_button = ttk.Checkbutton(
            button_frame,
            text = "Front",
            variable = self.var_isfront,
            command = self.apply_front
        )
        self.front_button.pack()

        self.chart_button = ttk.Button(
            button_frame,
            text = "graph",
            command = self.on_show_chart
        )
        self.chart_button.pack(side = "left", padx = 5)

    def apply_front(self):
        self.master.attributes("-topmost", bool(self.var_isfront.get()))

    def change_status(self):
        if self.current_mode == "break":
            self.current_mode = "work"
            self.status_label.config(text = "work")
        else:
            self.current_mode = "break"
            self.status_label.config(text = "break")
        self.status_label.config(text = self.current_mode)

    def update_timer_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text = f"{minutes:02}:{seconds:02}")
        # INFO: configメソッド -> 実行したウィジェットの設定を変更 （config = configure）
        # INFO: f-strings 0埋め ex){minutes:02} -> 表示する桁数を2桁（右）、0で残りを埋める（左）

    def scale_change(self, *args):
        if not self.timer_running:
            try:
                self.time_left = self.var_scaleminute.get() * 60
                self.update_timer_display()
            except tk.TclError:
                pass

    def increment_time(self):
        current_time = self.var_scaleminute.get()
        if current_time < 60:
            self.var_scaleminute.set(current_time + 1)
            print("時間が1分増えました")
        else:
            print("これ以上増やせません")
            #TODO: 警告するポップアップを作成

    def decrement_time(self):
        current_time = self.var_scaleminute.get()
        if current_time > 1:
            self.var_scaleminute.set(current_time - 1)
            print("時間が1分減りました")
        else:
            print("これ以上減らせません")
            #TODO: 警告するポップアップを作成

    def start_pause(self):
        print("タイマー開始")
        # TODO: ボタンの状態変更
        if self.timer_running:
            self.log_session()
            self.timer_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.start_pause_button.config(text = "start")
        else:
            self.timer_running = True
            self.start_pause_button.config(text = "pause")
            if self.current_mode == "work":
                self.session_start = time.time()
                self.session_mode = "work"
            self.countdown()

    def reset_timer(self):
        # TODO: ボタンの状態変更、リセット、表示の更新
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        self.time_left = self.var_scaleminute.get() * 60
        self.update_timer_display()
        self.start_pause_button.config(text = "start")
        self.current_mode = "work" # リセットされたら強制的にworkモード
        self.status_label.config(text = self.current_mode)
        
        self.log_session()
        self.session_start = None
        self.session_mode = None
        print("タイマーリセット")

    def countdown(self):
        if not self.timer_running:
            return
        # NOTE: 停止ボタンを押した時点で-1されるのを防止
        if self.var_ismuted.get() != True and 1 <= self.time_left <= 3:
            try:
                self.bell()
            except Exception:
                pass

        if self.time_left <= 0:
            self.finish_phase()
            return
        self.update_timer_display()
        self.time_left -= 1
        self.timer_id = self.after(1000, self.countdown)

    def finish_phase(self):
        self.log_session()
        self.change_status()
        if self.current_mode == "work":
            self.time_left = self.var_scaleminute.get() * 60
        else:
            self.time_left = self.var_breakminute.get() * 60
        self.update_timer_display()
        self.timer_id = None
        self.timer_running = False
        self.start_pause()

    def log_session(self):
        if self.session_start is not None and self.session_mode == "work":
            end_ts = time.time()
            insert_session(self.session_start, end_ts, "work")
        self.session_start = None
        self.session_mode = None

    def on_show_chart(self, days = 14):
        from charts import show_daily_minutes
        from db import get_conn
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT date(datetime(start_ts, "unixepoch", "localtime")) AS day,
                               SUM(end_ts - start_ts) / 60.0 AS minutes
                FROM session
                WHERE mode = "work"
                GROUP BY day
                ORDER BY day DESC
                LIMIT ?
                """, (days,))
            rows = cur.fetchall()
        
        rows.reverse()
        show_daily_minutes(self.master, rows, title = f"work per day (last {days})")