# coding=utf-8
"""
鸣潮角色查询模块
"""
from typing import Optional, Tuple

from nonebot import logger

from .models import RoleDetailData
from .utils import (
    get_role_id_by_name,
    get_role_name_by_id,
    format_role_detail,
)
from .refresh import get_refresh_manager
from .errors import error_reply, WAVES_CODE_103


class QueryManager:
    """查询管理器"""
    
    def __init__(self):
        self.refresh_manager = get_refresh_manager()
    
    async def query_role(
        self, 
        user_id: str, 
        role_name: str
    ) -> Tuple[bool, Optional[RoleDetailData], str]:
        """查询角色详情
        
        Args:
            user_id: 用户ID
            role_name: 角色名称
        
        Returns:
            Tuple[bool, Optional[RoleDetailData], str]: (是否成功, 角色数据, 返回消息)
        """
        logger.info(f"用户 {user_id} 查询角色 {role_name}")
        
        role_id = get_role_id_by_name(role_name)
        if not role_id:
            return False, None, f"❌ 未找到角色: {role_name}"
        
        role_detail = await self.refresh_manager.get_cached_role_detail_by_name(
            user_id, role_name
        )
        
        if not role_detail:
            return False, None, error_reply(WAVES_CODE_103)
        
        return True, role_detail, ""
    
    async def query_role_text(
        self, 
        user_id: str, 
        role_name: str
    ) -> Tuple[bool, str]:
        """查询角色详情（返回文本格式）
        
        Args:
            user_id: 用户ID
            role_name: 角色名称
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        success, role_detail, msg = await self.query_role(user_id, role_name)
        
        if not success:
            return False, msg
        
        if not role_detail:
            return False, "❌ 角色数据为空"
        
        text_info = self.format_role_info_text(role_detail)
        return True, text_info
    
    async def query_role_list(self, user_id: str) -> Tuple[bool, str]:
        """查询用户所有角色列表
        
        Args:
            user_id: 用户ID
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        logger.info(f"用户 {user_id} 查询角色列表")
        
        role_list = await self.refresh_manager.get_cached_role_list(user_id)
        
        if not role_list:
            return False, error_reply(WAVES_CODE_103)
        
        if not role_list:
            return False, "❌ 角色列表为空"
        
        lines = ["【你的角色列表】"]
        for role in role_list:
            role_name = role.roleName
            level = role.level
            star = "⭐" * role.starLevel
            lines.append(f"{star} {role_name} Lv.{level}")
        
        return True, "\n".join(lines)
    
    def format_role_info_text(self, role: RoleDetailData) -> str:
        """格式化角色详情信息为文本"""
        r = role.role
        lines = [
            f"【{r.roleName}】{'⭐' * r.starLevel}",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"等级: {role.level} (突破: {r.breach or 0})",
            f"命座: {role.get_chain_name()} ({role.get_chain_num()}/6)",
            f"",
            f"【武器】",
            f"{role.weaponData.weapon.weaponName} Lv.{role.weaponData.level} (突破: {role.weaponData.breach or 0})",
            f"精炼: {role.weaponData.resonLevel or 1} 阶",
            f"",
            f"【声骸】",
        ]
        
        phantom_list = role.phantomData.equipPhantomList if role.phantomData else []
        valid_phantoms = [p for p in phantom_list if p]
        lines.append(f"已装备: {len(valid_phantoms)}/5")
        
        if valid_phantoms:
            for idx, phantom in enumerate(valid_phantoms, 1):
                phantom_name = phantom.phantomProp.name
                phantom_quality = "☆" * (phantom.quality - 3)
                phantom_cost = phantom.cost
                phantom_level = phantom.level
                lines.append(f"{idx}. {phantom_name} {phantom_quality} +{phantom_level} (C{phantom_cost})")
        
        lines.append("")
        lines.append("【技能】")
        
        skill_list = role.get_skill_list()
        for skill_data in skill_list:
            skill_name = skill_data.skill.name
            skill_type = skill_data.skill.type
            skill_level = skill_data.level - 1
            lines.append(f"{skill_type}: Lv.{skill_level}")
        
        if role.activeBranchId:
            skill_branch = role.get_skill_branch()
            if skill_branch:
                lines.append(f"")
                lines.append("【技能分支】")
                lines.append(f"{skill_branch.branchName}")
        
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("提示: 使用 /刷新面板 更新数据")
        
        return "\n".join(lines)
    
    def format_role_summary(self, role: RoleDetailData) -> str:
        """格式化角色简略信息"""
        r = role.role
        chain_name = role.get_chain_name()
        weapon_name = role.weaponData.weapon.weaponName
        
        phantom_count = 0
        if role.phantomData and role.phantomData.equipPhantomList:
            phantom_count = len([p for p in role.phantomData.equipPhantomList if p])
        
        return f"{r.roleName} {role.level}级 {chain_name} {weapon_name} 声骸{phantom_count}/5"


_query_manager: Optional[QueryManager] = None


def get_query_manager() -> QueryManager:
    """获取查询管理器实例"""
    global _query_manager
    if _query_manager is None:
        _query_manager = QueryManager()
    return _query_manager
