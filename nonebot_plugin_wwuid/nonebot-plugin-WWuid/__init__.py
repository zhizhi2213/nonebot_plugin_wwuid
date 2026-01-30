from nonebot.plugin import PluginMetadata, inherit_supported_adapters

# 【新增】导入 CK 绑定功能
from .bind import bind_ck, query_bind, unbind_ck

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
            }
        ],
    },
)