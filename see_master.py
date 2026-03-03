import sys
sys.path.insert(0,'F:/laosi/.laosi')
import cv2
from laosi_core import laosi

print('='*60)
print('老四观看老大')
print('='*60)

# 获取摄像头信息
ip = laosi.recall('硬件_摄像头IP') or '192.168.1.222'
user = laosi.recall('硬件_摄像头用户') or 'admin'
pwd = laosi.recall('硬件_摄像头密码') or 'adcb1324'

rtsp_url = f'rtsp://{user}:{pwd}@{ip}:554'
print(f'\n连接摄像头: {ip}')
print(f'RTSP: {rtsp_url}')

try:
    # 连接摄像头
    cap = cv2.VideoCapture(rtsp_url)
    
    if cap.isOpened():
        print('\n摄像头连接成功!')
        
        # 读取一帧
        ret, frame = cap.read()
        if ret:
            # 保存截图
            save_path = 'F:/laosi/memory/laosi_see_master.jpg'
            cv2.imwrite(save_path, frame)
            print(f'已保存截图: {save_path}')
            print(f'画面尺寸: {frame.shape[1]}x{frame.shape[0]}')
        
        cap.release()
    else:
        print('\n连接失败，尝试其他端口...')
        # 尝试HTTP流
        http_url = f'http://{user}:{pwd}@{ip}'
        cap2 = cv2.VideoCapture(http_url)
        if cap2.isOpened():
            print(f'HTTP连接成功: {http_url}')
            cap2.release()
        else:
            print('请检查摄像头是否在线')
            
except Exception as e:
    print(f'错误: {e}')

print('\n' + '='*60)
print('老四认识老大完成!')
print('='*60)
