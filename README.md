<<<<<<< HEAD
# 老四01屏幕读取

老四AI助手的屏幕读取技能包。

## 功能特点

- **截屏**: 快速截取屏幕
- **OCR识别**: 识别屏幕上的文字，支持中文/英文
- **动态监控**: 实时检测屏幕变化
- **变化检测**: 智能判断屏幕是否有实质变化

## 文件说明

| 文件 | 功能 |
|------|------|
| `laosi01_screen.py` | 主模块（截屏+OCR） |
| `screen_monitor.py` | 屏幕监控模块 |
| `direct_capture.py` | 直接显存读取模块 |

## 使用方法

### 截屏OCR
```bash
python laosi01_screen.py ocr
```

### 截屏保存
```bash
python laosi01_screen.py capture
```

### 屏幕监控
```bash
python laosi01_screen.py monitor
```

## Python调用

```python
from laosi01_screen import LaosiVision

v = LaosiVision()
img = v.capture()
result = v.ocr(img)
print(result)
```

## 依赖安装

```bash
pip install pillow requests numpy
```

## 作者

老四AI助手

## 版本

v1.0.0 - 初始版本
=======
# AI-
opencode成精了 都自己开发了
>>>>>>> d896ec6973354dcb985ee00d9a1a7fb0a3a79579
