# coding=utf-8
"""
工具函数单元测试
"""
import pytest
from datetime import datetime, timedelta
from pathlib import Path

from nonebot_plugin_wwuid.utils import (
    get_role_id_by_name,
    get_role_name_by_id,
    normalize_role_name,
    format_role_info,
    safe_int,
    safe_float,
    format_number,
    truncate_text,
    is_cache_expired,
    clear_cache,
    save_user_cache,
    load_user_cache,
    save_role_cache,
    load_role_cache,
)


class TestRoleNameMapping:
    """角色名称映射测试"""

    def test_get_role_id_by_name_success(self):
        """测试通过角色名获取ID - 成功"""
        assert get_role_id_by_name("忌炎") == 1403
        assert get_role_id_by_name("吟霖") == 1402
        assert get_role_id_by_name("今汐") == 1101

    def test_get_role_id_by_name_not_found(self):
        """测试通过角色名获取ID - 未找到"""
        assert get_role_id_by_name("不存在的角色") is None
        assert get_role_id_by_name("") is None

    def test_get_role_name_by_id_success(self):
        """测试通过ID获取角色名 - 成功"""
        assert get_role_name_by_id(1403) == "忌炎"
        assert get_role_name_by_id(1402) == "吟霖"
        assert get_role_name_by_id(1101) == "今汐"

    def test_get_role_name_by_id_not_found(self):
        """测试通过ID获取角色名 - 未找到"""
        assert get_role_name_by_id(9999) is None
        assert get_role_name_by_id(0) is None

    def test_normalize_role_name(self):
        """测试角色名标准化"""
        assert normalize_role_name(" 忌炎 ") == "忌炎"
        assert normalize_role_name("今　汐") == "今汐"
        assert normalize_role_name("吟 霖") == "吟霖"


class TestNumberUtils:
    """数字工具函数测试"""

    def test_safe_int_success(self):
        """测试安全转整数 - 成功"""
        assert safe_int("123") == 123
        assert safe_int(123) == 123
        assert safe_int(123.45) == 123

    def test_safe_int_default(self):
        """测试安全转整数 - 使用默认值"""
        assert safe_int("abc") == 0
        assert safe_int("") == 0
        assert safe_int(None) == 0
        assert safe_int("abc", default=10) == 10

    def test_safe_float_success(self):
        """测试安全转浮点数 - 成功"""
        assert safe_float("123.45") == 123.45
        assert safe_float(123.45) == 123.45
        assert safe_float(123) == 123.0

    def test_safe_float_default(self):
        """测试安全转浮点数 - 使用默认值"""
        assert safe_float("abc") == 0.0
        assert safe_float("") == 0.0
        assert safe_float(None) == 0.0
        assert safe_float("abc", default=10.5) == 10.5

    def test_format_number_int(self):
        """测试格式化数字 - 整数"""
        assert format_number(123) == "123"
        assert format_number(0) == "0"

    def test_format_number_float(self):
        """测试格式化数字 - 浮点数"""
        assert format_number(123.456, decimals=2) == "123.46"
        assert format_number(123.456, decimals=3) == "123.456"
        assert format_number(123.0, decimals=2) == "123"
        assert format_number(123.4500, decimals=2) == "123.45"


class TestTextUtils:
    """文本工具函数测试"""

    def test_truncate_text_no_truncate(self):
        """测试截断文本 - 不需要截断"""
        assert truncate_text("Hello", max_length=10) == "Hello"
        assert truncate_text("", max_length=10) == ""

    def test_truncate_text_truncate(self):
        """测试截断文本 - 需要截断"""
        assert truncate_text("Hello World", max_length=5) == "Hello..."
        assert truncate_text("1234567890", max_length=5) == "12345..."


class TestCacheUtils:
    """缓存工具函数测试"""

    def test_save_and_load_user_cache(self, tmp_path, test_user_id):
        """测试保存和加载用户缓存"""
        cache_data = {
            "role_list": [
                {"roleId": 1403, "roleName": "忌炎", "level": 80}
            ],
            "refresh_time": "2024-01-01T00:00:00",
        }

        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                
                save_user_cache(test_user_id, cache_data)
                loaded_data = load_user_cache(test_user_id)
                
                assert loaded_data is not None
                assert loaded_data["role_list"][0]["roleName"] == "忌炎"
                assert loaded_data["refresh_time"] == cache_data["refresh_time"]
            finally:
                os.chdir(original_cwd)

    def test_load_user_cache_not_found(self, test_user_id):
        """测试加载用户缓存 - 文件不存在"""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                data = load_user_cache(test_user_id)
                assert data is None
            finally:
                os.chdir(original_cwd)

    def test_save_and_load_role_cache(self, tmp_path, test_user_id, test_role_id):
        """测试保存和加载角色缓存"""
        cache_data = {
            "role": {
                "roleId": test_role_id,
                "roleName": "忌炎",
                "level": 80,
            },
            "chainList": [],
            "skillList": [],
        }

        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                
                save_role_cache(test_user_id, str(test_role_id), cache_data)
                loaded_data = load_role_cache(test_user_id, str(test_role_id))
                
                assert loaded_data is not None
                assert loaded_data["role"]["roleName"] == "忌炎"
            finally:
                os.chdir(original_cwd)

    def test_is_cache_expired_true(self):
        """测试缓存过期检查 - 已过期"""
        old_time = datetime.now() - timedelta(minutes=61)
        assert is_cache_expired(old_time, expire_minutes=60) is True

    def test_is_cache_expired_false(self):
        """测试缓存过期检查 - 未过期"""
        recent_time = datetime.now() - timedelta(minutes=30)
        assert is_cache_expired(recent_time, expire_minutes=60) is False

    def test_is_cache_expired_exact(self):
        """测试缓存过期检查 - 刚好过期"""
        exact_time = datetime.now() - timedelta(minutes=60)
        assert is_cache_expired(exact_time, expire_minutes=60) is False


class TestFormatRoleInfo:
    """角色信息格式化测试"""

    def test_format_role_info_with_mock_role(self, mock_role_data):
        """测试格式化角色信息"""
        from nonebot_plugin_wwuid.models import Role
        
        role = Role(**mock_role_data)
        text = format_role_info(role)
        
        assert "忌炎" in text
        assert "80" in text
        assert "5" in text
        assert "风" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
