# coding=utf-8
"""
通用工具层
资源管理、下载器、通用函数
"""
from .common import (
    get_role_id_by_name,
    get_role_name_by_id,
    format_role_detail,
)
from .resource_mgr import (
    RESOURCE_PATH,
    CHARINFO_PATH,
    FONTS_PATH,
    BG_PATH,
    CACHE_PATH,
)
from .downloader import ResourceDownloader, get_downloader

__all__ = [
    # 通用工具
    "get_role_id_by_name",
    "get_role_name_by_id",
    "format_role_detail",
    # 资源路径
    "RESOURCE_PATH",
    "CHARINFO_PATH",
    "FONTS_PATH",
    "BG_PATH",
    "CACHE_PATH",
    # 下载器
    "ResourceDownloader",
    "get_downloader",
]
