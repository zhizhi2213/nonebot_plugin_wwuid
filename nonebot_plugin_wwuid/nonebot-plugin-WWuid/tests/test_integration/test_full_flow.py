# coding=utf-8
"""
完整流程集成测试
测试绑定->刷新->查询->渲染的完整流程
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio


class TestFullFlow:
    """测试完整业务流程"""
    
    @pytest.fixture
    def mock_bot(self):
        """创建模拟Bot对象"""
        bot = MagicMock()
        bot.send = AsyncMock()
        bot.send_private_msg = AsyncMock()
        bot.send_group_msg = AsyncMock()
        return bot
    
    @pytest.fixture
    def mock_event(self):
        """创建模拟事件对象"""
        event = MagicMock()
        event.get_user_id = MagicMock(return_value="123456789")
        event.get_session_id = MagicMock(return_value="group_987654321")
        event.group_id = 987654321
        event.user_id = 123456789
        return event
    
    @pytest.fixture
    def sample_ck(self):
        """样本CK数据"""
        return "token=sample_token;devCode=sample_dev_code"
    
    @pytest.fixture
    def sample_role_data(self):
        """样本角色数据"""
        return {
            "roleId": 1401,
            "roleName": "测试角色",
            "level": 90,
            "attributeId": 1,
            "weaponTypeId": 1,
            "roleIconUrl": "https://example.com/icon.png"
        }
    
    @pytest.fixture
    def sample_role_detail_data(self):
        """样本角色详情数据"""
        return {
            "role": {
                "roleId": 1401,
                "roleName": "测试角色",
                "level": 90,
                "attributeId": 1,
                "weaponTypeId": 1,
            },
            "weaponData": {
                "weapon": {
                    "weaponName": "测试武器",
                    "weaponStarLevel": 5,
                },
                "level": 90,
                "resonLevel": 5,
                "breach": 6,
            },
            "chainList": [
                {"name": "命座1", "unlocked": True},
                {"name": "命座2", "unlocked": True},
                {"name": "命座3", "unlocked": True},
                {"name": "命座4", "unlocked": False},
                {"name": "命座5", "unlocked": False},
                {"name": "命座6", "unlocked": False},
            ],
            "phantomData": {
                "equipPhantomList": [
                    {"phantomProp": {"name": "声骸1"}, "level": 25, "cost": 4},
                    {"phantomProp": {"name": "声骸2"}, "level": 25, "cost": 3},
                ]
            },
            "skillList": [
                {"skill": {"name": "技能1", "type": "类型1"}, "level": 10},
                {"skill": {"skillName": "技能2", "skillType": "类型2"}, "level": 10},
            ]
        }
    
    @pytest.mark.asyncio
    async def test_bind_flow(self, mock_bot, mock_event, sample_ck):
        """测试绑定流程"""
        with patch('nonebot_plugin_wwuid.core.bind.save_bind_data') as mock_save:
            mock_save.return_value = True
            
            # 模拟绑定处理
            user_id = mock_event.get_user_id()
            
            # 解析CK
            from nonebot_plugin_wwuid.core.bind import parse_ck
            token, dev_code = parse_ck(sample_ck)
            
            assert token is not None
            assert dev_code is not None
            
            # 保存绑定
            result = await mock_save(user_id, token, dev_code)
            assert result is True
    
    @pytest.mark.asyncio
    async def test_query_flow(self, mock_bot, mock_event, sample_role_data):
        """测试查询流程"""
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_list') as mock_get_list:
            mock_get_list.return_value = [sample_role_data]
            
            from nonebot_plugin_wwuid.core.query import QueryManager
            
            manager = QueryManager()
            user_id = mock_event.get_user_id()
            
            # 查询角色列表
            roles = await manager.get_role_list(user_id)
            
            assert len(roles) > 0
            assert roles[0]["roleName"] == "测试角色"
    
    @pytest.mark.asyncio
    async def test_refresh_flow(self, mock_bot, mock_event, sample_role_data):
        """测试刷新流程"""
        with patch('nonebot_plugin_wwuid.core.refresh.RefreshManager.refresh_role') as mock_refresh:
            mock_refresh.return_value = True
            
            from nonebot_plugin_wwuid.core.refresh import RefreshManager
            
            manager = RefreshManager()
            user_id = mock_event.get_user_id()
            role_id = sample_role_data["roleId"]
            
            # 刷新角色数据
            result = await manager.refresh_role(user_id, role_id)
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_render_flow(self, sample_role_detail_data):
        """测试渲染流程"""
        with patch('nonebot_plugin_wwuid.renderer.role_card.render_role_card') as mock_render:
            mock_render.return_value = b'fake_image_bytes'
            
            from nonebot_plugin_wwuid.renderer import render_role_card
            
            # 创建角色详情对象
            role_detail = MagicMock()
            role_detail.role = MagicMock()
            role_detail.role.roleName = sample_role_detail_data["role"]["roleName"]
            role_detail.role.level = sample_role_detail_data["role"]["level"]
            
            # 渲染角色卡片
            image_bytes = render_role_card(role_detail)
            
            assert image_bytes is not None
            assert isinstance(image_bytes, bytes)
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, mock_bot, mock_event, sample_ck, sample_role_data, sample_role_detail_data):
        """测试完整流程：绑定->查询->刷新->渲染"""
        
        # Step 1: 绑定
        with patch('nonebot_plugin_wwuid.core.bind.save_bind_data') as mock_save_bind:
            mock_save_bind.return_value = True
            
            from nonebot_plugin_wwuid.core.bind import parse_ck
            token, dev_code = parse_ck(sample_ck)
            bind_result = await mock_save_bind(mock_event.get_user_id(), token, dev_code)
            assert bind_result is True
        
        # Step 2: 查询角色列表
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_list') as mock_get_list:
            mock_get_list.return_value = [sample_role_data]
            
            from nonebot_plugin_wwuid.core.query import QueryManager
            query_manager = QueryManager()
            roles = await query_manager.get_role_list(mock_event.get_user_id())
            assert len(roles) > 0
            role_id = roles[0]["roleId"]
        
        # Step 3: 刷新角色数据
        with patch('nonebot_plugin_wwuid.core.refresh.RefreshManager.refresh_role') as mock_refresh:
            mock_refresh.return_value = True
            
            from nonebot_plugin_wwuid.core.refresh import RefreshManager
            refresh_manager = RefreshManager()
            refresh_result = await refresh_manager.refresh_role(mock_event.get_user_id(), role_id)
            assert refresh_result is True
        
        # Step 4: 查询角色详情
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_detail') as mock_get_detail:
            mock_get_detail.return_value = sample_role_detail_data
            
            role_detail = await query_manager.get_role_detail(mock_event.get_user_id(), role_id)
            assert role_detail is not None
        
        # Step 5: 渲染角色卡片
        with patch('nonebot_plugin_wwuid.renderer.role_card.render_role_card') as mock_render:
            mock_render.return_value = b'final_image_bytes'
            
            from nonebot_plugin_wwuid.renderer import render_role_card
            
            role_detail_mock = MagicMock()
            role_detail_mock.role = MagicMock()
            role_detail_mock.role.roleName = role_detail["role"]["roleName"]
            
            image_bytes = render_role_card(role_detail_mock)
            assert image_bytes is not None
            assert len(image_bytes) > 0


class TestErrorHandling:
    """测试错误处理流程"""
    
    @pytest.fixture
    def mock_event(self):
        """创建模拟事件对象"""
        event = MagicMock()
        event.get_user_id = MagicMock(return_value="123456789")
        return event
    
    @pytest.mark.asyncio
    async def test_bind_without_ck(self, mock_event):
        """测试未绑定CK时的查询"""
        with patch('nonebot_plugin_wwuid.core.bind.get_bind_data') as mock_get_bind:
            mock_get_bind.return_value = None
            
            from nonebot_plugin_wwuid.core.bind import get_bind_data
            
            user_id = mock_event.get_user_id()
            bind_data = await get_bind_data(user_id)
            
            assert bind_data is None
    
    @pytest.mark.asyncio
    async def test_query_api_error(self, mock_event):
        """测试API查询错误"""
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_list') as mock_get_list:
            mock_get_list.side_effect = Exception("API Error")
            
            from nonebot_plugin_wwuid.core.query import QueryManager
            
            manager = QueryManager()
            user_id = mock_event.get_user_id()
            
            with pytest.raises(Exception) as exc_info:
                await manager.get_role_list(user_id)
            
            assert "API Error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_render_error(self):
        """测试渲染错误"""
        with patch('nonebot_plugin_wwuid.renderer.role_card.render_role_card') as mock_render:
            mock_render.side_effect = Exception("Render Error")
            
            from nonebot_plugin_wwuid.renderer import render_role_card
            
            role_detail = MagicMock()
            
            with pytest.raises(Exception) as exc_info:
                render_role_card(role_detail)
            
            assert "Render Error" in str(exc_info.value)


class TestConcurrentAccess:
    """测试并发访问"""
    
    @pytest.mark.asyncio
    async def test_concurrent_queries(self):
        """测试并发查询"""
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_list') as mock_get_list:
            mock_get_list.return_value = [{"roleId": 1, "roleName": "角色1"}]
            
            from nonebot_plugin_wwuid.core.query import QueryManager
            
            manager = QueryManager()
            
            # 并发执行多个查询
            tasks = [
                manager.get_role_list("user1"),
                manager.get_role_list("user2"),
                manager.get_role_list("user3"),
            ]
            
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 3
            for result in results:
                assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_refresh_while_querying(self):
        """测试查询时刷新"""
        with patch('nonebot_plugin_wwuid.core.query.QueryManager.get_role_list') as mock_query:
            with patch('nonebot_plugin_wwuid.core.refresh.RefreshManager.refresh_role') as mock_refresh:
                mock_query.return_value = [{"roleId": 1}]
                mock_refresh.return_value = True
                
                from nonebot_plugin_wwuid.core.query import QueryManager
                from nonebot_plugin_wwuid.core.refresh import RefreshManager
                
                query_manager = QueryManager()
                refresh_manager = RefreshManager()
                
                # 同时执行查询和刷新
                query_task = query_manager.get_role_list("user1")
                refresh_task = refresh_manager.refresh_role("user1", 1)
                
                results = await asyncio.gather(query_task, refresh_task)
                
                assert results[0] is not None  # 查询结果
                assert results[1] is True  # 刷新结果


class TestDataConsistency:
    """测试数据一致性"""
    
    @pytest.mark.asyncio
    async def test_data_persistence(self):
        """测试数据持久化"""
        user_id = "test_user"
        
        with patch('nonebot_plugin_wwuid.core.bind.save_bind_data') as mock_save:
            with patch('nonebot_plugin_wwuid.core.bind.get_bind_data') as mock_get:
                mock_save.return_value = True
                mock_get.return_value = {
                    "token": "test_token",
                    "devCode": "test_dev_code"
                }
                
                from nonebot_plugin_wwuid.core.bind import save_bind_data, get_bind_data
                
                # 保存数据
                save_result = await save_bind_data(user_id, "test_token", "test_dev_code")
                assert save_result is True
                
                # 读取数据
                bind_data = await get_bind_data(user_id)
                assert bind_data is not None
                assert bind_data["token"] == "test_token"
                assert bind_data["devCode"] == "test_dev_code"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
