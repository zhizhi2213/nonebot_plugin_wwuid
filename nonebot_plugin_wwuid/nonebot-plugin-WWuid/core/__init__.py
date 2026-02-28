# coding=utf-8
"""
核心功能层
与NoneBot框架解耦的业务逻辑层
"""
from .bind import bind_ck, query_bind_cmd, delete_ck_cmd, delete_invalid_ck_cmd
from .query import QueryManager, get_query_manager
from .refresh import RefreshManager, get_refresh_manager
from .statistics import StatisticsManager, get_statistics_manager
from .auto_delete import auto_delete_all_invalid_cookie

__all__ = [
    # 绑定管理
    "bind_ck",
    "query_bind_cmd",
    "delete_ck_cmd",
    "delete_invalid_ck_cmd",
    # 查询管理
    "QueryManager",
    "get_query_manager",
    # 刷新管理
    "RefreshManager",
    "get_refresh_manager",
    # 统计管理
    "StatisticsManager",
    "get_statistics_manager",
    # 自动删除
    "auto_delete_all_invalid_cookie",
]
