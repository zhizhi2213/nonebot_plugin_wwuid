# coding=utf-8
"""
鸣潮工具函数
"""
import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Union

from nonebot import logger

from .models import Role, RoleDetailData


# 角色名称映射
ROLE_NAME_MAP: Dict[str, int] = {
    # 角色别名映射到角色ID
    "忌炎": 1403,
    "吟霖": 1402,
    "今汐": 1101,
    "长离": 1503,
    "椿": 1502,
    "炽霞": 1301,
    "安可": 1303,
    "鸣徽": 1506,
    "白芷": 1202,
    "吟霖": 1402,
    "维里奈": 1201,
    "忌炎": 1403,
    "卡卡罗": 1501,
    "莫特斐": 1504,
    "莉维娅": 1505,
    "凌阳": 1601,
    "相里要": 1602,
    "长离": 1503,
    "椿": 1502,
    "今汐": 1101,
    "炽霞": 1301,
    "安可": 1303,
    "白芷": 1202,
    "维里奈": 1201,
    "吟霖": 1402,
    "忌炎": 1403,
    "卡卡罗": 1501,
    "莫特斐": 1504,
    "莉维娅": 1505,
    "鸣徽": 1506,
    "凌阳": 1601,
    "相里要": 1602,
}

# 角色ID映射到名称
ROLE_ID_MAP: Dict[int, str] = {v: k for k, v in ROLE_NAME_MAP.items()}


# 缓存目录
CACHE_DIR = Path("data/waves_cache")


def get_cache_dir() -> Path:
    """获取缓存目录"""
    cache_dir = Path.cwd() / CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_user_cache_file(user_id: str) -> Path:
    """获取用户缓存文件路径"""
    cache_dir = get_cache_dir()
    return cache_dir / f"{user_id}.json"


def get_role_cache_file(user_id: str, role_id: str) -> Path:
    """获取角色缓存文件路径"""
    cache_dir = get_cache_dir()
    return cache_dir / f"{user_id}_{role_id}.json"


def save_user_cache(user_id: str, data: Dict[str, Any]) -> bool:
    """保存用户缓存数据"""
    try:
        cache_file = get_user_cache_file(user_id)
        cache_data = {
            "user_id": user_id,
            "update_time": datetime.now().isoformat(),
            "data": data,
        }
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存用户缓存失败: {e}")
        return False


def load_user_cache(user_id: str) -> Optional[Dict[str, Any]]:
    """加载用户缓存数据"""
    try:
        cache_file = get_user_cache_file(user_id)
        if not cache_file.exists():
            return None
        
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        return cache_data.get("data")
    except Exception as e:
        logger.error(f"加载用户缓存失败: {e}")
        return None


def save_role_cache(user_id: str, role_id: str, data: Dict[str, Any]) -> bool:
    """保存角色缓存数据"""
    try:
        cache_file = get_role_cache_file(user_id, role_id)
        cache_data = {
            "user_id": user_id,
            "role_id": role_id,
            "update_time": datetime.now().isoformat(),
            "data": data,
        }
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存角色缓存失败: {e}")
        return False


def load_role_cache(user_id: str, role_id: str) -> Optional[Dict[str, Any]]:
    """加载角色缓存数据"""
    try:
        cache_file = get_role_cache_file(user_id, role_id)
        if not cache_file.exists():
            return None
        
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        return cache_data.get("data")
    except Exception as e:
        logger.error(f"加载角色缓存失败: {e}")
        return None


def get_cache_update_time(user_id: str, role_id: Optional[str] = None) -> Optional[datetime]:
    """获取缓存更新时间"""
    try:
        if role_id:
            cache_file = get_role_cache_file(user_id, role_id)
        else:
            cache_file = get_user_cache_file(user_id)
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        update_time = cache_data.get("update_time")
        if update_time:
            return datetime.fromisoformat(update_time)
        return None
    except Exception as e:
        logger.error(f"获取缓存更新时间失败: {e}")
        return None


def clear_cache(user_id: str, role_id: Optional[str] = None) -> bool:
    """清除缓存"""
    try:
        if role_id:
            cache_file = get_role_cache_file(user_id, role_id)
        else:
            cache_file = get_user_cache_file(user_id)
        
        if cache_file.exists():
            cache_file.unlink()
        return True
    except Exception as e:
        logger.error(f"清除缓存失败: {e}")
        return False


def is_cache_expired(update_time: datetime, expire_minutes: int = 60) -> bool:
    """检查缓存是否过期"""
    now = datetime.now()
    delta = now - update_time
    return delta.total_seconds() > expire_minutes * 60


def normalize_role_name(role_name: str) -> str:
    """标准化角色名称（去除空格和特殊字符）"""
    return role_name.strip().replace(" ", "").replace("　", "")


def get_role_id_by_name(role_name: str) -> Optional[int]:
    """通过角色名称获取角色ID"""
    normal_name = normalize_role_name(role_name)
    return ROLE_NAME_MAP.get(normal_name)


def get_role_name_by_id(role_id: int) -> Optional[str]:
    """通过角色ID获取角色名称"""
    return ROLE_ID_MAP.get(role_id)


def format_role_info(role: Union[Role, RoleDetailData]) -> str:
    """格式化角色信息（文本形式）"""
    if isinstance(role, RoleDetailData):
        return format_role_detail(role)
    
    lines = [
        f"【{role.roleName}】",
        f"等级: {role.level} (突破: {role.breach or 0})",
        f"属性: {role.attributeName or '未知'}",
        f"武器: {role.weaponTypeName or '未知'}",
        f"星级: {'⭐' * role.starLevel}",
    ]
    return "\n".join(lines)


def format_role_detail(role: RoleDetailData) -> str:
    """格式化角色详情信息（文本形式）"""
    r = role.role
    lines = [
        f"【{r.roleName}】{'⭐' * r.starLevel}",
        f"等级: {role.level} (突破: {r.breach or 0})",
        f"命座: {role.get_chain_name()} ({role.get_chain_num()}/6)",
        f"武器: {role.weaponData.weapon.weaponName} Lv.{role.weaponData.level}",
        f"声骸: {len([p for p in (role.phantomData.equipPhantomList or []) if p])}/5",
    ]
    
    if r.attributeName:
        lines.append(f"属性: {r.attributeName}")
    
    if r.weaponTypeName:
        lines.append(f"武器类型: {r.weaponTypeName}")
    
    return "\n".join(lines)


async def run_in_executor(func, *args, **kwargs):
    """在线程池中执行阻塞操作"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


def safe_int(value: Any, default: int = 0) -> int:
    """安全转换为整数"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """安全转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def format_number(num: Union[int, float], decimals: int = 2) -> str:
    """格式化数字"""
    if isinstance(num, int):
        return str(num)
    return f"{num:.{decimals}f}".rstrip("0").rstrip(".")


def truncate_text(text: str, max_length: int = 50) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
