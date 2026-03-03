"""
老四语音合成模块 - TTS
功能：文字转语音，支持多种语音
"""

import os

def speak(text, lang='zh', output=None):
    """
    文字转语音
    参数:
        text: 要朗读的文字
        lang: 语言 (zh中文, en英文, ja日文)
        output: 输出文件路径
    """
    try:
        import pyttsx3
    except ImportError:
        return False, "请安装pyttsx3: pip install pyttsx3"
    
    engine = pyttsx3.init()
    
    # 设置语音
    voices = engine.getProperty('voices')
    if lang == 'zh':
        engine.setProperty('voice', voices[0].id)  # 中文语音
    else:
        engine.setProperty('voice', voices[1].id)  # 英文语音
    
    # 设置语速
    engine.setProperty('rate', 150)
    
    if output:
        engine.save_to_file(text, output)
        engine.runAndWait()
        return output, "已保存到文件"
    else:
        engine.say(text)
        engine.runAndWait()
        return True, "播放完成"


def edge_speak(text, lang='zh-CN', output=None):
    """
    Edge TTS语音合成（更自然）
    参数:
        text: 要朗读的文字
        lang: 语言代码
        output: 输出文件路径
    """
    try:
        from edge_tts import Communicate
    except ImportError:
        return False, "请安装edge-tts: pip install edge-tts"
    
    import asyncio
    
    # 语言映射
    voice_map = {
        'zh-CN': 'zh-CN-XiaoxiaoNeural',
        'zh-CN-Yunxi': 'zh-CN-YunxiNeural',
        'en-US': 'en-US-JennyNeural',
        'ja-JP': 'ja-JP-NanamiNeural',
    }
    
    voice = voice_map.get(lang, 'zh-CN-XiaoxiaoNeural')
    
    if output is None:
        output = 'F:/laosi/temp_speech.mp3'
    
    async def run():
        communicate = Communicate(text, voice)
        await communicate.save(output)
    
    asyncio.run(run())
    return output, "语音合成成功"


def play_audio(file_path):
    """播放音频文件"""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return True, "播放完成"
    except ImportError:
        return False, "请安装pygame: pip install pygame"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    print("老四语音合成模块")
    print("用法:")
    print("  from laosi_tts import speak")
    print("  speak('你好，我是老四')")
    print("  speak('Hello', 'en', 'hello.mp3')")
