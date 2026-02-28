# coding=utf-8
"""
pytest配置文件
提供共享fixture和测试配置
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# 模拟NoneBot
@pytest.fixture(scope="session", autouse=True)
def mock_nonebot():
    """模拟NoneBot环境"""
    nonebot_mock = MagicMock()
    nonebot_mock.logger = MagicMock()
    nonebot_mock.logger.info = print
    nonebot_mock.logger.warning = print
    nonebot_mock.logger.error = print
    nonebot_mock.logger.debug = print
    
    sys.modules['nonebot'] = nonebot_mock
    sys.modules['nonebot.plugin'] = MagicMock()
    sys.modules['nonebot.adapters'] = MagicMock()
    sys.modules['nonebot.adapters.onebot'] = MagicMock()
    sys.modules['nonebot.adapters.onebot.v11'] = MagicMock()
    sys.modules['nonebot.params'] = MagicMock()
    sys.modules['nonebot_plugin_orm'] = MagicMock()
    sys.modules['nonebot_plugin_apscheduler'] = MagicMock()
    
    return nonebot_mock


# 测试数据fixture
@pytest.fixture
def sample_role_data():
    """提供示例角色数据"""
    return {
        "roleId": 1409,
        "roleName": "卡提希娅",
        "roleIconUrl": "https://example.com/icon.png",
        "starLevel": 5,
        "attributeId": 1,
        "attributeName": "衍射",
        "weaponTypeId": 1,
        "weaponTypeName": "长刃",
        "level": 90,
        "breach": 6,
        "chainUnlockNum": 6,
    }


@pytest.fixture
def sample_weapon_data():
    """提供示例武器数据"""
    return {
        "weapon": {
            "weaponId": 123,
            "weaponName": "不屈命定之冠",
            "weaponIcon": "https://example.com/weapon.png",
            "weaponType": 1,
            "weaponStarLevel": 5,
        },
        "level": 90,
        "breach": 6,
        "resonLevel": 1,
    }


@pytest.fixture
def sample_chain_list():
    """提供示例命座数据"""
    return [
        {"order": 1, "name": "因命运戴上冠冕", "unlocked": True},
        {"order": 2, "name": "听风潮斩断利刃", "unlocked": True},
        {"order": 3, "name": "以自身束悬高塔", "unlocked": True},
        {"order": 4, "name": "为拯救舍弃其身", "unlocked": True},
        {"order": 5, "name": "将烈风重塑希望", "unlocked": True},
        {"order": 6, "name": "尽一线挣扎自由", "unlocked": True},
    ]


@pytest.fixture
def sample_skill_list():
    """提供示例技能数据"""
    return [
        {"skill": {"name": "以剑奉读此身", "type": "常态攻击"}, "level": 10},
        {"skill": {"name": "此剑以人之名", "type": "共鸣技能"}, "level": 10},
        {"skill": {"name": "听骑士从心祈愿", "type": "共鸣解放"}, "level": 10},
        {"skill": {"name": "此剑，为潮水的过去", "type": "变奏技能"}, "level": 10},
        {"skill": {"name": "暴风雨", "type": "共鸣回路"}, "level": 10},
    ]


@pytest.fixture
def sample_phantom_list():
    """提供示例声骸数据"""
    return [
        {
            "phantomProp": {"name": "共鸣回响·芙露德莉斯"},
            "level": 25,
            "cost": 4,
        },
        {
            "phantomProp": {"name": "梦魇·凯尔匹"},
            "level": 25,
            "cost": 4,
        },
        {
            "phantomProp": {"name": "小翼龙·热熔"},
            "level": 25,
            "cost": 1,
        },
        {
            "phantomProp": {"name": "苦信者的作俑"},
            "level": 25,
            "cost": 1,
        },
        {
            "phantomProp": {"name": "小翼龙·冷凝"},
            "level": 25,
            "cost": 1,
        },
    ]


@pytest.fixture
def sample_role_detail_data(sample_role_data, sample_weapon_data, sample_chain_list, sample_skill_list, sample_phantom_list):
    """提供完整角色详情数据"""
    return {
        "role": sample_role_data,
        "weaponData": sample_weapon_data,
        "chainList": sample_chain_list,
        "skillList": sample_skill_list,
        "phantomData": {
            "cost": 12,
            "equipPhantomList": sample_phantom_list,
        },
    }


# 临时目录fixture
@pytest.fixture
def temp_cache_dir(tmp_path):
    """提供临时缓存目录"""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


# Mock API响应fixture
@pytest.fixture
def mock_api_response():
    """提供Mock API响应"""
    def _create_response(code=200, data=None, msg="请求成功"):
        return {
            "code": code,
            "data": data or {},
            "msg": msg,
        }
    return _create_response
