#!/usr/bin/env python3
"""
批量给图片加白框 + 文字水印 + 品牌 logo。
Pillow ≥ 10 兼容，无 textsize。
"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import piexif

# ----------- 自己按需要改的路径 -----------
SRC_DIR      = Path(r'../imgs/input')          # 原图文件夹
OUT_DIR      = Path(r'../imgs/output')  # 输出文件夹
LOGO_DIR     = Path(r'../imgs/logo')           # 品牌 logo 文件夹（PNG，透明底）
FONT_PATH    = r'C:\Windows\Fonts\msyhbd.ttc'  # win11 示例
# ----------------------------------------

BORDER_RATIO = 0.04          # 边框宽度 = 长边 * 比例
FONT_SIZE_PT = 32
TEXT_MARGIN  = 30            # 文字离右下边缘距离
LOGO_MARGIN  = 25            # logo 离左下边缘距离

# 品牌→logo 文件名映射（不区分大小写）
BRAND_MAP = {
    # 'canon': 'canon.png',
    'nikon': 'nikon_1.png',
    # 'sony': 'sony.png',
    # 'fujifilm': 'fujifilm.png',
    # 'panasonic': 'lumix.png',
}

def _get_make_model(image_path: Path):
    """返回 (make, model) 字符串，读取失败返回 ('', '')"""
    try:
        exif = piexif.load(str(image_path))
        zeroth = exif.get('0th', {})
        make  = zeroth.get(piexif.ImageIFD.Make, b'').decode('utf-8').strip()
        model = zeroth.get(piexif.ImageIFD.Model, b'').decode('utf-8').strip()
        return make, model
    except Exception:
        return '', ''

def _text_size(text: str, font: ImageFont.FreeTypeFont):
    """Pillow ≥ 10 兼容：返回 (width, height)"""
    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1), 0)).textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def _pick_logo(make: str):
    """根据品牌名返回 logo 路径，没有返回 None"""
    if not make:
        return None
    key = make.lower()
    for k, v in BRAND_MAP.items():
        if k in key:
            return LOGO_DIR / v
    return None

def process_one(img_path: Path, out_path: Path):
    """单张图加框+水印+logo"""
    with Image.open(img_path) as im:
        im = im.convert('RGB')
        long = max(im.size)
        border = int(long * BORDER_RATIO)
        new_w  = im.width  + 2 * border
        new_h  = im.height + 2 * border

        canvas = Image.new('RGB', (new_w, new_h), (255, 255, 255))
        canvas.paste(im, (border, border))

        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE_PT)

        # 文字内容
        make, model = _get_make_model(img_path)
        text = f'Shot on {make} {model}'.strip()
        if not make:
            text = ''

        # 文字尺寸
        tw, th = _text_size(text, font)
        text_x = new_w - tw - TEXT_MARGIN
        text_y = new_h - th - TEXT_MARGIN
        draw.text((text_x, text_y), text, fill=(80, 80, 80), font=font)

        # logo
        logo_path = _pick_logo(make)
        if logo_path and logo_path.exists():
            with Image.open(logo_path) as logo:
                logo = logo.convert('RGBA')
                # 让 logo 高度 = 文字高度
                ratio = th / logo.height
                logo_w, logo_h = int(logo.width * ratio), int(logo.height * ratio)
                logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

                # 左下角定位
                lx = LOGO_MARGIN
                ly = new_h - logo_h - LOGO_MARGIN
                canvas.paste(logo, (lx, ly), logo)

        canvas.save(out_path, quality=95)
        print(f'saved -> {out_path}')

def main():
    OUT_DIR.mkdir(exist_ok=True)
    LOGO_DIR.mkdir(exist_ok=True)

    for ext in ('*.jpg', '*.jpeg', '*.JPG', '*.JPEG'):
        for file in SRC_DIR.glob(ext):
            out_file = OUT_DIR / (file.stem + '_wm.jpg')
            try:
                process_one(file, out_file)
            except Exception as e:
                print(f'FAIL {file}: {e}', file=sys.stderr)

if __name__ == '__main__':
    main()