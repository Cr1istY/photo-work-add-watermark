from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

# 1. 先算出“边框占总宽/高的比例”对应的像素值；
# 2. 用 ImageOps.expand 一次性填充；
# 3. 比例可自由调节。

def add_white_border(img_path: Path, ratio: float = 0.015, out_path: Path | None = None) -> Path:
    """
    按原图宽高 *ratio* 添加白色边框。
    例如 ratio=0.05 表示上下左右各加 5 % 的边。
    out_path 为 None 时，直接在原文件名后加 _border。
    """
    if out_path is None:
        out_path = img_path.with_stem(img_path.stem + "_border")

    with Image.open(img_path) as im:
        # 计算边框像素（四舍五入保证整数）
        border_h = int(round(im.height * ratio))
        border_w = int(round(im.width * ratio))
        left = border_w
        right = left
        top = border_h
        bottom = int(round(im.height * 0.18))

        # ImageOps.expand 四个边接受同一个数字时，上下左右均生效
        bordered = ImageOps.expand(im, border=(left, top, right, bottom), fill="white")
        bordered.save(out_path, quality=95, icc_profile=im.info.get("icc_profile"))

    return out_path
def add_bottom_border_watermark(
        img_path: Path,
        text: str = "©YourName",
        out_path: Path | None = None,
        font_size: int = 40,
        color: tuple[int, int, int] = (0, 0, 0),   # 浅灰，不扎眼
        font_ttf: Path | None = None
) -> Path:
    if out_path is None:
        out_path = img_path.with_stem(f"{img_path.stem}_signed")

    with Image.open(img_path) as im:
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(str(font_ttf), font_size) if font_ttf else ImageFont.load_default()

        # 文字宽高
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # 计算白边高度（之前 add_white_border 留下的）
        # 假设白边比例统一，用图片下半部分 1/2 区域作为“白边”估算
        border_h = im.height - int(im.height * 0.95)   # 5% 白边时约 0.95
        y = im.height - border_h // 2 - th // 2        # 垂直居中在白边
        x = (im.width - tw) // 2                       # 水平居中

        draw.text((x, y), text, font=font, fill=color)
        im.save(out_path, quality=95)
    return out_path




def add_bottom_border_and_white_border(img_path: Path, ratio: float = 0.015, out_path: Path | None = None, font_path: Path | None = None, font_size: int = 40) -> Path:
    """
    按原图宽高 *ratio* 添加白色边框。
    例如 ratio=0.05 表示上下左右各加 5 % 的边。
    out_path 为 None 时，直接在原文件名后加 _border。
    """
    if out_path is None:
        out_path = img_path.with_stem(img_path.stem + "_border")

    with Image.open(img_path) as im:
        # 计算边框像素（四舍五入保证整数）
        border_h = int(round(im.height * ratio))
        border_w = int(round(im.width * ratio))
        left = border_w
        right = left
        top = border_h
        bottom = int(round(im.height * 0.18))

        # ImageOps.expand 四个边接受同一个数字时，上下左右均生效
        bordered = ImageOps.expand(im, border=(left, top, right, bottom), fill="white")
        bordered.save(out_path, quality=100, icc_profile=im.info.get("icc_profile"))

        draw = ImageDraw.Draw(bordered)
        font = ImageFont.truetype(str(font_path), font_size) if font_path else ImageFont.load_default()

        # 文字宽高
        


    return out_path


