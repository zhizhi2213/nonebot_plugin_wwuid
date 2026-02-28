# coding=utf-8
"""
绑定功能测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestBindFunctions:
    """测试绑定相关函数"""
    
    def test_get_ck_and_devcode(self):
        """测试解析CK和devCode"""
        from core.bind import get_ck_and_devcode
        
        # 正常情况
        ck, did = get_ck_and_devcode("cookie123,device456")
        assert ck == "cookie123"
        assert did == "device456"
        
        # 只有CK
        ck, did = get_ck_and_devcode("cookie123")
        assert ck == "cookie123"
        assert did == ""
        
        # 多空格
        ck, did = get_ck_and_devcode("  cookie123  ,  device456  ")
        assert ck == "cookie123"
        assert did == "device456"
