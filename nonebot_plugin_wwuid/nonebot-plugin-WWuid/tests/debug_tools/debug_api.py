# coding=utf-8
"""
API调试工具
用于快速测试API接口和查看响应数据

使用方法:
    python tests/debug_tools/debug_api.py

功能:
    1. 测试get_request_token
    2. 测试get_game_role_list
    3. 测试get_role_detail
    4. 保存API响应供分析
"""
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from nonebot_plugin_wwuid.api.models import RoleDetailData
from nonebot_plugin_wwuid.api.waves_api import WavesApi, WavesApiResponse


class APIDebugger:
    """API调试器"""
    
    def __init__(self):
        self.api = WavesApi()
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)
    
    def save_response(self, name: str, data: dict):
        """保存API响应到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 响应数据已保存到: {filepath}")
        return filepath
    
    async def test_get_request_token(self, token: str, dev_code: str):
        """测试获取请求token"""
        print("\n" + "="*50)
        print("测试: get_request_token")
        print("="*50)
        
        try:
            result = await self.api.get_request_token(token, dev_code)
            print(f"结果类型: {type(result)}")
            print(f"结果: {result}")
            
            if result:
                self.save_response("request_token", {"token": result})
            
            return result
        except Exception as e:
            print(f"✗ 错误: {e}")
            return None
    
    async def test_get_game_role_list(self, token: str, dev_code: str):
        """测试获取游戏角色列表"""
        print("\n" + "="*50)
        print("测试: get_game_role_list")
        print("="*50)
        
        try:
            result = await self.api.get_game_role_list(token, dev_code)
            print(f"结果类型: {type(result)}")
            
            if result:
                roles = result.get("roleList", [])
                print(f"角色数量: {len(roles)}")
                
                for i, role in enumerate(roles[:5]):  # 只显示前5个
                    print(f"  [{i+1}] {role.get('roleName')} (ID: {role.get('roleId')}, Lv.{role.get('level')})")
                
                self.save_response("game_role_list", result)
            
            return result
        except Exception as e:
            print(f"✗ 错误: {e}")
            return None
    
    async def test_get_role_detail(self, token: str, dev_code: str, role_id: int, server_id: str = "76402e5b20be2c79f95d4f4ad46e55b1"):
        """测试获取角色详情"""
        print("\n" + "="*50)
        print(f"测试: get_role_detail (role_id={role_id})")
        print("="*50)
        
        try:
            result = await self.api.get_role_detail(token, dev_code, role_id, server_id)
            print(f"结果类型: {type(result)}")
            
            if result:
                role = result.get("role", {})
                print(f"角色名称: {role.get('roleName')}")
                print(f"角色等级: {role.get('level')}")
                
                weapon = result.get("weaponData", {}).get("weapon", {})
                if weapon:
                    print(f"武器: {weapon.get('weaponName')}")
                
                chains = result.get("chainList", [])
                unlocked = sum(1 for c in chains if c.get("unlocked"))
                print(f"命座: {unlocked}/6")
                
                phantoms = result.get("phantomData", {}).get("equipPhantomList", [])
                print(f"声骸: {len(phantoms)}/5")
                
                self.save_response(f"role_detail_{role_id}", result)
            
            return result
        except Exception as e:
            print(f"✗ 错误: {e}")
            return None
    
    async def run_all_tests(self, token: str, dev_code: str, role_id: int = None):
        """运行所有测试"""
        print("\n" + "="*50)
        print("鸣潮UID插件 - API调试工具")
        print("="*50)
        print(f"Token: {token[:20]}..." if len(token) > 20 else f"Token: {token}")
        print(f"DevCode: {dev_code[:20]}..." if len(dev_code) > 20 else f"DevCode: {dev_code}")
        
        # 测试1: 获取请求token
        request_token = await self.test_get_request_token(token, dev_code)
        
        if not request_token:
            print("\n✗ 获取请求token失败，停止后续测试")
            return
        
        # 测试2: 获取角色列表
        role_list = await self.test_get_game_role_list(token, dev_code)
        
        if not role_list:
            print("\n✗ 获取角色列表失败")
            return
        
        # 测试3: 获取角色详情
        if role_id:
            await self.test_get_role_detail(token, dev_code, role_id)
        else:
            # 自动选择第一个角色
            roles = role_list.get("roleList", [])
            if roles:
                first_role = roles[0]
                role_id = first_role.get("roleId")
                server_id = first_role.get("serverId", "76402e5b20be2c79f95d4f4ad46e55b1")
                print(f"\n自动选择角色: {first_role.get('roleName')} (ID: {role_id})")
                await self.test_get_role_detail(token, dev_code, role_id, server_id)
        
        print("\n" + "="*50)
        print("测试完成!")
        print(f"输出目录: {self.output_dir}")
        print("="*50)


def print_usage():
    """打印使用说明"""
    print("""
使用方法:
    python tests/debug_tools/debug_api.py <token> <dev_code> [role_id]

参数:
    token       - 游戏token
    dev_code    - 设备代码
    role_id     - 角色ID（可选，默认使用第一个角色）

示例:
    python tests/debug_tools/debug_api.py "your_token_here" "your_dev_code_here"
    python tests/debug_tools/debug_api.py "your_token_here" "your_dev_code_here" 1401
    """)


async def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    token = sys.argv[1]
    dev_code = sys.argv[2]
    role_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    debugger = APIDebugger()
    await debugger.run_all_tests(token, dev_code, role_id)


if __name__ == "__main__":
    asyncio.run(main())
