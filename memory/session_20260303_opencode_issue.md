# opencode TUI 崩溃问题记录
日期: 2026-03-03

## 问题描述
- **现象**: opencode TUI 窗口意外关闭，不止一次发生
- **环境**: Windows 11, opencode v1.2.15
- **影响**: 对话中断，需要重新开始

## 问题分析
通过 GitHub Issues 查询，发现是已知 bug：

### 相关 Issue
1. **Issue #15783** - Bun 运行时崩溃
   - 错误: `Internal assertion failure: ThreadLock is locked by thread X, not thread Y`
   - 原因: Bun 在 Windows 上的线程锁问题
   - 状态: Open，已指派开发者 nexxeln 处理
   
2. **Issue #15727** - 1.2.15 版本经常卡住
   - 现象: 卡在 "thinking" 或 "preparing patch"
   - 影响: 会话无法推进
   - 状态: Open

## 解决方案

### 方案1: 等待更新 (推荐)
- 官方正在修复
- 关注: https://github.com/anomalyco/opencode/issues/15783

### 方案2: 启用调试日志
```bash
opencode --print-logs --log-level DEBUG
```
- 崩溃时能看到错误信息
- 帮助定位问题

### 方案3: 降级版本
```bash
npm install -g opencode-ai@1.2.10
```
- 使用更稳定的旧版本

### 方案4: 更换终端
- 从 VSCode 终端切换到 Windows Terminal
- Windows Terminal 更稳定

## Windows Terminal 说明

### 是什么
微软开发的现代终端应用，统一管理多个命令行工具。

### 主要特点
- 多标签页 - 像浏览器一样切换 PowerShell、CMD、WSL
- 分屏功能 - 左右/上下分屏
- 自定义主题 - 背景、字体、配色可调
- GPU加速 - 渲染流畅
- 支持 Unicode - 中文和Emoji显示正常

### 打开方式
- 开始菜单搜索 "Windows Terminal"
- Win + X → 选择终端
- Win + R → 输入 wt

### VSCode终端 vs Windows Terminal
| 项目 | VSCode终端 | Windows Terminal |
|------|-----------|------------------|
| 环境 | 集成在编辑器内 | 独立应用 |
| 稳定性 | 可能受插件影响 | 更稳定 |
| 分屏 | 编辑器内分屏 | 终端内分屏 |
| 适用场景 | 开发调试 | 系统操作 |

## 技术细节

### opencode 信息
- 版本: 1.2.15
- 安装位置: C:\Users\lb\AppData\Roaming\npm\opencode
- 运行时: Bun (Windows x64 baseline)
- 平台: Windows 11

### 调试选项
```
--print-logs      输出日志到 stderr
--log-level       日志级别: DEBUG, INFO, WARN, ERROR
```

### 配置文件
- 位置: C:\Users\lb\.config\opencode\AGENTS.md
- 用途: 全局指令，每次打开自动加载

## 建议
1. 短期: 启用调试日志，收集错误信息
2. 中期: 关注官方 Issue，等待修复
3. 长期: 迁移到 Windows Terminal 使用

---
*此记录由老四 AI 助手保存*
