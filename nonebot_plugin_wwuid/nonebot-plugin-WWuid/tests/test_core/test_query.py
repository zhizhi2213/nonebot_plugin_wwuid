# coding=utf-8
"""
查询功能测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from core.query import QueryManager, get_query_manager


class TestQueryManager:
    """测试QueryManager"""
    
    @pytest.fixture
    def query_manager(self):
        """创建查询管理器实例"""
        return QueryManager()
    
    @pytest.mark.asyncio
    async def test_query_role_success(self, query_manager, sample_role_detail_data):
        """测试查询角色成功"""
        with patch.object(query_manager.refresh_manager, 'get_cached_role_detail_by_name', 
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sample_role_detail_data
            
            success, role_detail, msg = await query_manager.query_role(
                user_id="123456",
                role_name="卡提希娅"
            )
            
            assert success is True
            assert role_detail is not None
            assert role_detail.role.roleName == "卡提希娅"
    
    @pytest.mark.asyncio
    async def test_query_role_not_found(self, query_manager):
        """测试查询角色不存在"""
        with patch.object(query_manager.refresh_manager, 'get_cached_role_detail_by_name',
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            
            success, role_detail, msg = await query_manager.query_role(
                user_id="123456",
                role_name="不存在的角色"
            )
            
            assert success is False
            assert role_detail is None
    
    @pytest.mark.asyncio
    async def test_query_role_text(self, query_manager, sample_role_detail_data):
        """测试查询角色文本格式"""
        with patch.object(query_manager.refresh_manager, 'get_cached_role_detail_by_name',
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sample_role_detail_data
            
            success, message = await query_manager.query_role_text(
                user_id="123456",
                role_name="卡提希娅"
            )
            
            assert success is True
            assert "卡提希娅" in message
            assert "Lv.90" in message
    
    @pytest.mark.asyncio
    async def test_query_role_image(self, query_manager, sample_role_detail_data):
        """测试查询角色图片格式"""
        with patch.object(query_manager.refresh_manager, 'get_cached_role_detail_by_name',
                         new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sample_role_detail_data
            
            with patch('core.query.render_role_card') as mock_render:
                mock_render.return_value = b"fake_image_bytes"
                
                success, result = await query_manager.query_role_image(
                    user_id="123456",
                    role_name="卡提希娅"
                )
                
                assert success is True
                assert result == b"fake_image_bytes"


class TestGetQueryManager:
    """测试get_query_manager函数"""
    
    def test_singleton(self):
        """测试单例模式"""
        manager1 = get_query_manager()
        manager2 = get_query_manager()
        assert manager1 is manager2
