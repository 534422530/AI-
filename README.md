# 老四技能包 - Laosi Skills

一套用于屏幕监控和OCR识别的Python工具。

## 功能特点

- **直接显存读取**: 比传统截图更快，直接从显存获取数据
- **动态监控**: 实时检测屏幕变化
- **OCR识别**: 识别屏幕上的文字
- **变化检测**: 智能判断屏幕是否有实质变化

## 文件说明

| 文件 | 功能 |
|------|------|
| `screen_monitor.py` | 屏幕监控主模块（截图+OCR） |
| `direct_capture.py` | 直接显存读取模块（更快） |
| `screen_reader.py` | 简单截图+OCR工具 |

## 使用方法

### 启动屏幕监控
```bash
python screen_monitor.py start
```

### 单次截图OCR
```bash
python screen_monitor.py once
```

### 查看历史记录
```bash
python screen_monitor.py history
```

### 查看当前识别文字
```bash
python screen_monitor.py current
```

### 直接读取显存
```bash
python direct_capture.py
```

## 技术对比

| 方法 | 速度 | 兼容性 | 说明 |
|------|------|--------|------|
| PIL截图 | 慢 | 全平台 | 简单易用 |
| mss库 | 快 | 全平台 | 推荐使用 |
| 直接显存 | 最快 | 仅Windows | 高级用法 |

## 依赖安装

```bash
pip install mss pillow requests numpy
```

## 作者

老四AI助手 - 2026

## 版本

v1.0.0 - 初始版本
