"""
老四01屏幕读取 - Laosi01 Screen Reader
功能：屏幕捕捉、OCR识别、动态监控、变化检测
版本：v1.0.0
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

try:
    from PIL import ImageGrab, Image
    import io
except ImportError:
    print("请安装: pip install pillow requests")
    sys.exit(1)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class LaosiVision:
    """
    老四视觉系统主类
    提供屏幕捕捉和OCR识别功能
    """
    
    OCR_API_URL = 'https://api.ocr.space/parse/image'
    OCR_API_KEY = 'K82328918888957'
    
    def __init__(self):
        self.last_screen = None
        self.last_text = None
        self.monitoring = False
        self.history = []
        self._paddle_ocr = None
        # Python 3.13与PaddleOCR不兼容，暂时禁用
        self._use_paddle = False
    
    def _get_paddle_ocr(self):
        """获取PaddleOCR实例（延迟加载）"""
        if self._paddle_ocr is None:
            try:
                from paddleocr import PaddleOCR
                self._paddle_ocr = PaddleOCR(lang='ch', use_angle_cls=True)
                print("PaddleOCR 已加载")
            except Exception as e:
                print(f"PaddleOCR 加载失败: {e}")
                self._use_paddle = False
        return self._paddle_ocr
    
    def capture(self, region=None):
        """
        截取屏幕
        参数:
            region: (x, y, width, height) 截取区域，None为全屏
        返回:
            PIL.Image 对象
        """
        if region:
            x, y, w, h = region
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        else:
            img = ImageGrab.grab()
        return img
    
    def capture_save(self, path, region=None):
        """
        截取屏幕并保存
        参数:
            path: 保存路径
            region: 截取区域
        返回:
            保存的文件路径
        """
        img = self.capture(region)
        img.save(path)
        return path
    
    def ocr(self, image_or_path, lang='chs'):
        """
        OCR识别图片中的文字
        参数:
            image_or_path: PIL.Image对象或图片路径
            lang: 语言 ('chs'=中文, 'eng'=英文)
        返回:
            识别出的文字
        """
        # 先尝试PaddleOCR
        if self._use_paddle:
            try:
                paddle_ocr = self._get_paddle_ocr()
                if paddle_ocr:
                    import numpy as np
                    if isinstance(image_or_path, str):
                        result = paddle_ocr.ocr(image_or_path)
                    else:
                        img_array = np.array(image_or_path)
                        result = paddle_ocr.ocr(img_array)
                    
                    if result and result[0]:
                        texts = []
                        for line in result[0]:
                            if line and len(line) >= 2:
                                texts.append(line[1][0])
                        if texts:
                            return '\n'.join(texts)
            except Exception as e:
                print(f"PaddleOCR识别失败，尝试备用方案: {e}")
        
        # 备用方案：OCR Space API
        if isinstance(image_or_path, str):
            with open(image_or_path, 'rb') as f:
                img_bytes = f.read()
        else:
            # 压缩图片到1MB以下
            img = image_or_path
            img = img.resize((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)
            quality = 85
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=quality)
            while len(buf.getvalue()) > 900000 and quality > 20:
                buf = io.BytesIO()
                quality -= 5
                img.save(buf, format='JPEG', quality=quality)
            img_bytes = buf.getvalue()
        
        img_base64 = base64.b64encode(img_bytes).decode()
        
        try:
            resp = requests.post(
                self.OCR_API_URL,
                data={
                    'base64Image': f'data:image/png;base64,{img_base64}',
                    'language': lang,
                    'apikey': self.OCR_API_KEY,
                    'OCREngine': 2
                },
                timeout=60
            )
            result = resp.json()
            if result.get('ParsedResults'):
                return result['ParsedResults'][0].get('ParsedText', '')
            return None
        except Exception as e:
            print(f"OCR错误: {e}")
            return None
    
    def ocr_screen(self, lang='chs'):
        """
        截屏并OCR识别
        返回:
            识别出的文字
        """
        img = self.capture()
        return self.ocr(img, lang)
    
    def calc_diff(self, img1, img2):
        """
        计算两张图片的差异比例
        参数:
            img1, img2: PIL.Image对象
        返回:
            差异比例 (0-1)
        """
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        
        if HAS_NUMPY:
            arr1 = np.array(img1)
            arr2 = np.array(img2)
            diff = np.sum(arr1 != arr2) / arr1.size
            return float(diff)
        else:
            pixels1 = list(img1.getdata())
            pixels2 = list(img2.getdata())
            diff = sum(p1 != p2 for p1, p2 in zip(pixels1, pixels2))
            return diff / len(pixels1)
    
    def monitor_start(self, interval=3, threshold=0.05, callback=None):
        """
        启动屏幕监控
        参数:
            interval: 检测间隔(秒)
            threshold: 变化阈值
            callback: 变化回调函数 callback(text, diff_ratio)
        """
        self.monitoring = True
        
        def _monitor_loop():
            last_img = None
            while self.monitoring:
                try:
                    current_img = self.capture()
                    
                    if last_img is not None:
                        diff = self.calc_diff(last_img, current_img)
                        
                        if diff > threshold:
                            text = self.ocr(current_img)
                            if text:
                                self.history.append({
                                    'time': datetime.now().isoformat(),
                                    'diff': diff,
                                    'text': text[:500]
                                })
                                if callback:
                                    callback(text, diff)
                                print(f"[{datetime.now().strftime('%H:%M:%S')}] 变化: {diff:.1%}")
                    
                    last_img = current_img.copy()
                except Exception as e:
                    print(f"监控错误: {e}")
                
                time.sleep(interval)
        
        self._thread = threading.Thread(target=_monitor_loop, daemon=True)
        self._thread.start()
        print(f"监控已启动 (间隔: {interval}秒)")
    
    def monitor_stop(self):
        """停止监控"""
        self.monitoring = False
        print("监控已停止")
    
    def get_history(self, count=10):
        """获取历史记录"""
        return self.history[-count:]


vision = LaosiVision()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "ocr":
            text = vision.ocr_screen()
            print(text)
        
        elif cmd == "capture":
            path = sys.argv[2] if len(sys.argv) > 2 else "capture.png"
            vision.capture_save(path)
            print(f"已保存: {path}")
        
        elif cmd == "monitor":
            vision.monitor_start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                vision.monitor_stop()
        
        else:
            print("用法: python laosi_vision.py [ocr|capture|monitor]")
    else:
        print("老四视觉系统 v1.0")
        print("命令: ocr, capture, monitor")
