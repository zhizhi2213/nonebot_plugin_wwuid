# coding=utf-8
"""
鸣潮角色名称与ID映射表
"""
from typing import Dict

# 角色名称到角色ID的映射
ROLE_NAME_TO_ID: Dict[str, int] = {
    "忌炎": 1403,
    "吟霖": 1203,
    "今汐": 1605,
    "长离": 1105,
    "折枝": 1505,
    "相里要": 1205,
    "守岸人": 1104,
    "釉瑚": 1305,
    "椿": 1504,
    "灯灯": 1604,
    "卡提希娅": 1409,
    "可琳艾": 1306,
    "洛可可": 1204,
    "安可": 1102,
    "鉴心": 1302,
    "维里奈": 1502,
    "卡卡罗": 1202,
    "凌阳": 1103,
    "白芷": 1501,
    "秧秧": 1301,
    "炽霞": 1101,
    "散华": 1503,
    "丹瑾": 1201,
    "桃源": 1104,
    "秋水": 1402,
    "渊武": 1602,
    "莫特斐": 1401,
    "漂泊者·光": 1304,
    "漂泊者·暗": 1603,
}

# 角色ID到角色名称的映射
ROLE_ID_TO_NAME: Dict[int, str] = {v: k for k, v in ROLE_NAME_TO_ID.items()}

def get_role_id_by_name(name: str) -> int:
    """通过角色名称获取角色ID"""
    return ROLE_NAME_TO_ID.get(name, 0)

def get_role_name_by_id(role_id: int) -> str:
    """通过角色ID获取角色名称"""
    return ROLE_ID_TO_NAME.get(role_id, f"未知角色({role_id})")
