import tkinter as tk
import random
import time
import math
import sys

# ---------------------- 可自定义部分 ----------------------
tips = [
    "多喝热水", "早点休息", "记得吃饭", "保持好心情",
    "高新就业", "顺顺利利", "别熬夜", "快快乐乐",
    "你很棒", "照顾好自己", "晚安好梦", 
]

# 满屏暴击时优先显示的文案列表（会高频出现）
vote_tips = ["为我们投票"] * 20 + tips  # "为我们投票"占比更高

colors = [
    "pink", "lightblue", "lightgreen", "lemonchiffon",
    "hotpink", "skyblue"
]

# 弹窗大小（像素）
POPUP_W = 120
POPUP_H = 40
# 爱心采样点数量
HEART_N = 100
# 爱心绽放间隔（秒）
HEART_INTERVAL = 0.03
# 满屏暴击数量（可按需调大/调小）
FULL_SCREEN_COUNT_BASE = 50
# 满屏暴击每两个弹窗的间隔
FULL_SCREEN_INTERVAL = 0.005
# 满屏暴击展示时长（秒）
FULL_SCREEN_SHOW_SEC = 5
# --------------------------------------------------------

def heart_points(n: int, screen_w: int, screen_h: int):
    """在屏幕上生成心形曲线的 n 个点（左上角坐标）"""
    points = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t)
             - 5 * math.cos(2 * t)
             - 2 * math.cos(3 * t)
             - math.cos(4 * t))
        # 缩放并平移到屏幕中央（可自行调整倍数和偏移）
        sx = int(screen_w / 2 + x * 20 - POPUP_W / 2)
        sy = int(screen_h / 2 - y * 20 - POPUP_H / 2)
        # 保证窗口不会超出屏幕
        sx = max(0, min(sx, screen_w - POPUP_W))
        sy = max(0, min(sy, screen_h - POPUP_H))
        points.append((sx, sy))
    return points


def create_popup(root, x, y, tip=None, use_vote_mode=False):
    """创建一个置顶小弹窗，返回窗口对象"""
    win = tk.Toplevel(root)
    win.geometry(f"{POPUP_W}x{POPUP_H}+{x}+{y}")
    win.title("提示")
    win.attributes('-topmost', 1)          # 始终置顶
    if use_vote_mode:
        text = random.choice(vote_tips)  # 使用投票模式，高频显示"为我们投票"
    else:
        text = tip or random.choice(tips)
    bg = random.choice(colors)
    tk.Label(
        win,
        text=text,
        bg=bg,
        font=("微软雅黑", 14),
        width=20,
        height=3
    ).pack()

    # 绑定空格键：随时退出
    win.bind('<space>', lambda e: sys.exit(0))
    return win


def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口，只用 Toplevel 弹窗

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    hearts = []   # 存放“爱心形状”的弹窗
    all_wins = [] # 存放“满屏暴击”的弹窗

    # ------ 阶段 1：爱心绽放 ------
    pts = heart_points(HEART_N, sw, sh)
    for i, (x, y) in enumerate(pts):
        # 最后一个点可以放特殊文案（示例：不传则随机选）
        tip = "选我们" if i == len(pts) - 1 else None
        win = create_popup(root, x, y, tip=tip)
        hearts.append(win)
        root.update()
        time.sleep(HEART_INTERVAL)

    # 短暂展示爱心
    time.sleep(1)
    # 清除爱心窗口
    for w in hearts:
        try:
            if w.winfo_exists():
                w.destroy()
        except Exception:
            pass

    # ------ 阶段 2：满屏暴击 ------
    count = sw // POPUP_W * sh // POPUP_H + FULL_SCREEN_COUNT_BASE
    for _ in range(count):
        x = random.randint(0, sw - POPUP_W)
        y = random.randint(0, sh - POPUP_H)
        win = create_popup(root, x, y, use_vote_mode=True)  # 启用投票模式
        all_wins.append(win)
        root.update()
        time.sleep(FULL_SCREEN_INTERVAL)

    # 展示一段时间
    time.sleep(FULL_SCREEN_SHOW_SEC)

    # ------ 阶段 3：优雅关闭 ------
    # 把总时间（比如 1 秒）均匀分给所有窗口
    interval = 1.0 / max(len(all_wins), 1)
    for w in all_wins:
        try:
            if w.winfo_exists():
                w.destroy()
        except Exception:
            pass
        root.update()
        time.sleep(interval)

    root.mainloop()


if __name__ == "__main__":
    main()
