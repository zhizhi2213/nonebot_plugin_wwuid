# coding=utf-8
"""
图片工具函数和字体定义
"""
import io
import asyncio
import httpx
import shutil
import concurrent.futures
from pathlib import Path
from typing import Optional, Tuple, Union, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# --- 字体定义 ---
# 字体路径
FONT_ORIGIN_PATH = Path(__file__).parent / "assets" / "fonts" / "waves_fonts.ttf"
FONT2_ORIGIN_PATH = Path(__file__).parent / "assets" / "fonts" / "arial-unicode-ms-bold.ttf"
EMOJI_ORIGIN_PATH = Path(__file__).parent / "assets" / "fonts" / "NotoColorEmoji.ttf"


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

# --- 资源路径定义 ---
CHARINFO_PATH = Path(__file__).parent / "assets" / "images" / "charinfo"
BG_PATH = Path(__file__).parent / "assets" / "backgrounds"
FONTS_PATH = Path(__file__).parent / "assets" / "fonts"
CACHE_PATH = Path(__file__).parent / "cache"

# --- 缓存子路径 ---
AVATAR_CACHE_PATH = CACHE_PATH / "avatars"
SKILL_CACHE_PATH = CACHE_PATH / "skills"
PHANTOM_CACHE_PATH = CACHE_PATH / "phantoms"
CHAIN_CACHE_PATH = CACHE_PATH / "chains"
WEAPON_CACHE_PATH = CACHE_PATH / "weapons"

# 确保缓存目录存在
for p in [AVATAR_CACHE_PATH, SKILL_CACHE_PATH, PHANTOM_CACHE_PATH, CHAIN_CACHE_PATH, WEAPON_CACHE_PATH]:
    p.mkdir(parents=True, exist_ok=True)


async def _download_and_cache(url: str, cache_file: Path) -> Optional[Image.Image]:
    """通用的下载并缓存图片函数"""
    if not url:
        return None
    
    # 如果已经缓存，直接返回
    if cache_file.exists():
        try:
            return Image.open(cache_file).convert('RGBA')
        except Exception as e:
            logger.warning(f"读取缓存图片失败 {cache_file}: {e}")
            cache_file.unlink() # 删除损坏的缓存
    
    # 下载图片
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code == 200:
                img_data = response.content
                img = Image.open(io.BytesIO(img_data)).convert('RGBA')
                # 写入缓存
                with open(cache_file, 'wb') as f:
                    f.write(img_data)
                return img
            else:
                logger.warning(f"下载图片失败 {url}: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"下载并缓存图片出现异常 {url}: {e}")
    
    return None


def _download_and_cache_sync(url: str, cache_file: Path) -> Optional[Image.Image]:
    """通用的下载并缓存图片函数 (同步版本)"""
    if not url:
        return None
    
    # 如果已经缓存，直接返回
    if cache_file.exists():
        try:
            return Image.open(cache_file).convert('RGBA')
        except Exception as e:
            logger.warning(f"读取缓存图片失败 {cache_file}: {e}")
            cache_file.unlink()
    
    # 下载图片
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.get(url)
            if response.status_code == 200:
                img_data = response.content
                img = Image.open(io.BytesIO(img_data)).convert('RGBA')
                # 写入缓存
                with open(cache_file, 'wb') as f:
                    f.write(img_data)
                return img
            else:
                logger.warning(f"下载图片失败 {url}: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"下载并缓存图片出现异常 {url}: {e}")
    
    return None


def get_waves_bg(size: Tuple[int, int] = (1900, 1900)) -> Image.Image:
    """获取鸣潮背景图片"""
    # 尝试加载原项目的背景
    bg_files = ['bg3.jpg', 'bg2.jpg', 'bg1.jpg']
    for bg_file in bg_files:
        bg_path = BG_PATH / bg_file
        if bg_path.exists():
            try:
                bg = Image.open(bg_path).convert('RGBA')
                return bg.resize(size, Image.Resampling.LANCZOS)
            except Exception as e:
                logger.warning(f"加载背景图片失败 {bg_file}: {e}")
    
    # 回退到纯色背景
    bg = Image.new('RGBA', size, (30, 30, 40, 255))
    return bg


def get_attribute_icon(attribute_id: int) -> Optional[Image.Image]:
    """获取属性图标"""
    # 属性ID映射（中文文件名）
    attr_map = {
        1: '衍射',      # 光
        2: '湮灭',       # 暗
        3: '气动',       # 风
        4: '热熔',       # 火
        5: '冷凝',        # 冰
        6: '导电',   # 雷
    }
    attr_name = attr_map.get(attribute_id, '衍射')
    
    icon_path = BG_PATH / 'attribute' / f'attr_{attr_name}.png'
    if icon_path.exists():
        try:
            return Image.open(icon_path).convert("RGBA")
        except Exception as e:
            logger.warning(f"加载属性图标失败: {e}")
    return None


def get_weapon_type_icon(weapon_type_id: int) -> Optional[Image.Image]:
    """获取武器类型图标"""
    # 武器类型映射（中文文件名）
    weapon_map = {
        1: '长刃',
        2: '迅刀',
        3: '佩枪',
        4: '臂铠',
        5: '音感仪',
    }
    weapon_name = weapon_map.get(weapon_type_id, '长刃')
    
    icon_path = BG_PATH / 'weapon_type' / f'weapon_type_{weapon_name}.png'
    if icon_path.exists():
        try:
            return Image.open(icon_path).convert("RGBA")
        except Exception as e:
            logger.warning(f"加载武器图标失败: {e}")
    return None


def load_resource_image(name: str) -> Optional[Image.Image]:
    """加载资源图片"""
    img_path = CHARINFO_PATH / name
    if img_path.exists():
        try:
            return Image.open(img_path).convert('RGBA')
        except Exception as e:
            logger.warning(f"加载资源图片失败 {name}: {e}")
    return None


def draw_text_with_shadow(
    img: Image.Image,
    text: str,
    position: Tuple[int, int],
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int, int] = (255, 255, 255, 255),
    shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 180),
    shadow_offset: Tuple[int, int] = (2, 2),
    anchor: str = "lt"
) -> None:
    """绘制带阴影的文字"""
    draw = ImageDraw.Draw(img)
    
    # 绘制阴影
    shadow_pos = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
    draw.text(shadow_pos, text, font=font, fill=shadow_color, anchor=anchor)
    
    # 绘制主文字
    draw.text(position, text, font=font, fill=fill, anchor=anchor)


def add_footer(img: Image.Image, text: str = "NoneBot-Plugin-WWuid") -> Image.Image:
    """添加页脚"""
    draw = ImageDraw.Draw(img)
    font = waves_font_origin(20)
    
    # 页脚文字位置（右下角）
    text_pos = (img.width - 20, img.height - 20)
    draw.text(text_pos, text, font=font, fill=(200, 200, 200, 150), anchor="rb")
    
    return img


def crop_center_img(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """中心裁剪图片"""
    img_w, img_h = img.size
    target_w, target_h = size
    
    # 计算裁剪区域
    left = (img_w - target_w) // 2
    top = (img_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    
    return img.crop((left, top, right, bottom))


def resize_and_center_image(
    img: Image.Image,
    target_size: Tuple[int, int],
    bg_color: Tuple[int, int, int, int] = (0, 0, 0, 0)
) -> Image.Image:
    """调整图片尺寸并居中"""
    # 创建目标尺寸的背景
    result = Image.new('RGBA', target_size, bg_color)
    
    # 计算缩放比例
    img_w, img_h = img.size
    target_w, target_h = target_size
    
    scale = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    # 缩放图片
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 居中粘贴
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    result.paste(resized, (paste_x, paste_y), resized)
    
    return result


def create_rounded_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    """创建圆角遮罩"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def apply_blur(img: Image.Image, radius: int = 5) -> Image.Image:
    """应用模糊效果"""
    return img.filter(ImageFilter.GaussianBlur(radius))


async def get_role_picture(role_pic_url: Optional[str] = None, role_id: Optional[int] = None) -> Optional[Image.Image]:
    """获取角色立绘图片"""
    if not role_pic_url or not role_id:
        return None
    cache_file = AVATAR_CACHE_PATH / f"role_{role_id}.png"
    return await _download_and_cache(role_pic_url, cache_file)


def get_role_picture_sync(role_pic_url: Optional[str] = None, role_id: Optional[int] = None) -> Optional[Image.Image]:
    """同步获取角色立绘图片"""
    if not role_pic_url or not role_id:
        return None
    cache_file = AVATAR_CACHE_PATH / f"role_{role_id}.png"
    return _download_and_cache_sync(role_pic_url, cache_file)

def get_avatar_sync(avatar_url: Optional[str], uid: Optional[str]) -> Optional[Image.Image]:
    """同步获取账号头像"""
    if not avatar_url or not uid:
        return None
    cache_file = AVATAR_CACHE_PATH / f"avatar_{uid}.png"
    return _download_and_cache_sync(avatar_url, cache_file)

async def get_skill_icon_async(skill_id: int, icon_url: str) -> Optional[Image.Image]:
    """异步获取技能图标"""
    if not icon_url:
        return None
    cache_file = SKILL_CACHE_PATH / f"skill_{skill_id}.png"
    return await _download_and_cache(icon_url, cache_file)


def get_skill_icon_sync(skill_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取技能图标"""
    if not icon_url:
        return None
    cache_file = SKILL_CACHE_PATH / f"skill_{skill_id}.png"
    return _download_and_cache_sync(icon_url, cache_file)


async def get_phantom_icon_async(phantom_id: int, icon_url: str) -> Optional[Image.Image]:
    """异步获取声骸图标"""
    if not icon_url:
        return None
    cache_file = PHANTOM_CACHE_PATH / f"phantom_{phantom_id}.png"
    return await _download_and_cache(icon_url, cache_file)


def get_phantom_icon_sync(phantom_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取声骸图标"""
    if not icon_url:
        return None
    cache_file = PHANTOM_CACHE_PATH / f"phantom_{phantom_id}.png"
    return _download_and_cache_sync(icon_url, cache_file)


async def get_chain_icon_async(chain_order: int, icon_url: str) -> Optional[Image.Image]:
    """异步获取命座图标"""
    if not icon_url:
        return None
    cache_file = CHAIN_CACHE_PATH / f"chain_{chain_order}.png"
    return await _download_and_cache(icon_url, cache_file)


def get_chain_icon_sync(chain_order: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取命座图标"""
    if not icon_url:
        return None
    cache_file = CHAIN_CACHE_PATH / f"chain_{chain_order}.png"
    return _download_and_cache_sync(icon_url, cache_file)


async def get_weapon_icon_async(weapon_id: int, icon_url: str) -> Optional[Image.Image]:
    """异步获取武器图标"""
    if not icon_url:
        return None
    cache_file = WEAPON_CACHE_PATH / f"weapon_{weapon_id}.png"
    return await _download_and_cache(icon_url, cache_file)


def get_weapon_icon_sync(weapon_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取武器图标"""
    if not icon_url:
        return None
    cache_file = WEAPON_CACHE_PATH / f"weapon_{weapon_id}.png"
    return _download_and_cache_sync(icon_url, cache_file)
