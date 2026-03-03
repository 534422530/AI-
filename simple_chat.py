"""
老四简单聊天 - 稳定版
"""

from flask import Flask, request, Response

app = Flask(__name__)
msgs = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老四聊天</title>
    <style>
        body{font-family:Arial;margin:20px;background:#f5f5f5}
        h1{text-align:center}
        input,textarea{width:100%;padding:10px;margin:5px 0;box-sizing:border-box}
        button{background:#4CAF50;color:white;padding:15px;width:100%;border:none;font-size:18px}
        #msgs{background:white;padding:10px;margin-top:10px}
        .msg{padding:10px;background:#e8f5e9;margin:5px 0}
    </style>
</head>
<body>
    <h1>老四聊天</h1>
    <input id="name" placeholder="名字">
    <textarea id="text" rows="2" placeholder="消息"></textarea>
    <button onclick="send()">发送</button>
    <div id="msgs"></div>
    <script>
        function send(){
            var n=document.getElementById('name').value||'匿名';
            var t=document.getElementById('text').value;
            if(!t)return;
            fetch('/send?name='+encodeURIComponent(n)+'&text='+encodeURIComponent(t));
            document.getElementById('text').value='';
            load();
        }
        function load(){
            fetch('/msgs').then(r=>r.json()).then(d=>{
                document.getElementById('msgs').innerHTML=d.map(m=>
                    '<div class="msg"><b>'+m.name+':</b>'+m.text+'</div>'
                ).join('');
            });
        }
        setInterval(load,1000);
        load();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/send')
def send():
    msgs.insert(0, {'name': request.args.get('name', '匿名'), 'text': request.args.get('text', '')})
    return 'ok'

@app.route('/msgs')
def get_msgs():
    import json
    return msgs[:50]

@app.route('/wwRTVerify.txt')
def verify():
    return Response('企业微信域名验证', mimetype='text/plain')

if __name__ == '__main__':
    print('\n老四聊天启动!')
    print('访问: http://192.168.1.6:5000')
    app.run(host='0.0.0.0', port=5000)
