"""
老四局域网聊天服务器
让手机/电脑通过浏览器发消息给我
"""

from flask import Flask, request, render_template_string
import threading
import socket

app = Flask(__name__)

# 消息存储
messages = []
lock = threading.Lock()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老四聊天</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        h1 { color: #333; }
        .form { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; box-sizing: border-box; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        .messages { background: white; padding: 20px; border-radius: 10px; }
        .msg { padding: 10px; margin: 5px 0; background: #e0e0e0; border-radius: 5px; }
        .msg.self { background: #d4edda; }
    </style>
</head>
<body>
    <h1>📱 老四聊天窗口</h1>
    <div class="form">
        <h3>发送消息给我</h3>
        <input type="text" id="name" placeholder="你的名字">
        <textarea id="message" rows="3" placeholder="输入消息..."></textarea>
        <button onclick="send()">发送</button>
    </div>
    <div class="messages">
        <h3>消息记录</h3>
        <div id="msgList">
            {% for msg in messages %}
            <div class="msg {% if msg.self %}self{% endif %}">
                <strong>{{ msg.name }}:</strong> {{ msg.text }}
            </div>
            {% endfor %}
        </div>
    </div>
    <script>
        function send() {
            var name = document.getElementById('name').value || '匿名';
            var text = document.getElementById('message').value;
            if (!text) return;
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, text: text})
            }).then(r => {
                document.getElementById('message').value = '';
                location.reload();
            });
        }
        setInterval(() => location.reload(), 5000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    with lock:
        return render_template_string(HTML, messages=messages[-20:])

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    with lock:
        messages.append({
            'name': data.get('name', '匿名'),
            'text': data.get('text', ''),
            'self': False
        })
    return {'ok': True}

def get_local_ip():
    """获取本机局域网IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_server(port=5000):
    ip = get_local_ip()
    print(f"="*50)
    print(f"老四聊天服务器已启动!")
    print(f"局域网访问: http://{ip}:{port}")
    print(f"或 http://localhost:{port}")
    print(f"="*50)
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_server()
