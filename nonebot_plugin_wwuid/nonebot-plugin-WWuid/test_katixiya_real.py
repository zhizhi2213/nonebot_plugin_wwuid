# coding=utf-8
"""
卡提希娅角色练度卡片生成 - 使用真实API数据
从库洛API获取真实的图标URL并下载
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("卡提希娅角色练度卡片生成 - 真实API数据")
print("="*60)

# 检查依赖
print("\n[1/6] 检查依赖...")
try:
    from PIL import Image
    print("  ✓ PIL 已安装")
except ImportError as e:
    print(f"  ✗ PIL 未安装: {e}")
    sys.exit(1)

try:
    import httpx
    print("  ✓ httpx 已安装")
except ImportError as e:
    print(f"  ✗ httpx 未安装: {e}")
    sys.exit(1)

# 创建输出目录
print("\n[2/6] 创建输出目录...")
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
cache_dir = Path(__file__).parent / "cache" / "icons"
cache_dir.mkdir(parents=True, exist_ok=True)
print(f"  ✓ 输出目录: {output_dir}")
print(f"  ✓ 缓存目录: {cache_dir}")

# 从API获取角色数据
print("\n[3/6] 从API获取角色数据...")

async def fetch_role_data():
    """从库洛API获取角色数据"""
    try:
        from api.waves_api import WavesApi
    except ImportError:
        from .api.waves_api import WavesApi
    
    api = WavesApi()
    
    # 获取在线角色列表（不需要认证）
    print("  获取角色列表...")
    response = await api.get_online_role_list()
    
    if not response.success:
        print(f"  ✗ 获取角色列表失败: {response.message}")
        return None
    
    roles = response.data
    
    # 查找卡提希娅
    katixiya = None
    for role in roles:
        if role.roleId == 1604 or "卡提" in role.roleName:
            katixiya = role
            break
    
    if not katixiya:
        print("  ✗ 未找到卡提希娅角色数据")
        print(f"  可用角色数量: {len(roles)}")
        # 显示前5个角色
        for i, role in enumerate(roles[:5]):
            print(f"    - {role.roleName} (ID: {role.roleId})")
        return None
    
    print(f"  ✓ 找到角色: {katixiya.roleName} (ID: {katixiya.roleId})")
    print(f"  ✓ 角色图标URL: {katixiya.roleIconUrl}")
    
    return katixiya

# 下载图标
print("\n[4/6] 下载图标...")

async def download_icon(url: str, cache_path: Path) -> bool:
    """下载图标到本地缓存"""
    if cache_path.exists():
        print(f"  使用缓存: {cache_path.name}")
        return True
    
    if not url:
        return False
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            if response.status_code == 200:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                with open(cache_path, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ 下载成功: {cache_path.name}")
                return True
            else:
                print(f"  ✗ 下载失败 ({response.status_code}): {url}")
                return False
    except Exception as e:
        print(f"  ✗ 下载错误: {e}")
        return False

# 主函数
async def main():
    # 获取角色数据
    role_data = await fetch_role_data()
    
    if not role_data:
        print("\n  使用模拟数据继续...")
        # 使用已知的真实URL格式
        role_icon_url = "https://web-static.kurobbs.com/adminConfig/36/role_icon/1716031298428.png"
        weapon_icon_url = "https://web-static.kurobbs.com/adminConfig/29/weapon_icon/1716031228478.png"
    else:
        role_icon_url = role_data.roleIconUrl
        weapon_icon_url = None  # 需要从武器API获取
    
    # 下载角色图标
    print("\n[5/6] 下载资源...")
    role_icon_path = cache_dir / "katixiya_role.png"
    await download_icon(role_icon_url, role_icon_path)
    
    # 创建角色数据（使用真实URL）
    print("\n[6/6] 创建角色卡片...")
    
    from unittest.mock import MagicMock
    from renderer import render_role_card, get_renderer
    
    # 创建角色数据
    role = MagicMock()
    role.roleId = 1604
    role.roleName = "卡提希娅"
    role.level = 90
    role.breach = 6
    role.attributeId = 1
    role.attributeName = "衍射"
    role.weaponTypeId = 2
    role.weaponTypeName = "迅刀"
    role.starLevel = 5
    role.roleIconUrl = role_icon_url
    role.rolePicUrl = role_icon_url  # 使用相同的图标作为立绘
    
    # 武器
    weapon_data = MagicMock()
    weapon_data.weapon = MagicMock()
    weapon_data.weapon.weaponId = 211100
    weapon_data.weapon.weaponName = "裁春"
    weapon_data.weapon.weaponStarLevel = 5
    weapon_data.weapon.weaponIcon = weapon_icon_url or ""
    weapon_data.level = 90
    weapon_data.breach = 6
    weapon_data.resonLevel = 1
    
    # 命座
    chains = []
    chain_names = ["第一命座", "第二命座", "第三命座", "第四命座", "第五命座", "第六命座"]
    for i, name in enumerate(chain_names):
        chain = MagicMock()
        chain.name = name
        chain.order = i + 1
        chain.unlocked = i < 3
        chain.iconUrl = f"https://web-static.kurobbs.com/adminConfig/36/chain_icon/{1604}_{i+1}.png"
        chains.append(chain)
    
    # 技能
    skills = []
    skill_types = ["常态攻击", "共鸣技能", "共鸣回路", "共鸣解放", "变奏技能", "延奏技能"]
    skill_names = ["普通攻击", "技能攻击", "回路技能", "解放技能", "变奏技能", "延奏技能"]
    skill_levels = [10, 10, 10, 10, 6, 6]
    
    for i, (skill_type, skill_name, level) in enumerate(zip(skill_types, skill_names, skill_levels)):
        skill_data = MagicMock()
        skill_data.skill = MagicMock()
        skill_data.skill.id = 160400 + i + 1
        skill_data.skill.type = skill_type
        skill_data.skill.name = skill_name
        skill_data.skill.iconUrl = f"https://web-static.kurobbs.com/adminConfig/36/skill_icon/{1604}_{i+1}.png"
        skill_data.level = level
        skills.append(skill_data)
    
    # 声骸
    phantoms = []
    phantom_names = ["鸣钟之龟", "无常凶鹭", "燎照之骑", "飞廉之猩", "哀声鸷"]
    phantom_costs = [4, 3, 3, 3, 1]
    
    for i, (name, cost) in enumerate(zip(phantom_names, phantom_costs)):
        phantom = MagicMock()
        phantom.phantomProp = MagicMock()
        phantom.phantomProp.name = name
        phantom.phantomProp.phantomId = 390070051 + i
        phantom.phantomProp.quality = 5
        phantom.phantomProp.cost = cost
        phantom.phantomProp.iconUrl = f"https://web-static.kurobbs.com/adminConfig/35/phantom_icon/{390070051 + i}.png"
        
        phantom.cost = cost
        phantom.quality = 5
        phantom.level = 25
        
        # 主词条
        main_prop = MagicMock()
        main_prop.attributeName = "暴击" if i == 0 else "攻击"
        main_prop.attributeValue = "30.0%" if i == 0 else "150"
        main_prop.iconUrl = None
        phantom.mainProps = [main_prop]
        
        # 副词条
        sub_props = []
        sub_prop_names = ["暴击伤害", "攻击", "生命", "防御"]
        sub_prop_values = ["15.6%", "50", "580", "80"]
        for j, (attr_name, attr_value) in enumerate(zip(sub_prop_names, sub_prop_values)):
            sub_prop = MagicMock()
            sub_prop.attributeName = attr_name
            sub_prop.attributeValue = attr_value
            sub_prop.iconUrl = None
            sub_props.append(sub_prop)
        phantom.subProps = sub_props
        
        phantoms.append(phantom)
    
    phantom_data = MagicMock()
    phantom_data.equipPhantomList = phantoms
    
    # 组装
    role_detail = MagicMock()
    role_detail.role = role
    role_detail.weaponData = weapon_data
    role_detail.chainList = chains
    role_detail.phantomData = phantom_data
    role_detail.skillList = skills
    
    def get_skill_list():
        return skills
    role_detail.get_skill_list = get_skill_list
    
    # 渲染
    print("\n  渲染中...")
    try:
        renderer = get_renderer()
        image_bytes = renderer.render_role_card(role_detail)
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"katixiya_real_{timestamp}.png"
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"\n  ✓ 图片已保存: {output_path}")
        print(f"  ✓ 文件大小: {len(image_bytes) / 1024:.1f} KB")
        
        # 显示图片信息
        img = Image.open(output_path)
        print(f"  ✓ 图片尺寸: {img.size}")
        
    except Exception as e:
        print(f"\n  ✗ 渲染失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

# 运行
if __name__ == "__main__":
    result = asyncio.run(main())
    
    print("\n" + "="*60)
    if result:
        print("✓ 卡提希娅角色练度卡片生成完成!")
    else:
        print("✗ 生成失败")
    print("="*60)
    
    sys.exit(0 if result else 1)
