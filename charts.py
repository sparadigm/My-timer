import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_daily_minutes(parent, rows, title):
    rows = list(rows)
    days = [d for d, _ in rows]
    mins = [m for _, m in rows]

    top = tk.Toplevel(parent) 
    #INFO: Toplevel
    # メインウィンドウに紐づくサブウィンドウを作成
    top.title("Daily Work Time")
    top.geometry("700x380")

    fig = Figure(figsize = (6.8, 3.2), dpi = 100)
    ax = fig.add_subplot(111)
    ax.bar(days, mins)
    #INFO: bar
    #棒グラフの出力
    ax.set_ylabel("minutes")
    ax.set_title(title)
    ax.tick_params(axis = 'x', labelrotation = 45)
    #INFO: tick_params
    #目盛りの詳細設定を行う labelrotation -> 目盛ラベルの回転角度
    fig.tight_layout()
    #INFO: tight_layout
    # サブプロットが図の領域に収まるようにサブプロットパラメータを自動的に調整

    canvas = FigureCanvasTkAgg(fig, master = top)
    #INFO: FigureCanvasTkAgg
    # Matplotlibを使って作成したグラフをTkinter内で表示するために利用するもの
    canvas.get_tk_widget().pack(fill = "both", expand = True)
    canvas.draw()

    top.bind("<Escape>", lambda e: top.destroy())
    return top
    #NOTE: 
    # topつまりToplevelを返すので、たとえばMytimer.pyで呼び出す際に変数に格納した時、Mytimer側で操作が可能になる