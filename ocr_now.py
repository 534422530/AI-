from PIL import ImageGrab, Image
import base64
import requests
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

def screenshot_compress():
    img = ImageGrab.grab()
    img = img.resize((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    quality = 75
    img.save(buf, format='JPEG', quality=quality)
    while len(buf.getvalue()) > 900000 and quality > 20:
        buf = io.BytesIO()
        quality -= 5
        img.save(buf, format='JPEG', quality=quality)
    path = r"C:\Users\lb\.laosi\screen.png"
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    return buf.getvalue()

def ocr_space(image_bytes, language='chs'):
    img_base64 = base64.b64encode(image_bytes).decode()
    try:
        resp = requests.post(
            'https://api.ocr.space/parse/image',
            data={
                'base64Image': f'data:image/jpeg;base64,{img_base64}',
                'language': language,
                'apikey': 'K82328918888957',
                'OCREngine': 2
            },
            timeout=60
        )
        result = resp.json()
        if result.get('ParsedResults'):
            return result['ParsedResults'][0].get('ParsedText', '')
        return f"Error: {result.get('ErrorMessage', result)}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("截屏中...")
    img_bytes = screenshot_compress()
    print("OCR识别中...")
    text = ocr_space(img_bytes)
    print("=" * 50)
    print(text)
    print("=" * 50)
    with open(r"C:\Users\lb\.laosi\ocr_result.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("结果已保存")
