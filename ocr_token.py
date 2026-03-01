from PIL import ImageGrab, Image
import base64
import requests
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

def screenshot_token_area():
    img = ImageGrab.grab()
    width, height = img.size
    token_area = img.crop((width//4, height//3, width*3//4, height*2//3))
    token_area = token_area.resize((token_area.width * 2, token_area.height * 2), Image.Resampling.LANCZOS)
    path = r"C:\Users\lb\.laosi\token_area.png"
    token_area.save(path, 'PNG')
    buf = io.BytesIO()
    token_area.save(buf, format='PNG')
    return buf.getvalue()

def ocr_space(image_bytes, language='eng'):
    img_base64 = base64.b64encode(image_bytes).decode()
    try:
        resp = requests.post(
            'https://api.ocr.space/parse/image',
            data={
                'base64Image': f'data:image/png;base64,{img_base64}',
                'language': language,
                'apikey': 'K82328918888957',
                'OCREngine': 2,
                'isOverlayRequired': False
            },
            timeout=60
        )
        result = resp.json()
        if result.get('ParsedResults'):
            return result['ParsedResults'][0].get('ParsedText', '').strip()
        return f"Error: {result.get('ErrorMessage', result)}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("截取token区域...")
    img_bytes = screenshot_token_area()
    print("OCR识别(英文模式)...")
    text = ocr_space(img_bytes, 'eng')
    print("=" * 50)
    print("识别结果:")
    print(text)
    print("=" * 50)
    lines = text.replace(' ', '').replace('\n', '')
    print(f"去空格后: {lines}")
