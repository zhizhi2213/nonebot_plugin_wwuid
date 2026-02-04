from nonebot.plugin import PluginMetadata, inherit_supported_adapters

# 【新增】导入 CK 绑定功能
from .bind import bind_ck, query_bind, unbind_ck

# 【新增】导入角色练度功能
from .refresh import get_refresh_manager
from .query import get_query_manager
from .statistics import get_statistics_manager

# 【新增】导入角色练度命令
from .commands import (
    refresh_all,
    refresh_single,
    query_role,
    query_role_list,
    statistics_rank,
    statistics_summary,
)

__plugin_meta__ = PluginMetadata(
    name='鸣潮uid',
    description='查询鸣潮uid相关内容 + 用户绑定管理',
    usage='鸣潮uid帮助',
    type="application",
    homepage="https://github.com/zhizhi2213/nonebot_plugin_wwuid",  # 改成你的仓库地址
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", 
        "nonebot_plugin_htmlrender",
        "nonebot_plugin_apscheduler", 
        "nonebot_plugin_uninfo",
        "nonebot_plugin_orm"  # 【新增】添加 ORM 支持
    ),
    extra={
        'menu_data': [
            # 【新增】用户绑定相关功能
            {
                'func': '绑定游戏账号',
                'trigger_method': '添加ck <UID> <CK>',
                'trigger_condition': ' ',
                'brief_des': '绑定你的鸣潮游戏账号',
                'detail_des': '示例: /添加ck 123456789 your_cookie_here'
            },
            {
                'func': '查询绑定信息',
                'trigger_method': '我的ck',
                'trigger_condition': ' ',
                'brief_des': '查看你已绑定的游戏账号信息',
                'detail_des': '无'
            },
            {
                'func': '解绑游戏账号',
                'trigger_method': '解绑ck',
                'trigger_condition': ' ',
                'brief_des': '删除你的游戏账号绑定信息',
                'detail_des': '无'
            },
            # 【新增】角色练度相关功能
            {
                'func': '刷新面板',
                'trigger_method': '刷新面板',
                'trigger_condition': ' ',
                'brief_des': '刷新所有角色数据',
                'detail_des': '使用已绑定的CK获取最新角色数据'
            },
            {
                'func': '刷新单个角色',
                'trigger_method': '刷新 <角色名>',
                'trigger_condition': ' ',
                'brief_des': '刷新指定角色数据',
                'detail_des': '示例: /刷新 忌炎'
            },
            {
                'func': '查询角色面板',
                'trigger_method': '角色面板 <角色名>',
                'trigger_condition': ' ',
                'brief_des': '查看角色详细练度信息',
                'detail_des': '示例: /角色面板 忌炎'
            },
            {
                'func': '查看角色列表',
                'trigger_method': '角色列表',
                'trigger_condition': ' ',
                'brief_des': '查看所有已拥有角色',
                'detail_des': '显示所有角色的基础信息'
            },
            {
                'func': '练度统计',
                'trigger_method': '练度统计 [数量]',
                'trigger_condition': ' ',
                'brief_des': '查看角色练度排行榜',
                'detail_des': '示例: /练度统计 10'
            },
            {
                'func': '练度汇总',
                'trigger_method': '练度汇总',
                'trigger_condition': ' ',
                'brief_des': '查看角色练度汇总信息',
                'detail_des': '显示整体练度情况和统计'
            }
        ],
    },
)