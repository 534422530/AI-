"""
老四精准定位系统 V3 - 网格坐标显示
在截图上显示精确的坐标网格，方便定位点击
"""

import tkinter as tk
from tkinter import ttk
import time
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pyautogui
import os

class GridLocator:
    """网格坐标定位器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("老四 - 精准定位系统 (1920x1080)")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0d0d0d')
        
        # 顶部信息栏
        info_frame = tk.Frame(self.root, bg='#1a1a1a', height=40)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        info_frame.pack_propagate(False)
        
        self.info_label = tk.Label(info_frame, text="📍 鼠标位置: - , -   |   点击位置: - , -   |   F5刷新   |   右键复制坐标",
                                  bg='#1a1a1a', fg='#00ff88', font=('Consolas', 10))
        self.info_label.pack(side=tk.LEFT, padx=10)
        
        # 画布
        self.canvas = tk.Canvas(self.root, bg='#1a1a1a', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 图像
        self.tk_image = None
        self.zoom = 0.5  # 默认缩放
        self.image = None
        
        # 坐标
        self.mouse_pos = [0, 0]
        self.click_pos = [0, 0]
        
        # 事件绑定
        self.canvas.bind('<Motion>', self.on_move)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        
        self.root.withdraw()
    
    def on_move(self, event):
        """鼠标移动显示坐标"""
        # 显示坐标（考虑缩放）
        x = int(event.x / self.zoom)
        y = int(event.y / self.zoom)
        
        self.mouse_pos = [x, y]
        self.info_label.config(
            text=f"📍 鼠标位置: {x} , {y}   |   点击位置: {self.click_pos[0]} , {self.click_pos[1]}   |   F5刷新   |   右键复制"
        )
        
        # 绘制十字线
        self.draw_crosshair(event.x, event.y)
    
    def draw_crosshair(self, x, y):
        """绘制十字线"""
        # 清除之前的十字线
        self.canvas.delete('cross')
        
        # 绘制新的十字线
        self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), 
                                fill='#ff4444', dash=(2,2), tags='cross')
        self.canvas.create_line(0, y, self.canvas.winfo_width(), y, 
                                fill='#ff4444', dash=(2,2), tags='cross')
        
        # 坐标标签
        self.canvas.delete('coord')
        real_x = int(x / self.zoom)
        real_y = int(y / self.zoom)
        self.canvas.create_text(x+10, y-15, text=f"({real_x}, {real_y})", 
                               fill='#ffff00', font=('Consolas', 9), tags='coord')
    
    def on_click(self, event):
        """点击设置位置"""
        x = int(event.x / self.zoom)
        y = int(event.y / self.zoom)
        
        self.click_pos = [x, y]
        self.info_label.config(
            text=f"📍 鼠标位置: {self.mouse_pos[0]} , {self.mouse_pos[1]}   |   ✅ 点击位置: {x} , {y}"
        )
        
        # 在点击位置画个圈
        cx = event.x
        cy = event.y
        self.canvas.create_oval(cx-15, cy-15, cx+15, cy+15, 
                               outline='#00ff88', width=3, tags='click')
        self.canvas.create_text(cx, cy-25, text=f"点击: {x},{y}", 
                               fill='#00ff88', font=('Consolas', 10, 'bold'), tags='click')
        
        # 实际点击屏幕
        pyautogui.click(x, y)
    
    def on_right_click(self, event):
        """右键复制坐标"""
        import pyperclip
        x = int(event.x / self.zoom)
        y = int(event.y / self.zoom)
        pyperclip.copy(f"{x}, {y}")
        self.info_label.config(text=f"📍 已复制坐标: {x}, {y}")
        return "break"
    
    def show(self):
        """显示"""
        self.root.deiconify()
    
    def hide(self):
        """隐藏"""
        self.root.withdraw()
    
    def update(self, image=None, zoom=None):
        """更新显示"""
        if image is None:
            image = pyautogui.screenshot()
        
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        if zoom is not None:
            self.zoom = zoom
        
        self.image = image
        w, h = image.size
        
        # 显示尺寸
        new_w = int(w * self.zoom)
        new_h = int(h * self.zoom)
        
        img_resized = image.resize((new_w, new_h), Image.LANCZOS)
        
        # 添加网格
        draw = ImageDraw.Draw(img_resized)
        
        # 画网格线 (每100像素)
        grid_color = (50, 50, 50)
        for i in range(0, new_w, int(100 * self.zoom)):
            draw.line([(i, 0), (i, new_h)], fill=grid_color, width=1)
        for i in range(0, new_h, int(100 * self.zoom)):
            draw.line([(0, i), (new_w, i)], fill=grid_color, width=1)
        
        # 画坐标标签
        try:
            font = ImageFont.truetype("msyh.ttc", 10)
        except:
            font = ImageFont.load_default()
        
        for i in range(0, new_w, int(200 * self.zoom)):
            x_val = int(i / self.zoom)
            draw.text((i+2, 2), str(x_val), fill='#888888', font=font)
        for i in range(0, new_h, int(200 * self.zoom)):
            y_val = int(i / self.zoom)
            draw.text((2, i+2), str(y_val), fill='#888888', font=font)
        
        self.tk_image = ImageTk.PhotoImage(img_resized)
        
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        self.root.title(f"老四 - 精准定位系统 ({w}x{h}) - 缩放:{self.zoom}")
    
    def set_status(self, text):
        self.info_label.config(text=text)


# 全局实例
grid_locator = GridLocator()

def open_grid():
    """打开网格定位器"""
    grid_locator.show()

def close_grid():
    """关闭网格定位器"""
    grid_locator.hide()

def refresh_grid(zoom=0.5):
    """刷新并显示网格"""
    grid_locator.update(zoom=zoom)
    grid_locator.set_status("✅ 屏幕已刷新 - 点击图像定位")

def click_at(x, y):
    """点击指定坐标"""
    pyautogui.click(x, y)

def get_pos():
    """获取当前鼠标位置"""
    return pyautogui.position()


if __name__ == "__main__":
    print("网格坐标定位器")
    grid_locator.show()
    grid_locator.update(zoom=0.5)
    grid_locator.root.mainloop()
