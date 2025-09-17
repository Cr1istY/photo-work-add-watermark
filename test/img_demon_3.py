from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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


if __name__ == "__main__":
    path = '../imgs/input/YKW_3338_border.jpg'
    font_path = '../fonts/ELEPHNT.TTF'
    add_bottom_border_watermark(Path(path), "crist", font_size=100, font_ttf=Path(font_path))