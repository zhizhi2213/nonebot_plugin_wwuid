# coding=utf-8
"""
鸣潮API请求模块
"""
import json
import random
import string
from typing import Dict, Any, Optional, List
from datetime import datetime

import httpx

from .errors import (
    WAVES_CODE_101,
    WAVES_CODE_102,
    WAVES_CODE_999,
)


class WavesApiResponse:
    """API响应统一格式"""
    
    def __init__(self, code: int = 0, data: Any = None, message: str = ""):
        self.code = code
        self.data = data
        self.message = message
    
    @property
    def success(self) -> bool:
        return self.code == 0
    
    def throw_msg(self) -> str:
        return self.message or f"错误代码: {self.code}"
    
    def model_dump(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "data": self.data,
            "message": self.message
        }


class WavesApi:
    """鸣潮API客户端"""
    
    def __init__(self):
        self.SERVER_ID = "76402e5b20be2c39f095a152090afddc"
        self.MAIN_URL = "https://api.kurobbs.com"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        await self.client.aclose()
    
    def _get_server_id(self, role_id: str) -> str:
        """获取服务器ID"""
        try:
            role_id_int = int(role_id)
            if role_id_int >= 200000000:
                return "919752ae5ea09c1ced910dd668a63ffb"
        except (ValueError, TypeError):
            pass
        return self.SERVER_ID
    
    def _get_headers(self, cookie: str, role_id: str) -> Dict[str, str]:
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "token": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    async def _request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        role_id: Optional[str] = None,
    ) -> WavesApiResponse:
        """统一请求方法"""
        try:
            if method.upper() == "GET":
                response = await self.client.get(url, headers=headers)
            else:
                response = await self.client.post(url, json=data, headers=headers)
            
            result = response.json()
            
            if isinstance(result, dict):
                code = result.get("code", -1)
                data = result.get("data", None)
                if isinstance(data, str) and data:
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        pass
                message = result.get("message", "")
                return WavesApiResponse(code=code, data=data, message=message)
            else:
                return WavesApiResponse(code=-1, message="响应格式错误")
                
        except httpx.TimeoutException:
            return WavesApiResponse(code=WAVES_CODE_999, message="请求超时")
        except httpx.RequestError as e:
            return WavesApiResponse(code=WAVES_CODE_999, message=f"网络错误: {str(e)}")
        except Exception as e:
            return WavesApiResponse(code=WAVES_CODE_999, message=f"未知错误: {str(e)}")
    
    async def login_log(self, role_id: str, cookie: str) -> WavesApiResponse:
        """登录校验"""
        url = f"{self.MAIN_URL}/user/login/log"
        headers = self._get_headers(cookie, role_id)
        headers["version"] = "1.0"
        return await self._request(url, method="POST", headers=headers)
    
    async def get_base_info(self, role_id: str, cookie: str) -> WavesApiResponse:
        """获取账户基础信息"""
        url = f"{self.MAIN_URL}/aki/roleBox/akiBox/baseData"
        headers = self._get_headers(cookie, role_id)
        
        data = {
            "gameId": 2,
            "serverId": self._get_server_id(role_id),
            "roleId": role_id,
        }
        
        return await self._request(url, method="POST", data=data, headers=headers)
    
    async def get_role_info(self, role_id: str, cookie: str) -> WavesApiResponse:
        """获取角色列表"""
        url = f"{self.MAIN_URL}/gamer/role/list"
        headers = self._get_headers(cookie, role_id)
        headers["devCode"] = ""
        
        data = {"gameId": 2}
        
        return await self._request(url, method="POST", data=data, headers=headers)
    
    async def get_role_detail_info(
        self,
        char_id: str,
        role_id: str,
        cookie: str,
    ) -> WavesApiResponse:
        """获取单个角色详情"""
        url = f"{self.MAIN_URL}/aki/roleBox/akiBox/getRoleDetail"
        headers = self._get_headers(cookie, role_id)
        
        data = {
            "gameId": 2,
            "serverId": self._get_server_id(role_id),
            "roleId": role_id,
            "channelId": "19",
            "countryCode": "1",
            "id": char_id,
        }
        
        return await self._request(url, method="POST", data=data, headers=headers)
    
    async def refresh_data(self, role_id: str, cookie: str) -> WavesApiResponse:
        """刷新数据"""
        url = f"{self.MAIN_URL}/aki/roleBox/akiBox/refreshData"
        headers = self._get_headers(cookie, role_id)
        
        data = {
            "gameId": 2,
            "serverId": self._get_server_id(role_id),
            "roleId": role_id,
        }
        
        return await self._request(url, method="POST", data=data, headers=headers)
    
    async def get_owned_role_info(self, role_id: str, cookie: str) -> WavesApiResponse:
        """获取已拥有角色信息"""
        url = f"{self.MAIN_URL}/aki/calculator/ownedRole/roleInfo"
        headers = self._get_headers(cookie, role_id)
        
        data = {
            "serverId": self._get_server_id(role_id),
            "roleId": role_id,
        }
        
        return await self._request(url, method="POST", data=data, headers=headers)


def generate_random_jwt_token() -> str:
    """生成随机JWT Token（用于兜底）"""
    chars = string.ascii_letters + string.digits
    payload = "".join(random.choice(chars) for _ in range(58))
    signature = "".join(random.choice(chars) for _ in range(43))
    return f"eyJhbGciOiJIUzI1NiJ9.{payload}.{signature}"
