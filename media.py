from PIL import Image, ImageDraw, ImageFont
from core import ROOT
from io import BytesIO
def banner(product):
    im=Image.new('RGB',(900,450),'#15263d'); d=ImageDraw.Draw(im)
    photo=Image.open(ROOT/'images'/f"{product['id']}.png").convert('RGB'); photo.thumbnail((380,380)); im.paste(photo,(480,35))
    def font(n):
        try: return ImageFont.truetype('DejaVuSans.ttf',n)
        except OSError: return ImageFont.load_default()
    d.text((35,70),'SHOP TODAY',font=font(30),fill='#78dfc5'); d.text((35,145),product['name'],font=font(48),fill='white'); d.text((35,230),f"INR {product['price']:,}",font=font(40),fill='white'); d.text((35,340),'Discover your next favourite',font=font(20),fill='white')
    out=BytesIO(); im.save(out,format='PNG'); return out.getvalue()
def speech(text):
    from gtts import gTTS
    out=BytesIO(); gTTS(text.replace('₹',' rupees '),lang='en').write_to_fp(out); return out.getvalue()
