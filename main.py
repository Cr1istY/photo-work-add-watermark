from core import *
from pathlib import Path


if __name__ == "__main__":
    path = 'imgs/input/YKW_3338.jpg'
    font_path = 'fonts/尔雅新大黑.ttf'

    add_exif_footer_left(
        Path(path),
        color=(90, 90, 90),
        font_ttf=Path(font_path),  # 按需修改
        bottom_crop_ratio=0.055,
    )

    print('done')