"""
老四实时聊天 - WebSocket版
手机发消息，我立刻能收到
"""

from flask import Flask, request, render_template_string
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'laosi'
socketio = SocketIO(app, cors_allowed_origins="*")

messages = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老四聊天</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #f5f5f5; }
        h1 { text-align: center; color: #333; }
        .form { background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; box-sizing: border-box; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background: #45a049; }
        #messages { background: white; padding: 15px; border-radius: 10px; }
        .msg { padding: 10px; margin: 5px 0; background: #e8f5e9; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>📱 老四聊天</h1>
    <div class="form">
        <input type="text" id="name" placeholder="你的名字">
        <textarea id="message" rows="2" placeholder="输入消息..."></textarea>
        <button onclick="send()">发送</button>
    </div>
    <div id="messages"></div>
    <script>
        var socket = io();
        socket.on('new_message', function(data) {
            var div = document.createElement('div');
            div.className = 'msg';
            div.innerHTML = '<strong>' + data.name + ':</strong> ' + data.text;
            document.getElementById('messages').insertBefore(div, document.getElementById('messages').firstChild);
        });
        function send() {
            var name = document.getElementById('name').value || '匿名';
            var text = document.getElementById('message').value;
            if (!text) return;
            socket.emit('send_message', {name: name, text: text});
            document.getElementById('message').value = '';
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('send_message')
def handle_message(data):
    messages.append(data)
    if len(messages) > 50:
        messages.pop(0)
    emit('new_message', data, broadcast=True)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()

def run():
    ip = get_ip()
    print(f"\n{'='*50}")
    print(f"老四实时聊天!")
    print(f"手机访问: http://{ip}:5000")
    print(f"{'='*50}\n")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    run()
