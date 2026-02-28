# coding=utf-8
"""
角色查询相关命令
"""
from nonebot import on_command
from nonebot.adapters import Message, Event, Bot
from nonebot.params import CommandArg

from ..core import get_query_manager
from ..config import get_config


query_role = on_command('角色面板', aliases={'查询角色', 'role', 'char'}, priority=5, block=True)


@query_role.handle()
async def handle_query_role(bot: Bot, event: Event, args: Message = CommandArg()):
    """
    查询角色详情
    命令格式: /角色面板 <角色名>
    例如: /角色面板 忌炎
    """
    user_id = event.get_user_id()
    arg_text = args.extract_plain_text().strip()
    
    if not arg_text:
        await query_role.finish(
            "❌ 请指定要查询的角色！\n"
            "使用方法: /角色面板 <角色名>\n"
            "例如: /角色面板 忌炎"
        )
    
    config = get_config()
    query_manager = get_query_manager()
    
    # 根据配置决定输出格式
    if config.ENABLE_IMAGE_RENDER:
        # 使用图片输出
        success, result = await query_manager.query_role_image(user_id, arg_text)
        
        if not success:
            await query_role.finish(result)
        
        # 发送图片
        from nonebot.adapters.onebot.v11 import MessageSegment
        await query_role.finish(MessageSegment.image(result))
    else:
        # 使用文本输出
        success, message = await query_manager.query_role_text(user_id, arg_text)
        await query_role.finish(message)


query_role_list = on_command('角色列表', aliases={'我的角色', 'myroles'}, priority=5, block=True)


@query_role_list.handle()
async def handle_query_role_list(event: Event):
    """
    查询用户所有角色列表
    命令格式: /角色列表
    """
    user_id = event.get_user_id()
    
    query_manager = get_query_manager()
    
    success, message = await query_manager.query_role_list(user_id)
    
    await query_role_list.finish(message)
