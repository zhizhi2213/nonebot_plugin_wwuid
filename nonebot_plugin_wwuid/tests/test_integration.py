# coding=utf-8
"""
本地集成测试
"""
import pytest
import tempfile
import os
from pathlib import Path

from nonebot_plugin_wwuid.models import (
    Role,
    RoleDetailData,
)
from nonebot_plugin_wwuid.utils import (
    save_user_cache,
    load_user_cache,
    save_role_cache,
    load_role_cache,
    get_role_id_by_name,
    get_role_name_by_id,
)
from nonebot_plugin_wwuid.statistics import (
    StatisticsManager,
    RoleScore,
)


class TestIntegrationCache:
    """缓存集成测试"""

    def test_cache_lifecycle(self, test_user_id, test_role_id):
        """测试缓存完整生命周期"""
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                
                user_cache_data = {
                    "role_list": [
                        {
                            "roleId": test_role_id,
                            "roleName": "忌炎",
                            "level": 80,
                            "starLevel": 5,
                        }
                    ],
                    "refresh_time": "2024-01-01T00:00:00",
                }
                
                save_user_cache(test_user_id, user_cache_data)
                
                loaded_data = load_user_cache(test_user_id)
                
                assert loaded_data is not None
                assert loaded_data["role_list"][0]["roleName"] == "忌炎"
                
                role_cache_data = {
                    "role": {
                        "roleId": test_role_id,
                        "roleName": "忌炎",
                        "level": 80,
                    },
                    "chainList": [],
                    "skillList": [],
                }
                
                save_role_cache(test_user_id, str(test_role_id), role_cache_data)
                
                loaded_role = load_role_cache(test_user_id, str(test_role_id))
                
                assert loaded_role is not None
                assert loaded_role["role"]["roleName"] == "忌炎"
                
            finally:
                os.chdir(original_cwd)


class TestIntegrationRoleMapping:
    """角色映射集成测试"""

    def test_role_name_bidirectional_mapping(self):
        """测试角色名称双向映射"""
        role_name = "忌炎"
        role_id = get_role_id_by_name(role_name)
        
        assert role_id is not None
        
        mapped_name = get_role_name_by_id(role_id)
        
        assert mapped_name == role_name

    def test_multiple_roles_mapping(self):
        """测试多个角色映射"""
        test_roles = ["忌炎", "吟霖", "今汐", "长离"]
        
        for role_name in test_roles:
            role_id = get_role_id_by_name(role_name)
            assert role_id is not None
            
            mapped_name = get_role_name_by_id(role_id)
            assert mapped_name == role_name


class TestIntegrationStatistics:
    """统计集成测试"""

    def test_calculate_multiple_roles(self, mock_role_detail_data):
        """测试计算多个角色评分"""
        manager = StatisticsManager()
        
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        score = manager._calculate_single_role_score(role_detail)
        
        assert isinstance(score, RoleScore)
        assert score.total_score > 0
        assert score.total_score <= 100

    def test_statistics_weight_sum(self):
        """测试统计权重总和"""
        manager = StatisticsManager()
        
        total_weight = sum(manager.weight_config.values())
        
        assert total_weight == pytest.approx(100.0, abs=0.1)

    def test_role_score_ordering(self, mock_role_detail_data):
        """测试角色评分排序"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        manager = StatisticsManager()
        
        scores = []
        for i in range(5):
            role_detail = RoleDetailData(**mock_role_detail_data)
            score = manager._calculate_single_role_score(role_detail)
            scores.append(score)
        
        sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
        
        assert sorted_scores[0].total_score >= sorted_scores[-1].total_score


class TestIntegrationDataFlow:
    """数据流集成测试"""

    def test_full_data_processing_flow(self, mock_role_detail_data):
        """测试完整数据处理流程"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        assert role_detail.role.roleName == "忌炎"
        
        chain_num = role_detail.get_chain_num()
        assert 0 <= chain_num <= 6
        
        chain_name = role_detail.get_chain_name()
        assert chain_name in ["零链", "一链", "二链", "三链", "四链", "五链", "六链"]
        
        skill_list = role_detail.get_skill_list()
        assert len(skill_list) > 0
        
        from nonebot_plugin_wwuid.utils import format_role_detail
        text = format_role_detail(role_detail)
        
        assert "忌炎" in text
        assert "Lv." in text or "Lv" in text


class TestIntegrationErrorHandling:
    """错误处理集成测试"""

    def test_handle_invalid_role_data(self):
        """测试处理无效角色数据"""
        invalid_data = {
            "role": {
                "roleId": 9999,
            }
        }
        
        try:
            from nonebot_plugin_wwuid.models import RoleDetailData
            role_detail = RoleDetailData(**invalid_data)
        except Exception as e:
            assert isinstance(e, (ValueError, TypeError))

    def test_handle_missing_role_name(self):
        """测试处理缺失角色名"""
        role_id = get_role_id_by_name("不存在的角色")
        assert role_id is None

    def test_handle_cache_not_found(self):
        """测试处理缓存未找到"""
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                
                data = load_user_cache("non_existent_user")
                assert data is None
                
                data = load_role_cache("user", "9999")
                assert data is None
                
            finally:
                os.chdir(original_cwd)


class TestIntegrationPerformance:
    """性能集成测试"""

    def test_bulk_role_mapping_lookup(self):
        """测试批量角色映射查找性能"""
        test_names = ["忌炎", "吟霖", "今汐", "长离", "椿"] * 100
        
        import time
        start_time = time.time()
        
        for name in test_names:
            role_id = get_role_id_by_name(name)
            assert role_id is not None
        
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 1.0, f"批量查找耗时: {elapsed_time:.3f}秒"

    def test_bulk_score_calculation(self, mock_role_detail_data):
        """测试批量评分计算性能"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        
        manager = StatisticsManager()
        
        role_detail = RoleDetailData(**mock_role_detail_data)
        
        import time
        start_time = time.time()
        
        for _ in range(100):
            score = manager._calculate_single_role_score(role_detail)
            assert 0 <= score.total_score <= 100
        
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 5.0, f"批量计算耗时: {elapsed_time:.3f}秒"


class TestRealScenario:
    """真实场景测试"""

    def test_user_journey_scenario(self, test_user_id, mock_role_detail_data):
        """模拟用户使用场景"""
        from nonebot_plugin_wwuid.models import RoleDetailData
        from nonebot_plugin_wwuid.utils import format_role_detail
        from nonebot_plugin_wwuid.statistics import StatisticsManager
        
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                
                user_cache = {
                    "role_list": [
                        {
                            "roleId": 1403,
                            "roleName": "忌炎",
                            "level": 80,
                            "starLevel": 5,
                        }
                    ],
                    "refresh_time": "2024-01-01T00:00:00",
                }
                
                save_user_cache(test_user_id, user_cache)
                
                loaded_cache = load_user_cache(test_user_id)
                assert loaded_cache is not None
                
                role_detail = RoleDetailData(**mock_role_detail_data)
                
                formatted_text = format_role_detail(role_detail)
                assert "忌炎" in formatted_text
                
                manager = StatisticsManager()
                score = manager._calculate_single_role_score(role_detail)
                assert score.total_score > 0
                
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
