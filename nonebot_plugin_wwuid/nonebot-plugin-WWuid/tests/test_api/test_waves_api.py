# coding=utf-8
"""
Waves API测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from api.waves_api import WavesApi, WavesApiResponse


class TestWavesApi:
    """测试WavesApi类"""
    
    @pytest.fixture
    def api(self):
        """创建API实例"""
        return WavesApi()
    
    def test_init(self, api):
        """测试API初始化"""
        assert api.MAIN_URL == "https://api.kurobbs.com"
        assert api.SERVER_ID == "76402e5b20be2c39f095a152090afddc"
    
    def test_get_server_id(self, api):
        """测试获取服务器ID"""
        # 国服
        assert api._get_server_id("100276895") == "76402e5b20be2c39f095a152090afddc"
        # 国际服（roleId >= 200000000）
        assert api._get_server_id("200000001") == "919752ae5ea09c1ced910dd668a63ffb"
    
    def test_get_headers(self, api):
        """测试获取请求头"""
        headers = api._get_headers(cookie="test_cookie", is_community=True)
        
        assert headers["token"] == "test_cookie"
        assert "devCode" in headers
        assert headers["version"] == "2.10.0"
    
    @pytest.mark.asyncio
    async def test_get_request_token_success(self, api, mock_api_response):
        """测试获取request_token成功"""
        mock_data = {"accessToken": "test_bat_token"}
        mock_resp = mock_api_response(code=200, data=mock_data)
        
        with patch.object(api, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=200,
                data=mock_data,
                message="请求成功"
            )
            
            success, bat = await api.get_request_token(
                role_id="100276895",
                cookie="test_cookie",
                did="test_did"
            )
            
            assert success is True
            assert bat == "test_bat_token"
    
    @pytest.mark.asyncio
    async def test_get_request_token_failure(self, api, mock_api_response):
        """测试获取request_token失败"""
        with patch.object(api, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=10000,
                data={},
                message="参数错误"
            )
            
            success, bat = await api.get_request_token(
                role_id="100276895",
                cookie="test_cookie",
                did="test_did"
            )
            
            assert success is False
            assert "参数错误" in bat


class TestWavesApiResponse:
    """测试WavesApiResponse类"""
    
    def test_success_property_code_0(self):
        """测试code=0时success为True"""
        resp = WavesApiResponse(code=0, data={}, message="成功")
        assert resp.success is True
    
    def test_success_property_code_200(self):
        """测试code=200时success为True"""
        resp = WavesApiResponse(code=200, data={}, message="成功")
        assert resp.success is True
    
    def test_success_property_code_other(self):
        """测试其他code时success为False"""
        resp = WavesApiResponse(code=10000, data={}, message="失败")
        assert resp.success is False
    
    def test_throw_msg(self):
        """测试错误消息"""
        resp = WavesApiResponse(code=10000, data={}, message="参数错误")
        assert "参数错误" in resp.throw_msg()
