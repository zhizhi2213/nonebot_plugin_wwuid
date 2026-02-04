# coding=utf-8
"""
鸣潮角色数据刷新模块
"""
import asyncio
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

from nonebot import logger
from nonebot_plugin_orm import get_session

from .waves_api import WavesApi, WavesApiResponse
from .models import (
    WutheringWavesBind,
    RoleList,
    RoleDetailData,
    Role,
)
from .utils import (
    save_user_cache,
    save_role_cache,
    load_user_cache,
    get_cache_update_time,
    is_cache_expired,
    get_role_name_by_id,
    safe_int,
)
from .errors import error_reply, WAVES_CODE_102


class RefreshManager:
    """刷新管理器"""
    
    def __init__(self):
        self.api = WavesApi()
    
    async def refresh_all(self, user_id: str) -> Tuple[bool, str]:
        """刷新所有角色数据
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        logger.info(f"用户 {user_id} 请求刷新所有角色数据")
        
        ck = await self._get_user_ck(user_id)
        if not ck:
            return False, error_reply(WAVES_CODE_102)
        
        role_id = await self._get_user_role_id(user_id, ck)
        if not role_id:
            return False, error_reply(WAVES_CODE_102)
        
        try:
            await self.api.login_log(role_id, ck)
        except Exception as e:
            logger.warning(f"登录校验失败: {e}")
        
        role_list_response = await self.api.get_role_info(role_id, ck)
        if not role_list_response.success:
            return False, error_reply(role_list_response.code, role_list_response.message)
        
        role_list_data = role_list_response.data
        if not role_list_data or "roleList" not in role_list_data:
            return False, error_reply(101, "未获取到角色列表")
        
        role_list = role_list_data["roleList"]
        if not role_list:
            return False, error_reply(101, "角色列表为空")
        
        role_ids = [role["roleId"] for role in role_list]
        
        success_count = 0
        failed_count = 0
        failed_roles = []
        
        await self.api.refresh_data(role_id, ck)
        await asyncio.sleep(1)
        
        for role_info in role_list:
            char_id = role_info["roleId"]
            try:
                role_detail_response = await self.api.get_role_detail_info(
                    str(char_id), role_id, ck
                )
                
                if role_detail_response.success:
                    role_detail_data = role_detail_response.data
                    if role_detail_data:
                        save_role_cache(user_id, str(char_id), role_detail_data)
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_roles.append(get_role_name_by_id(char_id) or f"ID:{char_id}")
                else:
                    failed_count += 1
                    failed_roles.append(get_role_name_by_id(char_id) or f"ID:{char_id}")
                    logger.warning(f"获取角色 {char_id} 详情失败: {role_detail_response.message}")
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                failed_count += 1
                failed_roles.append(get_role_name_by_id(char_id) or f"ID:{char_id}")
                logger.error(f"刷新角色 {char_id} 时发生错误: {e}")
        
        cache_data = {
            "role_list": role_list,
            "refresh_time": datetime.now().isoformat(),
            "success_count": success_count,
            "failed_count": failed_count,
        }
        save_user_cache(user_id, cache_data)
        
        if failed_count == 0:
            message = f"✅ 刷新完成！成功获取 {success_count} 个角色数据"
        elif success_count == 0:
            message = f"❌ 刷新失败！所有角色数据获取失败"
        else:
            failed_text = ", ".join(failed_roles[:3])
            if failed_count > 3:
                failed_text += f" 等 {failed_count} 个角色"
            message = f"⚠️ 刷新完成！成功 {success_count} 个，失败 {failed_count} 个\n失败角色: {failed_text}"
        
        return True, message
    
    async def refresh_single(self, user_id: str, role_name: str) -> Tuple[bool, str]:
        """刷新单个角色数据
        
        Args:
            user_id: 用户ID
            role_name: 角色名称
        
        Returns:
            Tuple[bool, str]: (是否成功, 返回消息)
        """
        from .utils import get_role_id_by_name
        
        logger.info(f"用户 {user_id} 请求刷新角色 {role_name}")
        
        role_id_by_name = get_role_id_by_name(role_name)
        if not role_id_by_name:
            return False, f"❌ 未找到角色: {role_name}"
        
        ck = await self._get_user_ck(user_id)
        if not ck:
            return False, error_reply(WAVES_CODE_102)
        
        role_id = await self._get_user_role_id(user_id, ck)
        if not role_id:
            return False, error_reply(WAVES_CODE_102)
        
        try:
            await self.api.login_log(role_id, ck)
        except Exception as e:
            logger.warning(f"登录校验失败: {e}")
        
        await self.api.refresh_data(role_id, ck)
        await asyncio.sleep(1)
        
        try:
            role_detail_response = await self.api.get_role_detail_info(
                str(role_id_by_name), role_id, ck
            )
            
            if not role_detail_response.success:
                return False, error_reply(role_detail_response.code, role_detail_response.message)
            
            role_detail_data = role_detail_response.data
            if not role_detail_data:
                return False, error_reply(101, "未获取到角色数据")
            
            save_role_cache(user_id, str(role_id_by_name), role_detail_data)
            
            return True, f"✅ 刷新成功！{role_name} 数据已更新"
            
        except Exception as e:
            logger.error(f"刷新角色 {role_name} 时发生错误: {e}")
            return False, f"❌ 刷新失败: {str(e)}"
    
    async def _get_user_ck(self, user_id: str) -> Optional[str]:
        """获取用户CK"""
        async with get_session() as session:
            result = await session.execute(
                "SELECT waves_ck FROM wuthering_waves_bind WHERE user_id = ?",
                (user_id,)
            )
            row = result.fetchone()
            if row:
                return row[0]
            return None
    
    async def _get_user_role_id(self, user_id: str, ck: str) -> Optional[str]:
        """获取用户游戏角色ID"""
        try:
            base_info_response = await self.api.get_base_info("0", ck)
            if base_info_response.success:
                data = base_info_response.data
                if data and "roleBoxBaseData" in data:
                    base_data = data["roleBoxBaseData"]
                    if base_data and len(base_data) > 0:
                        return str(base_data[0].get("roleId", "0"))
            return None
        except Exception as e:
            logger.error(f"获取用户角色ID失败: {e}")
            return None
    
    async def get_cached_role_list(self, user_id: str) -> Optional[List[Role]]:
        """获取缓存的角色列表"""
        cache_data = load_user_cache(user_id)
        if not cache_data:
            return None
        
        role_list_data = cache_data.get("role_list", [])
        if not role_list_data:
            return None
        
        roles = []
        for role_data in role_list_data:
            try:
                role = Role(**role_data)
                roles.append(role)
            except Exception as e:
                logger.warning(f"解析角色数据失败: {e}")
        
        return roles
    
    async def get_cached_role_detail(
        self, 
        user_id: str, 
        role_id: str
    ) -> Optional[RoleDetailData]:
        """获取缓存的角色详情"""
        from .utils import load_role_cache
        
        cache_data = load_role_cache(user_id, role_id)
        if not cache_data:
            return None
        
        try:
            return RoleDetailData(**cache_data)
        except Exception as e:
            logger.warning(f"解析角色详情数据失败: {e}")
            return None
    
    async def get_cached_role_detail_by_name(
        self, 
        user_id: str, 
        role_name: str
    ) -> Optional[RoleDetailData]:
        """通过角色名获取缓存的角色详情"""
        from .utils import get_role_id_by_name
        
        role_id = get_role_id_by_name(role_name)
        if not role_id:
            return None
        
        return await self.get_cached_role_detail(user_id, str(role_id))


_refresh_manager: Optional[RefreshManager] = None


def get_refresh_manager() -> RefreshManager:
    """获取刷新管理器实例"""
    global _refresh_manager
    if _refresh_manager is None:
        _refresh_manager = RefreshManager()
    return _refresh_manager
