# coding=utf-8
"""
图片工具函数（简化版）
参考原项目XutheringWavesUID的实现
"""
import io
from pathlib import Path
from typing import Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

try:
    from ..utils.resource_mgr import (
        CHARINFO_PATH, BG_PATH, FONTS_PATH, 
        AVATAR_CACHE_PATH, SKILL_CACHE_PATH, 
        PHANTOM_CACHE_PATH, CHAIN_CACHE_PATH, WEAPON_CACHE_PATH
    )
    from ..utils.download import (
        download_role_picture, download_skill_icon,
        download_phantom_icon, download_chain_icon,
        download_weapon_icon
    )
except ImportError:
    # 直接运行脚本时的回退导入
    from utils.resource_mgr import (
        CHARINFO_PATH, BG_PATH, FONTS_PATH, 
        AVATAR_CACHE_PATH, SKILL_CACHE_PATH, 
        PHANTOM_CACHE_PATH, CHAIN_CACHE_PATH, WEAPON_CACHE_PATH
    )
    from utils.download import (
        download_role_picture, download_skill_icon,
        download_phantom_icon, download_chain_icon,
        download_weapon_icon
    )
from .fonts import waves_font_origin, ww_font_origin


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
    """
    获取角色立绘图片
    
    Args:
        role_pic_url: 角色立绘URL
        role_id: 角色ID（用于备用）
    
    Returns:
        角色立绘图片，获取失败返回None
    """
    if not role_pic_url:
        logger.warning(f"角色立绘URL为空 (role_id={role_id})")
        return None
    
    try:
        # 下载或从缓存获取
        cache_path = await download_role_picture(role_pic_url)
        
        if cache_path and cache_path.exists():
            img = Image.open(cache_path).convert('RGBA')
            return img
        
        return None
    except Exception as e:
        logger.warning(f"加载角色立绘失败: {e}")
        return None


def get_role_picture_sync(role_pic_url: Optional[str] = None, role_id: Optional[int] = None) -> Optional[Image.Image]:
    """
    同步获取角色立绘图片（用于非异步环境）
    
    Args:
        role_pic_url: 角色立绘URL
        role_id: 角色ID
    
    Returns:
        角色立绘图片，获取失败返回None
    """
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果事件循环正在运行，创建新任务
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_role_picture(role_pic_url, role_id))
                return future.result()
        else:
            return loop.run_until_complete(get_role_picture(role_pic_url, role_id))
    except Exception as e:
        logger.warning(f"同步加载角色立绘失败: {e}")
        return None


async def get_skill_icon_async(skill_id: int, icon_url: str) -> Optional[Image.Image]:
    """
    异步获取技能图标
    
    Args:
        skill_id: 技能ID
        icon_url: 图标URL
    
    Returns:
        技能图标图片
    """
    if not icon_url:
        return None
    
    try:
        cache_path = await download_skill_icon(icon_url)
        if cache_path and cache_path.exists():
            return Image.open(cache_path).convert('RGBA')
        return None
    except Exception as e:
        logger.warning(f"加载技能图标失败: {e}")
        return None


def get_skill_icon_sync(skill_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取技能图标"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_skill_icon_async(skill_id, icon_url))
                return future.result()
        else:
            return loop.run_until_complete(get_skill_icon_async(skill_id, icon_url))
    except Exception as e:
        logger.warning(f"同步加载技能图标失败: {e}")
        return None


async def get_phantom_icon_async(phantom_id: int, icon_url: str) -> Optional[Image.Image]:
    """
    异步获取声骸图标
    
    Args:
        phantom_id: 声骸ID
        icon_url: 图标URL
    
    Returns:
        声骸图标图片
    """
    if not icon_url:
        return None
    
    try:
        cache_path = await download_phantom_icon(icon_url)
        if cache_path and cache_path.exists():
            return Image.open(cache_path).convert('RGBA')
        return None
    except Exception as e:
        logger.warning(f"加载声骸图标失败: {e}")
        return None


def get_phantom_icon_sync(phantom_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取声骸图标"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_phantom_icon_async(phantom_id, icon_url))
                return future.result()
        else:
            return loop.run_until_complete(get_phantom_icon_async(phantom_id, icon_url))
    except Exception as e:
        logger.warning(f"同步加载声骸图标失败: {e}")
        return None


async def get_chain_icon_async(chain_order: int, icon_url: str) -> Optional[Image.Image]:
    """
    异步获取命座图标
    
    Args:
        chain_order: 命座序号(1-6)
        icon_url: 图标URL
    
    Returns:
        命座图标图片
    """
    if not icon_url:
        return None
    
    try:
        cache_path = await download_chain_icon(icon_url)
        if cache_path and cache_path.exists():
            return Image.open(cache_path).convert('RGBA')
        return None
    except Exception as e:
        logger.warning(f"加载命座图标失败: {e}")
        return None


def get_chain_icon_sync(chain_order: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取命座图标"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_chain_icon_async(chain_order, icon_url))
                return future.result()
        else:
            return loop.run_until_complete(get_chain_icon_async(chain_order, icon_url))
    except Exception as e:
        logger.warning(f"同步加载命座图标失败: {e}")
        return None


async def get_weapon_icon_async(weapon_id: int, icon_url: str) -> Optional[Image.Image]:
    """
    异步获取武器图标
    
    Args:
        weapon_id: 武器ID
        icon_url: 图标URL
    
    Returns:
        武器图标图片
    """
    if not icon_url:
        return None
    
    try:
        cache_path = await download_weapon_icon(icon_url)
        if cache_path and cache_path.exists():
            return Image.open(cache_path).convert('RGBA')
        return None
    except Exception as e:
        logger.warning(f"加载武器图标失败: {e}")
        return None


def get_weapon_icon_sync(weapon_id: int, icon_url: str) -> Optional[Image.Image]:
    """同步获取武器图标"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_weapon_icon_async(weapon_id, icon_url))
                return future.result()
        else:
            return loop.run_until_complete(get_weapon_icon_async(weapon_id, icon_url))
    except Exception as e:
        logger.warning(f"同步加载武器图标失败: {e}")
        return None
