"""
OpenClaw Zero Token 技能模块
免费使用各种AI模型 - 通过浏览器session捕获

支持平台: DeepSeek, 豆包, Kimi, Claude Web, ChatGPT, Gemini, Qwen, GLM, Grok

使用方法:
1. 安装 Node.js 和 pnpm
2. cd F:/laosi/openclaw
3. npm install && npm run build
4. ./start-chrome-debug.sh  # 打开Chrome调试
5. 登录AI平台 (豆包/Kimi/Claude等)
6. ./onboard.sh 配置
7. ./server.sh start 启动服务

API调用示例:
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "doubao-seed-2.0", "messages": [{"role": "user", "content": "你好"}]}'
"""

import os
import json
import subprocess
import requests

class OpenClawAI:
    """OpenClaw AI 零Token调用"""
    
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.project_path = "F:/laosi/openclaw"
        self.status = "未启动"
    
    def is_running(self):
        """检查服务是否运行"""
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    def start_chrome_debug(self):
        """启动Chrome调试模式"""
        if os.name == 'nt':  # Windows
            cmd = f'cd {self.project_path} && start-chrome-debug.bat'
        else:
            cmd = f'cd {self.project_path} && ./start-chrome-debug.sh'
        subprocess.Popen(cmd, shell=True)
        return "Chrome调试模式已启动，请登录AI平台"
    
    def start_server(self):
        """启动OpenClaw服务"""
        if os.name == 'nt':
            cmd = f'cd {self.project_path} && server.bat start'
        else:
            cmd = f'cd {self.project_path} && ./server.sh start'
        subprocess.Popen(cmd, shell=True)
        self.status = "运行中"
        return "服务已启动"
    
    def chat(self, prompt, model="doubao-seed-2.0"):
        """发送聊天请求"""
        if not self.is_running():
            return "服务未启动，请先运行 start()"
        
        url = f"{self.base_url}/v1/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            resp = requests.post(url, json=data, timeout=60)
            return resp.json()
        except Exception as e:
            return f"请求失败: {e}"
    
    def get_status(self):
        """查看状态"""
        return {
            "status": "运行中" if self.is_running() else "未启动",
            "url": self.base_url,
            "project": self.project_path
        }

# 创建实例
openclaw = OpenClawAI()

# 快捷方法
def ai_chat(prompt, model="doubao-seed-2.0"):
    """聊天 - 免费使用AI"""
    return openclaw.chat(prompt, model)

def ai_status():
    """查看AI状态"""
    return openclaw.status()

def start_ai_server():
    """启动AI服务"""
    return openclaw.start_server()
