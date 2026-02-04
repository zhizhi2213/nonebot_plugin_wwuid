# coding=utf-8
"""
数据模型单元测试
"""
import pytest
from pydantic import ValidationError

from nonebot_plugin_wwuid.models import (
    Chain,
    Weapon,
    WeaponData,
    PhantomProp,
    FetterDetail,
    Props,
    EquipPhantom,
    EquipPhantomData,
    Skill,
    SkillData,
    SkillBranch,
    Role,
    RoleDetailData,
    AccountBaseInfo,
    RoleList,
)


class TestChain:
    """命座模型测试"""

    def test_chain_valid_data(self):
        """测试创建有效的命座数据"""
        chain = Chain(
            name="命座1",
            order=1,
            description="命座1描述",
            iconUrl="https://example.com/chain1.png",
            unlocked=True,
        )
        assert chain.name == "命座1"
        assert chain.order == 1
        assert chain.unlocked is True

    def test_chain_minimal_data(self):
        """测试创建最小命座数据"""
        chain = Chain(order=1, unlocked=False)
        assert chain.order == 1
        assert chain.unlocked is False


class TestWeapon:
    """武器模型测试"""

    def test_weapon_valid_data(self):
        """测试创建有效的武器数据"""
        weapon = Weapon(
            weaponId=1001,
            weaponName="千古洵游",
            weaponType=1,
            weaponStarLevel=5,
            weaponIcon="https://example.com/weapon.png",
            weaponEffectName="武器效果",
        )
        assert weapon.weaponId == 1001
        assert weapon.weaponName == "千古洵游"
        assert weapon.weaponStarLevel == 5


class TestWeaponData:
    """武器数据模型测试"""

    def test_weapon_data_valid(self):
        """测试创建有效的武器数据"""
        weapon = Weapon(
            weaponId=1001,
            weaponName="千古洵游",
            weaponType=1,
            weaponStarLevel=5,
        )
        weapon_data = WeaponData(
            weapon=weapon,
            level=90,
            breach=5,
            resonLevel=5,
        )
        assert weapon_data.level == 90
        assert weapon_data.breach == 5
        assert weapon_data.resonLevel == 5
        assert weapon_data.weapon.weaponName == "千古洵游"


class TestPhantom:
    """声骸模型测试"""

    def test_phantom_prop_valid(self):
        """测试创建有效的声骸属性"""
        phantom_prop = PhantomProp(
            phantomPropId=1,
            name="飞廉之猩",
            phantomId=101,
            quality=5,
            cost=4,
            iconUrl="https://example.com/phantom.png",
            skillDescription="声骸技能描述",
        )
        assert phantom_prop.name == "飞廉之猩"
        assert phantom_prop.quality == 5
        assert phantom_prop.cost == 4

    def test_fetter_detail_valid(self):
        """测试创建有效的声骸共鸣"""
        fetter = FetterDetail(
            groupId=1,
            name="飞廉",
            iconUrl="https://example.com/fetter.png",
            num=2,
            firstDescription="第一效果",
            secondDescription="第二效果",
        )
        assert fetter.name == "飞廉"
        assert fetter.num == 2

    def test_props_valid(self):
        """测试创建有效的属性词条"""
        props = Props(
            attributeName="攻击力",
            iconUrl="https://example.com/atk.png",
            attributeValue="100",
        )
        assert props.attributeName == "攻击力"
        assert props.attributeValue == "100"

    def test_equip_phantom_valid(self):
        """测试创建有效的装备声骸"""
        phantom_prop = PhantomProp(
            phantomPropId=1,
            name="飞廉之猩",
            phantomId=101,
            quality=5,
            cost=4,
            iconUrl="https://example.com/phantom.png",
        )
        fetter = FetterDetail(
            groupId=1,
            name="飞廉",
            num=2,
        )
        main_props = [
            Props(attributeName="攻击力", attributeValue="100"),
        ]
        
        equip_phantom = EquipPhantom(
            phantomProp=phantom_prop,
            cost=4,
            quality=5,
            level=15,
            fetterDetail=fetter,
            mainProps=main_props,
            subProps=[],
        )
        assert equip_phantom.level == 15
        assert equip_phantom.cost == 4
        assert len(equip_phantom.get_props()) == 1


class TestSkill:
    """技能模型测试"""

    def test_skill_valid(self):
        """测试创建有效的技能"""
        skill = Skill(
            id=1,
            type="常态攻击",
            name="飞驰",
            description="技能描述",
            iconUrl="https://example.com/skill.png",
        )
        assert skill.name == "飞驰"
        assert skill.type == "常态攻击"

    def test_skill_data_valid(self):
        """测试创建有效的技能数据"""
        skill = Skill(
            id=1,
            type="常态攻击",
            name="飞驰",
            description="技能描述",
            iconUrl="https://example.com/skill.png",
        )
        skill_data = SkillData(
            skill=skill,
            level=5,
        )
        assert skill_data.level == 5
        assert skill_data.skill.name == "飞驰"


class TestRole:
    """角色模型测试"""

    def test_role_valid(self):
        """测试创建有效的角色"""
        role = Role(
            roleId=1403,
            level=80,
            breach=5,
            roleName="忌炎",
            roleIconUrl="https://example.com/icon.png",
            rolePicUrl="https://example.com/pic.png",
            starLevel=5,
            attributeId=1,
            attributeName="风",
            weaponTypeId=1,
            weaponTypeName="迅刀",
        )
        assert role.roleId == 1403
        assert role.roleName == "忌炎"
        assert role.level == 80
        assert role.starLevel == 5


class TestRoleDetailData:
    """角色详情数据模型测试"""

    def test_role_detail_data_valid(self, mock_role_detail_data):
        """测试创建有效的角色详情数据"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        assert role_detail.level == 80
        assert role_detail.role.roleName == "忌炎"
        assert len(role_detail.chainList) == 6
        assert role_detail.weaponData.weapon.weaponName == "千古洵游"
        assert len(role_detail.skillList) == 6

    def test_get_chain_num(self, mock_role_detail_data):
        """测试获取命座数量"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        assert role_detail.get_chain_num() == 2

    def test_get_chain_name(self, mock_role_detail_data):
        """测试获取命座名称"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        chain_name = role_detail.get_chain_name()
        assert chain_name == "二链"

    def test_get_chain_name_six_chains(self):
        """测试六链命座名称"""
        data = {
            "role": {
                "roleId": 1403,
                "level": 80,
                "breach": 5,
                "roleName": "忌炎",
                "starLevel": 5,
            },
            "level": 80,
            "chainList": [
                {"order": 1, "unlocked": True},
                {"order": 2, "unlocked": True},
                {"order": 3, "unlocked": True},
                {"order": 4, "unlocked": True},
                {"order": 5, "unlocked": True},
                {"order": 6, "unlocked": True},
            ],
            "weaponData": {
                "weapon": {
                    "weaponId": 1001,
                    "weaponName": "千古洵游",
                    "weaponType": 1,
                    "weaponStarLevel": 5,
                },
                "level": 90,
            },
            "phantomData": {
                "cost": 0,
                "equipPhantomList": [],
            },
            "skillList": [],
        }
        role_detail = RoleDetailData(**data)
        assert role_detail.get_chain_name() == "六链"

    def test_get_skill_level(self, mock_role_detail_data):
        """测试获取指定技能等级"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        level = role_detail.get_skill_level("常态攻击")
        assert level == 4
        
        level = role_detail.get_skill_level("共鸣技能")
        assert level == 9

    def test_get_skill_list(self, mock_role_detail_data):
        """测试获取排序后的技能列表"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        skill_list = role_detail.get_skill_list()
        assert len(skill_list) == 6
        assert skill_list[0].skill.type == "常态攻击"
        assert skill_list[1].skill.type == "共鸣技能"

    def test_get_skill_branch_no_active(self, mock_role_detail_data):
        """测试获取技能分支 - 无激活分支"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        branch = role_detail.get_skill_branch()
        assert branch is None

    def test_get_phantom_count(self, mock_role_detail_data):
        """测试获取声骸数量"""
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        phantom_count = 0
        if role_detail.phantomData and role_detail.phantomData.equipPhantomList:
            phantom_count = len([p for p in role_detail.phantomData.equipPhantomList if p])
        
        assert phantom_count == 1


class TestAccountBaseInfo:
    """账户基础信息模型测试"""

    def test_account_base_info_valid(self):
        """测试创建有效的账户基础信息"""
        info = AccountBaseInfo(
            name="测试账号",
            id=100000001,
            creatTime=1234567890,
            activeDays=100,
            level=60,
            worldLevel=5,
            roleNum=10,
            bigCount=5000,
            smallCount=30000,
            achievementCount=100,
            achievementStar=500,
        )
        assert info.name == "测试账号"
        assert info.id == 100000001
        assert info.is_full is True

    def test_account_base_info_partial(self):
        """测试部分账户信息"""
        info = AccountBaseInfo(
            name="测试账号",
            id=100000001,
        )
        assert info.name == "测试账号"
        assert info.is_full is False


class TestRoleList:
    """角色列表模型测试"""

    def test_role_list_valid(self):
        """测试创建有效的角色列表"""
        role_list_data = {
            "roleList": [
                {
                    "roleId": 1403,
                    "roleName": "忌炎",
                    "level": 80,
                    "starLevel": 5,
                },
                {
                    "roleId": 1402,
                    "roleName": "吟霖",
                    "level": 70,
                    "starLevel": 5,
                },
            ],
            "showRoleIdList": [1403, 1402],
            "showToGuest": True,
        }
        
        role_list = RoleList(**role_list_data)
        assert len(role_list.roleList) == 2
        assert role_list.showToGuest is True
        assert len(role_list.showRoleIdList) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
