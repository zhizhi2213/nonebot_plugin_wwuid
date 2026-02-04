# coding=utf-8
"""
API模块单元测试
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx

from nonebot_plugin_wwuid.waves_api import (
    WavesApi,
    WavesApiResponse,
    generate_random_jwt_token,
)


class TestWavesApiResponse:
    """API响应类测试"""

    def test_response_success(self):
        """测试成功的响应"""
        response = WavesApiResponse(code=0, data={"key": "value"}, message="success")
        
        assert response.success is True
        assert response.code == 0
        assert response.data == {"key": "value"}
        assert response.message == "success"

    def test_response_failure(self):
        """测试失败的响应"""
        response = WavesApiResponse(code=101, data=None, message="error")
        
        assert response.success is False
        assert response.code == 101
        assert response.data is None
        assert response.message == "error"

    def test_throw_msg(self):
        """测试获取错误消息"""
        response = WavesApiResponse(code=101, message="未找到数据")
        
        msg = response.throw_msg()
        assert msg == "未找到数据"

    def test_throw_msg_default(self):
        """测试获取默认错误消息"""
        response = WavesApiResponse(code=999, message="")
        
        msg = response.throw_msg()
        assert "错误代码: 999" in msg

    def test_model_dump(self):
        """测试序列化为字典"""
        response = WavesApiResponse(
            code=0,
            data={"key": "value"},
            message="success"
        )
        
        dumped = response.model_dump()
        
        assert dumped["code"] == 0
        assert dumped["data"] == {"key": "value"}
        assert dumped["message"] == "success"


class TestWavesApi:
    """WavesApi类测试"""

    def test_init(self):
        """测试初始化"""
        api = WavesApi()
        
        assert api.SERVER_ID == "76402e5b20be2c39f095a152090afddc"
        assert api.MAIN_URL == "https://api.kurobbs.com"
        assert api.client is not None

    @pytest.mark.asyncio
    async def test_close(self):
        """测试关闭客户端"""
        api = WavesApi()
        
        await api.close()
        
        assert True

    def test_get_server_id_default(self):
        """测试获取服务器ID - 默认"""
        api = WavesApi()
        
        server_id = api._get_server_id("123456789")
        
        assert server_id == "76402e5b20be2c39f095a152090afddc"

    def test_get_server_id_foreign(self):
        """测试获取服务器ID - 外服"""
        api = WavesApi()
        
        server_id = api._get_server_id("200000001")
        
        assert server_id == "919752ae5ea09c1ced910dd668a63ffb"

    def test_get_server_id_invalid(self):
        """测试获取服务器ID - 无效ID"""
        api = WavesApi()
        
        server_id = api._get_server_id("abc")
        
        assert server_id == "76402e5b20be2c39f095a152090afddc"

    def test_get_headers(self):
        """测试获取请求头"""
        api = WavesApi()
        
        headers = api._get_headers("test_cookie", "123456789")
        
        assert headers["Content-Type"] == "application/json"
        assert headers["token"] == "test_cookie"
        assert "User-Agent" in headers

    @pytest.mark.asyncio
    async def test_request_get_success(self):
        """测试GET请求 - 成功"""
        api = WavesApi()
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"result": "success"},
            "message": "OK",
        }
        
        with patch.object(api.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            result = await api._request(
                "https://test.com/api",
                method="GET",
                headers={"token": "test"},
            )
            
            assert result.success is True
            assert result.code == 0
            assert result.data == {"result": "success"}

    @pytest.mark.asyncio
    async def test_request_post_success(self):
        """测试POST请求 - 成功"""
        api = WavesApi()
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"result": "success"},
            "message": "OK",
        }
        
        with patch.object(api.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await api._request(
                "https://test.com/api",
                method="POST",
                data={"key": "value"},
                headers={"token": "test"},
            )
            
            assert result.success is True
            assert result.code == 0

    @pytest.mark.asyncio
    async def test_request_timeout(self):
        """测试请求超时"""
        api = WavesApi()
        
        with patch.object(api.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Timeout")
            
            result = await api._request(
                "https://test.com/api",
                method="GET",
                headers={"token": "test"},
            )
            
            assert result.success is False
            assert result.code == 999
            assert "超时" in result.message

    @pytest.mark.asyncio
    async def test_request_network_error(self):
        """测试网络错误"""
        api = WavesApi()
        
        with patch.object(api.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.RequestError("Network error")
            
            result = await api._request(
                "https://test.com/api",
                method="GET",
                headers={"token": "test"},
            )
            
            assert result.success is False
            assert result.code == 999
            assert "网络错误" in result.message

    @pytest.mark.asyncio
    async def test_login_log(self):
        """测试登录校验"""
        api = WavesApi()
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": None,
            "message": "success",
        }
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data=None,
                message="success"
            )
            
            result = await api.login_log("123456789", "test_cookie")
            
            assert result.code == 0

    @pytest.mark.asyncio
    async def test_get_base_info(self):
        """测试获取账户基础信息"""
        api = WavesApi()
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data={
                    "roleBoxBaseData": [
                        {
                            "roleId": "123456789",
                            "name": "测试账号",
                        }
                    ]
                },
                message="success"
            )
            
            result = await api.get_base_info("123456789", "test_cookie")
            
            assert result.code == 0
            assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_role_info(self):
        """测试获取角色列表"""
        api = WavesApi()
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data={
                    "roleList": [
                        {
                            "roleId": 1403,
                            "roleName": "忌炎",
                            "level": 80,
                        }
                    ]
                },
                message="success"
            )
            
            result = await api.get_role_info("123456789", "test_cookie")
            
            assert result.code == 0
            assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_role_detail_info(self):
        """测试获取单个角色详情"""
        api = WavesApi()
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data={
                    "role": {
                        "roleId": 1403,
                        "roleName": "忌炎",
                    }
                },
                message="success"
            )
            
            result = await api.get_role_detail_info(
                "1403", "123456789", "test_cookie"
            )
            
            assert result.code == 0
            assert result.data is not None

    @pytest.mark.asyncio
    async def test_refresh_data(self):
        """测试刷新数据"""
        api = WavesApi()
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data={"status": "success"},
                message="success"
            )
            
            result = await api.refresh_data("123456789", "test_cookie")
            
            assert result.code == 0

    @pytest.mark.asyncio
    async def test_get_owned_role_info(self):
        """测试获取已拥有角色信息"""
        api = WavesApi()
        
        with patch.object(api, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = WavesApiResponse(
                code=0,
                data={
                    "ownedRoleList": [
                        {
                            "roleId": 1403,
                            "roleName": "忌炎",
                        }
                    ]
                },
                message="success"
            )
            
            result = await api.get_owned_role_info("123456789", "test_cookie")
            
            assert result.code == 0


class TestGenerateRandomJwtToken:
    """生成随机JWT Token测试"""

    def test_generate_token_length(self):
        """测试生成Token长度"""
        token = generate_random_jwt_token()
        
        parts = token.split(".")
        assert len(parts) == 3
        assert len(parts[0]) == 36  # header
        assert len(parts[1]) == 58   # payload
        assert len(parts[2]) == 43   # signature

    def test_generate_token_format(self):
        """测试生成Token格式"""
        token = generate_random_jwt_token()
        
        assert token.startswith("eyJhbGciOiJIUzI1NiJ9.")

    def test_generate_token_unique(self):
        """测试生成Token唯一性"""
        token1 = generate_random_jwt_token()
        token2 = generate_random_jwt_token()
        
        assert token1 != token2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
