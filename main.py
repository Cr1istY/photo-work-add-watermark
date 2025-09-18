from core.core import *
from core.po.camera import Camera
from pathlib import Path


if __name__ == "__main__":
    path = 'imgs/input/YKW_3338.jpg'
    font_path = 'fonts/尔雅新大黑.ttf'
    info = Camera(Path(path)).info
    focal = info.focal_length
    aperture = info.aperture_value
    shutter = info.exposure_time
    camera = info.model
    lens = info.lens_model
    creator = info.artist

    add_exif_footer(
        Path(path),
        focal,
        aperture,
        shutter,
        camera,
        lens,
        creator,
        color=(90, 90, 90),
        font_ttf=Path(font_path),  # 按需修改
        bottom_crop_ratio=0.055,
    )

    print('done')