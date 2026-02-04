# coding=utf-8
"""
鸣潮角色练度命令
"""
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg

from .refresh import get_refresh_manager
from .query import get_query_manager
from .statistics import get_statistics_manager
from .utils import get_role_id_by_name, get_role_name_by_id


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


query_role = on_command('角色面板', aliases={'查询角色', 'role', 'char'}, priority=5, block=True)


@query_role.handle()
async def handle_query_role(event: Event, args: Message = CommandArg()):
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
    
    query_manager = get_query_manager()
    
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


statistics_rank = on_command('练度统计', aliases={'练度排行', 'rank'}, priority=5, block=True)


@statistics_rank.handle()
async def handle_statistics_rank(event: Event, args: Message = CommandArg()):
    """
    查看角色练度排行榜
    命令格式: /练度统计 [数量]
    例如: /练度统计 10
    """
    from .config import get_config
    
    user_id = event.get_user_id()
    arg_text = args.extract_plain_text().strip()
    
    config = get_config()
    top_n = config.STATISTICS_TOP_N
    
    if arg_text and arg_text.isdigit():
        top_n = min(int(arg_text), 20)
    
    await statistics_rank.send(f"⏳ 正在统计角色练度，请稍候...")
    
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
