# coding=utf-8
"""
资源下载管理模块
用于下载和缓存角色立绘、技能图标、声骸图标等资源
"""
import asyncio
import hashlib
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from .resource_mgr import (
    AVATAR_CACHE_PATH,
    WEAPON_CACHE_PATH,
    SKILL_CACHE_PATH,
    PHANTOM_CACHE_PATH,
    CHAIN_CACHE_PATH,
)


class ResourceDownloader:
    """资源下载器"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """获取HTTP客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout))
        return self._client
    
    async def close(self):
        """关闭HTTP客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    def _get_cache_path(self, url: str, cache_dir: Path) -> Path:
        """获取缓存文件路径"""
        # 使用URL的MD5作为文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()
        # 保留原始扩展名
        parsed = urlparse(url)
        original_path = parsed.path
        ext = Path(original_path).suffix or ".png"
        return cache_dir / f"{url_hash}{ext}"
    
    async def download_image(
        self,
        url: str,
        cache_dir: Path,
        force_download: bool = False
    ) -> Optional[Path]:
        """
        下载图片并缓存
        
        Args:
            url: 图片URL
            cache_dir: 缓存目录
            force_download: 是否强制重新下载
        
        Returns:
            缓存文件路径，下载失败返回None
        """
        if not HTTPX_AVAILABLE:
            logger.error("httpx未安装，无法下载图片")
            return None
        
        cache_path = self._get_cache_path(url, cache_dir)
        
        # 检查缓存
        if not force_download and cache_path.exists():
            logger.debug(f"使用缓存图片: {cache_path}")
            return cache_path
        
        # 下载图片
        try:
            client = await self._get_client()
            response = await client.get(url)
            response.raise_for_status()
            
            # 保存到缓存
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, 'wb') as f:
                f.write(response.content)
            
            logger.debug(f"下载图片成功: {url} -> {cache_path}")
            return cache_path
        
        except Exception as e:
            logger.warning(f"下载图片失败 {url}: {e}")
            return None
    
    async def download_role_picture(self, url: str, force_download: bool = False) -> Optional[Path]:
        """下载角色立绘"""
        return await self.download_image(url, AVATAR_CACHE_PATH, force_download)
    
    async def download_skill_icon(self, url: str, force_download: bool = False) -> Optional[Path]:
        """下载技能图标"""
        return await self.download_image(url, SKILL_CACHE_PATH, force_download)
    
    async def download_phantom_icon(self, url: str, force_download: bool = False) -> Optional[Path]:
        """下载声骸图标"""
        return await self.download_image(url, PHANTOM_CACHE_PATH, force_download)
    
    async def download_weapon_icon(self, url: str, force_download: bool = False) -> Optional[Path]:
        """下载武器图标"""
        return await self.download_image(url, WEAPON_CACHE_PATH, force_download)
    
    async def download_chain_icon(self, url: str, force_download: bool = False) -> Optional[Path]:
        """下载命座图标"""
        return await self.download_image(url, CHAIN_CACHE_PATH, force_download)


# 全局下载器实例
_downloader: Optional[ResourceDownloader] = None


def get_downloader() -> ResourceDownloader:
    """获取下载器实例"""
    global _downloader
    if _downloader is None:
        _downloader = ResourceDownloader()
    return _downloader


async def download_role_picture(url: str) -> Optional[Path]:
    """下载角色立绘（便捷函数）"""
    downloader = get_downloader()
    return await downloader.download_role_picture(url)


async def download_skill_icon(url: str) -> Optional[Path]:
    """下载技能图标（便捷函数）"""
    downloader = get_downloader()
    return await downloader.download_skill_icon(url)


async def download_phantom_icon(url: str) -> Optional[Path]:
    """下载声骸图标（便捷函数）"""
    downloader = get_downloader()
    return await downloader.download_phantom_icon(url)


async def download_chain_icon(url: str) -> Optional[Path]:
    """下载命座图标（便捷函数）"""
    downloader = get_downloader()
    return await downloader.download_chain_icon(url)


async def download_weapon_icon(url: str) -> Optional[Path]:
    """下载武器图标（便捷函数）"""
    downloader = get_downloader()
    return await downloader.download_weapon_icon(url)


async def close_downloader():
    """关闭下载器"""
    global _downloader
    if _downloader:
        await _downloader.close()
        _downloader = None
