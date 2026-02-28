# coding=utf-8
"""
刷新功能测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from core.refresh import RefreshManager, get_refresh_manager


class TestRefreshManager:
    """测试RefreshManager"""
    
    @pytest.fixture
    def refresh_manager(self):
        """创建刷新管理器实例"""
        return RefreshManager()
    
    @pytest.mark.asyncio
    async def test_refresh_single_success(self, refresh_manager):
        """测试刷新单个角色成功"""
        with patch.object(refresh_manager, '_get_user_ck', new_callable=AsyncMock) as mock_get_ck:
            mock_get_ck.return_value = ("test_cookie", "test_did", "test_bat")
            
            with patch.object(refresh_manager.api, 'get_request_token', new_callable=AsyncMock) as mock_token:
                mock_token.return_value = (True, "test_bat")
                
                with patch.object(refresh_manager.api, 'get_role_detail_info', new_callable=AsyncMock) as mock_detail:
                    mock_detail.return_value = MagicMock(
                        success=True,
                        data={"role": {"roleId": 1409, "roleName": "卡提希娅"}}
                    )
                    
                    success, message = await refresh_manager.refresh_single(
                        user_id="123456",
                        role_name="卡提希娅"
                    )
                    
                    assert success is True
                    assert "成功" in message or "刷新" in message
    
    @pytest.mark.asyncio
    async def test_refresh_single_no_ck(self, refresh_manager):
        """测试刷新单个角色无CK"""
        with patch.object(refresh_manager, '_get_user_ck', new_callable=AsyncMock) as mock_get_ck:
            mock_get_ck.return_value = None
            
            success, message = await refresh_manager.refresh_single(
                user_id="123456",
                role_name="卡提希娅"
            )
            
            assert success is False
            assert "未绑定" in message
    
    @pytest.mark.asyncio
    async def test_refresh_all(self, refresh_manager):
        """测试刷新所有角色"""
        with patch.object(refresh_manager, '_get_user_ck', new_callable=AsyncMock) as mock_get_ck:
            mock_get_ck.return_value = ("test_cookie", "test_did", "test_bat")
            
            with patch.object(refresh_manager.api, 'get_game_role_list', new_callable=AsyncMock) as mock_list:
                mock_list.return_value = MagicMock(
                    success=True,
                    data=[{"roleId": 1409, "roleName": "卡提希娅"}]
                )
                
                with patch.object(refresh_manager, 'refresh_single', new_callable=AsyncMock) as mock_refresh:
                    mock_refresh.return_value = (True, "刷新成功")
                    
                    success, message = await refresh_manager.refresh_all(user_id="123456")
                    
                    assert success is True


class TestGetRefreshManager:
    """测试get_refresh_manager函数"""
    
    def test_singleton(self):
        """测试单例模式"""
        manager1 = get_refresh_manager()
        manager2 = get_refresh_manager()
        assert manager1 is manager2
