from core import *
from pathlib import Path


# TODO: 字体美化
# TODO: 排版美化
# TODO: 多案例测试 - 字段多行

if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent

    path = HERE / 'imgs/input/YKW_3324.jpg'
    font_path = 'fonts/尔雅新大黑.ttf'
    out_path = HERE / 'imgs' / 'output'

    add_exif_footer_left(
        Path(path),
        color=(90, 90, 90),
        font_ttf=Path(font_path),  # 按需修改
        bottom_crop_ratio=0.055,
        out_path=out_path,
    )

    print('done')