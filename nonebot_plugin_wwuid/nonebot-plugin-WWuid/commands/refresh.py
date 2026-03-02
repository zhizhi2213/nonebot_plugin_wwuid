# coding=utf-8
"""
刷新相关命令
"""
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg

from ..core import get_refresh_manager


refresh_all = on_command('刷新面板', aliases={'刷新全部', 'refreshall'}, priority=5, block=True)


@refresh_all.handle()
async def handle_refresh_all(event: Event):
    """
    刷新所有角色数据
    命令格式: /刷新面板
    """
    user_id = event.get_user_id()
    
    refresh_manager = get_refresh_manager()
    
    await refresh_all.send("⏳ 正在刷新角色数据，请稍候...")
    
    success, message = await refresh_manager.refresh_all(user_id)
    
    await refresh_all.finish(message)


refresh_single = on_command('刷新', aliases={'刷新角色', 'refresh'}, priority=5, block=True)


@refresh_single.handle()
async def handle_refresh_single(event: Event, args: Message = CommandArg()):
    """
    刷新单个角色数据
    命令格式: /刷新 <角色名>
    例如: /刷新 忌炎
    """
    user_id = event.get_user_id()
    arg_text = args.extract_plain_text().strip()
    
    if not arg_text:
        await refresh_single.finish(
            "❌ 请指定要刷新的角色！\n"
            "使用方法: /刷新 <角色名>\n"
            "例如: /刷新 忌炎"
        )
    
    refresh_manager = get_refresh_manager()
    
    await refresh_single.send(f"⏳ 正在刷新 {arg_text} 的数据，请稍候...")
    
    success, message = await refresh_manager.refresh_single(user_id, arg_text)
    
    await refresh_single.finish(message)
