"""
老四视频制作模块 - Video Maker
功能：文字转视频、漫画风格转换、视频合成
"""

import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_text_image(text, size=(1920, 1080), fontsize=80, color='white'):
    """创建文字图片"""
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("msyh.ttc", fontsize)
    except:
        font = ImageFont.load_default()
    
    # 居中文字
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=color)
    return np.array(img)

def create_video(content, style='cartoon', output='F:/laosi/output.mp4'):
    """
    制作视频
    参数:
        content: 视频内容描述
        style: 风格 (cartoon漫画, anime动漫, real真实)
        output: 输出路径
    返回:
        (文件路径, 状态)
    """
    try:
        os.makedirs(os.path.dirname(output) or 'F:/laosi', exist_ok=True)
        
        clips = []
        
        # 标题页
        title_img = create_text_image(f"《{content}》", fontsize=100)
        title_clip = ImageClip(title_img).set_duration(3)
        clips.append(title_clip)
        
        # 内容页
        content_img = create_text_image(f"视频风格: {style}", fontsize=60)
        content_clip = ImageClip(content_img).set_duration(2)
        clips.append(content_clip)
        
        # 结束页
        end_img = create_text_image("制作完成 - 老四", fontsize=60)
        end_clip = ImageClip(end_img).set_duration(2)
        clips.append(end_clip)
        
        # 合成视频
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output, fps=24, codec='libx264')
        
        return output, "视频创建成功"
    
    except Exception as e:
        return None, str(e)

def add_background_music(video_path, audio_path, output=None):
    """添加背景音乐"""
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        audio = audio.subclip(0, video.duration)
        video = video.set_audio(audio)
        
        if output is None:
            output = video_path.replace('.mp4', '_with_music.mp4')
        
        video.write_videofile(output, fps=24)
        return output, "成功"
    except Exception as e:
        return None, str(e)

def convert_to_cartoon(video_path, output=None):
    """转换为漫画风格"""
    # 漫画风格转换需要OpenCV处理
    import cv2
    
    if output is None:
        output = video_path.replace('.mp4', '_cartoon.mp4')
    
    cap = cv2.VideoCapture(video_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, 30, (1920, 1080))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 简易漫画滤镜
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        out.write(edges_color)
    
    cap.release()
    out.release()
    
    return output, "漫画风格转换成功"


if __name__ == "__main__":
    print("老四视频制作模块")
    print("用法:")
    print("  from video_maker import create_video")
    print("  create_video('学习AI', 'cartoon', 'output.mp4')")
