from enum import IntEnum

class ExposureProgram(IntEnum):
    """EXIF ExposureProgram tag (34850) 取值含义"""
    NOT_DEFINED   = 0
    MANUAL        = 1
    NORMAL        = 2
    APERTURE_PRIO = 3
    SHUTTER_PRIO  = 4
    CREATIVE      = 5
    ACTION        = 6
    PORTRAIT      = 7
    LANDSCAPE     = 8
    BULB          = 9

    def __str__(self):
        return _EP_STR_MAP.get(self, f"Unknown({self.value})")


_EP_STR_MAP = {
    ExposureProgram.NOT_DEFINED:   "未定义",
    ExposureProgram.MANUAL:        "手动曝光 (M)",
    ExposureProgram.NORMAL:        "程序自动 (P)",
    ExposureProgram.APERTURE_PRIO: "光圈优先 (A/Av)",
    ExposureProgram.SHUTTER_PRIO:  "快门优先 (S/Tv)",
    ExposureProgram.CREATIVE:      "创意程序 (景深优先)",
    ExposureProgram.ACTION:        "运动程序 (高速优先)",
    ExposureProgram.PORTRAIT:      "人像场景",
    ExposureProgram.LANDSCAPE:     "风景场景",
    ExposureProgram.BULB:          "B 门",
}


# 快速测试
if __name__ == "__main__":
    print(ExposureProgram(1))          # 输出: 手动曝光 (M)
    print(ExposureProgram.APERTURE_PRIO.value)  # 输出: 3