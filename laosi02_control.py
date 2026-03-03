"""
老四02键鼠控制 - 改进版
功能：控制键盘鼠标操作电脑
增强版：带位置验证和错误检测
"""

import pyautogui
import time

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

class LaosiControl:
    """键盘鼠标控制类"""
    
    @staticmethod
    def mouse_click(x=None, y=None, button='left', clicks=1):
        """鼠标点击"""
        pyautogui.click(x, y, clicks=clicks, button=button)
    
    @staticmethod
    def mouse_move(x, y, duration=0.5):
        """移动鼠标"""
        pyautogui.moveTo(x, y, duration=duration)
    
    @staticmethod
    def mouse_position():
        """获取鼠标位置"""
        return pyautogui.position()
    
    @staticmethod
    def mouse_scroll(clicks):
        """滚动鼠标"""
        pyautogui.scroll(clicks)
    
    @staticmethod
    def key_press(key):
        """按键一次"""
        pyautogui.press(key)
    
    @staticmethod
    def key_type(text, interval=0.05):
        """输入文字"""
        pyautogui.typewrite(text, interval=interval)
    
    @staticmethod
    def hotkey(*keys):
        """快捷键"""
        pyautogui.hotkey(*keys)
    
    # ========== 增强功能 ==========
    
    @staticmethod
    def move_and_click(x, y, duration=0.5):
        """移动到位置并点击"""
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(0.2)
        pyautogui.click()
    
    @staticmethod
    def verify_position(expected_x, expected_y, tolerance=50):
        """验证鼠标位置"""
        actual = pyautogui.position()
        diff = abs(actual.x - expected_x) + abs(actual.y - expected_y)
        return diff < tolerance
    
    @staticmethod
    def get_screen_size():
        """获取屏幕尺寸"""
        return pyautogui.size()


control = LaosiControl()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "pos":
            print(control.mouse_position())
        elif cmd == "size":
            print(control.get_screen_size())
    else:
        print("老四02键鼠控制")
        print("命令: pos, size")
