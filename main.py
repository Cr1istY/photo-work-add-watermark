from core.core import *
from core.po.camera import Camera
from pathlib import Path


if __name__ == "__main__":
    path = 'imgs/input/YKW_3338.jpg'
    font_path = 'fonts/尔雅新大黑.ttf'
    info = Camera(Path(path)).info
    focal = str(info.focal_length)
    aperture = str(info.aperture_value)
    shutter = str(info.exposure_time)
    camera = info.model
    lens = info.lens_model
    creator = info.artist

    new_path = add_white_border(Path(path))

    add_exif_footer(
        new_path,
        focal,
        aperture,
        shutter,
        camera,
        lens,
        creator,
        font_size=100,
        color=(90, 90, 90),
        font_ttf=Path(font_path),  # 按需修改
        bottom_crop_ratio=0.055,
        up_offset=50,
    )

    print('done')