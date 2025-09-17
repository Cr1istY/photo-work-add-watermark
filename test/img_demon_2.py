from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def add_text_watermark(
        img_path: Path,
        text: str = "©YourName",
        out_path: Path | None = None,
        margin: int = 20,               # 离边缘距离
        font_size: int = 36,
        color: tuple[int, int, int, int] = (0, 0, 0, 128),  # RGBA
        font_ttf: Path | None = None
) -> Path:
    if out_path is None:
        out_path = img_path.with_stem(f"{img_path.stem}_wm")

    # 打开图片并转成 RGBA 以便加透明度
    with Image.open(img_path).convert("RGBA") as base:
        txt_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)

        font = ImageFont.truetype(str(font_ttf), font_size) if font_ttf else ImageFont.load_default()
        # 计算文字宽高
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x = base.width - w - margin
        y = base.height - h - margin
        draw.text((x, y), text, font=font, fill=color)

        # 合并并保存
        watermarked = Image.alpha_composite(base, txt_layer).convert("RGB")
        watermarked.save(out_path, quality=95)
    return out_path


if __name__ == "__main__":
    path = '../imgs/input/YKW_3338_border.jpg'
    font_path = '../fonts/AcadEref.ttf'
    add_text_watermark(Path(path), "crist", font_size=100, font_ttf=Path(font_path))



