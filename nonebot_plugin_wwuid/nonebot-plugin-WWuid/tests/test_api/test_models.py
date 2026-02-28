# coding=utf-8
"""
数据模型测试
"""
import pytest
from api.models import (
    Role,
    Weapon,
    WeaponData,
    Skill,
    SkillData,
    Phantom,
    PhantomData,
    RoleDetailData,
)


class TestRoleModel:
    """测试Role模型"""
    
    def test_role_creation(self, sample_role_data):
        """测试创建Role实例"""
        role = Role.model_validate(sample_role_data)
        
        assert role.roleId == 1409
        assert role.roleName == "卡提希娅"
        assert role.starLevel == 5
        assert role.level == 90
        assert role.breach == 6
    
    def test_role_defaults(self):
        """测试Role默认值"""
        minimal_data = {
            "roleId": 1001,
            "roleName": "测试角色",
        }
        role = Role.model_validate(minimal_data)
        
        assert role.starLevel == 4  # 默认值
        assert role.level == 1  # 默认值
        assert role.breach == 0  # 默认值


class TestWeaponModel:
    """测试Weapon模型"""
    
    def test_weapon_creation(self, sample_weapon_data):
        """测试创建Weapon实例"""
        weapon_data = WeaponData.model_validate(sample_weapon_data)
        
        assert weapon_data.weapon.weaponName == "不屈命定之冠"
        assert weapon_data.level == 90
        assert weapon_data.resonLevel == 1


class TestSkillModel:
    """测试Skill模型"""
    
    def test_skill_creation(self, sample_skill_list):
        """测试创建Skill实例"""
        skill_data = SkillData.model_validate(sample_skill_list[0])
        
        assert skill_data.skill.name == "以剑奉读此身"
        assert skill_data.skill.type == "常态攻击"
        assert skill_data.level == 10


class TestPhantomModel:
    """测试Phantom模型"""
    
    def test_phantom_creation(self, sample_phantom_list):
        """测试创建Phantom实例"""
        phantom = Phantom.model_validate(sample_phantom_list[0])
        
        assert phantom.phantomProp.name == "共鸣回响·芙露德莉斯"
        assert phantom.level == 25
        assert phantom.cost == 4


class TestRoleDetailData:
    """测试RoleDetailData模型"""
    
    def test_role_detail_creation(self, sample_role_detail_data):
        """测试创建完整角色详情"""
        role_detail = RoleDetailData.model_validate(sample_role_detail_data)
        
        assert role_detail.role.roleName == "卡提希娅"
        assert role_detail.weaponData.weapon.weaponName == "不屈命定之冠"
        assert len(role_detail.chainList) == 6
        assert len(role_detail.skillList) == 5
        assert len(role_detail.phantomData.equipPhantomList) == 5
    
    def test_get_skill_list(self, sample_role_detail_data):
        """测试获取技能列表"""
        role_detail = RoleDetailData.model_validate(sample_role_detail_data)
        skills = role_detail.get_skill_list()
        
        assert len(skills) == 5
        assert skills[0].skill.type == "常态攻击"
