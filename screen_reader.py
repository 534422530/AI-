import os
import sys
from PIL import ImageGrab, Image
import base64
import requests
import io
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "last_screen.jpg")
RESULT_PATH = os.path.join(os.path.dirname(__file__), "last_ocr.txt")

def screenshot_region(x=0, y=0, width=None, height=None):
    img = ImageGrab.grab(bbox=(x, y, x + width if width else ImageGrab.grab().width, y + height if height else ImageGrab.grab().height))
    img = img.resize((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    quality = 75
    img.save(buf, format='JPEG', quality=quality)
    while len(buf.getvalue()) > 900000 and quality > 20:
        buf = io.BytesIO()
        quality -= 5
        img.save(buf, format='JPEG', quality=quality)
    with open(SCREENSHOT_PATH, 'wb') as f:
        f.write(buf.getvalue())
    return SCREENSHOT_PATH

def ocr_image(image_path, language='chs'):
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()
    try:
        resp = requests.post(
            'https://api.ocr.space/parse/image',
            data={'base64Image': f'data:image/jpeg;base64,{img_base64}', 'language': language, 'apikey': 'K82328918888957', 'OCREngine': 2},
            timeout=60
        )
        result = resp.json()
        if result.get('ParsedResults'):
            text = result['ParsedResults'][0].get('ParsedText', '')
            with open(RESULT_PATH, 'w', encoding='utf-8') as f:
                f.write(text)
            return text
        return f"Error: {result.get('ErrorMessage', result)}"
    except Exception as e:
        return f"Error: {e}"

def read_screen(region=None):
    if region:
        x, y, w, h = region
        img_path = screenshot_region(x, y, w, h)
    else:
        img_path = screenshot_region()
    return ocr_image(img_path)

def find_window(window_title):
    import subprocess
    result = subprocess.run(['powershell', '-Command', 
        f"Get-Process | Where-Object {{$_.MainWindowTitle -like '*{window_title}*'}} | Select-Object Id, MainWindowTitle"],
        capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "ocr":
            print(read_screen())
        elif cmd == "window":
            title = sys.argv[2] if len(sys.argv) > 2 else ""
            print(find_window(title))
    else:
        print(read_screen())
