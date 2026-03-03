"""
老四会话记录系统 - Laosi Session System

功能：记录所有对话内容，保存到F盘
版本：v1.0.0
作者：老四AI助手
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any

class LaosiSession:
    """
    老四会话记录主类
    提供对话内容记录和持久化功能
    """
    
    def __init__(self, base_path: str = "F:/laosi/sessions"):
        self.base_path = base_path
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.messages = []
        self.user_id = "admin"
        self.token = "adcb1324"
        self.ip = "192.168.1.222"
        
        # 创建目录
        os.makedirs(self.base_path, exist_ok=True)
        
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return f"session_{int(time.time())}_{os.getpid()}"
    
    def start_session(self):
        """开始会话"""
        print(f"[会话] 开始新会话: {self.session_id}")
        self._save_metadata()
    
    def add_message(self, role: str, content: str, tokens: int = 0):
        """添加消息"""
        message = {
            'timestamp': datetime.now().isoformat(),
            'role': role,
            'content': content,
            'tokens': tokens
        }
        self.messages.append(message)
        self._save_to_file()
    
    def end_session(self, summary: str = ""):
        """结束会话"""
        self.end_time = datetime.now().isoformat()
        self._save_metadata()
        print(f"[会话] 会话结束: {self.session_id}")
    
    def _save_metadata(self):
        """保存会话元数据"""
        metadata = {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'token': self.token,
            'ip': self.ip,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_messages': len(self.messages),
            'created_at': datetime.now().isoformat()
        }
        
        metadata_path = os.path.join(self.base_path, f"{self.session_id}_meta.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def _save_to_file(self):
        """保存到文件"""
        messages_path = os.path.join(self.base_path, f"{self.session_id}_messages.json")
        with open(messages_path, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
    
    def get_session_info(self) -> Dict[str, Any]:
        """获取会话信息"""
        return {
            'session_id': self.session_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_messages': len(self.messages),
            'user_id': self.user_id,
            'ip': self.ip
        }
    
    def get_all_messages(self) -> List[Dict]:
        """获取所有消息"""
        return self.messages
    
    def get_summary(self) -> str:
        """获取会话摘要"""
        if not self.messages:
            return "无对话内容"
        
        user_msgs = [m for m in self.messages if m['role'] == 'user']
        assistant_msgs = [m for m in self.messages if m['role'] == 'assistant']
        
        summary = f"会话ID: {self.session_id}\n"
        summary += f"开始时间: {self.start_time}\n"
        summary += f"消息数量: {len(self.messages)} (用户: {len(user_msgs)}, AI: {len(assistant_msgs)})\n"
        summary += f"IP地址: {self.ip}\n"
        summary += f"用户ID: {self.user_id}\n"
        
        if self.end_time:
            summary += f"结束时间: {self.end_time}\n"
        
        return summary


# 创建会话实例
laosi_session = LaosiSession()

if __name__ == "__main__":
    print("老四会话记录系统已初始化")
    print(f"会话ID: {laosi_session.session_id}")
    print(f"存储路径: {laosi_session.base_path}")
    print("\n用法:")
    print("  laosi_session.add_message('user', '你好')")
    print("  laosi_session.add_message('assistant', '你好，有什么可以帮助你的？')")
    print("  laosi_session.end_session('对话完成')")