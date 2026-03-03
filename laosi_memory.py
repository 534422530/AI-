"""
老四记忆系统 V4.0 - Laosi Memory System
集成四种长期记忆方法 + 技能永久存储
"""

import os
import json
import sqlite3
import hashlib
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional

# ========== 技能永久存储 ==========
# 关键技能代码直接嵌入，永不丢失

LAOSI_SKILLS = {
    "screen_capture": """
import ctypes
from ctypes import wintypes
HWND_DESKTOP = 0
SRCCOPY = 0x00CC0020
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def capture_screen():
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    hdc = user32.GetWindowDC(HWND_DESKTOP)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bitmap = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(memdc, bitmap)
    gdi32.BitBlt(memdc, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
    return w, h
""",
    
    "mouse_control": """
import pyautogui
pyautogui.FAILSAFE = False

def click(x, y):
    pyautogui.click(x, y)

def move(x, y):
    pyautogui.moveTo(x, y)

def type_text(text):
    pyautogui.typewrite(text)

def press(key):
    pyautogui.press(key)

def hotkey(*keys):
    pyautogui.hotkey(*keys)
""",

    "tts": """
import edge_tts
import asyncio

async def speak(text, voice='zh-CN-XiaoxiaoNeural'):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save('output.mp3')
    
def say(text):
    asyncio.run(speak(text))
""",

    "ocr": """
from PIL import Image
import pytesseract

def ocr_image(image_path, lang='chi_sim+eng'):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text
"""
}

# 技能注册表 - 记录所有技能的元信息
SKILL_REGISTRY = {
    "laosi01_screen": {
        "name": "屏幕读取",
        "desc": "截屏、OCR识别、屏幕监控",
        "methods": ["capture", "ocr", "monitor"],
        "embedded": True
    },
    "laosi02_control": {
        "name": "键鼠控制",
        "desc": "鼠标点击、键盘输入、快捷键",
        "methods": ["click", "move", "type", "press", "hotkey"],
        "embedded": True
    },
    "laosi_tts": {
        "name": "语音合成",
        "desc": "文字转语音、中英文支持",
        "methods": ["speak", "say"],
        "embedded": True
    },
    "video_maker": {
        "name": "视频制作",
        "desc": "文字转视频、漫画风格、剪辑合并",
        "methods": ["make", "clip", "concat", "add_music", "to_cartoon"],
        "embedded": False
    },
    "direct_capture": {
        "name": "显存读取",
        "desc": "直接从显存读取屏幕数据",
        "methods": ["get_screen_data", "get_pixel_hash"],
        "embedded": True
    },
    "ip_scanner": {
        "name": "IP扫描",
        "desc": "扫描本地网络设备IP",
        "methods": ["scan_network"],
        "embedded": False
    }
}

# ========== METHOD 1: Structured Memory Folders ==========
# 结构化记忆文件夹 - 完全透明可查看

class StructuredMemory:
    """
    方法1: 结构化记忆文件夹
    - 完全透明，可随时查看
    - 文件夹结构清晰
    - 支持版本控制
    """
    
    def __init__(self, base_path: str = "F:/laosi/memory"):
        self.base_path = base_path
        self._init_structure()
    
    def _init_structure(self):
        """初始化文件夹结构"""
        structure = {
            "goals.md": "# 目标\n\n## 短期目标\n## 长期目标\n",
            "decisions.md": "# 决策记录\n\n",
            "preferences.md": "# 偏好设置\n\n",
            "communication.md": "# 对话风格\n\n",
            "projects/projects.md": "# 项目列表\n\n",
            "sessions/": "",
            "context/context.md": "# 上下文信息\n\n"
        }
        
        for path, default_content in structure.items():
            full_path = os.path.join(self.base_path, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            if not os.path.exists(full_path) and default_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(default_content)
    
    def save_session(self, session_id: str, content: Dict):
        """保存会话记忆"""
        path = os.path.join(self.base_path, "sessions", f"{session_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        return path
    
    def add_goal(self, goal: str, priority: str = "medium"):
        """添加目标"""
        path = os.path.join(self.base_path, "goals.md")
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"\n- [{priority}] {goal} - {datetime.now().strftime('%Y-%m-%d')}\n")
    
    def add_decision(self, decision: str, reason: str):
        """记录决策"""
        path = os.path.join(self.base_path, "decisions.md")
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**决策**: {decision}\n")
            f.write(f"**原因**: {reason}\n")
    
    def read_all(self) -> Dict[str, str]:
        """读取所有记忆"""
        memory = {}
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(('.md', '.json', '.txt')):
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, self.base_path)
                    with open(path, 'r', encoding='utf-8') as f:
                        memory[rel_path] = f.read()
        return memory


# ========== METHOD 2: Works With Any LLM ==========
# 适配所有大模型 - 抽象接口层

class LLMAdapter:
    """
    方法2: 适配所有大模型
    - 抽象接口
    - 支持多种LLM
    - 统一记忆格式
    """
    
    PROVIDERS = {
        'openai': {'models': ['gpt-4', 'gpt-3.5-turbo']},
        'anthropic': {'models': ['claude-3', 'claude-2']},
        'nvidia': {'models': ['glm4', 'nemotron']},
        'local': {'models': ['ollama', 'llamacpp']}
    }
    
    def __init__(self, provider: str = 'nvidia'):
        self.provider = provider
        self.memory_format = self._get_memory_format()
    
    def _get_memory_format(self) -> Dict:
        """获取统一的记忆格式"""
        return {
            "timestamp": "",
            "role": "",
            "content": "",
            "metadata": {
                "provider": self.provider,
                "model": "",
                "tokens": 0
            },
            "embedding": []
        }
    
    def format_for_llm(self, memory: Dict) -> str:
        """将记忆格式化为LLM可理解的格式"""
        formatted = []
        for key, value in memory.items():
            if isinstance(value, str) and len(value) > 10:
                formatted.append(f"[{key}]\n{value}\n")
        return "\n".join(formatted)
    
    def get_context_window(self, model: str) -> int:
        """获取模型上下文窗口大小"""
        windows = {
            'gpt-4': 128000,
            'gpt-3.5-turbo': 16000,
            'claude-3': 200000,
            'glm4': 128000,
            'local': 4096
        }
        return windows.get(model, 4096)


# ========== METHOD 3: MemO - Automated Memory ==========
# 自动记忆系统 - 观察、提取、检索

class AutomatedMemory:
    """
    方法3: 自动记忆系统
    - Watch: 观察对话
    - Extract: 提取重要信息
    - Retrieve: 检索相关记忆
    """
    
    def __init__(self, db_path: str = "F:/laosi/memory/auto_memory.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                content TEXT,
                importance REAL,
                category TEXT,
                embedding_hash TEXT,
                metadata TEXT
            )
        ''')
        
        c.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
        
        conn.commit()
        conn.close()
    
    def watch(self, conversation: str) -> Dict:
        """观察对话内容"""
        return {
            "raw": conversation,
            "length": len(conversation),
            "timestamp": datetime.now().isoformat(),
            "hash": hashlib.md5(conversation.encode()).hexdigest()
        }
    
    def extract(self, observed: Dict) -> List[Dict]:
        """提取重要信息"""
        # 简单的关键词提取（实际可接入LLM）
        important_patterns = [
            ('goal', ['目标', '计划', '要做', '需要']),
            ('preference', ['喜欢', '偏好', '习惯', '希望']),
            ('decision', ['决定', '选择', '采用', '方案']),
            ('fact', ['是', '叫做', '位于', '属于']),
            ('skill', ['技能', '能力', '功能', '可以'])
        ]
        
        extracted = []
        content = observed['raw']
        
        for category, keywords in important_patterns:
            for keyword in keywords:
                if keyword in content:
                    extracted.append({
                        'category': category,
                        'content': content,
                        'importance': 0.8 if category in ['goal', 'skill'] else 0.5
                    })
                    break
        
        return extracted
    
    def save(self, extracted: List[Dict]):
        """保存提取的记忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for item in extracted:
            c.execute('''
                INSERT INTO memories (timestamp, content, importance, category, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                item['content'],
                item['importance'],
                item['category'],
                json.dumps({'source': 'auto'})
            ))
        
        conn.commit()
        conn.close()
    
    def retrieve(self, query: str, limit: int = 10) -> List[Dict]:
        """检索相关记忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 简单的关键词匹配
        c.execute('''
            SELECT timestamp, content, importance, category 
            FROM memories 
            WHERE content LIKE ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = []
        for row in c.fetchall():
            results.append({
                'timestamp': row[0],
                'content': row[1],
                'importance': row[2],
                'category': row[3]
            })
        
        conn.close()
        return results


# ========== METHOD 4: SQLite Native Power ==========
# SQLite原生能力 - 密集结构化数据、精确查询、便携持久

class SQLiteMemory:
    """
    方法4: SQLite原生记忆
    - Dense Structured Data: 密集结构化数据
    - Precise Queries: 精确查询
    - Portable & Persistent: 便携持久
    - Zero Dependencies: 零依赖（Python内置）
    """
    
    def __init__(self, db_path: str = "F:/laosi/memory/laosi_memory.db"):
        self.db_path = db_path
        self._init_tables()
    
    def _init_tables(self):
        """初始化所有表"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 会话表
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                created_at TEXT,
                ended_at TEXT,
                summary TEXT,
                tokens_used INTEGER
            )
        ''')
        
        # 消息表
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TEXT,
                tokens INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        # 记忆表（长期记忆）
        c.execute('''
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT,
                category TEXT,
                importance INTEGER,
                created_at TEXT,
                updated_at TEXT,
                access_count INTEGER
            )
        ''')
        
        # 技能表
        c.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                module_path TEXT,
                usage_count INTEGER,
                last_used TEXT
            )
        ''')
        
        # 偏好表
        c.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')
        
        # 创建索引
        c.execute('CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_memory_category ON long_term_memory(category)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_memory_importance ON long_term_memory(importance)')
        
        conn.commit()
        conn.close()
    
    # ===== 会话管理 =====
    
    def start_session(self, session_id: str):
        """开始新会话"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO sessions (session_id, created_at) VALUES (?, ?)',
                  (session_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def end_session(self, session_id: str, summary: str, tokens: int):
        """结束会话"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            UPDATE sessions SET ended_at = ?, summary = ?, tokens_used = ?
            WHERE session_id = ?
        ''', (datetime.now().isoformat(), summary, tokens, session_id))
        conn.commit()
        conn.close()
    
    # ===== 消息存储 =====
    
    def add_message(self, session_id: str, role: str, content: str, tokens: int = 0):
        """添加消息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO messages (session_id, role, content, timestamp, tokens)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, role, content, datetime.now().isoformat(), tokens))
        conn.commit()
        conn.close()
    
    def get_messages(self, session_id: str, limit: int = 100) -> List[Dict]:
        """获取会话消息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT role, content, timestamp FROM messages
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        messages = [{'role': r[0], 'content': r[1], 'timestamp': r[2]} for r in c.fetchall()]
        conn.close()
        return messages
    
    # ===== 长期记忆 =====
    
    def remember(self, key: str, value: str, category: str = 'general', importance: int = 5):
        """存储长期记忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.now().isoformat()
        
        c.execute('SELECT id FROM long_term_memory WHERE key = ?', (key,))
        if c.fetchone():
            c.execute('''
                UPDATE long_term_memory 
                SET value = ?, updated_at = ?, access_count = access_count + 1
                WHERE key = ?
            ''', (value, now, key))
        else:
            c.execute('''
                INSERT INTO long_term_memory (key, value, category, importance, created_at, access_count)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (key, value, category, importance, now))
        
        conn.commit()
        conn.close()
    
    def recall(self, key: str) -> Optional[str]:
        """回忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            UPDATE long_term_memory SET access_count = access_count + 1
            WHERE key = ?
        ''', (key,))
        
        c.execute('SELECT value FROM long_term_memory WHERE key = ?', (key,))
        result = c.fetchone()
        conn.commit()
        conn.close()
        
        return result[0] if result else None
    
    def recall_by_category(self, category: str) -> List[Dict]:
        """按类别回忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT key, value, importance, access_count FROM long_term_memory
            WHERE category = ?
            ORDER BY importance DESC, access_count DESC
        ''', (category,))
        
        results = [{'key': r[0], 'value': r[1], 'importance': r[2], 'access': r[3]} 
                   for r in c.fetchall()]
        conn.close()
        return results
    
    def search(self, query: str) -> List[Dict]:
        """搜索记忆"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT key, value, category, importance FROM long_term_memory
            WHERE key LIKE ? OR value LIKE ?
            ORDER BY importance DESC
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%'))
        
        results = [{'key': r[0], 'value': r[1], 'category': r[2], 'importance': r[3]} 
                   for r in c.fetchall()]
        conn.close()
        return results
    
    # ===== 技能管理 =====
    
    def register_skill(self, name: str, description: str, module_path: str):
        """注册技能"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO skills (name, description, module_path, usage_count, last_used)
            VALUES (?, ?, ?, 0, ?)
        ''', (name, description, module_path, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_skills(self) -> List[Dict]:
        """获取所有技能"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT name, description, usage_count FROM skills ORDER BY usage_count DESC')
        
        skills = [{'name': r[0], 'desc': r[1], 'usage': r[2]} for r in c.fetchall()]
        conn.close()
        return skills
    
    def used_skill(self, name: str):
        """记录技能使用"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            UPDATE skills SET usage_count = usage_count + 1, last_used = ?
            WHERE name = ?
        ''', (datetime.now().isoformat(), name))
        conn.commit()
        conn.close()
    
    # ===== 偏好管理 =====
    
    def set_preference(self, key: str, value: str):
        """设置偏好"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """获取偏好"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT value FROM preferences WHERE key = ?', (key,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else default
    
    # ===== 统计分析 =====
    
    def stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        stats = {}
        
        c.execute('SELECT COUNT(*) FROM sessions')
        stats['total_sessions'] = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM messages')
        stats['total_messages'] = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM long_term_memory')
        stats['total_memories'] = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM skills')
        stats['total_skills'] = c.fetchone()[0]
        
        c.execute('SELECT SUM(tokens_used) FROM sessions')
        stats['total_tokens'] = c.fetchone()[0] or 0
        
        conn.close()
        return stats
    
    # ===== 导出导入 =====
    
    def export_memory(self, output_path: str):
        """导出记忆（便携）"""
        conn = sqlite3.connect(self.db_path)
        
        # 导出为SQL
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        
        conn.close()
        return output_path
    
    def import_memory(self, input_path: str):
        """导入记忆"""
        conn = sqlite3.connect(self.db_path)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            conn.executescript(sql)
        
        conn.commit()
        conn.close()


# ========== 统一记忆接口 ==========

class LaosiMemorySystem:
    """
    老四记忆系统 - 整合四种方法
    """
    
    def __init__(self, base_path: str = "F:/laosi/memory"):
        self.structured = StructuredMemory(base_path)
        self.automated = AutomatedMemory(f"{base_path}/auto_memory.db")
        self.sqlite = SQLiteMemory(f"{base_path}/laosi_memory.db")
        self.llm_adapter = LLMAdapter()
        
        print("[记忆系统] 已初始化四种记忆方法")
    
    # 快捷方法
    
    def remember(self, key: str, value: str, category: str = 'general'):
        """记住"""
        self.sqlite.remember(key, value, category)
    
    def recall(self, key: str) -> Optional[str]:
        """回忆"""
        return self.sqlite.recall(key)
    
    def search(self, query: str) -> List[Dict]:
        """搜索"""
        return self.sqlite.search(query)
    
    def auto_learn(self, conversation: str):
        """自动学习"""
        observed = self.automated.watch(conversation)
        extracted = self.automated.extract(observed)
        self.automated.save(extracted)
    
    def get_context(self, query: str) -> str:
        """获取上下文"""
        # 从多个来源获取
        memories = self.search(query)
        files = self.structured.read_all()
        
        context = []
        for m in memories[:5]:
            context.append(f"记忆: {m['key']} = {m['value']}")
        
        for path, content in files.items():
            if query.lower() in content.lower():
                context.append(f"文件[{path}]: {content[:200]}...")
        
        return '\n'.join(context)
    
    def status(self) -> Dict:
        """状态"""
        return {
            'sqlite': self.sqlite.stats(),
            'structured_files': len(self.structured.read_all()),
            'version': '4.0'
        }


# 初始化
memory = LaosiMemorySystem()


if __name__ == "__main__":
    print("=" * 50)
    print("老四记忆系统 V4.0")
    print("=" * 50)
    
    # 测试
    m = LaosiMemorySystem()
    
    # 测试存储
    m.remember("主人", "老大", "identity")
    m.remember("角色", "AI编程助手", "identity")
    m.remember("名字", "老四", "identity")
    
    # 测试回忆
    print("\n回忆测试:")
    print(f"主人: {m.recall('主人')}")
    print(f"角色: {m.recall('角色')}")
    
    # 测试搜索
    print("\n搜索测试:")
    results = m.search("老四")
    for r in results:
        print(f"  {r['key']}: {r['value']}")
    
    # 状态
    print("\n系统状态:")
    print(m.status())
