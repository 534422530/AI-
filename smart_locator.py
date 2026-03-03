"""
老四精准定位系统 V2 - 点击追踪定位
用户点击画中画中的位置 → 自动在真实窗口同样位置点击
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import numpy as np
from PIL import Image, ImageTk
import pyautogui
import os

class SmartLocator:
    """智能定位器 - 画中画+点击追踪"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("老四 - 精准定位 (点击画中画=点击屏幕)")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # 顶部提示
        tip = tk.Label(self.root, text="👆 在下面图像中点击想要点击的位置 = 会在真实屏幕同样位置点击",
                      bg='#1a1a1a', fg='#ff6b6b', font=('Microsoft YaHei', 11))
        tip.pack(pady=5)
        
        # 画布
        self.canvas = tk.Canvas(self.root, bg='#2d2d2d', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 状态
        self.status = tk.Label(self.root, text="等待捕获屏幕...",
                             bg='#1a1a1a', fg='#00ff00', font=('Consolas', 10))
        self.status.pack(side=tk.BOTTOM, pady=5)
        
        # 坐标显示
        self.coord_label = tk.Label(self.root, text="鼠标: - , -",
                                   bg='#1a1a1a', fg='#888', font=('Consolas', 10))
        self.coord_label.pack(side=tk.BOTTOM)
        
        # 图像
        self.tk_image = None
        self.ori_w, self.ori_h = 0, 0
        self.zoom = 1.0
        self.disp_w, self.disp_h = 0, 0
        
        # 事件
        self.canvas.bind('<Motion>', self.on_move)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-3>', self.on_right_click)  # 右键刷新
        
        self.root.withdraw()
        
        # 上次点击时间
        self.last_click_time = 0
    
    def on_move(self, event):
        """鼠标移动"""
        # 显示显示坐标
        x = int(event.x / self.zoom)
        y = int(event.y / self.zoom)
        self.coord_label.config(text=f"显示坐标: {event.x},{event.y} → 真实坐标: {x},{y}")
    
    def on_click(self, event):
        """点击画中画 = 点击真实屏幕"""
        # 防止双击
        now = time.time()
        if now - self.last_click_time < 0.3:
            return
        self.last_click_time = now
        
        # 转换坐标
        x = int(event.x / self.zoom)
        y = int(event.y / self.zoom)
        
        self.status.config(text=f"✅ 已点击真实坐标: {x}, {y}", fg='#00ff00')
        self.root.update()
        
        # 在真实屏幕位置点击
        pyautogui.click(x, y)
        print(f"点击: {x}, {y}")
    
    def on_right_click(self, event):
        """右键刷新"""
        self.status.config(text="🔄 刷新屏幕...", fg='#ffaa00')
        self.root.update()
        return "break"
    
    def show(self):
        """显示"""
        self.root.deiconify()
    
    def hide(self):
        """隐藏"""
        self.root.withdraw()
    
    def update(self, image=None):
        """更新显示"""
        if image is None:
            # 捕获整个屏幕
            image = pyautogui.screenshot()
        
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        self.ori_w, self.ori_h = image.size
        
        # 计算缩放（适应窗口）- 延迟获取确保窗口已创建
        try:
            win_w = self.canvas.winfo_width() or 860
            win_h = self.canvas.winfo_height() or 600
        except:
            win_w, win_h = 860, 600
        
        if win_w <= 1 or win_h <= 1:
            win_w, win_h = 860, 600
        
        scale_w = win_w / self.ori_w
        scale_h = win_h / self.ori_h
        self.zoom = min(scale_w, scale_h) * 0.95
        
        new_w = int(self.ori_w * self.zoom)
        new_h = int(self.ori_h * self.zoom)
        
        img_resized = image.resize((new_w, new_h), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img_resized)
        
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        self.disp_w, self.disp_h = new_w, new_h
    
    def set_status(self, text, color='#00ff00'):
        self.status.config(text=text, fg=color)


# 全局
locator = SmartLocator()

def open_locator():
    """打开定位器"""
    locator.show()

def close_locator():
    """关闭定位器"""
    locator.hide()

def refresh_screen():
    """刷新屏幕显示"""
    locator.update()
    locator.set_status("✅ 屏幕已刷新", '#00ff00')

def click_at(x, y):
    """点击指定坐标"""
    pyautogui.click(x, y)

def get_screen_size():
    """获取屏幕尺寸"""
    return pyautogui.size()


if __name__ == "__main__":
    print("智能定位器 - 精准点击系统")
    locator.show()
    locator.update()
    locator.root.mainloop()
