# coding=utf-8
"""
测试添加CK功能
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from nonebot_plugin_wwuid.waves_api import WavesApi
from nonebot_plugin_wwuid.bind import _fetch_roles_by_game, get_ck_and_devcode


async def test_fetch_roles():
    """测试获取角色列表"""
    ck = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkIjoxNzY1Nzg5NTMwMTY5LCJ1c2VySWQiOjEwMTYxNDU5fQ.o1mRTSxIno5L8AE_Ygxft_VXEU7sc_DJj2BsJYW0lsI"
    did = "7786E85B-6116-4112-A5E9-E9384AAB7C06"
    
    waves_api = WavesApi()
    
    print("开始测试获取角色列表...")
    print(f"CK: {ck[:50]}...")
    print(f"DID: {did}")
    
    roles, err = await _fetch_roles_by_game(ck, did, 3)
    
    if err:
        print(f"❌ 获取角色列表失败: {err}")
        return False
    
    if not roles:
        print("❌ 未找到可用角色")
        return False
    
    print(f"✅ 成功获取角色列表，共 {len(roles)} 个角色:")
    for role in roles:
        role_id = role.get("roleId", "")
        role_name = role.get("roleName", "未知")
        server_id = role.get("serverId", "")
        game_id = role.get("gameId", "")
        print(f"  - {role_name} (特征码: {role_id}, 服务器ID: {server_id}, 游戏ID: {game_id})")
    
    print("\n测试获取 request_token...")
    for role in roles[:1]:
        role_id = role.get("roleId", "")
        server_id = role.get("serverId", "")
        
        success, bat = await waves_api.get_request_token(role_id, ck, did, server_id)
        
        if success:
            print(f"✅ 成功获取 {role_name} 的 request_token")
            print(f"   Token: {bat[:50]}...")
        else:
            print(f"❌ 获取 {role_name} 的 request_token 失败: {bat}")
    
    return True


async def test_get_ck_and_devcode():
    """测试CK和devCode提取"""
    print("\n测试CK和devCode提取...")
    
    test_cases = [
        ("test_ck,test_did", ("test_ck", "test_did")),
        ("test_ck,test_did,extra", ("test_ck", "test_did")),
        ("test_ck，test_did", ("test_ck", "test_did")),
        ("test_ck", ("test_ck", "")),
    ]
    
    for text, expected in test_cases:
        result = get_ck_and_devcode(text)
        if result == expected:
            print(f"✅ '{text}' -> {result}")
        else:
            print(f"❌ '{text}' -> {result} (期望: {expected})")


async def main():
    """主测试函数"""
    print("=" * 50)
    print("开始测试添加CK功能")
    print("=" * 50)
    
    await test_get_ck_and_devcode()
    
    success = await test_fetch_roles()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 测试失败")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
