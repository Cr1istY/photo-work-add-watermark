from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
from camera import Camera

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
        if "exif" in im.info:
            bordered.save(out_path, quality=100, icc_profile=im.info.get("icc_profile"), exif=im.info["exif"])
        else:
            bordered.save(out_path, quality=100, icc_profile=im.info.get("icc_profile"))

    return out_path


def add_exif_footer(
    img_path: Path,
    out_path: Path | None = None,
    font_ttf: Path | None = None,
    color: tuple[int, int, int] = (100, 100, 100),
    bottom_crop_ratio: float = 0.012,   # 白边占整图比例
    output_quality: int = 100,
) -> Path:

    img_path = add_white_border(img_path)

    info = Camera(Path(img_path)).info
    focal = info.focal_length
    aperture = info.aperture_value
    shutter = info.exposure_time
    camera = info.model
    lens = info.lens_model
    creator = info.artist
    iso = info.iso


    """在底部白边内写入两行拍摄信息"""
    if out_path is None:
        out_path = img_path

    with Image.open(img_path) as im:
        # 字体参数自适应
        line_spacing = int(round(im.height * 0.005))
        font_size = int(round(im.height * 0.03))

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(str(font_ttf), font_size) if font_ttf else ImageFont.load_default()
        # 转换设备参数
        real_focal = focal[0] / focal[1]
        focal = f"{real_focal:.0f}"
        real_aperture = aperture[0] / aperture[1]
        aperture = f"{real_aperture:.2f}"
        shutter = f"1 / {shutter[1]}" if shutter[1] > 1 else f"{shutter[0]}"


        # 组装两行文字
        line1 = f"{focal} mm　|　f {aperture}　| {shutter} s |  iso: {iso}"
        line2 = f"{camera}　|　{lens}　| {creator}"

        # 测量尺寸
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        total_h = h1 + h2 + line_spacing

        # 白边区域
        border_h = int(im.height * bottom_crop_ratio)
        y0 = im.height - border_h + (border_h - total_h) // 2 - border_h

        # 画第一行
        x1 = (im.width - w1) // 2
        draw.text((x1, y0), line1, font=font, fill=color)
        # 画第二行
        x2 = (im.width - w2) // 2
        draw.text((x2, y0 + h1 + line_spacing), line2, font=font, fill=color)

        im.save(out_path, quality=output_quality, exif=im.info["exif"])
    return out_path

def add_exif_footer_left(
    img_path: Path,
    focal: tuple,
    aperture: tuple,
    shutter: tuple,
    camera: str,
    lens: str,
    creator: str,
    out_path: Path | None = None,
    font_ttf: Path | None = None,
    color: tuple[int, int, int] = (100, 100, 100),
    bottom_crop_ratio: float = 0.012,   # 白边占整图比例
    output_quality: int = 100,
) -> Path:

    img_path = add_white_border(img_path)

    """在底部白边内写入两行拍摄信息"""
    if out_path is None:
        out_path = img_path

    with Image.open(img_path) as im:
        # 字体参数自适应
        line_spacing = int(round(im.height * 0.005))
        font_size = int(round(im.height * 0.03))

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(str(font_ttf), font_size) if font_ttf else ImageFont.load_default()
        # 转换设备参数
        real_focal = focal[0] / focal[1]
        focal = f"{real_focal:.0f}"
        real_aperture = aperture[0] / aperture[1]
        aperture = f"{real_aperture:.2f}"
        shutter = f"1 / {shutter[1]}" if shutter[1] > 1 else f"{shutter[0]}"


        # 组装两行文字
        line1 = f"{focal} mm　|　f {aperture}　| {shutter} s | "
        line2 = f"{camera}　|　{lens}　| {creator}"





        # 测量尺寸
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        total_h = h1 + h2 + line_spacing

        # 白边区域
        border_h = int(im.height * bottom_crop_ratio)
        y0 = im.height - border_h + (border_h - total_h) // 2 - border_h

        # 画第一行
        x1 = (im.width - w1) // 2
        draw.text((x1, y0), line1, font=font, fill=color)
        # 画第二行
        x2 = (im.width - w2) // 2
        draw.text((x2, y0 + h1 + line_spacing), line2, font=font, fill=color)

        im.save(out_path, quality=output_quality)
    return out_path



