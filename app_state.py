from pathlib import Path
import json

STATE_FILE = (Path(__file__).resolve().parent / ".mytimer_state.json")
#INFO: __file__ -> 実行中のこのファイル自身のパスを表す

def load_state(root, app):
    try:
        obj = json.loads(STATE_FILE.read_text(encoding = "utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        # INFO: JSONDecodeError -> 文字列やファイルがjsonフォーマットであるか
        # INFO: FileNotFoundError -> ファイルやディレクトリが存在しない場合に送出
        return
    
    geo = obj.get("geometry") # KeyErrorを回避

    if geo != "":
        root.update_idletasks()
        root.after(0, lambda g = geo: root.geometry(g))

    if "topmost" in obj:
        app.var_isfront.set(bool(obj["topmost"]))
        root.after(0, app.apply_front)
        # INFO: レイアウト確定後、ウィンドウが画面に出るタイミングでgeometry
    
    if "work_minutes" in obj:
        app.var_scaleminute.set(int(obj["work_minutes"]))
    if "break_minutes" in obj:
        app.var_breakminute.set(int(obj["break_minutes"]))
        # INFO: hasattr -> 第一引数: オブジェクト 第二引数: 属性名
        # 指定された属性がオブジェクトに存在するかboolで返す
    if "muted" in obj:
        app.var_ismuted.set(bool(obj["muted"]))

def save_state(root, app):
    if root.state() == 'iconic':
        # INFO: state()をトップレベルウィンドウに呼ぶと、ウィンドウの現在の状態を表す文字列を返す
        # "normal": 通常表示, "iconic": 最小化, "withdrawn": 非表示, "zoomed": 最大化
        # 最小化中にgeometryを保存すると、値がおかしくなることがある
        return
    data = {"geometry": root.geometry(),
            "topmost": bool(root.attributes("-topmost")),
            "work_minutes": int(app.var_scaleminute.get()),
            "break_minutes": int(app.var_breakminute.get()),
            "muted": bool(app.var_ismuted.get())
            }
    STATE_FILE.write_text(json.dumps(data, ensure_ascii = False, indent = 2), encoding = "utf-8")
    # INFO: json.dumps -> dataをJSON文字列にシリアライズ
    # endure_ascii = False -> 日本語などの非ASCII文字をそのまま書く