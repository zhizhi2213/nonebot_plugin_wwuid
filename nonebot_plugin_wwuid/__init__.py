from nonebot.plugin import PluginMetadata, inherit_supported_adapters



__plugin_meta__ = PluginMetadata(
    name='鸣潮uid',
    description='查询鸣潮uid相关内容',
    usage='鸣潮uid帮助',
    type="application",
    homepage="https://github.com/Zyone2/nonebot_plugin_wwuid",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_htmlrender","nonebot_plugin_apscheduler", "nonebot_plugin_uninfo"),
    extra={
        'menu_data': [
            {
                'func': '添加token',
                'trigger_method': '绑定鸣潮信息',
                'trigger_condition': ' ',
                'brief_des': '添加token ck,token',
                'detail_des': '无'
            },
        ],
    },
)
