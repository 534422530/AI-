"""
老四精准定位系统 - 画中画窗口
在独立窗口中显示网页，实现精准元素定位
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import numpy as np
from PIL import Image, ImageTk
import pyautogui
import os

class PiPWindow:
    """画中画精准定位窗口"""
    
    def __init__(self, title="老四 - 精准定位"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # 画布显示图像
        self.canvas = tk.Canvas(self.root, bg='#2d2d2d', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 状态栏
        self.status_var = tk.StringVar(value="等待连接...")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               bg='#1a1a1a', fg='#00ff00', font=('Consolas', 10))
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # 鼠标位置
        self.mouse_pos = [0, 0]
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_click)
        self.click_callback = None
        
        # 图像
        self.image_id = None
        self.zoom = 1.0
        
        # 自动刷新
        self.auto_refresh = False
        self.refresh_interval = 0.5
        
        self.root.withdraw()
    
    def on_mouse_move(self, event):
        """鼠标移动"""
        self.mouse_pos = [event.x, event.y]
    
    def on_click(self, event):
        """点击"""
        if self.click_callback:
            # 转换坐标到原图
            x = int(event.x / self.zoom)
            y = int(event.y / self.zoom)
            self.click_callback(x, y)
    
    def show(self):
        """显示窗口"""
        self.root.deiconify()
    
    def hide(self):
        """隐藏窗口"""
        self.root.withdraw()
    
    def update_image(self, image, zoom=1.0):
        """更新显示的图像"""
        self.zoom = zoom
        
        if isinstance(image, np.ndarray):
            # 转换numpy数组到PIL
            image = Image.fromarray(image)
        
        if image:
            # 调整大小
            w, h = image.size
            new_w, new_h = int(w * zoom), int(h * zoom)
            image = image.resize((new_w, new_h), Image.LANCZOS)
            
            # 转为Tkinter图像
            self.tk_image = ImageTk.PhotoImage(image)
            
            # 显示
            self.canvas.delete('all')
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            # 显示网格
            for i in range(0, new_w, 50):
                self.canvas.create_line(i, 0, i, new_h, fill='#3d3d3d', dash=(2,2))
            for i in range(0, new_h, 50):
                self.canvas.create_line(0, i, new_w, i, fill='#3d3d3d', dash=(2,2))
    
    def set_status(self, text):
        """设置状态"""
        self.status_var.set(text)
    
    def run(self):
        """运行"""
        self.root.mainloop()


class PrecisionLocator:
    """精准定位器 - 整合画中画和屏幕识别"""
    
    def __init__(self):
        self.pip = PiPWindow()
        self.target_window = None
        self.region = None
    
    def find_window(self, name):
        """查找目标窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(name)
            if windows:
                self.target_window = windows[0]
                return True
            return False
        except:
            return False
    
    def capture_window(self):
        """截取窗口图像"""
        if not self.target_window:
            return None
        
        # 激活窗口
        try:
            self.target_window.activate()
        except:
            pass
        
        time.sleep(0.2)
        
        # 截取窗口区域
        import pyautogui
        left = self.target_window.left
        top = self.target_window.top
        width = self.target_window.width
        height = self.target_window.height
        
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        return np.array(screenshot), (left, top, width, height)
    
    def show_in_pip(self, image, zoom=1.0):
        """在画中画窗口显示"""
        self.pip.update_image(image, zoom)
        self.pip.show()
    
    def locate_element(self, image, target_text):
        """在图像中定位元素（通过颜色/特征匹配）"""
        # 这里可以用OpenCV模板匹配
        # 简化版本：返回中心点
        h, w = image.shape[:2]
        return w // 2, h // 2
    
    def click_relative(self, rel_x, rel_y):
        """相对目标窗口点击"""
        if self.target_window:
            x = self.target_window.left + rel_x
            y = self.target_window.top + rel_y
            pyautogui.click(x, y)
            return x, y
        return None, None


# 全局实例
locator = PrecisionLocator()


def open_pip():
    """打开画中画窗口"""
    locator.pip.show()

def close_pip():
    """关闭画中画窗口"""
    locator.pip.hide()

def capture_target_window(window_name):
    """捕获目标窗口并在画中画显示"""
    if locator.find_window(window_name):
        img, region = locator.capture_window()
        if img is not None:
            locator.show_in_pip(img, zoom=1.0)
            return img, region
    return None, None

def click_at(x, y):
    """在目标窗口指定位置点击"""
    return locator.click_relative(x, y)

def set_click_handler(callback):
    """设置点击回调"""
    locator.pip.click_callback = callback


if __name__ == "__main__":
    print("精准定位系统测试")
    print("用法:")
    print("  from pip_locator import open_pip, capture_target_window, click_at")
    print("  open_pip()  # 打开画中画窗口")
    print("  capture_target_window('Chrome')  # 捕获窗口")
