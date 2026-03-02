# coding=utf-8
"""
统计相关命令
"""
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg

from ..core import get_statistics_manager
from ..plugin_core.config import get_config


statistics_rank = on_command('练度统计', aliases={'练度排行', 'rank'}, priority=5, block=True)


@statistics_rank.handle()
async def handle_statistics_rank(event: Event, args: Message = CommandArg()):
    """
    查看角色练度排行榜
    命令格式: /练度统计 [数量]
    例如: /练度统计 10
    """
    user_id = event.get_user_id()
    arg_text = args.extract_plain_text().strip()
    
    config = get_config()
    top_n = config.STATISTICS_TOP_N
    
    if arg_text and arg_text.isdigit():
        top_n = min(int(arg_text), 20)
    
    await statistics_rank.send("⏳ 正在统计角色练度，请稍候...")
    
    statistics_manager = get_statistics_manager()
    success, message = await statistics_manager.get_statistics_text(user_id, top_n)
    
    await statistics_rank.finish(message)


statistics_summary = on_command('练度汇总', aliases={'角色汇总', 'summary'}, priority=5, block=True)


@statistics_summary.handle()
async def handle_statistics_summary(event: Event):
    """
    查看角色练度汇总
    命令格式: /练度汇总
    """
    user_id = event.get_user_id()
    
    statistics_manager = get_statistics_manager()
    success, message = await statistics_manager.get_role_summary_text(user_id)
    
    await statistics_summary.finish(message)
