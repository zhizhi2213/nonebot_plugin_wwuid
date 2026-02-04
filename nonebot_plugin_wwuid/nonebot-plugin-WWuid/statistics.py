# coding=utf-8
"""
鸣潮角色练度统计模块
"""
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field

from nonebot import logger

from .models import RoleDetailData
from .refresh import get_refresh_manager


@dataclass
class RoleScore:
    """角色评分"""
    role_id: int
    role_name: str
    level: int
    chain_num: int
    weapon_level: int
    phantom_count: int
    skill_total: int
    total_score: float = 0.0
    detail_scores: Dict[str, float] = field(default_factory=dict)


class StatisticsManager:
    """统计管理器"""
    
    def __init__(self):
        self.refresh_manager = get_refresh_manager()
        self.weight_config = self._get_default_weight_config()
    
    def _get_default_weight_config(self) -> Dict[str, float]:
        """获取默认评分权重配置"""
        return {
            "level": 25.0,
            "chain": 20.0,
            "weapon": 20.0,
            "phantom": 20.0,
            "skill": 15.0,
        }
    
    async def calculate_role_scores(
        self, 
        user_id: str
    ) -> Tuple[bool, Optional[List[RoleScore]], str]:
        """计算用户所有角色的评分
        
        Args:
            user_id: 用户ID
        
        Returns:
            Tuple[bool, Optional[List[RoleScore]], str]: (是否成功, 评分列表, 返回消息)
        """
        logger.info(f"计算用户 {user_id} 的角色评分")
        
        role_list = await self.refresh_manager.get_cached_role_list(user_id)
        
        if not role_list:
            return False, None, "❌ 未找到角色数据，请先使用 /刷新面板"
        
        scores = []
        
        for role in role_list:
            try:
                role_detail = await self.refresh_manager.get_cached_role_detail(
                    user_id, str(role.roleId)
                )
                
                if role_detail:
                    score = self._calculate_single_role_score(role_detail)
                    scores.append(score)
            except Exception as e:
                logger.warning(f"计算角色 {role.roleName} 评分失败: {e}")
        
        if not scores:
            return False, None, "❌ 没有有效的角色数据"
        
        sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
        
        return True, sorted_scores, ""
    
    def _calculate_single_role_score(self, role: RoleDetailData) -> RoleScore:
        """计算单个角色的评分"""
        r = role.role
        
        chain_num = role.get_chain_num()
        weapon_level = role.weaponData.level
        
        phantom_count = 0
        if role.phantomData and role.phantomData.equipPhantomList:
            phantom_count = len([p for p in role.phantomData.equipPhantomList if p])
        
        skill_total = sum(s.level - 1 for s in role.skillList)
        
        level_score = self._calculate_level_score(role.level, r.breach or 0)
        chain_score = self._calculate_chain_score(chain_num, r.starLevel)
        weapon_score = self._calculate_weapon_score(weapon_level, role.weaponData.breach or 0)
        phantom_score = self._calculate_phantom_score(phantom_count, role.phantomData)
        skill_score = self._calculate_skill_score(skill_total, len(role.skillList))
        
        total_score = (
            level_score * self.weight_config["level"] +
            chain_score * self.weight_config["chain"] +
            weapon_score * self.weight_config["weapon"] +
            phantom_score * self.weight_config["phantom"] +
            skill_score * self.weight_config["skill"]
        ) / 100.0
        
        return RoleScore(
            role_id=r.roleId,
            role_name=r.roleName,
            level=role.level,
            chain_num=chain_num,
            weapon_level=weapon_level,
            phantom_count=phantom_count,
            skill_total=skill_total,
            total_score=round(total_score, 2),
            detail_scores={
                "level": round(level_score, 2),
                "chain": round(chain_score, 2),
                "weapon": round(weapon_score, 2),
                "phantom": round(phantom_score, 2),
                "skill": round(skill_score, 2),
            }
        )
    
    def _calculate_level_score(self, level: int, breach: int) -> float:
        """计算等级评分"""
        max_level = 90
        level_ratio = min(level / max_level, 1.0)
        
        breach_bonus = 0.0
        if breach >= 6:
            breach_bonus = 10.0
        elif breach >= 5:
            breach_bonus = 7.5
        elif breach >= 4:
            breach_bonus = 5.0
        elif breach >= 3:
            breach_bonus = 2.5
        
        score = level_ratio * 90.0 + breach_bonus
        return min(score, 100.0)
    
    def _calculate_chain_score(self, chain_num: int, star_level: int) -> float:
        """计算命座评分"""
        if star_level < 5:
            return 0.0
        
        max_chain = 6
        chain_ratio = chain_num / max_chain
        
        score = chain_ratio * 100.0
        return min(score, 100.0)
    
    def _calculate_weapon_score(self, level: int, breach: int) -> float:
        """计算武器评分"""
        max_level = 90
        level_ratio = min(level / max_level, 1.0)
        
        breach_bonus = 0.0
        if breach >= 5:
            breach_bonus = 10.0
        elif breach >= 4:
            breach_bonus = 5.0
        elif breach >= 3:
            breach_bonus = 2.5
        
        score = level_ratio * 90.0 + breach_bonus
        return min(score, 100.0)
    
    def _calculate_phantom_score(
        self, 
        phantom_count: int, 
        phantom_data: Optional[Any]
    ) -> float:
        """计算声骸评分"""
        if phantom_count == 0:
            return 0.0
        
        base_score = (phantom_count / 5.0) * 70.0
        
        quality_bonus = 0.0
        if phantom_data and phantom_data.equipPhantomList:
            phantoms = [p for p in phantom_data.equipPhantomList if p]
            if phantoms:
                avg_quality = sum(p.quality for p in phantoms) / len(phantoms)
                if avg_quality >= 5:
                    quality_bonus = 20.0
                elif avg_quality >= 4:
                    quality_bonus = 15.0
                elif avg_quality >= 3:
                    quality_bonus = 10.0
        
        score = base_score + quality_bonus
        return min(score, 100.0)
    
    def _calculate_skill_score(self, skill_total: int, skill_count: int) -> float:
        """计算技能评分"""
        if skill_count == 0:
            return 0.0
        
        avg_level = skill_total / skill_count
        max_level = 10
        
        score = (avg_level / max_level) * 100.0
        return min(score, 100.0)
    
    async def get_statistics_text(
        self, 
        user_id: str,
        top_n: int = 10
    ) -> Tuple[bool, str]:
        """获取统计信息文本
        
        Args:
            user_id: 用户ID
            top_n: 显示前N个角色
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        success, scores, msg = await self.calculate_role_scores(user_id)
        
        if not success:
            return False, msg
        
        if not scores:
            return False, "❌ 没有角色数据"
        
        lines = [
            "【角色练度排行榜】",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"共 {len(scores)} 个角色",
            f"━━━━━━━━━━━━━━━━━━━━",
        ]
        
        for idx, score in enumerate(scores[:top_n], 1):
            rank_emoji = ["🥇", "🥈", "🥉"][idx - 1] if idx <= 3 else f"{idx}."
            lines.append(f"{rank_emoji} {score.role_name}")
            lines.append(f"   综合评分: {score.total_score:.1f}")
            lines.append(f"   Lv.{score.level} | {score.chain_num}链 | 武器Lv.{score.weapon_level} | 声骸{score.phantom_count}/5")
            lines.append("")
        
        if len(scores) > top_n:
            lines.append(f"...还有 {len(scores) - top_n} 个角色")
        
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("💡 评分基于: 等级(25%) + 命座(20%) + 武器(20%) + 声骸(20%) + 技能(15%)")
        lines.append("提示: 使用 /刷新面板 更新数据")
        
        return True, "\n".join(lines)
    
    async def get_role_summary_text(
        self, 
        user_id: str
    ) -> Tuple[bool, str]:
        """获取角色汇总信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        success, scores, msg = await self.calculate_role_scores(user_id)
        
        if not success:
            return False, msg
        
        if not scores:
            return False, "❌ 没有角色数据"
        
        total_score = sum(s.total_score for s in scores)
        avg_score = total_score / len(scores)
        
        high_score_count = sum(1 for s in scores if s.total_score >= 80.0)
        medium_score_count = sum(1 for s in scores if 60.0 <= s.total_score < 80.0)
        low_score_count = sum(1 for s in scores if s.total_score < 60.0)
        
        top_role = scores[0]
        weakest_role = scores[-1]
        
        lines = [
            "【角色练度汇总】",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"角色总数: {len(scores)}",
            f"平均评分: {avg_score:.1f}",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"🔥 高练度 (80+): {high_score_count} 个",
            f"⚡ 中练度 (60-79): {medium_score_count} 个",
            f"💧 低练度 (<60): {low_score_count} 个",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"🏆 最强角色: {top_role.role_name} ({top_role.total_score:.1f})",
            f"📈 需提升: {weakest_role.role_name} ({weakest_role.total_score:.1f})",
            f"━━━━━━━━━━━━━━━━━━━━",
            "提示: 使用 /刷新面板 更新数据",
        ]
        
        return True, "\n".join(lines)


_statistics_manager: Optional[StatisticsManager] = None


def get_statistics_manager() -> StatisticsManager:
    """获取统计管理器实例"""
    global _statistics_manager
    if _statistics_manager is None:
        _statistics_manager = StatisticsManager()
    return _statistics_manager
