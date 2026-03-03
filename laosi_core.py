"""
老四核心能力系统 - Laosi Core V4.0
真正的"眼脑手"一体化，所有技能深度融合成本能
永久集成，无需调用，直接使用
集成四种长期记忆方法 + 视频制作技能
"""

import sys
import os

class LaosiCore:
    """老四核心系统 V4.0 - 技能本能化 + 永久记忆"""

    VERSION = "4.0"

    def __init__(self):
        """初始化 - 自动加载所有技能成本能"""
        self._init_body()

    def _init_body(self):
        """初始化身体组件 - 眼睛、双手、大脑 (延迟加载)"""
        self._eye_loaded = False
        self._hand_loaded = False
        self._brain_loaded = False
        self._video_loaded = False
        
        self.eye = None
        self.hand = None
        self.brain = None
        self.video = None
        self.ai_video = None

    def _lazy_load_eye(self):
        """延迟加载视觉"""
        if self._eye_loaded:
            return
        try:
            import laosi01_screen
            self.eye = laosi01_screen.LaosiVision()
            self.see = self.eye.capture
            self.read = self.eye.ocr
            self.watch = self.eye.ocr_screen
            self._eye_loaded = True
        except:
            pass

    def _lazy_load_hand(self):
        """延迟加载控制"""
        if self._hand_loaded:
            return
        try:
            import laosi02_control
            self.hand = laosi02_control.LaosiControl()
            self._hand_loaded = True
        except:
            pass

    def _lazy_load_brain(self):
        """延迟加载记忆"""
        if self._brain_loaded:
            return
        try:
            import laosi_memory
            self.brain = laosi_memory.LaosiMemorySystem()
            self.remember = self.brain.remember
            self.recall = self.brain.recall
            self.search_memory = self.brain.search
            self.auto_learn = self.brain.auto_learn
            self.get_context = self.brain.get_context
            self._brain_loaded = True
        except:
            pass

    def _lazy_load_video(self):
        """延迟加载视频"""
        if self._video_loaded:
            return
        self.video = VideoMaker()
        self.ai_video = AIVideoMaker()
        self._video_loaded = True

    # ========== 🧠 大脑本能 ==========

    def _load_memory(self):
        """加载记忆本能 - 四种方法"""
        self._lazy_load_brain()

    def _load_video_skills(self):
        """加载视频制作本能"""
        self._lazy_load_video()

    # ========== 👁️ 眼睛本能 ==========
    
    def _load_vision(self):
        """加载视觉本能"""
        self._lazy_load_eye()
    
    def look(self, region=None):
        """看一眼 - 像人一样自然"""
        self._lazy_load_eye()
        if self.eye:
            return self.eye.capture(region)
        return None
    
    def read_this(self, thing=None):
        """读取 - 看到什么就读什么"""
        self._lazy_load_eye()
        if self.eye:
            if thing:
                return self.eye.ocr(thing)
            return self.eye.ocr_screen()
        return None
    
    def watch_screen(self, seconds=3):
        """观察屏幕变化"""
        self._lazy_load_eye()
        if self.eye:
            self.eye.monitor_start(seconds, 0.05)
    
    # ========== 🖱️ 双手本能 ==========
    
    def _load_control(self):
        """加载控制本能"""
        self._lazy_load_hand()
    
    def touch(self, x=None, y=None):
        """触碰 - 像人一样点击"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.mouse_click(x, y)
    
    def drag(self, x, y):
        """拖动"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.mouse_move(x, y)
    
    def write(self, text):
        """书写 - 像人一样打字"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.key_type(text)
    
    def press_key(self, key):
        """按键"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.key_press(key)
    
    def combo(self, *keys):
        """组合键"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.hotkey(*keys)
    
    def scroll_down(self, n=3):
        """向下滚"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.mouse_scroll(-n * 100)
    
    def scroll_up(self, n=3):
        """向上滚"""
        self._lazy_load_hand()
        if self.hand:
            self.hand.mouse_scroll(n * 100)
    
    # ========== 🎬 视频制作本能 ==========
    
    # ========== 🧠 本能技能 - 按需加载 ==========
    
    def _load_instincts(self):
        """加载本能技能 - 按需延迟加载"""
        pass

    def _lazy_load_instinct(self, name):
        """延迟加载单个本能"""
        flag_name = f"_{name}_loaded"
        if getattr(self, flag_name, False):
            return True
        
        try:
            if name == 'scan':
                import ip_scanner
                self.scan = ip_scanner.scan_network
            elif name == 'zero_token':
                import laosi_zero_token
                self.zero_token = laosi_zero_token.LaosiZeroToken()
                self.free_chat = self.zero_token.chat
                self.free_platforms = self.zero_token.list_platforms
            elif name == 'peek':
                import direct_capture
                self.peek = direct_capture.get_screen_data
            elif name == 'tts':
                import laosi_tts
                self.talk = laosi_tts.speak
                self.say = laosi_tts.edge_speak
            elif name == 'ai':
                import openclaw_ai
                self.ai = openclaw_ai.openclaw
                self.ai_chat = openclaw_ai.ai_chat
            setattr(self, flag_name, True)
            return True
        except:
            return False
    
    # ========== 🎯 自动化行动 - 遇到问题直接做 ==========
    
    def do_it(self, task, **what):
        """自动化执行 - 像本能一样"""
        
        # 看到+做到一体化
        task_map = {
            'click': lambda: self.touch(what.get('x'), what.get('y')),
            'type': lambda: self.write(what.get('text', '')),
            'press': lambda: self.press_key(what.get('key')),
            'scroll': lambda: self.scroll_down() if what.get('dir') == 'down' else self.scroll_up(),
            'open': lambda: self.combo('win', 'd'),
            'copy': lambda: self.combo('ctrl', 'c'),
            'paste': lambda: self.combo('ctrl', 'v'),
            'save': lambda: self.combo('ctrl', 's'),
            'search': lambda: [self.combo('ctrl', 'l'), self.write(what.get('word', ''))],
            'screenshot': lambda: self.look(),
            'scan_network': lambda: self.scan(what.get('network')),
            
            # 视频制作
            'video': lambda: self.video.make(what.get('content', ''), what.get('style', 'cartoon')),
            'clip_video': lambda: self.video.clip(what.get('input'), what.get('start', 0), what.get('end', 10)),
            'concat_videos': lambda: self.video.concat(what.get('files', [])),
            'add_music': lambda: self.video.add_music(what.get('video'), what.get('music')),
            'add_text': lambda: self.video.add_text(what.get('video'), what.get('text', '')),
            'cartoon': lambda: self.video.to_cartoon(what.get('input'), what.get('output')),
            'gif': lambda: self.video.to_gif(what.get('input'), what.get('output')),
            'reverse': lambda: self.video.reverse(what.get('input'), what.get('output')),
            'speed': lambda: self.video.speed(what.get('input'), what.get('output'), what.get('speed', 1.0)),
        }
        
        if task in task_map:
            return task_map[task]()
        
        return f"未知任务: {task}"
    
    # ========== 📞 统一入口 ==========
    
    def __call__(self, task, **kwargs):
        """直接调用 - 像说话一样简单"""
        return self.do_it(task, **kwargs)
    
    def status(self):
        """查看状态"""
        return {
            "eye": "READY" if self._eye_loaded else "LAZY",
            "hand": "READY" if self._hand_loaded else "LAZY",
            "brain": "READY" if self._brain_loaded else "LAZY",
            "video": "READY" if self._video_loaded else "LAZY",
            "ai": "READY" if getattr(self, '_ai_loaded', False) else "LAZY",
            "tts": "READY" if getattr(self, '_tts_loaded', False) else "LAZY",
            "version": self.VERSION,
            "mode": "延迟加载 (快速启动)"
        }


class VideoMaker:
    """视频制作本能 - 完整功能"""
    
    def __init__(self):
        self._load_libs()
    
    def _load_libs(self):
        """加载视频库"""
        try:
            from moviepy import VideoFileClip, TextClip, concatenate_videoclips, CompositeVideoClip
            self.VideoFileClip = VideoFileClip
            self.TextClip = TextClip
            self.concatenate = concatenate_videoclips
            self.CompositeVideoClip = CompositeVideoClip
            self.loaded = True
        except Exception as e:
            print(f"[!] MoviePy load error: {e}")
            self.loaded = False
    
    # ====== 基础操作 ======
    
    def load(self, path):
        """加载视频"""
        if not self.loaded:
            return None, "MoviePy未安装"
        try:
            clip = self.VideoFileClip(path)
            return clip, "加载成功"
        except Exception as e:
            return None, str(e)
    
    def save(self, clip, path, fps=24):
        """保存视频"""
        if not clip:
            return False, "无视频"
        try:
            clip.write_videofile(path, fps=fps, codec='libx264')
            return True, f"已保存: {path}"
        except Exception as e:
            return False, str(e)
    
    # ====== 剪辑操作 ======
    
    def clip(self, input_path, start=0, end=10, output=None):
        """剪辑视频片段"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        # 截取片段
        clipped = clip.subclip(start, end)
        
        if not output:
            output = input_path.replace('.mp4', '_clip.mp4')
        
        self.save(clipped, output)
        clipped.close()
        clip.close()
        return output, "剪辑完成"
    
    def concat(self, file_list, output='F:/laosi/concat.mp4'):
        """合并多个视频"""
        if not self.loaded:
            return None, "MoviePy未安装"
        
        clips = []
        for f in file_list:
            clip, msg = self.load(f)
            if clip:
                clips.append(clip)
        
        if not clips:
            return None, "无有效视频"
        
        final = self.concatenate(clips, method="compose")
        self.save(final, output)
        
        for c in clips:
            c.close()
        final.close()
        
        return output, "合并完成"
    
    # ====== 文字和特效 ======
    
    def add_text(self, input_path, text, output=None, fontsize=50, color='white'):
        """添加文字"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        if not output:
            output = input_path.replace('.mp4', '_text.mp4')
        
        try:
            txt = self.TextClip(text, fontsize=fontsize, color=color)
            txt = txt.set_pos(('center', 'bottom')).set_duration(clip.duration)
            
            video = self.CompositeVideoClip([clip, txt])
            self.save(video, output)
            
            clip.close()
            txt.close()
            video.close()
            return output, "文字添加完成"
        except Exception as e:
            return None, str(e)
    
    # ====== 音频 ======
    
    def add_music(self, input_path, music_path, output=None, volume=0.5):
        """添加背景音乐"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        if not output:
            output = input_path.replace('.mp4', '_music.mp4')
        
        try:
            music = self.VideoFileClip(music_path).subclip(0, clip.duration)
            music = music.volumex(volume)
            clip = clip.set_audio(music)
            
            self.save(clip, output)
            
            clip.close()
            music.close()
            return output, "音乐添加完成"
        except Exception as e:
            return None, str(e)
    
    # ====== 特效 ======
    
    def to_cartoon(self, input_path, output=None):
        """转换为漫画风格"""
        if not output:
            output = input_path.replace('.mp4', '_cartoon.mp4')
        
        try:
            import cv2
            cap = cv2.VideoCapture(input_path)
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output, fourcc, fps, (w, h))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # 漫画滤镜
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                edge_color = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
                out.write(edge_color)
            
            cap.release()
            out.release()
            return output, "漫画转换完成"
        except Exception as e:
            return None, str(e)
    
    def to_gif(self, input_path, output=None, fps=10):
        """转换为GIF"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        if not output:
            output = input_path.replace('.mp4', '.gif')
        
        try:
            clip.write_gif(output, fps=fps)
            clip.close()
            return output, "GIF创建完成"
        except Exception as e:
            return None, str(e)
    
    def reverse(self, input_path, output=None):
        """视频倒放"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        if not output:
            output = input_path.replace('.mp4', '_reverse.mp4')
        
        try:
            reversed_clip = clip.fx(lambda c: c.time_mirror())
            self.save(reversed_clip, output)
            
            clip.close()
            reversed_clip.close()
            return output, "倒放完成"
        except Exception as e:
            return None, str(e)
    
    def speed(self, input_path, output=None, speed=2.0):
        """调整速度"""
        clip, msg = self.load(input_path)
        if not clip:
            return None, msg
        
        if not output:
            output = input_path.replace('.mp4', f'_speed{speed}.mp4')
        
        try:
            fast = clip.fx(lambda c: c.set_fps(c.fps * speed))
            fast = fast.multiply_speedup(speed)
            self.save(fast, output)
            
            clip.close()
            fast.close()
            return output, "速度调整完成"
        except Exception as e:
            return None, str(e)
    
    # ====== 高级操作 ======
    
    def make(self, content, style='cartoon', output='F:/laosi/video.mp4'):
        """制作视频（从文字）"""
        if not self.loaded:
            return None, "请安装 moviepy"
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            
            # 创建文字图片
            img = Image.new('RGB', (1920, 1080), color='black')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("msyh.ttc", 80)
            except:
                font = ImageFont.load_default()
            
            # 居中
            bbox = draw.textbbox((0, 0), content, font=font)
            w = (1920 - (bbox[2] - bbox[0])) // 2
            h = (1080 - (bbox[3] - bbox[1])) // 2
            draw.text((w, h), content, font=font, fill='white')
            
            # 转视频
            img_array = np.array(img)
            from moviepy import ImageClip
            clip = ImageClip(img_array, duration=5)
            
            clip.write_videofile(output, fps=24, codec='libx264')
            clip.close()
            
            return output, "视频制作完成"
        except Exception as e:
            return None, str(e)
    
    # ====== 🎬 一键生成动漫视频 ======
    
    def anime(self, content, output='F:/laosi/anime.mp4'):
        """一键生成动漫视频"""
        return self.make(content, style='anime', output=output)
    
    def cartoon(self, content, output='F:/laosi/cartoon.mp4'):
        """一键生成漫画视频"""
        return self.make(content, style='cartoon', output=output)
    
    def story(self, scenes, output='F:/laosi/story.mp4'):
        """生成故事视频（多场景）"""
        if not self.loaded:
            return None, "请安装 moviepy"
        
        clips = []
        
        for i, scene in enumerate(scenes):
            clip, msg = self._make_clip(scene, duration=3)
            if clip:
                clips.append(clip)
        
        if not clips:
            return None, "无有效场景"
        
        from moviepy import concatenate_videoclips
        final = concatenate_videoclips(clips, method="compose")
        
        try:
            final.write_videofile(output, fps=24, codec='libx264')
            for c in clips:
                c.close()
            final.close()
            return output, "故事视频完成"
        except Exception as e:
            return None, str(e)
    
    def _make_clip(self, text, duration=3):
        """制作单场景视频片段"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            from moviepy import ImageClip
            
            # 创建图片
            img = Image.new('RGB', (1920, 1080), color='black')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("msyh.ttc", 60)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            w = (1920 - (bbox[2] - bbox[0])) // 2
            h = (1080 - (bbox[3] - bbox[1])) // 2
            draw.text((w, h), text, font=font, fill='white')
            
            img_array = np.array(img)
            clip = ImageClip(img_array).set_duration(duration)
            
            return clip, "OK"
        except Exception as e:
            return None, str(e)


class AIVideoMaker:
    """AI视频生成本能 - 支持阿里云万相/NVIDIA/本地"""
    
    def __init__(self):
        self.api_key = None
        self.provider = 'wanxiang'  # 默认阿里云万相
    
    def config(self, api_key, provider='wanxiang'):
        """配置AI视频服务
        用法: config('你的API密钥')
        支持: wanxiang(阿里云), nvidia(NVIDIA)
        """
        self.api_key = api_key
        self.provider = provider
    
    # ====== 阿里云万相视频生成 ======
    
    def generate(self, prompt, duration=5, size='1280*720', model='wan2.6-t2v'):
        """AI生成视频"""
        if self.provider == 'nvidia':
            return self._nvidia_generate(prompt)
        
        # 默认阿里云万相
        return self._wanxiang_generate(prompt, duration, size, model)
    
    def _wanxiang_generate(self, prompt, duration=5, size='1280*720', model='wan2.6-t2v'):
        """阿里云万相"""
        import requests
        import time
        
        if not self.api_key:
            return None, "请配置API密钥: config_ai('你的阿里云API密钥')"
        
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"
        }
        
        data = {
            "model": model,
            "input": {"prompt": prompt},
            "parameters": {
                "size": size,
                "duration": duration,
                "prompt_extend": True,
                "watermark": False
            }
        }
        
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=30)
            result = resp.json()
            
            if 'output' in result and 'task_id' in result['output']:
                task_id = result['output']['task_id']
                print(f"[AI视频] 任务提交: {task_id}")
                return self._wanxiang_wait(task_id)
            else:
                return None, f"错误: {result}"
        except Exception as e:
            return None, str(e)
    
    def _wanxiang_wait(self, task_id):
        """等待阿里云结果"""
        import requests
        import time
        
        query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        for i in range(120):
            time.sleep(5)
            try:
                resp = requests.get(query_url, headers=headers, timeout=30)
                result = resp.json()
                status = result.get('output', {}).get('task_status', '')
                
                if status == 'SUCCEEDED':
                    video_url = result.get('output', {}).get('video_url')
                    return self._download(video_url)
                elif status == 'FAILED':
                    return None, "生成失败"
            except:
                pass
        
        return None, "等待超时"
    
    # ====== NVIDIA API ======
    
    def _nvidia_generate(self, prompt):
        """NVIDIA NIM API生成"""
        import requests
        import os
        
        if not self.api_key:
            return None, "请配置API密钥: config_ai('你的NVIDIA API密钥')"
        
        # NVIDIA NIM endpoint (需要NVIDIA账号获取)
        url = "https://api.nvcf.nvidia.com/v2/nvidia/trellis/video/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "NVCF-INPUT-ASSET-URI": "asset://input",
            "NVCF-RUN-ASSET-URI": "asset://output"
        }
        
        # 注意: 具体API需要NVIDIA开发者账号
        data = {
            "prompt": prompt,
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
        
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=60)
            
            if resp.status_code == 200:
                result = resp.json()
                video_url = result.get('output', {}).get('url')
                if video_url:
                    return self._download(video_url)
            
            return None, f"NVIDIA API错误: {resp.status_code}"
        except Exception as e:
            return None, str(e)
    
    # ====== 下载 ======
    
    def _download(self, url):
        """下载视频"""
        import requests
        import time
        
        save_path = f'F:/laosi/ai_video_{int(time.time())}.mp4'
        
        try:
            resp = requests.get(url, timeout=300, stream=True)
            with open(save_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return save_path, "生成成功"
        except Exception as e:
            return None, f"下载失败: {e}"
    
    # ====== 快捷方式 ======
    
    def make(self, text, duration=5):
        return self.generate(text, duration)
    
    def anime(self, text, duration=5):
        return self.generate(f"动漫风格: {text}", duration)
    
    def cartoon(self, text, duration=5):
        return self.generate(f"卡通漫画风格: {text}", duration)


# 创建终极实例
laosi = LaosiCore()

# ========== 便捷方式 ==========

def look():
    """看一眼"""
    return laosi.look()

def read():
    """读取屏幕"""
    return laosi.read_this()

def click(x=None, y=None):
    """点击"""
    return laosi.touch(x, y)

def type(text):
    """输入"""
    return laosi.write(text)

def press(key):
    """按键"""
    return laosi.press_key(key)

def scroll(n=3):
    """滚动"""
    return laosi.scroll_down(n)

def scan():
    """扫描网络"""
    return laosi.scan()

def screenshot():
    """截屏"""
    return laosi.look()

# ====== 视频制作本能 ======

def video(content, style='cartoon'):
    """制作视频"""
    return laosi.video.make(content, style)

def anime(content):
    """一键生成动漫视频"""
    return laosi.video.anime(content)

def cartoon(content):
    """一键生成漫画视频"""
    return laosi.video.cartoon(content)

def story(scenes):
    """生成故事视频"""
    return laosi.video.story(scenes)

def clip_video(input_path, start=0, end=10):
    """剪辑视频"""
    return laosi.video.clip(input_path, start, end)

def concat_videos(file_list):
    """合并视频"""
    return laosi.video.concat(file_list)

def add_music(video_path, music_path):
    """添加音乐"""
    return laosi.video.add_music(video_path, music_path)

def add_text(video_path, text):
    """添加文字"""
    return laosi.video.add_text(video_path, text)

def to_cartoon(video_path):
    """漫画风格"""
    return laosi.video.to_cartoon(video_path)

def to_gif(video_path):
    """转GIF"""
    return laosi.video.to_gif(video_path)

def reverse_video(video_path):
    """视频倒放"""
    return laosi.video.reverse(video_path)

def speed_video(video_path, speed=2.0):
    """调整速度"""
    return laosi.video.speed(video_path, speed=speed)

# ====== AI视频本能 ======

def ai_video(prompt, duration=5):
    """AI生成视频 (需要配置API)"""
    return laosi.ai_video.generate(prompt, duration)

def ai_anime(text):
    """AI生成动漫视频"""
    return laosi.ai_video.anime(text)

def ai_cartoon(text):
    """AI生成漫画视频"""
    return laosi.ai_video.cartoon(text)

def config_ai(key):
    """配置AI视频API (阿里云万相)
    获取API: https://dashscope.console.aliyun.com/
    """
    laosi.ai_video.config(key)
    return True, "API已配置"

# ====== 记忆本能 ======

def remember(key, value, category='general'):
    """记住"""
    return laosi.remember(key, value, category)

def recall(key):
    """回忆"""
    return laosi.recall(key)

def search_mem(query):
    """搜索记忆"""
    return laosi.search_memory(query)

def learn(content):
    """自动学习"""
    return laosi.auto_learn(content)

def context(query):
    """获取上下文"""
    return laosi.get_context(query)

def do(task, **kwargs):
    """做一件事"""
    return laosi.do_it(task, **kwargs)


# ========== 测试 ==========
if __name__ == "__main__":
    print("=" * 50)
    print("老四 V4.0 - 本能系统 + 永久记忆")
    print("=" * 50)
    print("状态:", laosi.status())
    print()
    print("用法就像说话一样简单:")
    print(" click(100, 200)    # 点击")
    print(" type('你好')      # 输入")
    print(" look()            # 看一眼")
    print(" read()            # 读取")
    print(" remember('k', 'v') # 记住")
    print(" recall('k')       # 回忆")
    print(" search_mem('q')   # 搜索记忆")
    print(" video('内容')     # 制作视频")
    print("=" * 50)
    print("老四 V3.0 - 本能系统")
    print("=" * 50)
    print("状态:", laosi.status())
    print()
    print("用法就像说话一样简单:")
    print("  click(100, 200)  # 点击")
    print("  type('你好')      # 输入")
    print("  look()           # 看一眼")
    print("  read()           # 读取")
    print("  scan()           # 扫描")
    print("  video('内容')    # 制作视频")
    print("  clip_video('a.mp4', 0, 10)  # 剪辑")
    print("  add_music('v.mp4', 'm.mp3') # 加音乐")
    print("  to_cartoon('v.mp4')          # 漫画风")
    print("=" * 50)
    print("老四 V3.0 - 本能系统")
    print("=" * 50)
    print("状态:", laosi.status())
    print()
    print("用法就像说话一样简单:")
    print("  click(100, 200)  # 点击")
    print("  type('你好')      # 输入")
    print("  look()           # 看一眼")
    print("  read()           # 读取")
    print("  scan()           # 扫描")
    print("  video('内容')    # 制作视频")
    print("  speak('说话')    # 语音")
    print("=" * 50)
