"""
老四核心能力系统 - Laosi Core
整合所有技能，统一入口
"""

import os
import sys

class LaosiCore:
    """老四核心能力系统"""
    
    def __init__(self):
        self.skills = {}
        self.load_skills()
    
    def load_skills(self):
        """加载所有技能"""
        # 视觉技能
        try:
            from .laosi_vision import LaosiVision
            self.skills['vision'] = LaosiVision()
        except ImportError:
            self.skills['vision'] = None
        
        # 其他技能待加载...
    
    # ========== 视觉能力 ==========
    
    def capture(self, region=None, save_path=None):
        """
        截屏
        参数:
            region: (x, y, w, h) 区域，None=全屏
            save_path: 保存路径，None=不保存
        返回:
            PIL.Image 或 文件路径
        """
        if not self.skills.get('vision'):
            return None, "视觉模块未加载"
        
        img = self.skills['vision'].capture(region)
        if save_path:
            img.save(save_path)
            return save_path, "截图已保存"
        return img, "成功"
    
    def ocr(self, image=None, lang='chs'):
        """
        OCR识别
        参数:
            image: PIL.Image或图片路径，None=截屏识别
            lang: 语言 ('chs'=中文, 'eng'=英文)
        返回:
            识别文字
        """
        if not self.skills.get('vision'):
            return None, "视觉模块未加载"
        
        if image is None:
            return self.skills['vision'].ocr_screen(lang), "成功"
        return self.skills['vision'].ocr(image, lang), "成功"
    
    def read_screen(self, region=None):
        """
        读取屏幕内容（截屏+OCR）
        参数:
            region: 截取区域
        返回:
            识别的文字
        """
        img = self.skills['vision'].capture(region)
        return self.skills['vision'].ocr(img)
    
    def monitor(self, action='start', interval=3, threshold=0.05):
        """
        屏幕监控
        参数:
            action: 'start' 或 'stop'
            interval: 检测间隔(秒)
            threshold: 变化阈值
        """
        if not self.skills.get('vision'):
            return False, "视觉模块未加载"
        
        if action == 'start':
            self.skills['vision'].monitor_start(interval, threshold)
            return True, "监控已启动"
        elif action == 'stop':
            self.skills['vision'].monitor_stop()
            return True, "监控已停止"
        return False, "未知命令"
    
    # ========== 工具能力 ==========
    
    def read_file(self, path):
        """读取文件内容"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read(), "成功"
        except Exception as e:
            return None, str(e)
    
    def write_file(self, path, content):
        """写入文件"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已保存"
        except Exception as e:
            return False, str(e)
    
    # ========== 统一入口 ==========
    
    def do(self, command, **kwargs):
        """
        统一执行命令
        用法: laosi.do('capture', save_path='xxx.png')
              laosi.do('ocr', lang='eng')
              laosi.do('read_screen')
              laosi.do('monitor', action='start')
        """
        commands = {
            'capture': lambda: self.capture(**kwargs),
            'ocr': lambda: self.ocr(**kwargs),
            'read_screen': lambda: self.read_screen(**kwargs),
            'monitor': lambda: self.monitor(**kwargs),
            'read_file': lambda: self.read_file(kwargs.get('path')),
            'write_file': lambda: self.write_file(kwargs.get('path'), kwargs.get('content')),
        }
        
        if command in commands:
            return commands[command]()
        return None, f"未知命令: {command}"


# 创建全局实例
laosi = LaosiCore()


# 便捷函数
def capture(region=None, save_path=None):
    """截屏"""
    return laosi.capture(region, save_path)

def ocr(image=None, lang='chs'):
    """OCR识别"""
    return laosi.ocr(image, lang)

def read_screen(region=None):
    """读取屏幕"""
    return laosi.read_screen(region)

def monitor(action='start', interval=3, threshold=0.05):
    """屏幕监控"""
    return laosi.monitor(action, interval, threshold)

def read_file(path):
    """读取文件"""
    return laosi.read_file(path)

def write_file(path, content):
    """写入文件"""
    return laosi.write_file(path, content)


if __name__ == "__main__":
    print("老四核心系统 v1.0")
    print("命令: capture, ocr, read_screen, monitor, read_file, write_file")
    print("用法示例:")
    print("  python -c \"from laosi_core import *; print(read_screen())\"")
