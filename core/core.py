from pathlib import Path
from PIL import Image, ImageOps

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

