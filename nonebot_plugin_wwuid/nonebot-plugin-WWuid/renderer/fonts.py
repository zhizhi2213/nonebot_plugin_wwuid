# coding=utf-8
"""
字体定义
从原项目XutheringWavesUID复制
"""
from pathlib import Path
from PIL import ImageFont

# 字体路径
FONT_ORIGIN_PATH = Path(__file__).parent.parent / "resources" / "fonts" / "waves_fonts.ttf"
FONT2_ORIGIN_PATH = Path(__file__).parent.parent / "resources" / "fonts" / "arial-unicode-ms-bold.ttf"
EMOJI_ORIGIN_PATH = Path(__file__).parent.parent / "resources" / "fonts" / "NotoColorEmoji.ttf"


def waves_font_origin(size: int) -> ImageFont.FreeTypeFont:
    """获取主字体"""
    if FONT_ORIGIN_PATH.exists():
        return ImageFont.truetype(str(FONT_ORIGIN_PATH), size=size)
    else:
        # 回退到系统字体
        try:
            return ImageFont.truetype("msyh.ttc", size=size)
        except:
            return ImageFont.load_default()


def ww_font_origin(size: int) -> ImageFont.FreeTypeFont:
    """获取备用字体"""
    if FONT2_ORIGIN_PATH.exists():
        return ImageFont.truetype(str(FONT2_ORIGIN_PATH), size=size)
    else:
        try:
            return ImageFont.truetype("msyh.ttc", size=size)
        except:
            return ImageFont.load_default()


def emoji_font_origin(size: int) -> ImageFont.FreeTypeFont:
    """获取emoji字体"""
    if EMOJI_ORIGIN_PATH.exists():
        return ImageFont.truetype(str(EMOJI_ORIGIN_PATH), size=size)
    else:
        return ImageFont.load_default()


# 预定义字体大小
waves_font_10 = waves_font_origin(10)
waves_font_12 = waves_font_origin(12)
waves_font_14 = waves_font_origin(14)
waves_font_16 = waves_font_origin(16)
waves_font_15 = waves_font_origin(15)
waves_font_18 = waves_font_origin(18)
waves_font_20 = waves_font_origin(20)
waves_font_22 = waves_font_origin(22)
waves_font_23 = waves_font_origin(23)
waves_font_24 = waves_font_origin(24)
waves_font_25 = waves_font_origin(25)
waves_font_26 = waves_font_origin(26)
waves_font_28 = waves_font_origin(28)
waves_font_30 = waves_font_origin(30)
waves_font_32 = waves_font_origin(32)
waves_font_34 = waves_font_origin(34)
waves_font_36 = waves_font_origin(36)
waves_font_38 = waves_font_origin(38)
waves_font_40 = waves_font_origin(40)
waves_font_42 = waves_font_origin(42)
waves_font_44 = waves_font_origin(44)
waves_font_50 = waves_font_origin(50)
waves_font_58 = waves_font_origin(58)
waves_font_60 = waves_font_origin(60)
waves_font_62 = waves_font_origin(62)
waves_font_70 = waves_font_origin(70)
waves_font_84 = waves_font_origin(84)

ww_font_12 = ww_font_origin(12)
ww_font_14 = ww_font_origin(14)
ww_font_16 = ww_font_origin(16)
ww_font_15 = ww_font_origin(15)
ww_font_18 = ww_font_origin(18)
ww_font_20 = ww_font_origin(20)
ww_font_22 = ww_font_origin(22)
ww_font_23 = ww_font_origin(23)
ww_font_24 = ww_font_origin(24)
ww_font_25 = ww_font_origin(25)
ww_font_26 = ww_font_origin(26)
ww_font_28 = ww_font_origin(28)
ww_font_30 = ww_font_origin(30)
ww_font_32 = ww_font_origin(32)
ww_font_34 = ww_font_origin(34)
ww_font_36 = ww_font_origin(36)
ww_font_38 = ww_font_origin(38)
ww_font_40 = ww_font_origin(40)
ww_font_42 = ww_font_origin(42)
ww_font_44 = ww_font_origin(44)
ww_font_50 = ww_font_origin(50)
ww_font_58 = ww_font_origin(58)
ww_font_60 = ww_font_origin(60)
ww_font_62 = ww_font_origin(62)
ww_font_70 = ww_font_origin(70)
ww_font_84 = ww_font_origin(84)

emoji_font = emoji_font_origin(109)
