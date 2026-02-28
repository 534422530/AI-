"""
老四屏幕监控工具 - Laosi Screen Monitor
功能：截屏、OCR识别、动态监控、变化检测
作者：老四AI助手
"""

import os
import sys
import time
import threading
import base64
import requests
import json
from datetime import datetime

# 尝试导入mss库（跨平台截图），如果失败则使用PIL
try:
    from mss import mss
    HAS_MSS = True
except ImportError:
    from PIL import ImageGrab, Image
    HAS_MSS = False

import numpy as np

# 配置路径
MONITOR_DIR = os.path.join(os.path.dirname(__file__), "monitor_logs")
LAST_SCREEN = os.path.join(os.path.dirname(__file__), "current_screen.jpg")
LAST_TEXT = os.path.join(os.path.dirname(__file__), "current_text.txt")
CHANGE_LOG = os.path.join(os.path.dirname(__file__), "change_log.txt")

# 确保日志目录存在
os.makedirs(MONITOR_DIR, exist_ok=True)


class ScreenMonitor:
    """
    屏幕监控类
    功能：实时监控屏幕变化，OCR识别文字
    """
    
    def __init__(self, interval=5, threshold=0.05):
        """
        初始化监控器
        参数：
            interval: 检测间隔（秒）
            threshold: 变化阈值（0-1之间，超过此值认为有变化）
        """
        self.interval = interval          # 检测间隔
        self.threshold = threshold        # 变化阈值
        self.running = False              # 运行状态
        self.last_hash = None             # 上次截图哈希值
        self.callback = None              # 变化回调函数
        self.history = []                 # 历史记录
    
    def screenshot_compress(self):
        """
        截取屏幕并压缩图片
        返回：压缩后的图片字节数据
        """
        if HAS_MSS:
            # 使用mss库截图（更快）
            with mss() as sct:
                shot = sct.shot(output=None)
                img = Image.open(io.BytesIO(shot))
        else:
            # 使用PIL截图（兼容性好）
            img = ImageGrab.grab()
        
        # 缩小图片尺寸（减少数据量）
        img = img.resize((img.width // 3, img.height // 3), Image.Resampling.LANCZOS)
        
        # 压缩为JPEG格式
        import io
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=60)
        return buf.getvalue()
    
    def ocr(self, image_bytes):
        """
        调用OCR API识别图片中的文字
        参数：
            image_bytes: 图片字节数据
        返回：识别出的文字
        """
        img_base64 = base64.b64encode(image_bytes).decode()
        try:
            # 调用OCR Space API（免费OCR服务）
            resp = requests.post(
                'https://api.ocr.space/parse/image',
                data={
                    'base64Image': f'data:image/jpeg;base64,{img_base64}',
                    'language': 'chs',      # 中文简体
                    'apikey': 'K82328918888957',
                    'OCREngine': 2          # 使用OCR引擎2（更准确）
                },
                timeout=30
            )
            result = resp.json()
            if result.get('ParsedResults'):
                return result['ParsedResults'][0].get('ParsedText', '')
        except Exception as e:
            print(f"OCR错误: {e}")
        return None
    
    def image_hash(self, image_bytes):
        """
        计算图片的哈希值（用于快速判断图片是否变化）
        参数：
            image_bytes: 图片字节数据
        返回：MD5哈希值
        """
        import hashlib
        return hashlib.md5(image_bytes).hexdigest()
    
    def calc_diff_ratio(self, img1_bytes, img2_bytes):
        """
        计算两张图片的差异比例
        参数：
            img1_bytes: 第一张图片
            img2_bytes: 第二张图片
        返回：差异比例（0-1之间）
        """
        if not img1_bytes or not img2_bytes:
            return 1.0
        
        # 哈希相同则完全一样
        h1 = self.image_hash(img1_bytes)
        h2 = self.image_hash(img2_bytes)
        if h1 == h2:
            return 0.0
        
        # 转换为灰度图进行像素对比
        img1 = Image.open(io.BytesIO(img1_bytes)).convert('L')
        img2 = Image.open(io.BytesIO(img2_bytes)).convert('L')
        
        # 统一尺寸
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        
        # 计算像素差异
        pixels1 = list(img1.getdata())
        pixels2 = list(img2.getdata())
        diff = sum(abs(a - b) > 30 for a, b in zip(pixels1, pixels2))
        return diff / len(pixels1)
    
    def on_change(self, callback):
        """
        设置变化回调函数
        参数：
            callback: 回调函数，参数为(text, diff_ratio, log)
        """
        self.callback = callback
    
    def log_change(self, text, diff_ratio):
        """
        记录变化日志
        参数：
            text: 识别的文字
            diff_ratio: 差异比例
        返回：日志条目
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_entry = f"[{timestamp}] 变化检测 (差异: {diff_ratio:.2%})\n{text[:200]}...\n{'='*50}\n"
        
        # 写入日志文件
        with open(CHANGE_LOG, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # 保存到历史记录
        self.history.append({
            'time': timestamp,
            'text': text,
            'diff': diff_ratio
        })
        return log_entry
    
    def monitor_loop(self):
        """
        监控主循环（在独立线程中运行）
        """
        last_bytes = None
        
        while self.running:
            try:
                # 截取当前屏幕
                current_bytes = self.screenshot_compress()
                current_hash = self.image_hash(current_bytes)
                
                # 检查是否有变化
                if last_bytes is None or current_hash != self.last_hash:
                    diff = self.calc_diff_ratio(last_bytes, current_bytes) if last_bytes else 1.0
                    
                    # 变化超过阈值则处理
                    if diff > self.threshold:
                        text = self.ocr(current_bytes)
                        if text:
                            # 保存结果
                            with open(LAST_TEXT, 'w', encoding='utf-8') as f:
                                f.write(text)
                            with open(LAST_SCREEN, 'wb') as f:
                                f.write(current_bytes)
                            
                            # 记录日志
                            log = self.log_change(text, diff)
                            
                            # 调用回调
                            if self.callback:
                                self.callback(text, diff, log)
                            
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] 检测到变化: {diff:.1%}")
                
                # 更新状态
                last_bytes = current_bytes
                self.last_hash = current_hash
                
            except Exception as e:
                print(f"监控错误: {e}")
            
            # 等待下次检测
            time.sleep(self.interval)
    
    def start(self):
        """
        启动监控
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.thread.start()
            print(f"屏幕监控已启动 (间隔: {self.interval}秒, 阈值: {self.threshold:.0%})")
    
    def stop(self):
        """
        停止监控
        """
        self.running = False
        print("屏幕监控已停止")
    
    def get_current_text(self):
        """
        获取当前识别的文字
        返回：文字内容
        """
        if os.path.exists(LAST_TEXT):
            with open(LAST_TEXT, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def get_history(self, count=10):
        """
        获取历史记录
        参数：
            count: 返回的记录数量
        返回：历史记录列表
        """
        return self.history[-count:]


# 创建默认监控器实例
monitor = ScreenMonitor(interval=3, threshold=0.03)


def print_change(text, diff, log):
    """
    默认的变化回调函数
    参数：
        text: 识别的文字
        diff: 差异比例
        log: 日志条目
    """
    print(f"\n{'='*30}\n屏幕内容更新:\n{text[:500]}\n{'='*30}\n")


if __name__ == "__main__":
    """
    主程序入口
    用法：
        python screen_monitor.py start    - 启动监控
        python screen_monitor.py once     - 单次截图OCR
        python screen_monitor.py history  - 查看历史
        python screen_monitor.py current  - 查看当前文字
    """
    import io
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "start":
            # 启动持续监控
            monitor.on_change(print_change)
            monitor.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop()
        
        elif cmd == "once":
            # 单次截图并OCR
            img_bytes = monitor.screenshot_compress()
            text = monitor.ocr(img_bytes)
            print(text)
        
        elif cmd == "history":
            # 显示历史记录
            for h in monitor.get_history():
                print(f"[{h['time']}] {h['diff']:.0%}")
        
        elif cmd == "current":
            # 显示当前文字
            print(monitor.get_current_text())
        
        else:
            print("未知命令")
            print("用法: python screen_monitor.py [start|once|history|current]")
    
    else:
        print("老四屏幕监控工具")
        print("用法: python screen_monitor.py [start|once|history|current]")
