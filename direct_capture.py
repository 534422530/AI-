"""
老四直接显存读取模块 - Laosi Direct Capture
功能：直接从显存读取像素数据，比截图更快
作者：老四AI助手
"""

import ctypes
from ctypes import wintypes
import numpy as np
import time

# Windows API 常量定义
HWND_DESKTOP = 0        # 桌面窗口句柄
SRCCOPY = 0x00CC0020    # BitBlt复制模式

# 加载Windows系统库
user32 = ctypes.windll.user32  # 用户界面库
gdi32 = ctypes.windll.gdi32    # 图形设备接口库


def get_screen_data():
    """
    直接从显存读取屏幕数据
    原理：使用Windows GDI的BitBlt函数直接复制显存
    返回：(像素数组, 宽度, 高度)
    
    优点：
        - 比PIL/mss更快
        - 直接获取原始像素数据
        - 无需中间文件
    
    缺点：
        - 仅支持Windows
        - 需要了解Windows GDI
    """
    # 获取屏幕尺寸
    width = user32.GetSystemMetrics(0)   # 屏幕宽度
    height = user32.GetSystemMetrics(1)  # 屏幕高度
    
    # 获取桌面窗口的设备上下文（DC）
    hwnd_dc = user32.GetWindowDC(HWND_DESKTOP)
    
    # 创建兼容的内存DC
    mem_dc = gdi32.CreateCompatibleDC(hwnd_dc)
    
    # 创建兼容的位图
    bitmap = gdi32.CreateCompatibleBitmap(hwnd_dc, width, height)
    
    # 选择位图到内存DC
    old_bitmap = gdi32.SelectObject(mem_dc, bitmap)
    
    # 复制屏幕内容到内存DC（核心操作）
    gdi32.BitBlt(mem_dc, 0, 0, width, height, hwnd_dc, 0, 0, SRCCOPY)
    
    # 准备位图信息头
    bmi = np.zeros((1, 1), dtype=[
        ('biSize', np.uint32),           # 结构体大小
        ('biWidth', np.int32),           # 宽度
        ('biHeight', np.int32),          # 高度（负数表示从上到下）
        ('biPlanes', np.uint16),         # 颜色平面数（必须为1）
        ('biBitCount', np.uint16),       # 每像素位数（24位RGB）
        ('biCompression', np.uint32),    # 压缩方式（0=不压缩）
        ('biSizeImage', np.uint32),      # 图像数据大小
        ('biXPelsPerMeter', np.int32),   # 水平分辨率
        ('biYPelsPerMeter', np.int32),   # 垂直分辨率
        ('biClrUsed', np.uint32),        # 使用的颜色数
        ('biClrImportant', np.uint32)    # 重要颜色数
    ])
    
    # 填充位图信息
    bmi['biSize'] = 40
    bmi['biWidth'] = width
    bmi['biHeight'] = -height          # 负数表示从上到下扫描
    bmi['biPlanes'] = 1
    bmi['biBitCount'] = 24             # 24位真彩色
    bmi['biCompression'] = 0
    
    # 计算每行字节数（需要4字节对齐）
    row_size = ((width * 3 + 3) // 4) * 4
    buf_size = row_size * height
    
    # 创建缓冲区接收数据
    buf = np.zeros(buf_size, dtype=np.uint8)
    
    # 从位图读取像素数据
    gdi32.GetDIBits(hwnd_dc, bitmap, 0, height, buf.ctypes, bmi.ctypes, 0)
    
    # 释放资源（重要！避免内存泄漏）
    gdi32.SelectObject(mem_dc, old_bitmap)
    gdi32.DeleteObject(bitmap)
    gdi32.DeleteDC(mem_dc)
    user32.ReleaseDC(HWND_DESKTOP, hwnd_dc)
    
    # 转换为RGB数组
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            idx = y * row_size + x * 3
            # BGR转RGB
            pixels[y, x] = [buf[idx+2], buf[idx+1], buf[idx]]
    
    return pixels, width, height


def get_pixel_hash(pixels):
    """
    计算像素数组的哈希值
    参数：
        pixels: numpy像素数组
    返回：哈希值（用于快速判断是否变化）
    """
    return hash(pixels.tobytes())


def monitor_changes(interval=1, callback=None):
    """
    持续监控屏幕变化
    参数：
        interval: 检测间隔（秒）
        callback: 变化回调函数，参数为(diff_ratio, pixels)
    """
    last_hash = None
    last_pixels = None
    
    while True:
        # 获取当前屏幕
        pixels, w, h = get_screen_data()
        current_hash = get_pixel_hash(pixels)
        
        # 检查变化
        if last_hash is None or current_hash != last_hash:
            if last_pixels is not None:
                # 计算差异比例
                diff = np.sum(pixels != last_pixels) / pixels.size
                
                # 调用回调
                if callback:
                    callback(diff, pixels)
                
                print(f"[{time.strftime('%H:%M:%S')}] 变化: {diff:.2%}")
            
            last_pixels = pixels.copy()
        
        last_hash = current_hash
        time.sleep(interval)


if __name__ == "__main__":
    """
    测试直接读取显存
    """
    print("读取显存数据...")
    pixels, w, h = get_screen_data()
    print(f"分辨率: {w}x{h}")
    print(f"数据大小: {pixels.nbytes/1024/1024:.1f}MB")
    print(f"像素哈希: {get_pixel_hash(pixels)}")
