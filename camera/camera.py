from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Optional, Tuple

import piexif


# ------------------ 拍摄方式枚举 ------------------
class ExposureProgram(IntEnum):
    NOT_DEFINED = 0
    MANUAL = 1
    NORMAL = 2
    APERTURE_PRIO = 3
    SHUTTER_PRIO = 4
    CREATIVE = 5
    ACTION = 6
    PORTRAIT = 7
    LANDSCAPE = 8
    BULB = 9


# ------------------ 数据结构 ------------------
@dataclass(slots=True)
class PhotoInfo:
    make: Optional[str] = None
    model: Optional[str] = None
    artist: Optional[str] = None
    lens_model: Optional[str] = None
    exposure_time: Optional[Tuple[int, int]] = None
    aperture_value: Optional[Tuple[int, int]] = None
    iso: Optional[int] = None
    focal_length: Optional[Tuple[int, int]] = None
    exposure_program: Optional[ExposureProgram] = None

    # ---------- 友好显示 ----------
    @property
    def exposure_str(self) -> str:
        if self.exposure_time:
            n, d = self.exposure_time
            return f"{n}/{d} s" if d != 1 else f"{n} s"
        return "N/A"

    @property
    def aperture_str(self) -> str:
        if self.aperture_value:
            n, d = self.aperture_value
            return f"f/{n / d:.1f}"
        return "N/A"

    @property
    def focal_str(self) -> str:
        if self.focal_length:
            n, d = self.focal_length
            return f"{n / d:.1f} mm"
        return "N/A"


# ------------------ 核心类 ------------------
class Camera:
    __slots__ = ("img_path", "_info")

    def __init__(self, img_path: Path):
        self.img_path = img_path
        self._info: Optional[PhotoInfo] = None
        self._parse()

    # -------------- 公有入口 --------------
    @property
    def info(self) -> PhotoInfo:
        """返回解析后的 PhotoInfo；解析失败则返回全 None 的实例。"""
        return self._info or PhotoInfo()

    # -------------- 内部 --------------
    def _parse(self) -> None:
        try:
            raw = piexif.load(str(self.img_path))
        except Exception:  # 文件损坏或非图片
            self._info = None
            return

        self._info = PhotoInfo(
            make=self._str(raw, "0th", piexif.ImageIFD.Make),
            model=self._str(raw, "0th", piexif.ImageIFD.Model),
            artist=self._str(raw, "0th", piexif.ImageIFD.Artist),
            lens_model=self._str(raw, "Exif", piexif.ExifIFD.LensModel),
            exposure_time=self._ratio(raw, "Exif", piexif.ExifIFD.ExposureTime),
            aperture_value=self._ratio(raw, "Exif", piexif.ExifIFD.FNumber),
            iso=self._int(raw, "Exif", piexif.ExifIFD.ISOSpeedRatings),
            focal_length=self._ratio(raw, "Exif", piexif.ExifIFD.FocalLength),
            exposure_program=self._enum(raw, "Exif", piexif.ExifIFD.ExposureProgram, ExposureProgram),
        )

    # ---------- 静态小工具 ----------
    @staticmethod
    def _get(group: dict, tag: int):
        return group.get(tag)

    @staticmethod
    def _str(raw: dict, which: str, tag: int) -> Optional[str]:
        val = Camera._get(raw.get(which, {}), tag)
        if val:
            return val.decode() if isinstance(val, bytes) else str(val)
        return None

    @staticmethod
    def _int(raw: dict, which: str, tag: int) -> Optional[int]:
        val = Camera._get(raw.get(which, {}), tag)
        return int(val) if val else None

    @staticmethod
    def _ratio(raw: dict, which: str, tag: int) -> Optional[Tuple[int, int]]:
        val = Camera._get(raw.get(which, {}), tag)
        if val and len(val) == 2:
            return int(val[0]), int(val[1])  # (numerator, denominator)
        return None

    @staticmethod
    def _enum(raw: dict, which: str, tag: int, enum_cls):
        val = Camera._int(raw, which, tag)
        return enum_cls(val) if val is not None else None


# ------------------ demo ------------------
if __name__ == "__main__":
    cam = Camera(Path("../imgs/input/YKW_3338.jpg"))
    info = cam.info
    print(info.model)
    print("曝光:", info.exposure_str, "光圈:", info.aperture_str, "焦距:", info.focal_str)