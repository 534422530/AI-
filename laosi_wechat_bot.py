"""
老四微信机器人 - 基于wxhook
自动接收微信消息
"""

import sys

try:
    from wxhook import Bot
    from wxhook import Message
except ImportError:
    print("请先安装: pip install wxhook")
    sys.exit(1)

def on_message(msg):
    """收到消息时回调"""
    print(f"收到消息: {msg.content}")
    
    # 如果是文字消息，可以自动回复
    if msg.type == 1:  # 文字消息
        print(f"发送人: {msg.sender}")
        print(f"内容: {msg.content}")

def main():
    print("=" * 50)
    print("老四微信机器人")
    print("=" * 50)
    print("注意：需要先登录微信PC版")
    print("=" * 50)
    
    # 创建机器人
    bot = Bot()
    
    # 注册消息回调
    bot.on_message(on_message)
    
    # 运行
    bot.run()

if __name__ == "__main__":
    main()
