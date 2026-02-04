# coding=utf-8
"""
鸣潮插件配置管理
"""
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from nonebot import get_driver


class WavesConfig(BaseModel):
    """鸣潮插件配置"""
    
    API_URL: str = Field(
        default="https://api.kurobbs.com",
        description="鸣潮API地址"
    )
    
    SERVER_ID: str = Field(
        default="76402e5b20be2c39f095a152090afddc",
        description="默认服务器ID"
    )
    
    CACHE_EXPIRE_MINUTES: int = Field(
        default=60,
        description="缓存过期时间（分钟）"
    )
    
    MAX_REFRESH_INTERVAL: int = Field(
        default=300,
        description="刷新间隔限制（秒）"
    )
    
    ENABLE_IMAGE_RENDER: bool = Field(
        default=False,
        description="是否启用图片渲染"
    )
    
    IMAGE_WIDTH: int = Field(
        default=1080,
        description="图片宽度"
    )
    
    IMAGE_HEIGHT: int = Field(
        default=1920,
        description="图片高度"
    )
    
    STATISTICS_TOP_N: int = Field(
        default=10,
        description="统计排行榜显示前N名"
    )
    
    SCORE_WEIGHT_LEVEL: float = Field(
        default=25.0,
        description="等级评分权重"
    )
    
    SCORE_WEIGHT_CHAIN: float = Field(
        default=20.0,
        description="命座评分权重"
    )
    
    SCORE_WEIGHT_WEAPON: float = Field(
        default=20.0,
        description="武器评分权重"
    )
    
    SCORE_WEIGHT_PHANTOM: float = Field(
        default=20.0,
        description="声骸评分权重"
    )
    
    SCORE_WEIGHT_SKILL: float = Field(
        default=15.0,
        description="技能评分权重"
    )


_driver = get_driver()


@_driver.on_startup
async def init_config():
    """初始化配置"""
    global _config
    _config = WavesConfig(**_driver.config.dict())


_config: Optional[WavesConfig] = None


def get_config() -> WavesConfig:
    """获取配置实例"""
    global _config
    if _config is None:
        _config = WavesConfig()
    return _config


def get_cache_dir() -> Path:
    """获取缓存目录"""
    cache_dir = Path.cwd() / "data" / "waves_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
