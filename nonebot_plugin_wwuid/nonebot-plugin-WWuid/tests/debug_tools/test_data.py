# coding=utf-8
"""
测试数据生成工具
提供Mock数据和样本角色数据
"""
from unittest.mock import MagicMock
from datetime import datetime
from typing import List, Optional, Dict, Any


def create_mock_role(
    role_id: int = 1401,
    role_name: str = "测试角色",
    level: int = 90,
    attribute_id: int = 1,
    weapon_type_id: int = 1,
    role_icon_url: str = "https://example.com/icon.png"
) -> MagicMock:
    """
    创建模拟角色数据
    
    Args:
        role_id: 角色ID
        role_name: 角色名称
        level: 角色等级
        attribute_id: 属性ID
        weapon_type_id: 武器类型ID
        role_icon_url: 角色图标URL
    
    Returns:
        MagicMock: 模拟角色对象
    """
    role = MagicMock()
    role.roleId = role_id
    role.roleName = role_name
    role.level = level
    role.attributeId = attribute_id
    role.weaponTypeId = weapon_type_id
    role.roleIconUrl = role_icon_url
    return role


def create_mock_weapon(
    weapon_name: str = "测试武器",
    weapon_star_level: int = 5,
    level: int = 90,
    reson_level: int = 5,
    breach: int = 6
) -> MagicMock:
    """
    创建模拟武器数据
    
    Args:
        weapon_name: 武器名称
        weapon_star_level: 武器星级
        level: 武器等级
        reson_level: 精炼等级
        breach: 突破等级
    
    Returns:
        MagicMock: 模拟武器数据对象
    """
    weapon_data = MagicMock()
    weapon_data.weapon = MagicMock()
    weapon_data.weapon.weaponName = weapon_name
    weapon_data.weapon.weaponStarLevel = weapon_star_level
    weapon_data.level = level
    weapon_data.resonLevel = reson_level
    weapon_data.breach = breach
    return weapon_data


def create_mock_chain_list(unlocked_count: int = 3) -> List[MagicMock]:
    """
    创建模拟命座列表
    
    Args:
        unlocked_count: 已解锁命座数量
    
    Returns:
        List[MagicMock]: 命座列表
    """
    chain_names = [
        "命座一：测试效果1",
        "命座二：测试效果2",
        "命座三：测试效果3",
        "命座四：测试效果4",
        "命座五：测试效果5",
        "命座六：测试效果6",
    ]
    
    chains = []
    for i, name in enumerate(chain_names):
        chain = MagicMock()
        chain.name = name
        chain.unlocked = i < unlocked_count
        chains.append(chain)
    
    return chains


def create_mock_phantom(
    name: str = "测试声骸",
    level: int = 25,
    cost: int = 4
) -> MagicMock:
    """
    创建模拟声骸数据
    
    Args:
        name: 声骸名称
        level: 声骸等级
        cost: cost值
    
    Returns:
        MagicMock: 模拟声骸对象
    """
    phantom = MagicMock()
    phantom.phantomProp = MagicMock()
    phantom.phantomProp.name = name
    phantom.level = level
    phantom.cost = cost
    return phantom


def create_mock_phantom_data(count: int = 5) -> MagicMock:
    """
    创建模拟声骸数据
    
    Args:
        count: 声骸数量
    
    Returns:
        MagicMock: 模拟声骸数据对象
    """
    phantom_names = [
        "鸣钟之龟",
        "无常凶鹭",
        "燎照之骑",
        "飞廉之猩",
        "哀声鸷",
    ]
    
    phantom_data = MagicMock()
    phantom_data.equipPhantomList = []
    
    for i in range(min(count, len(phantom_names))):
        phantom = create_mock_phantom(
            name=phantom_names[i],
            level=25,
            cost=4 if i == 0 else 3
        )
        phantom_data.equipPhantomList.append(phantom)
    
    return phantom_data


def create_mock_skill(
    name: str = "测试技能",
    skill_type: str = "常态攻击",
    level: int = 10
) -> MagicMock:
    """
    创建模拟技能数据
    
    Args:
        name: 技能名称
        skill_type: 技能类型
        level: 技能等级
    
    Returns:
        MagicMock: 模拟技能数据对象
    """
    skill_data = MagicMock()
    skill_data.skill = MagicMock()
    skill_data.skill.name = name
    skill_data.skill.type = skill_type
    skill_data.level = level
    return skill_data


def create_mock_skill_list() -> List[MagicMock]:
    """
    创建模拟技能列表
    
    Returns:
        List[MagicMock]: 技能列表
    """
    skills_info = [
        ("常态攻击", "普通攻击"),
        ("共鸣技能", "技能攻击"),
        ("共鸣解放", "大招"),
        ("变奏技能", "入场技"),
        ("延奏技能", "退场技"),
        ("固有技能", "被动1"),
        ("固有技能", "被动2"),
    ]
    
    skills = []
    for skill_type, name in skills_info:
        skill = create_mock_skill(name, skill_type, level=10)
        skills.append(skill)
    
    return skills


def create_mock_role_detail(
    role_name: str = "测试角色",
    level: int = 90,
    attribute_id: int = 1,
    weapon_type_id: int = 1,
    with_weapon: bool = True,
    with_chain: bool = True,
    with_phantom: bool = True,
    with_skill: bool = True
) -> MagicMock:
    """
    创建模拟角色详情数据
    
    Args:
        role_name: 角色名称
        level: 角色等级
        attribute_id: 属性ID
        weapon_type_id: 武器类型ID
        with_weapon: 是否包含武器数据
        with_chain: 是否包含命座数据
        with_phantom: 是否包含声骸数据
        with_skill: 是否包含技能数据
    
    Returns:
        MagicMock: 模拟角色详情对象
    """
    role_detail = MagicMock()
    
    # 角色基础信息
    role_detail.role = create_mock_role(
        role_id=1401,
        role_name=role_name,
        level=level,
        attribute_id=attribute_id,
        weapon_type_id=weapon_type_id
    )
    
    # 武器信息
    if with_weapon:
        role_detail.weaponData = create_mock_weapon()
    else:
        role_detail.weaponData = None
    
    # 命座信息
    if with_chain:
        role_detail.chainList = create_mock_chain_list(unlocked_count=3)
    else:
        role_detail.chainList = []
    
    # 声骸信息
    if with_phantom:
        role_detail.phantomData = create_mock_phantom_data(count=5)
    else:
        role_detail.phantomData = None
    
    # 技能信息
    if with_skill:
        role_detail.get_skill_list = MagicMock(return_value=create_mock_skill_list())
    else:
        role_detail.get_skill_list = MagicMock(return_value=[])
    
    return role_detail


def create_sample_role_data() -> Dict[str, Any]:
    """
    创建样本角色数据（字典格式）
    
    Returns:
        Dict[str, Any]: 角色数据字典
    """
    return {
        "roleId": 1401,
        "roleName": "测试角色",
        "level": 90,
        "attributeId": 1,
        "weaponTypeId": 1,
        "roleIconUrl": "https://example.com/icon.png",
        "serverId": "76402e5b20be2c79f95d4f4ad46e55b1"
    }


def create_sample_role_detail_data() -> Dict[str, Any]:
    """
    创建样本角色详情数据（字典格式）
    
    Returns:
        Dict[str, Any]: 角色详情数据字典
    """
    return {
        "role": {
            "roleId": 1401,
            "roleName": "测试角色",
            "level": 90,
            "attributeId": 1,
            "weaponTypeId": 1,
        },
        "weaponData": {
            "weapon": {
                "weaponName": "测试武器",
                "weaponStarLevel": 5,
            },
            "level": 90,
            "resonLevel": 5,
            "breach": 6,
        },
        "chainList": [
            {"name": "命座一：测试效果1", "unlocked": True},
            {"name": "命座二：测试效果2", "unlocked": True},
            {"name": "命座三：测试效果3", "unlocked": True},
            {"name": "命座四：测试效果4", "unlocked": False},
            {"name": "命座五：测试效果5", "unlocked": False},
            {"name": "命座六：测试效果6", "unlocked": False},
        ],
        "phantomData": {
            "equipPhantomList": [
                {"phantomProp": {"name": "鸣钟之龟"}, "level": 25, "cost": 4},
                {"phantomProp": {"name": "无常凶鹭"}, "level": 25, "cost": 3},
                {"phantomProp": {"name": "燎照之骑"}, "level": 25, "cost": 3},
                {"phantomProp": {"name": "飞廉之猩"}, "level": 25, "cost": 3},
                {"phantomProp": {"name": "哀声鸷"}, "level": 25, "cost": 1},
            ]
        },
        "skillList": [
            {"skill": {"name": "普通攻击", "type": "常态攻击"}, "level": 10},
            {"skill": {"name": "技能攻击", "type": "共鸣技能"}, "level": 10},
            {"skill": {"name": "大招", "type": "共鸣解放"}, "level": 10},
            {"skill": {"name": "入场技", "type": "变奏技能"}, "level": 10},
            {"skill": {"name": "退场技", "type": "延奏技能"}, "level": 10},
            {"skill": {"name": "被动1", "type": "固有技能"}, "level": 10},
            {"skill": {"name": "被动2", "type": "固有技能"}, "level": 10},
        ]
    }


def create_sample_bind_data() -> Dict[str, str]:
    """
    创建样本绑定数据
    
    Returns:
        Dict[str, str]: 绑定数据字典
    """
    return {
        "token": "sample_token_value_here",
        "devCode": "sample_dev_code_value_here",
        "bind_time": datetime.now().isoformat()
    }


def create_sample_ck() -> str:
    """
    创建样本CK字符串
    
    Returns:
        str: CK字符串
    """
    return "token=sample_token;devCode=sample_dev_code"


# 预定义的测试数据集合
SAMPLE_ROLES = [
    {"roleId": 1401, "roleName": "漂泊者·衍射", "level": 90, "attributeId": 1},
    {"roleId": 1402, "roleName": "漂泊者·湮灭", "level": 90, "attributeId": 2},
    {"roleId": 1501, "roleName": "秧秧", "level": 80, "attributeId": 3},
    {"roleId": 1502, "roleName": "炽霞", "level": 80, "attributeId": 4},
    {"roleId": 1503, "roleName": "白芷", "level": 70, "attributeId": 5},
    {"roleId": 1504, "roleName": "卡卡罗", "level": 90, "attributeId": 6},
]

SAMPLE_WEAPONS = [
    {"name": "裁春", "star": 5},
    {"name": "赫奕流明", "star": 5},
    {"name": "千古洑流", "star": 5},
    {"name": "苍鳞千嶂", "star": 5},
    {"name": "掣傀之手", "star": 5},
]

SAMPLE_PHANTOMS = [
    "鸣钟之龟",
    "无常凶鹭",
    "燎照之骑",
    "飞廉之猩",
    "哀声鸷",
    "云闪之鳞",
    "朔雷之鳞",
    "聚械机偶",
    "无冠者",
    "暗鬃狼",
]


if __name__ == "__main__":
    # 测试数据生成
    print("生成测试数据...")
    
    role = create_mock_role()
    print(f"角色: {role.roleName} (Lv.{role.level})")
    
    weapon = create_mock_weapon()
    print(f"武器: {weapon.weapon.weaponName}")
    
    chains = create_mock_chain_list(unlocked_count=4)
    print(f"命座: {sum(1 for c in chains if c.unlocked)}/6")
    
    phantom_data = create_mock_phantom_data()
    print(f"声骸: {len(phantom_data.equipPhantomList)}/5")
    
    skills = create_mock_skill_list()
    print(f"技能: {len(skills)}")
    
    role_detail = create_mock_role_detail()
    print(f"\n完整角色详情已创建")
    print(f"  - 角色: {role_detail.role.roleName}")
    print(f"  - 武器: {role_detail.weaponData.weapon.weaponName if role_detail.weaponData else '无'}")
    print(f"  - 命座: {sum(1 for c in role_detail.chainList if c.unlocked)}/6")
    print(f"  - 声骸: {len(role_detail.phantomData.equipPhantomList) if role_detail.phantomData else 0}/5")
    print(f"  - 技能: {len(role_detail.get_skill_list())}")
