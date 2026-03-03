"""
读取老四聊天消息
"""
import sys
sys.path.insert(0, r'C:\Users\lb\.laosi')

# 这个需要和服务器共享数据
# 简单方法：读取服务器生成的网页

def get_messages():
    """从聊天服务器获取消息"""
    try:
        import requests
        resp = requests.get('http://localhost:5000/', timeout=2)
        return resp.text
    except:
        return None

if __name__ == '__main__':
    result = get_messages()
    if result:
        print("服务器运行中...")
    else:
        print("请先运行: python laosi_chat.py")
