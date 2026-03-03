"""
老四 AI 零Token调用系统 - 学习自 OpenClaw Zero Token
核心技术: 浏览器session捕获 + Web API调用

支持平台:
- 豆包 (doubao-seed-2.0, doubao-pro)  
- DeepSeek Web
- Kimi
- Claude Web
- Qwen
- GLM

原理:
1. 通过 Playwright/Chrome CDP 连接浏览器
2. 用户登录AI平台后捕获 cookies (sessionid, ttwid等)
3. 使用这些cookies调用Web API
4. 支持流式响应 (SSE)
"""

import json
import time
import threading
import queue
from typing import Generator, Optional, Dict, Any
import urllib.parse

class BrowserSession:
    """浏览器会话 - 核心能力"""
    
    def __init__(self):
        self.cookies = {}
        self.headers = {}
        self.browser = None
        self.page = None
    
    def from_chrome(self, port=9222) -> bool:
        """从Chrome浏览器获取session"""
        try:
            import requests
            resp = requests.get(f"http://localhost:{port}/json", timeout=5)
            tabs = resp.json()
            if tabs:
                self.debugger_url = tabs[0]["webSocketDebuggerUrl"]
                return True
        except:
            pass
        return False
    
    def capture_cookies(self, url: str) -> Dict:
        """访问URL并捕获cookies"""
        if not self.browser:
            return {}
        # 实际实现需要Playwright或CDP
        return self.cookies

class AIWebClient:
    """AI Web客户端 - 核心实现"""
    
    def __init__(self, platform: str = "doubao"):
        self.platform = platform
        self.session = BrowserSession()
        self.cookies = {}
        self.base_url = self._get_base_url()
    
    def _get_base_url(self) -> str:
        urls = {
            "doubao": "https://www.doubao.com",
            "deepseek": "https://chat.deepseek.com",
            "kimi": "https://kimi.moonshot.cn",
            "qwen": "https://qwen.ai",
            "claude": "https://claude.ai",
            "glm": "https://www.zhipuai.cn",
        }
        return urls.get(self.platform, "")
    
    def set_cookies(self, cookies: Dict):
        """设置cookies"""
        self.cookies = cookies
    
    def chat(self, prompt: str, model: str = None, 
             stream: bool = True) -> Generator[str, None]:
        """发送聊天请求 - 流式响应"""
        
        if self.platform == "doubao":
            return self._doubao_chat(prompt, model, stream)
        elif self.platform == "deepseek":
            return self._deepseek_chat(prompt, model, stream)
        # 可以扩展更多平台...
        yield from []
    
    def _doubao_chat(self, prompt: str, model: str = None, 
                     stream: bool = True) -> Generator[str, None]:
        """豆包 Web API 调用"""
        import requests
        
        url = f"{self.base_url}/api/v3/chat/completions"
        
        # 构建请求
        data = {
            "model": model or "doubao-seed-2.0",
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream
        }
        
        # 构建cookies字符串
        cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": self.base_url,
            "Referer": self.base_url
        }
        
        try:
            if stream:
                resp = requests.post(url, json=data, headers=headers, 
                                   stream=True, timeout=30)
                for line in resp.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            yield line[6:]  # 返回SSE数据
            else:
                resp = requests.post(url, json=data, headers=headers, timeout=30)
                yield resp.json()
        except Exception as e:
            yield f"Error: {e}"
    
    def _deepseek_chat(self, prompt: str, model: str = None,
                       stream: bool = True) -> Generator[str, None]:
        """DeepSeek Web API 调用"""
        import requests
        
        url = f"{self.base_url}/api/v0/chat/completions"
        
        data = {
            "model": model or "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream
        }
        
        cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": self.base_url,
        }
        
        try:
            resp = requests.post(url, json=data, headers=headers, 
                               stream=True, timeout=30)
            for line in resp.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        yield line[6:]
        except Exception as e:
            yield f"Error: {e}"

class LaosiAI:
    """老四 AI 零Token系统"""
    
    def __init__(self):
        self.clients = {}
        self._init_clients()
    
    def _init_clients(self):
        """初始化各平台客户端"""
        platforms = ["doubao", "deepseek", "kimi", "qwen", "claude", "glm"]
        for p in platforms:
            self.clients[p] = AIWebClient(p)
    
    def set_cookies(self, platform: str, cookies: Dict):
        """设置平台cookies"""
        if platform in self.clients:
            self.clients[platform].set_cookies(cookies)
    
    def chat(self, prompt: str, platform: str = "doubao", 
             model: str = None) -> Generator[str, None]:
        """聊天"""
        if platform in self.clients:
            yield from self.clients[platform].chat(prompt, model)
    
    def auto_chat(self, prompt: str) -> Generator[str, None]:
        """自动选择最佳平台"""
        # 默认用豆包
        yield from self.chat(prompt, "doubao")

# 全局实例
ai = LaosiAI()

# 快捷函数
def ai_chat(prompt: str, platform: str = "doubao", model: str = None):
    """聊天"""
    result = []
    for chunk in ai.chat(prompt, platform, model):
        result.append(chunk)
    return "\n".join(result)

def ai_set_cookies(platform: str, cookies: Dict):
    """设置cookies"""
    ai.set_cookies(platform, cookies)

def ai_status():
    """查看状态"""
    return {
        "platforms": list(ai.clients.keys()),
        "note": "需要先通过浏览器登录并捕获cookies"
    }

# 浏览器捕获辅助
def capture_from_browser(platform: str = "doubao") -> Dict:
    """
    从浏览器捕获cookies
    
    使用方法:
    1. 先用 Chrome 调试模式访问AI网站并登录
    2. 运行 capture_from_browser('doubao') 获取cookies
    3. 用 ai_set_cookies 设置cookies
    4. 开始聊天
    """
    # 这个需要实现 - 使用 CDP 获取cookies
    return {
        "sessionid": "",
        "ttwid": "",
        "note": "需要Chrome CDP连接"
    }
