# coding=utf-8
"""
资源路径配置
"""
from pathlib import Path

# 基础资源目录
RESOURCE_PATH = Path(__file__).parent.parent / "resources"

# 角色面板资源
CHARINFO_PATH = RESOURCE_PATH / "images" / "charinfo"

# 字体资源
FONTS_PATH = RESOURCE_PATH / "fonts"

# 背景资源
BG_PATH = RESOURCE_PATH / "images"

# 缓存目录（放在utils目录下）
CACHE_PATH = Path(__file__).parent / "cache"
CACHE_PATH.mkdir(parents=True, exist_ok=True)

# 角色头像缓存
AVATAR_CACHE_PATH = CACHE_PATH / "avatar"
AVATAR_CACHE_PATH.mkdir(parents=True, exist_ok=True)

# 武器图标缓存
WEAPON_CACHE_PATH = CACHE_PATH / "weapon"
WEAPON_CACHE_PATH.mkdir(parents=True, exist_ok=True)

# 命座图标缓存
CHAIN_CACHE_PATH = CACHE_PATH / "chain"
CHAIN_CACHE_PATH.mkdir(parents=True, exist_ok=True)

# 技能图标缓存
SKILL_CACHE_PATH = CACHE_PATH / "skill"
SKILL_CACHE_PATH.mkdir(parents=True, exist_ok=True)

# 声骸图标缓存
PHANTOM_CACHE_PATH = CACHE_PATH / "phantom"
PHANTOM_CACHE_PATH.mkdir(parents=True, exist_ok=True)
