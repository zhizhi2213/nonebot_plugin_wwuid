# coding=utf-8
"""
鸣潮用户绑定数据模型
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from nonebot_plugin_orm import Model
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, field_validator


class WutheringWavesBind(Model):
    """鸣潮用户绑定表"""
    
    # 主键ID，自增
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 用户QQ号，唯一索引（一个QQ只能绑定一个游戏账号）
    user_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    
    # 游戏UID
    game_uid: Mapped[str] = mapped_column(String(50))
    
    # 游戏Cookie/Token
    cookie: Mapped[str] = mapped_column(String(500))
    
    # 别名：waves_ck（用于新功能）
    @property
    def waves_ck(self) -> str:
        return self.cookie
    
    # 创建时间
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # 更新时间（每次修改绑定时更新）
    update_time: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now
    )


# ==================== 鸣潮角色数据模型 ====================


class Chain(BaseModel):
    """命座"""
    name: Optional[str] = None
    order: int
    description: Optional[str] = None
    iconUrl: Optional[str] = None
    unlocked: bool


class Weapon(BaseModel):
    """武器"""
    weaponId: int
    weaponName: str
    weaponType: int
    weaponStarLevel: int
    weaponIcon: Optional[str] = None
    weaponEffectName: Optional[str] = None


class WeaponData(BaseModel):
    """武器数据"""
    weapon: Weapon
    level: int
    breach: Optional[int] = None
    resonLevel: Optional[int] = None


class PhantomProp(BaseModel):
    """声骸属性"""
    phantomPropId: int
    name: str
    phantomId: int
    quality: int
    cost: int
    iconUrl: str
    skillDescription: Optional[str] = None


class FetterDetail(BaseModel):
    """声骸共鸣"""
    groupId: int
    name: str
    iconUrl: Optional[str] = None
    num: int
    firstDescription: Optional[str] = None
    secondDescription: Optional[str] = None


class Props(BaseModel):
    """属性词条"""
    attributeName: str
    iconUrl: Optional[str] = None
    attributeValue: str


class EquipPhantom(BaseModel):
    """装备的声骸"""
    phantomProp: PhantomProp
    cost: int
    quality: int
    level: int
    fetterDetail: FetterDetail
    mainProps: Optional[List[Props]] = None
    subProps: Optional[List[Props]] = None
    
    def get_props(self) -> List[Props]:
        """获取所有词条"""
        props = []
        if self.mainProps:
            props.extend(self.mainProps)
        if self.subProps:
            props.extend(self.subProps)
        return props


class EquipPhantomData(BaseModel):
    """声骸装备数据"""
    cost: int
    equipPhantomList: Optional[List[Optional[EquipPhantom]]] = None


class Skill(BaseModel):
    """技能"""
    id: int
    type: str
    name: str
    description: str
    iconUrl: str


class SkillData(BaseModel):
    """技能数据"""
    skill: Skill
    level: int


class SkillBranch(BaseModel):
    """技能分支"""
    activePic: str
    branchId: int
    branchName: str
    desc: str
    pic: str
    skillIcon: str


class Role(BaseModel):
    """角色基础信息"""
    roleId: int
    level: int
    breach: Optional[int] = None
    roleName: str
    roleIconUrl: Optional[str] = None
    rolePicUrl: Optional[str] = None
    starLevel: int
    attributeId: int
    attributeName: Optional[str] = None
    weaponTypeId: int
    weaponTypeName: Optional[str] = None
    acronym: Optional[str] = None
    chainUnlockNum: Optional[int] = None
    isMainRole: Optional[bool] = None
    totalSkillLevel: Optional[int] = None


class RoleDetailData(BaseModel):
    """角色详情数据"""
    role: Role
    level: int
    chainList: List[Chain]
    weaponData: WeaponData
    phantomData: Optional[EquipPhantomData] = None
    skillList: List[SkillData]
    activeBranchId: int = 0
    skillBranchList: Optional[List[SkillBranch]] = None
    
    def get_chain_num(self) -> int:
        """获取已解锁命座数量"""
        return sum(1 for chain in self.chainList if chain.unlocked)
    
    def get_chain_name(self) -> str:
        """获取命座名称"""
        num = self.get_chain_num()
        names = ["零", "一", "二", "三", "四", "五", "六"]
        return f"{names[min(num, 6)]}链" if num < len(names) else "六链"
    
    def get_skill_level(self, skill_type: str) -> int:
        """获取指定类型的技能等级"""
        skill = next((s for s in self.skillList if s.skill.type == skill_type), None)
        return (skill.level - 1) if skill else 0
    
    def get_skill_list(self) -> List[SkillData]:
        """获取排序后的技能列表"""
        sort_order = ["常态攻击", "共鸣技能", "共鸣回路", "共鸣解放", "变奏技能", "延奏技能", "谐度破坏"]
        return sorted(self.skillList, key=lambda x: sort_order.index(x.skill.type) if x.skill.type in sort_order else 999)
    
    def get_skill_branch(self) -> Optional[SkillBranch]:
        """获取当前激活的技能分支"""
        if self.activeBranchId and self.skillBranchList:
            return next((b for b in self.skillBranchList if b.branchId == self.activeBranchId), None)
        return None


class AccountBaseInfo(BaseModel):
    """账户基础信息"""
    name: str
    id: int
    creatTime: Optional[int] = None
    activeDays: Optional[int] = None
    level: Optional[int] = None
    worldLevel: Optional[int] = None
    roleNum: Optional[int] = None
    bigCount: Optional[int] = None
    smallCount: Optional[int] = None
    achievementCount: Optional[int] = None
    achievementStar: Optional[int] = None
    
    @property
    def is_full(self) -> bool:
        """是否有完整数据"""
        return isinstance(self.creatTime, int)


class RoleList(BaseModel):
    """角色列表"""
    roleList: List[Role]
    showRoleIdList: Optional[List[int]] = None
    showToGuest: bool = True