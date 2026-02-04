# coding=utf-8
"""
统计模块单元测试
"""
import pytest
from nonebot_plugin_wwuid.statistics import (
    StatisticsManager,
    RoleScore,
)


class TestStatisticsManager:
    """统计管理器测试"""

    def test_init_statistics_manager(self):
        """测试初始化统计管理器"""
        manager = StatisticsManager()
        assert manager is not None
        assert manager.weight_config is not None
        assert "level" in manager.weight_config
        assert "chain" in manager.weight_config

    def test_get_default_weight_config(self):
        """测试获取默认权重配置"""
        manager = StatisticsManager()
        weights = manager._get_default_weight_config()
        
        assert weights["level"] == 25.0
        assert weights["chain"] == 20.0
        assert weights["weapon"] == 20.0
        assert weights["phantom"] == 20.0
        assert weights["skill"] == 15.0

    def test_calculate_level_score_max(self):
        """测试等级评分 - 满分"""
        manager = StatisticsManager()
        score = manager._calculate_level_score(90, 6)
        
        assert score == 100.0

    def test_calculate_level_score_mid(self):
        """测试等级评分 - 中等"""
        manager = StatisticsManager()
        score = manager._calculate_level_score(70, 3)
        
        assert 70 < score < 90

    def test_calculate_level_score_low(self):
        """测试等级评分 - 低分"""
        manager = StatisticsManager()
        score = manager._calculate_level_score(40, 0)
        
        assert 0 < score < 50

    def test_calculate_chain_score_max(self):
        """测试命座评分 - 满分"""
        manager = StatisticsManager()
        score = manager._calculate_chain_score(6, 5)
        
        assert score == 100.0

    def test_calculate_chain_score_half(self):
        """测试命座评分 - 半数"""
        manager = StatisticsManager()
        score = manager._calculate_chain_score(3, 5)
        
        assert score == 50.0

    def test_calculate_chain_score_zero(self):
        """测试命座评分 - 零命"""
        manager = StatisticsManager()
        score = manager._calculate_chain_score(0, 5)
        
        assert score == 0.0

    def test_calculate_chain_score_4star(self):
        """测试命座评分 - 4星角色（无命座）"""
        manager = StatisticsManager()
        score = manager._calculate_chain_score(0, 4)
        
        assert score == 0.0

    def test_calculate_weapon_score_max(self):
        """测试武器评分 - 满分"""
        manager = StatisticsManager()
        score = manager._calculate_weapon_score(90, 5)
        
        assert score == 100.0

    def test_calculate_weapon_score_mid(self):
        """测试武器评分 - 中等"""
        manager = StatisticsManager()
        score = manager._calculate_weapon_score(70, 3)
        
        assert 70 < score < 90

    def test_calculate_phantom_score_full(self, mock_role_detail_data):
        """测试声骸评分 - 全装备高品质"""
        manager = StatisticsManager()
        
        phantom_count = 5
        score = manager._calculate_phantom_score(
            phantom_count,
            mock_role_detail_data.get("phantomData")
        )
        
        assert score > 70

    def test_calculate_phantom_score_partial(self, mock_role_detail_data):
        """测试声骸评分 - 部分装备"""
        manager = StatisticsManager()
        
        phantom_count = 2
        score = manager._calculate_phantom_score(
            phantom_count,
            mock_role_detail_data.get("phantomData")
        )
        
        assert 20 < score < 50

    def test_calculate_phantom_score_zero(self):
        """测试声骸评分 - 无装备"""
        manager = StatisticsManager()
        score = manager._calculate_phantom_score(0, None)
        
        assert score == 0.0

    def test_calculate_skill_score_max(self):
        """测试技能评分 - 满级"""
        manager = StatisticsManager()
        score = manager._calculate_skill_score(60, 6)
        
        assert score == 100.0

    def test_calculate_skill_score_mid(self):
        """测试技能评分 - 中等"""
        manager = StatisticsManager()
        score = manager._calculate_skill_score(30, 6)
        
        assert 40 < score < 60

    def test_calculate_single_role_score(self, mock_role_detail_data):
        """测试计算单个角色评分"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        manager = StatisticsManager()
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        score = manager._calculate_single_role_score(role_detail)
        
        assert isinstance(score, RoleScore)
        assert score.role_name == "忌炎"
        assert score.level == 80
        assert score.chain_num == 2
        assert score.weapon_level == 90
        assert 0 < score.total_score <= 100

    def test_calculate_single_role_score_detail_scores(self, mock_role_detail_data):
        """测试计算单个角色评分 - 详细评分"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        manager = StatisticsManager()
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        score = manager._calculate_single_role_score(role_detail)
        
        assert "level" in score.detail_scores
        assert "chain" in score.detail_scores
        assert "weapon" in score.detail_scores
        assert "phantom" in score.detail_scores
        assert "skill" in score.detail_scores
        
        for key, value in score.detail_scores.items():
            assert 0 <= value <= 100


class TestRoleScore:
    """角色评分数据类测试"""

    def test_role_score_creation(self):
        """测试创建角色评分"""
        score = RoleScore(
            role_id=1403,
            role_name="忌炎",
            level=80,
            chain_num=2,
            weapon_level=90,
            phantom_count=5,
            skill_total=30,
            total_score=85.5,
            detail_scores={
                "level": 90.0,
                "chain": 33.3,
                "weapon": 100.0,
                "phantom": 80.0,
                "skill": 50.0,
            }
        )
        
        assert score.role_id == 1403
        assert score.role_name == "忌炎"
        assert score.total_score == 85.5
        assert len(score.detail_scores) == 5

    def test_role_score_default_values(self):
        """测试角色评分默认值"""
        score = RoleScore(
            role_id=1403,
            role_name="忌炎",
            level=80,
            chain_num=0,
            weapon_level=1,
            phantom_count=0,
            skill_total=0,
        )
        
        assert score.total_score == 0.0
        assert score.detail_scores == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
