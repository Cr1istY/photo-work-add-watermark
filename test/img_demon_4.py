from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def add_exif_footer(
    img_path: Path,
    focal: str,
    aperture: str,
    shutter: str,
    camera: str,
    lens: str,
    creator: str,
    out_path: Path | None = None,
    font_ttf: Path | None = None,
    font_size: int = 36,
    color: tuple[int, int, int] = (100, 100, 100),
    bottom_crop_ratio: float = 0.06,   # 白边占整图比例
    line_spacing: int = 8,             # 两行文字之间额外像素
    side_margin: int = 60,             # 左右留空
    output_quality: int = 95,
    up_offset: int = 0,
) -> Path:
    """在底部白边内写入两行拍摄信息"""
    if out_path is None:
        out_path = img_path.with_stem(f"{img_path.stem}_exif")

    with Image.open(img_path) as im:
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(str(font_ttf), font_size) if font_ttf else ImageFont.load_default()

        # 组装两行文字
        line1 = f"焦距 {focal}　|　光圈 {aperture}　|　快门 {shutter}"
        line2 = f"{camera}　|　{lens}　|　创 {creator}"

        # 测量尺寸
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        total_h = h1 + h2 + line_spacing

        # 白边区域
        border_h = int(im.height * bottom_crop_ratio)
        y0 = im.height - border_h + (border_h - total_h) // 2 - up_offset

        # 画第一行
        x1 = (im.width - w1) // 2
        draw.text((x1, y0), line1, font=font, fill=color)
        # 画第二行
        x2 = (im.width - w2) // 2
        draw.text((x2, y0 + h1 + line_spacing), line2, font=font, fill=color)

        im.save(out_path, quality=output_quality)
    return out_path


# ------------------ 调用示例 ------------------
if __name__ == "__main__":
    path = '../imgs/input/YKW_3338_border.jpg'
    font_path = '../fonts/尔雅新大黑.ttf'
    add_exif_footer(
        Path(path),
        focal="35 mm",
        aperture="f/1.8",
        shutter="1/2000 s",
        camera="NIKON Z 50",
        lens="NIKKOR Z DX 16-50 mm f/3.5-6.3 VR",
        creator="CristY",
        font_size=100,
        color=(90, 90, 90),
        font_ttf=Path(font_path),  # 按需修改
        bottom_crop_ratio=0.055,
        up_offset=50,
    )