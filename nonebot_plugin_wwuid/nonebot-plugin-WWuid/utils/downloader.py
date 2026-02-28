# coding=utf-8
"""
资源下载器
用于下载角色头像、武器图标等动态资源
"""
import asyncio
import hashlib
from pathlib import Path
from typing import Optional
import httpx
from PIL import Image

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from .resource_mgr import (
    AVATAR_CACHE_PATH, WEAPON_CACHE_PATH,
    CHAIN_CACHE_PATH, SKILL_CACHE_PATH, PHANTOM_CACHE_PATH
)


class ResourceDownloader:
    """资源下载器"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.base_url = "https://api.kurobbs.com"
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
    
    async def download_image(self, url: str, cache_path: Path) -> Optional[Image.Image]:
        """下载图片并缓存"""
        # 检查缓存
        if cache_path.exists():
            try:
                return Image.open(cache_path).convert("RGBA")
            except Exception as e:
                logger.warning(f"加载缓存图片失败: {e}")
        
        # 下载图片
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                # 保存到缓存
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                with open(cache_path, "wb") as f:
                    f.write(response.content)
                
                # 返回图片
                return Image.open(io.BytesIO(response.content)).convert("RGBA")
            else:
                logger.warning(f"下载图片失败: {url}, status={response.status_code}")
        except Exception as e:
            logger.warning(f"下载图片错误: {e}")
        
        return None
    
    async def get_role_avatar(self, role_id: int, icon_url: str) -> Optional[Image.Image]:
        """获取角色头像"""
        if not icon_url:
            return None
        
        # 生成缓存文件名
        url_hash = hashlib.md5(icon_url.encode()).hexdigest()[:8]
        cache_path = AVATAR_CACHE_PATH / f"role_{role_id}_{url_hash}.png"
        
        return await self.download_image(icon_url, cache_path)
    
    async def get_weapon_icon(self, weapon_id: int, icon_url: str) -> Optional[Image.Image]:
        """获取武器图标"""
        if not icon_url:
            return None
        
        url_hash = hashlib.md5(icon_url.encode()).hexdigest()[:8]
        cache_path = WEAPON_CACHE_PATH / f"weapon_{weapon_id}_{url_hash}.png"
        
        return await self.download_image(icon_url, cache_path)
    
    async def get_skill_icon(self, skill_id: int, icon_url: str) -> Optional[Image.Image]:
        """获取技能图标"""
        if not icon_url:
            return None
        
        url_hash = hashlib.md5(icon_url.encode()).hexdigest()[:8]
        cache_path = SKILL_CACHE_PATH / f"skill_{skill_id}_{url_hash}.png"
        
        return await self.download_image(icon_url, cache_path)
    
    async def get_phantom_icon(self, phantom_id: int, icon_url: str) -> Optional[Image.Image]:
        """获取声骸图标"""
        if not icon_url:
            return None
        
        url_hash = hashlib.md5(icon_url.encode()).hexdigest()[:8]
        cache_path = PHANTOM_CACHE_PATH / f"phantom_{phantom_id}_{url_hash}.png"
        
        return await self.download_image(icon_url, cache_path)


# 全局下载器实例
_downloader: Optional[ResourceDownloader] = None


def get_downloader() -> ResourceDownloader:
    """获取下载器实例"""
    global _downloader
    if _downloader is None:
        _downloader = ResourceDownloader()
    return _downloader


import io  # 延迟导入
