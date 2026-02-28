# coding=utf-8
"""
统计功能测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from core.statistics import StatisticsManager, RoleScore, get_statistics_manager


class TestRoleScore:
    """测试RoleScore数据类"""
    
    def test_creation(self):
        """测试创建RoleScore"""
        score = RoleScore(
            role_id=1409,
            role_name="卡提希娅",
            level=90,
            chain_num=6,
            weapon_level=90,
            phantom_count=5,
            skill_total=50,
        )
        
        assert score.role_id == 1409
        assert score.role_name == "卡提希娅"
        assert score.total_score == 0.0
        assert score.detail_scores == {}


class TestStatisticsManager:
    """测试StatisticsManager"""
    
    @pytest.fixture
    def stats_manager(self):
        """创建统计管理器实例"""
        return StatisticsManager()
    
    def test_calculate_role_score(self, stats_manager, sample_role_detail_data):
        """测试计算角色评分"""
        from api.models import RoleDetailData
        role_detail = RoleDetailData.model_validate(sample_role_detail_data)
        
        score = stats_manager._calculate_role_score(role_detail)
        
        assert isinstance(score, RoleScore)
        assert score.role_name == "卡提希娅"
        assert score.level == 90
        assert score.chain_num == 6
    
    @pytest.mark.asyncio
    async def test_get_statistics_text(self, stats_manager, sample_role_detail_data):
        """测试获取统计文本"""
        with patch.object(stats_manager.refresh_manager, 'get_all_cached_roles',
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = [sample_role_detail_data]
            
            success, message = await stats_manager.get_statistics_text(
                user_id="123456",
                top_n=10
            )
            
            assert success is True
            assert "卡提希娅" in message
    
    @pytest.mark.asyncio
    async def test_get_role_summary_text(self, stats_manager, sample_role_detail_data):
        """测试获取角色汇总文本"""
        with patch.object(stats_manager.refresh_manager, 'get_all_cached_roles',
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = [sample_role_detail_data]
            
            success, message = await stats_manager.get_role_summary_text(user_id="123456")
            
            assert success is True
            assert "汇总" in message or "统计" in message


class TestGetStatisticsManager:
    """测试get_statistics_manager函数"""
    
    def test_singleton(self):
        """测试单例模式"""
        manager1 = get_statistics_manager()
        manager2 = get_statistics_manager()
        assert manager1 is manager2
