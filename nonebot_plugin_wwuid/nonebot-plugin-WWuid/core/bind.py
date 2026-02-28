# coding=utf-8
"""
鸣潮CK绑定功能
"""
from typing import Optional
from nonebot import on_command, get_bot
from nonebot.adapters import Event
from nonebot.params import CommandArg
from nonebot_plugin_orm import get_session
from sqlalchemy import select, delete
from ..api.models import WutheringWavesBind
from ..api.waves_api import WavesApi
from ..constants import WAVES_GAME_ID

waves_api = WavesApi()


def get_ck_and_devcode(text: str, split_str: str = ",") -> tuple[str, str]:
    """从文本中提取CK和devCode"""
    parts = text.split(split_str)
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    return text.strip(), ""


async def _fetch_roles_by_game(ck: str, did: str, game_id: int = WAVES_GAME_ID):
    """通过游戏ID获取角色列表"""
    roles = await waves_api.get_kuro_role_list(ck, did, game_id)
    if not roles.success or not roles.data or not isinstance(roles.data, list):
        return None, roles.throw_msg()
    return roles.data, None


async def add_cookie(event: Event, ck: str, did: str = "", is_login: bool = False) -> str:
    """添加Cookie并自动获取角色信息"""
    user_id = event.get_user_id()
    bot_id = str(event.get_self_id())
    group_id = str(event.group_id) if hasattr(event, 'group_id') and event.group_id else ""
    
    waves_roles, err = await _fetch_roles_by_game(ck, did, WAVES_GAME_ID)
    if err:
        return err
    
    if not waves_roles:
        return "登录失败\n未找到可用角色"
    
    role_list = []
    
    async with get_session() as session:
        for role_data in waves_roles:
            if role_data.get("gameId") != WAVES_GAME_ID:
                continue
            
            role_id = role_data.get("roleId", "")
            role_name = role_data.get("roleName", "未知角色")
            server_id = role_data.get("serverId", "")
            
            if not role_id:
                continue
            
            success, bat = await waves_api.get_request_token(role_id, ck, did, server_id)
            if not success:
                return f"获取令牌失败: {bat}"
            
            existing_bind = await session.execute(
                select(WutheringWavesBind).where(
                    WutheringWavesBind.user_id == user_id,
                    WutheringWavesBind.bot_id == bot_id,
                    WutheringWavesBind.game_uid == role_id,
                    WutheringWavesBind.game_id == WAVES_GAME_ID
                )
            )
            existing_bind = existing_bind.scalar_one_or_none()
            
            if existing_bind:
                existing_bind.cookie = ck
                existing_bind.status = ""
                existing_bind.did = did
                existing_bind.bat = bat
                existing_bind.platform = "qq"
                existing_bind.is_login = existing_bind.is_login or is_login
                existing_bind.group_id = group_id
                
                final_is_login = existing_bind.is_login or is_login
                if final_is_login and did:
                    await WutheringWavesBind.update_token_by_login(role_id, WAVES_GAME_ID, ck, did)
            else:
                new_bind = WutheringWavesBind(
                    user_id=user_id,
                    bot_id=bot_id,
                    game_uid=role_id,
                    cookie=ck,
                    did=did,
                    bat=bat,
                    status="",
                    game_id=WAVES_GAME_ID,
                    is_login=is_login,
                    platform="qq",
                    group_id=group_id
                )
                session.add(new_bind)
                
                if is_login and did:
                    await WutheringWavesBind.update_token_by_login(role_id, WAVES_GAME_ID, ck, did)
            
            role_list.append(
                {
                    "名字": role_name,
                    "特征码": role_id,
                }
            )
        
        await session.commit()
    
    if not role_list:
        return "登录失败\n"
    
    msg = []
    for role in role_list:
        msg.append(f"[鸣潮]【{role['名字']}】特征码【{role['特征码']}】登录成功!")
    return "\n".join(msg)


async def delete_cookie(user_id: str, uid: str, bot_id: str = "") -> str:
    """删除指定UID的Cookie"""
    async with get_session() as session:
        stmt = delete(WutheringWavesBind).where(
            WutheringWavesBind.user_id == user_id,
            WutheringWavesBind.game_uid == uid
        )
        if bot_id:
            stmt = stmt.where(WutheringWavesBind.bot_id == bot_id)
        
        result = await session.execute(stmt)
        await session.commit()
        
        if result.rowcount == 0:
            return f"[鸣潮] 特征码[{uid}]的token删除失败!\n❌不存在该特征码的token!\n"
        return f"[鸣潮] 特征码[{uid}]的token删除成功!\n"


async def refresh_bind(event: Event) -> str:
    """刷新绑定"""
    user_id = event.get_user_id()
    bot_id = str(event.get_self_id())
    group_id = str(event.group_id) if hasattr(event, 'group_id') and event.group_id else ""
    
    async with get_session() as session:
        result = await session.execute(
            select(WutheringWavesBind).where(
                WutheringWavesBind.user_id == user_id,
                WutheringWavesBind.bot_id == bot_id,
                WutheringWavesBind.game_id == WAVES_GAME_ID
            )
        )
        user_list = result.scalars().all()
    
    if not user_list:
        return "未找到可用的token，请先登录或添加token\n"
    
    waves_msg = []
    seen_waves = set()
    invalid = False
    
    for user in user_list:
        if not user.cookie or user.status == "无效":
            continue
        
        login_res = await waves_api.login_log(user.game_uid, user.cookie)
        if not login_res.success:
            invalid = True
            continue
        
        waves_roles, err = await _fetch_roles_by_game(user.cookie, user.did, WAVES_GAME_ID)
        if err:
            continue
        
        if waves_roles:
            for role in waves_roles:
                if role.get("gameId") != WAVES_GAME_ID:
                    continue
                
                role_id = role.get("roleId", "")
                role_name = role.get("roleName", "未知角色")
                
                if not role_id or role_id in seen_waves:
                    continue
                
                seen_waves.add(role_id)
                waves_msg.append(f"[鸣潮]已刷新【{role_name}】特征码【{role_id}】")
    
    if not waves_msg:
        if invalid:
            return "刷新绑定失败，token已失效，请重新登录后再试\n"
        return "刷新绑定失败，请确认token有效后重试\n"
    
    return "\n".join(waves_msg)


bind_ck = on_command("添加CK", aliases={"添加ck", "添加Token", "添加token", "添加TOKEN"}, priority=5, block=True)


@bind_ck.handle()
async def handle_bind_ck(event: Event, args: str = CommandArg()):
    """处理添加CK命令"""
    at_sender = True if hasattr(event, 'group_id') and event.group_id else False
    text = args.extract_plain_text().strip()
    
    ck, did = "", ""
    for split_char in ["，", ","]:
        if split_char in text:
            ck, did = get_ck_and_devcode(text, split_str=split_char)
            break
    
    if not ck:
        ck = text.strip()
    
    if did and len(did) not in (32, 36, 40):
        msg = "❌ devCode长度错误！\n应为32、36或40位"
        return await bind_ck.finish(f"{'@' + str(event.user_id) + ' ' if at_sender else ''}{msg}")
    
    if not ck:
        msg = "❌ 参数错误！\n使用方法: /添加CK <CK> [devCode]\n例如: /添加CK your_cookie_here"
        return await bind_ck.finish(f"{'@' + str(event.user_id) + ' ' if at_sender else ''}{msg}")
    
    ck_msg = await add_cookie(event, ck, did, is_login=False)
    await bind_ck.finish(f"{'@' + str(event.user_id) + ' ' if at_sender else ''}{ck_msg}")


refresh_bind_cmd = on_command("刷新绑定", aliases={"刷新CK", "刷新ck"}, priority=5, block=True)


@refresh_bind_cmd.handle()
async def handle_refresh_bind(event: Event):
    """处理刷新绑定命令"""
    msg = await refresh_bind(event)
    await refresh_bind_cmd.finish(msg)


delete_ck_cmd = on_command("删除CK", aliases={"删除ck", "删除Token", "删除token"}, priority=5, block=True)


@delete_ck_cmd.handle()
async def handle_delete_ck(event: Event, args: str = CommandArg()):
    """处理删除CK命令"""
    user_id = event.get_user_id()
    bot_id = str(event.get_self_id())
    
    uid = args.extract_plain_text().strip()
    
    if not uid:
        async with get_session() as session:
            result = await session.execute(
                select(WutheringWavesBind).where(
                    WutheringWavesBind.user_id == user_id,
                    WutheringWavesBind.game_id == WAVES_GAME_ID
                )
            )
            binds = result.scalars().all()
        
        if not binds:
            msg = "❌ 未找到绑定的token"
            return await delete_ck_cmd.finish(msg)
        
        msg = "📋 你的绑定列表：\n"
        for bind in binds:
            status = "✅有效" if bind.status != "无效" else "❌失效"
            msg += f"特征码: {bind.game_uid} ({status})\n"
        msg += "\n使用 /删除CK <特征码> 删除指定绑定"
        return await delete_ck_cmd.finish(msg)
    
    msg = await delete_cookie(user_id, uid, bot_id)
    await delete_ck_cmd.finish(msg)


query_bind_cmd = on_command("我的CK", aliases={"查询绑定", "myck"}, priority=5, block=True)


@query_bind_cmd.handle()
async def handle_query_bind(event: Event):
    """查询绑定信息"""
    user_id = event.get_user_id()
    
    async with get_session() as session:
        result = await session.execute(
            select(WutheringWavesBind).where(
                WutheringWavesBind.user_id == user_id,
                WutheringWavesBind.game_id == WAVES_GAME_ID
            )
        )
        binds = result.scalars().all()
    
    if not binds:
        msg = "❌ 你还没有绑定游戏账号！\n请使用 /添加CK <CK> [devCode] 进行绑定"
        return await query_bind_cmd.finish(msg)
    
    msg = []
    for bind in binds:
        if not (bind.game_uid and bind.game_uid.isdigit() and len(bind.game_uid) == 9):
            continue
        if not bind.cookie or bind.status == "无效":
            continue
        
        msg.append(f"鸣潮特征码: {bind.game_uid} 的 token 和 did")
        msg.append(f"添加token {bind.cookie}, {bind.did}")
        msg.append("--------------------------------")
    
    if not msg:
        msg = "您当前未绑定token或者token已全部失效\n"
        return await query_bind_cmd.finish(msg)
    
    msg.append("直接复制并加上前缀即可用于token登录")
    
    return await query_bind_cmd.finish("\n".join(msg))


delete_invalid_ck_cmd = on_command("删除无效CK", aliases={"删除无效ck", "删除无效token"}, priority=5, block=True)


@delete_invalid_ck_cmd.handle()
async def handle_delete_invalid_ck(event: Event):
    """删除所有无效CK"""
    user_id = event.get_user_id()
    
    del_count = await WutheringWavesBind.delete_all_invalid_cookie(WAVES_GAME_ID)
    
    if del_count == 0:
        msg = "✅ 当前没有无效的token需要删除"
    else:
        msg = f"✅ 已成功删除 {del_count} 个无效token"
    
    await delete_invalid_ck_cmd.finish(msg)
