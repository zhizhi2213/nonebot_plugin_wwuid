# coding=utf-8
"""
图片渲染层
角色卡片渲染和通用UI组件
"""
from .role_card import RoleCardRenderer, render_role_card, get_renderer
from .utils import (
    get_waves_bg,
    get_attribute_icon,
    get_weapon_type_icon,
    load_resource_image,
    draw_text_with_shadow,
    add_footer,
    get_role_picture,
    get_role_picture_sync,
    get_skill_icon_async,
    get_skill_icon_sync,
    get_phantom_icon_async,
    get_phantom_icon_sync,
    get_chain_icon_async,
    get_chain_icon_sync,
    get_weapon_icon_async,
    get_weapon_icon_sync,
)
from .fonts import waves_font_origin

__all__ = [
    # 角色卡片渲染
    "RoleCardRenderer",
    "render_role_card",
    "get_renderer",
    # 工具函数
    "get_waves_bg",
    "get_attribute_icon",
    "get_weapon_type_icon",
    "load_resource_image",
    "draw_text_with_shadow",
    "add_footer",
    "get_role_picture",
    "get_role_picture_sync",
    "get_skill_icon_async",
    "get_skill_icon_sync",
    "get_phantom_icon_async",
    "get_phantom_icon_sync",
    "get_chain_icon_async",
    "get_chain_icon_sync",
    "get_weapon_icon_async",
    "get_weapon_icon_sync",
    # 字体
    "waves_font_origin",
]
