"""
老四语音聊天系统
手机扫码访问 + 语音识别
"""

from flask import Flask, request, render_template_string
import socket
import qrcode
import io
import base64
import threading

app = Flask(__name__)
messages = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老四语音聊天</title>
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 500px; margin: 0 auto; }
        h1 { text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .form { background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        input { width: 100%; padding: 12px; margin: 10px 0; box-sizing: border-box; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        .voice-btn { 
            width: 100%; padding: 20px; background: #ff6b6b; color: white; border: none; 
            border-radius: 10px; font-size: 18px; cursor: pointer; margin: 10px 0;
        }
        .voice-btn:active { background: #ee5a5a; }
        .voice-btn.recording { background: #ff0000; animation: pulse 1s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        #messages { background: white; padding: 15px; border-radius: 15px; }
        .msg { padding: 12px; margin: 8px 0; background: #f0f0f0; border-radius: 8px; }
        .msg.self { background: #d4edda; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 老四语音聊天</h1>
        <div class="form">
            <input type="text" id="name" placeholder="你的名字">
            <input type="text" id="text_msg" placeholder="或输入文字">
            <button class="voice-btn" id="voiceBtn" onclick="startVoice()">🎤 按住说话</button>
            <button onclick="sendText()" style="width:100%;padding:12px;background:#4CAF50;color:white;border:none;border-radius:8px;">发送</button>
        </div>
        <div id="messages"></div>
    </div>
    <script>
        var recognition = null;
        var isRecording = false;
        
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'zh-CN';
            recognition.onresult = function(e) {
                var text = e.results[0][0].transcript;
                sendMsg(text);
            };
            recognition.onend = function() {
                isRecording = false;
                document.getElementById('voiceBtn').classList.remove('recording');
                document.getElementById('voiceBtn').innerText = '🎤 按住说话';
            };
        }
        
        function startVoice() {
            if (!recognition) {
                alert('请用Chrome浏览器');
                return;
            }
            if (isRecording) {
                recognition.stop();
            } else {
                isRecording = true;
                document.getElementById('voiceBtn').classList.add('recording');
                document.getElementById('voiceBtn').innerText = '🔴 录音中...';
                recognition.start();
            }
        }
        
        function sendText() {
            var text = document.getElementById('text_msg').value;
            if (text) sendMsg(text);
        }
        
        function sendMsg(text) {
            var name = document.getElementById('name').value || '匿名';
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'name=' + encodeURIComponent(name) + '&text=' + encodeURIComponent(text)
            }).then(() => {
                document.getElementById('text_msg').value = '';
                loadMsgs();
            });
        }
        
        function loadMsgs() {
            fetch('/msgs').then(r => r.json()).then(data => {
                document.getElementById('messages').innerHTML = data.map(m => 
                    '<div class="msg self"><strong>' + m.name + ':</strong> ' + m.text + '</div>'
                ).join('');
            });
        }
        
        setInterval(loadMsgs, 1000);
        loadMsgs();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/send', methods=['POST'])
def send():
    name = request.form.get('name', '匿名')
    text = request.form.get('text', '')
    messages.insert(0, {'name': name, 'text': text})
    return 'ok'

@app.route('/msgs')
def msgs():
    import json
    return messages[:20]

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()

def generate_qr(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

def run():
    ip = get_ip()
    url = f"http://{ip}:5000"
    qr_b64 = generate_qr(url)
    
    print(f"\n{'='*50}")
    print(f"老四语音聊天系统!")
    print(f"手机扫码访问: {url}")
    print(f"{'='*50}\n")
    
    # 保存二维码到桌面
    with open(r'C:\Users\lb\Desktop\laosi_qr.png', 'wb') as f:
        f.write(base64.b64decode(qr_b64))
    print(f"二维码已保存到桌面: laosi_qr.png")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    run()
