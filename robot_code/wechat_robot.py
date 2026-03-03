"""
老四微信机器人 - 基于wxhook
监听微信消息并处理
"""

from py_process_hooker import inject_python_and_monitor_dir
from wxhook import get_on_startup
from wxhook.msg_plugins import PrintMsg
from wxhook.other_plugins import HttpApi

if __name__ == "__main__":
    process_name = "WeChat.exe"
    open_console = True
    
    on_startup = get_on_startup(
        msg_plugins=[PrintMsg],
        other_plugins=[HttpApi]
    )
    
    print("正在注入微信...")
    inject_python_and_monitor_dir(
        process_name=process_name,
        open_console=open_console,
        on_startup=on_startup
    )
