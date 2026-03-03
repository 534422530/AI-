"""
老四摄像机系统 - Laosi Camera System

功能：摄像机连接、图像处理、实时监控
版本：v1.0.0
作者：老四AI助手
"""

import cv2
import numpy as np
import threading
import time
from typing import Optional, Dict, Any

class LaosiCamera:
    """
    老四摄像机主类
    提供摄像机连接和图像处理功能
    """
    
    def __init__(self, ip: str = "192.168.1.222", port: int = 8080):
        self.ip = ip
        self.port = port
        self.camera = None
        self.is_opened = False
        self.frame = None
        self.frame_lock = threading.Lock()
        self.running = False
        self.stream_url = f"rtsp://{ip}:{port}/user=admin&password=adcb1324&channel=1&stream=0"
        
    def connect(self) -> bool:
        """连接摄像机"""
        try:
            # 尝试本地摄像头
            self.camera = cv2.VideoCapture(0)
            if self.camera.isOpened():
                self.is_opened = True
                self._start_capture()
                print(f"[摄像机] 本地摄像头连接成功")
                return True
            
            # 尝试网络摄像头
            self.camera = cv2.VideoCapture(self.stream_url)
            if self.camera.isOpened():
                self.is_opened = True
                self._start_capture()
                print(f"[摄像机] 网络摄像头连接成功: {self.stream_url}")
                return True
            
        except Exception as e:
            print(f"[摄像机] 连接失败: {e}")
            return False
        
        print("[摄像机] 连接失败，未找到可用摄像头")
        return False
    
    def _start_capture(self):
        """开始图像捕获"""
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
    
    def _capture_loop(self):
        """捕获循环"""
        while self.running:
            if self.camera and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    with self.frame_lock:
                        self.frame = frame.copy()
            time.sleep(0.05)  # 20 FPS
    
    def get_frame(self) -> Optional[np.ndarray]:
        """获取最新帧"""
        if not self.is_opened:
            return None
        
        with self.frame_lock:
            return self.frame.copy() if self.frame is not None else None
    
    def show_preview(self, duration: int = 10):
        """显示预览"""
        if not self.is_opened:
            print("[摄像机] 未连接")
            return
        
        start_time = time.time()
        while time.time() - start_time < duration:
            frame = self.get_frame()
            if frame is not None:
                cv2.imshow('Camera Preview', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.05)
        
        cv2.destroyAllWindows()
    
    def capture_image(self, path: str = "capture.jpg") -> bool:
        """捕获图像"""
        if not self.is_opened:
            print("[摄像机] 未连接")
            return False
        
        frame = self.get_frame()
        if frame is not None:
            cv2.imwrite(path, frame)
            print(f"[摄像机] 图像已保存: {path}")
            return True
        return False
    
    def detect_faces(self) -> int:
        """人脸检测"""
        if not self.is_opened:
            return 0
        
        frame = self.get_frame()
        if frame is None:
            return 0
        
        # 使用OpenCV的人脸检测
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                           'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # 绘制检测结果
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('Face Detection', frame)
        cv2.waitKey(1)
        
        return len(faces)
    
    def motion_detection(self, sensitivity: int = 30) -> bool:
        """运动检测"""
        if not self.is_opened:
            return False
        
        frame = self.get_frame()
        if frame is None:
            return False
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if not hasattr(self, '_prev_frame'):
            self._prev_frame = gray
            return False
        
        frame_delta = cv2.absdiff(self._prev_frame, gray)
        thresh = cv2.threshold(frame_delta, sensitivity, 255, cv2.THRESH_BINARY)[1]
        
        # 更新上一帧
        self._prev_frame = gray
        
        # 检测运动
        if np.sum(thresh) > sensitivity * 100:
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'connected': self.is_opened,
            'ip': self.ip,
            'port': self.port,
            'stream_url': self.stream_url,
            'frame_available': self.frame is not None,
            ɿps': 20
        }
    
    def close(self):
        """关闭摄像机"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        print("[摄像机] 已关闭")


# 创建摄像机实例
laosi_camera = LaosiCamera()

if __name__ == "__main__":
    print("老四摄像机系统已初始化")
    print(f"目标IP: {laosi_camera.ip}")
    print(f"目标端口: {laosi_camera.port}")
    print(f"RTSP地址: {laosi_camera.stream_url}")
    
    print("\n尝试连接...")
    if laosi_camera.connect():
        print("连接成功!")
        print("摄像机状态:")
        print(laosi_camera.get_status())
        
        print("\n开始预览...")
        laosi_camera.show_preview(10)
        
        print("\n人脸检测:")
        faces = laosi_camera.detect_faces()
        print(f"检测到 {faces} 个人脸")
        
        print("\n运动检测:")
        if laosi_camera.motion_detection():
            print("检测到运动!")
        else:
            print("无运动")
        
        laosi_camera.close()
    else:
        print("连接失败")
        print("尝试使用本地摄像头...")
        
        # 测试本地摄像头
        local_camera = LaosiCamera(ip="本地", port=0)
        if local_camera.connect():
            print("本地摄像头连接成功!")
            local_camera.show_preview(5)
            local_camera.close()
        else:
            print("本地摄像头也连接失败")


# 快捷方式

def connect_camera():
    """连接摄像机"""
    return laosi_camera.connect()

def show_camera():
    """显示摄像机"""
    laosi_camera.show_preview(10)

def capture_photo(path="capture.jpg"):
    """拍照"""
    return laosi_camera.capture_image(path)

def detect_faces():
    """检测人脸"""
    return laosi_camera.detect_faces()

def motion_detect():
    """运动检测"""
    return laosi_camera.motion_detection()