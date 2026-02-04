# coding=utf-8
"""
鸣潮插件测试配置
"""
import asyncio
import pytest
from pathlib import Path
from typing import Dict, Any

from nonebot import get_driver


@pytest.fixture
def test_user_id():
    """测试用户ID"""
    return "test_user_123456"


@pytest.fixture
def test_game_uid():
    """测试游戏UID"""
    return "100000001"


@pytest.fixture
def test_ck():
    """测试CK（仅用于测试）"""
    return "test_cookie_1234567890abcdef"


@pytest.fixture
def test_role_id():
    """测试角色ID"""
    return 1403


@pytest.fixture
def test_role_name():
    """测试角色名"""
    return "忌炎"


@pytest.fixture
def mock_role_data():
    """模拟角色数据"""
    return {
        "roleId": 1403,
        "level": 80,
        "breach": 5,
        "roleName": "忌炎",
        "roleIconUrl": "https://example.com/icon.png",
        "rolePicUrl": "https://example.com/pic.png",
        "starLevel": 5,
        "attributeId": 1,
        "attributeName": "风",
        "weaponTypeId": 1,
        "weaponTypeName": "迅刀",
    }


@pytest.fixture
def mock_role_detail_data():
    """模拟角色详情数据"""
    return {
        "role": {
            "roleId": 1403,
            "level": 80,
            "breach": 5,
            "roleName": "忌炎",
            "roleIconUrl": "https://example.com/icon.png",
            "starLevel": 5,
            "attributeId": 1,
            "attributeName": "风",
            "weaponTypeId": 1,
            "weaponTypeName": "迅刀",
        },
        "level": 80,
        "chainList": [
            {
                "name": "命座1",
                "order": 1,
                "description": "命座1描述",
                "iconUrl": "https://example.com/chain1.png",
                "unlocked": True,
            },
            {
                "name": "命座2",
                "order": 2,
                "description": "命座2描述",
                "iconUrl": "https://example.com/chain2.png",
                "unlocked": True,
            },
            {
                "name": "命座3",
                "order": 3,
                "description": "命座3描述",
                "iconUrl": "https://example.com/chain3.png",
                "unlocked": False,
            },
            {
                "name": "命座4",
                "order": 4,
                "description": "命座4描述",
                "iconUrl": "https://example.com/chain4.png",
                "unlocked": False,
            },
            {
                "name": "命座5",
                "order": 5,
                "description": "命座5描述",
                "iconUrl": "https://example.com/chain5.png",
                "unlocked": False,
            },
            {
                "name": "命座6",
                "order": 6,
                "description": "命座6描述",
                "iconUrl": "https://example.com/chain6.png",
                "unlocked": False,
            },
        ],
        "weaponData": {
            "weapon": {
                "weaponId": 1001,
                "weaponName": "千古洵游",
                "weaponType": 1,
                "weaponStarLevel": 5,
                "weaponIcon": "https://example.com/weapon.png",
            },
            "level": 90,
            "breach": 5,
            "resonLevel": 5,
        },
        "phantomData": {
            "cost": 0,
            "equipPhantomList": [
                {
                    "phantomProp": {
                        "phantomPropId": 1,
                        "name": "飞廉之猩",
                        "phantomId": 101,
                        "quality": 5,
                        "cost": 4,
                        "iconUrl": "https://example.com/phantom1.png",
                    },
                    "cost": 4,
                    "quality": 5,
                    "level": 15,
                    "fetterDetail": {
                        "groupId": 1,
                        "name": "飞廉",
                        "iconUrl": "https://example.com/fetter.png",
                        "num": 2,
                    },
                    "mainProps": [
                        {
                            "attributeName": "攻击力",
                            "iconUrl": "https://example.com/atk.png",
                            "attributeValue": "100",
                        }
                    ],
                    "subProps": [],
                },
                None,
                None,
                None,
                None,
            ],
        },
        "skillList": [
            {
                "skill": {
                    "id": 1,
                    "type": "常态攻击",
                    "name": "飞驰",
                    "description": "常态攻击描述",
                    "iconUrl": "https://example.com/skill1.png",
                },
                "level": 5,
            },
            {
                "skill": {
                    "id": 2,
                    "type": "共鸣技能",
                    "name": "踏风",
                    "description": "共鸣技能描述",
                    "iconUrl": "https://example.com/skill2.png",
                },
                "level": 10,
            },
            {
                "skill": {
                    "id": 3,
                    "type": "共鸣回路",
                    "name": "贯雷",
                    "description": "共鸣回路描述",
                    "iconUrl": "https://example.com/skill3.png",
                },
                "level": 10,
            },
            {
                "skill": {
                    "id": 4,
                    "type": "共鸣解放",
                    "name": "啸空",
                    "description": "共鸣解放描述",
                    "iconUrl": "https://example.com/skill4.png",
                },
                "level": 9,
            },
            {
                "skill": {
                    "id": 5,
                    "type": "变奏技能",
                    "name": "破风",
                    "description": "变奏技能描述",
                    "iconUrl": "https://example.com/skill5.png",
                },
                "level": 8,
            },
            {
                "skill": {
                    "id": 6,
                    "type": "延奏技能",
                    "name": "掠空",
                    "description": "延奏技能描述",
                    "iconUrl": "https://example.com/skill6.png",
                },
                "level": 1,
            },
        ],
        "activeBranchId": 0,
        "skillBranchList": [],
    }


@pytest.fixture
def temp_cache_dir(tmp_path):
    """临时缓存目录"""
    cache_dir = tmp_path / "waves_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


@pytest.fixture
def mock_api_response_success():
    """模拟成功的API响应"""
    return {
        "code": 0,
        "data": {
            "roleList": [
                {
                    "roleId": 1403,
                    "level": 80,
                    "breach": 5,
                    "roleName": "忌炎",
                    "starLevel": 5,
                }
            ]
        },
        "message": "success",
    }


@pytest.fixture
def mock_api_response_error():
    """模拟失败的API响应"""
    return {
        "code": 101,
        "data": None,
        "message": "未找到数据",
    }


@pytest.fixture(scope="session")
def event_loop():
    """事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
