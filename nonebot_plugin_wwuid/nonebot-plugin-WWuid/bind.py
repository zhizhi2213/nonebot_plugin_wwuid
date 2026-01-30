# coding=utf-8
"""
鸣潮CK绑定功能
"""
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from nonebot_plugin_orm import get_session
from sqlalchemy import select
from .models import WutheringWavesBind


# 注册命令：添加ck
bind_ck = on_command('添加ck', aliases={'绑定ck', 'bindck'}, priority=5, block=True)


@bind_ck.handle()
async def handle_bind_ck(event: Event, args: Message = CommandArg()):
    """
    处理添加CK命令
    命令格式: /添加ck <游戏UID> <CK>
    例如: /添加ck 123456789 abcdefgh1234567890
    """
    # 获取用户QQ号
    user_id = event.get_user_id()
    
    # 获取命令参数
    arg_text = args.extract_plain_text().strip()
    
    # 检查参数是否为空
    if not arg_text:
        await bind_ck.finish(
            "❌ 参数错误！\n"
            "使用方法: /添加ck <游戏UID> <CK>\n"
            "例如: /添加ck 123456789 your_cookie_here"
        )
    
    # 分割参数（按空格分割）
    params = arg_text.split(maxsplit=1)  # 最多分割1次，防止CK中有空格
    
    # 检查参数数量
    if len(params) != 2:
        await bind_ck.finish(
            "❌ 参数数量错误！\n"
            "需要提供两个参数：游戏UID 和 CK\n"
            "使用方法: /添加ck <游戏UID> <CK>"
        )
    
    game_uid, cookie = params
    
    # 简单验证UID格式（数字，长度合理）
    if not game_uid.isdigit():
        await bind_ck.finish("❌ 游戏UID格式错误，应该是纯数字！")
    
    # 简单验证CK长度
    if len(cookie) < 10:
        await bind_ck.finish("❌ CK长度太短，请检查是否完整！")
    
    # 数据库操作
    async with get_session() as session:
        # 查询该用户是否已经绑定过
        stmt = select(WutheringWavesBind).where(
            WutheringWavesBind.user_id == user_id
        )
        result = await session.execute(stmt)
        existing_bind = result.scalar_one_or_none()
        
        if existing_bind:
            # 用户已存在，更新绑定信息
            existing_bind.game_uid = game_uid
            existing_bind.cookie = cookie
            await session.commit()
            await bind_ck.finish(
                f"✅ 绑定信息已更新！\n"
                f"游戏UID: {game_uid}\n"
                f"提示：CK已安全保存"
            )
        else:
            # 新用户，创建绑定记录
            new_bind = WutheringWavesBind(
                user_id=user_id,
                game_uid=game_uid,
                cookie=cookie
            )
            session.add(new_bind)
            await session.commit()
            await bind_ck.finish(
                f"🎉 绑定成功！\n"
                f"游戏UID: {game_uid}\n"
                f"提示：CK已安全保存"
            )


# 注册命令：查询绑定
query_bind = on_command('我的ck', aliases={'查询绑定', 'myck'}, priority=5, block=True)


@query_bind.handle()
async def handle_query_bind(event: Event):
    """
    查询当前用户的绑定信息
    """
    user_id = event.get_user_id()
    
    async with get_session() as session:
        stmt = select(WutheringWavesBind).where(
            WutheringWavesBind.user_id == user_id
        )
        result = await session.execute(stmt)
        bind_info = result.scalar_one_or_none()
        
        if bind_info:
            # 隐藏CK的大部分内容，只显示前后几位
            masked_cookie = f"{bind_info.cookie[:6]}...{bind_info.cookie[-6:]}"
            await query_bind.finish(
                f"📋 你的绑定信息：\n"
                f"游戏UID: {bind_info.game_uid}\n"
                f"CK: {masked_cookie}\n"
                f"绑定时间: {bind_info.create_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            await query_bind.finish(
                "❌ 你还没有绑定游戏账号！\n"
                "请使用 /添加ck <游戏UID> <CK> 进行绑定"
            )


# 注册命令：解绑
unbind_ck = on_command('解绑ck', aliases={'删除ck', 'unbindck'}, priority=5, block=True)


@unbind_ck.handle()
async def handle_unbind_ck(event: Event):
    """
    解绑当前用户的游戏账号
    """
    user_id = event.get_user_id()
    
    async with get_session() as session:
        stmt = select(WutheringWavesBind).where(
            WutheringWavesBind.user_id == user_id
        )
        result = await session.execute(stmt)
        bind_info = result.scalar_one_or_none()
        
        if bind_info:
            await session.delete(bind_info)
            await session.commit()
            await unbind_ck.finish("✅ 解绑成功！你的游戏账号信息已删除。")
        else:
            await unbind_ck.finish("❌ 你还没有绑定游戏账号，无需解绑。")