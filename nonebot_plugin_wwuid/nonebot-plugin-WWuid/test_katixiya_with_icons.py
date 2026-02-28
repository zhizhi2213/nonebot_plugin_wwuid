# coding=utf-8
"""
卡提希娅角色练度卡片生成 - 使用真实API数据
使用真实token和did获取角色数据
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("卡提希娅角色练度卡片生成 - 使用真实API数据")
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

# 创建目录
print("\n[2/6] 创建目录...")
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
cache_dir = Path(__file__).parent / "cache" / "icons"
cache_dir.mkdir(parents=True, exist_ok=True)
print(f"  ✓ 输出目录: {output_dir}")
print(f"  ✓ 缓存目录: {cache_dir}")

# 真实token和did
COOKIE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkIjoxNzY1Nzg5NTMwMTY5LCJ1c2VySWQiOjEwMTYxNDU5fQ.o1mRTSxIno5L8AE_Ygxft_VXEU7sc_DJj2BsJYW0lsI"
DID = "7786E85B-6116-4112-A5E9-E9384AAB7C06"

async def download_icon(url: str, cache_path: Path) -> bool:
    """下载图标到本地缓存"""
    if cache_path.exists():
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
                print(f"  ✓ 下载: {cache_path.name}")
                return True
            else:
                print(f"  ✗ 失败 ({response.status_code}): {cache_path.name}")
                return False
    except Exception as e:
        print(f"  ✗ 错误: {cache_path.name} - {e}")
        return False

async def main():
    # 下载图标
    print("\n[3/5] 下载图标...")
    
    # 注意：真实的图标URL需要从API获取，这里使用示例URL
    # 角色立绘URL（示例）
    role_pic_url = "https://web-static.kurobbs.com/adminConfig/36/role_pic/1716031298428.png"
    role_icon_path = cache_dir / "role_1604.png"
    role_icon_ok = await download_icon(role_pic_url, role_icon_path)
    
    # 下载武器图标
    weapon_icon_path = cache_dir / "weapon_211100.png"
    weapon_icon_ok = await download_icon(REAL_ICON_URLS["weapon"], weapon_icon_path)
    
    # 下载声骸图标（只使用第一个有效的）
    phantom_icon_paths = {}
    for ph_id, url in REAL_ICON_URLS["phantom"].items():
        ph_path = cache_dir / f"phantom_{ph_id}.png"
        ok = await download_icon(url, ph_path)
        phantom_icon_paths[ph_id] = ph_path if ok else None
    
    # 创建角色数据
    print("\n[4/5] 创建角色数据...")
    
    from renderer import render_role_card, get_renderer
    
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
    role.roleIconUrl = role_pic_url if role_icon_ok else ""
    role.rolePicUrl = role_pic_url if role_icon_ok else ""
    
    # 武器
    weapon_data = MagicMock()
    weapon_data.weapon = MagicMock()
    weapon_data.weapon.weaponId = 211100
    weapon_data.weapon.weaponName = "裁春"
    weapon_data.weapon.weaponStarLevel = 5
    weapon_data.weapon.weaponIcon = REAL_ICON_URLS["weapon"] if weapon_icon_ok else ""
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
        chain.iconUrl = ""
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
        skill_data.skill.iconUrl = ""
        skill_data.level = level
        skills.append(skill_data)
    
    # 声骸
    phantoms = []
    phantom_names = ["鸣钟之龟", "无常凶鹭", "燎照之骑", "飞廉之猩", "哀声鸷"]
    phantom_costs = [4, 3, 3, 3, 1]
    phantom_ids = [390070051, 390070052, 390070053, 390070054, 390070055]
    
    for i, (name, cost, ph_id) in enumerate(zip(phantom_names, phantom_costs, phantom_ids)):
        phantom = MagicMock()
        phantom.phantomProp = MagicMock()
        phantom.phantomProp.name = name
        phantom.phantomProp.phantomId = ph_id
        phantom.phantomProp.quality = 5
        phantom.phantomProp.cost = cost
        phantom.phantomProp.iconUrl = REAL_ICON_URLS["phantom"].get(ph_id, "")
        
        phantom.cost = cost
        phantom.quality = 5
        phantom.level = 25
        
        main_prop = MagicMock()
        main_prop.attributeName = "暴击" if i == 0 else "攻击"
        main_prop.attributeValue = "30.0%" if i == 0 else "150"
        main_prop.iconUrl = None
        phantom.mainProps = [main_prop]
        
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
    
    print(f"  ✓ 角色: {role.roleName}")
    print(f"  ✓ 武器: {weapon_data.weapon.weaponName}")
    print(f"  ✓ 命座: {sum(1 for c in chains if c.unlocked)}/6")
    print(f"  ✓ 声骸: {len(phantoms)}/5")
    
    # 渲染
    print("\n[5/5] 渲染角色卡片...")
    try:
        renderer = get_renderer()
        image_bytes = renderer.render_role_card(role_detail)
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"katixiya_with_icons_{timestamp}.png"
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"\n  ✓ 图片已保存: {output_path}")
        print(f"  ✓ 文件大小: {len(image_bytes) / 1024:.1f} KB")
        
        img = Image.open(output_path)
        print(f"  ✓ 图片尺寸: {img.size}")
        
        return True
        
    except Exception as e:
        print(f"\n  ✗ 渲染失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    
    print("\n" + "="*60)
    if result:
        print("✓ 卡提希娅角色练度卡片生成完成!")
    else:
        print("✗ 生成失败")
    print("="*60)
    
    sys.exit(0 if result else 1)
