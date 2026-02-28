# coding=utf-8
"""
卡提希娅角色练度卡片测试
生成卡提希娅的完整角色练度卡片
"""
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock

# 添加当前目录到路径（因为当前目录就是包根目录）
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PIL import Image
from renderer import render_role_card, get_renderer


def create_katixiya_role_detail():
    """创建卡提希娅的完整角色数据"""
    
    # 角色基础信息
    role = MagicMock()
    role.roleId = 1604  # 卡提希娅角色ID
    role.roleName = "卡提希娅"
    role.level = 90
    role.breach = 6
    role.roleIconUrl = "https://web-static.kurobbs.com/adminConfig/36/role_icon/1716031298428.png"
    role.rolePicUrl = "https://web-static.kurobbs.com/adminConfig/36/role_pic/1716031298428.png"
    role.starLevel = 5
    role.attributeId = 1  # 衍射
    role.attributeName = "衍射"
    role.weaponTypeId = 2  # 迅刀
    role.weaponTypeName = "迅刀"
    
    # 武器数据
    weapon_data = MagicMock()
    weapon_data.weapon = MagicMock()
    weapon_data.weapon.weaponId = 211100
    weapon_data.weapon.weaponName = "裁春"
    weapon_data.weapon.weaponType = 2
    weapon_data.weapon.weaponStarLevel = 5
    weapon_data.weapon.weaponIcon = "https://web-static.kurobbs.com/adminConfig/36/weapon_icon/1716031298428.png"
    weapon_data.level = 90
    weapon_data.breach = 6
    weapon_data.resonLevel = 1
    
    # 命座数据
    chains = []
    chain_names = [
        "一链：初醒的启程",
        "二链：闪耀的旅途",
        "三链：交织的羁绊",
        "四链：共鸣的乐章",
        "五链：无尽的旋律",
        "六链：永恒的回响"
    ]
    for i, name in enumerate(chain_names):
        chain = MagicMock()
        chain.name = name
        chain.order = i + 1
        chain.unlocked = i < 3  # 前3个命座解锁
        chain.iconUrl = f"https://web-static.kurobbs.com/adminConfig/36/chain_icon/{1604}_{i+1}.png"
        chains.append(chain)
    
    # 技能数据
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
    
    # 声骸数据
    phantoms = []
    phantom_names = ["鸣钟之龟", "无常凶鹭", "燎照之骑", "飞廉之猩", "哀声鸷"]
    phantom_costs = [4, 3, 3, 3, 1]
    
    for i, (name, cost) in enumerate(zip(phantom_names, phantom_costs)):
        phantom = MagicMock()
        phantom.phantomProp = MagicMock()
        phantom.phantomProp.phantomPropId = 390070051 + i
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
    phantom_data.cost = sum(p.cost for p in phantoms)
    phantom_data.equipPhantomList = phantoms
    
    # 组装角色详情
    role_detail = MagicMock()
    role_detail.role = role
    role_detail.level = 90
    role_detail.chainList = chains
    role_detail.weaponData = weapon_data
    role_detail.phantomData = phantom_data
    role_detail.skillList = skills
    role_detail.activeBranchId = 0
    role_detail.skillBranchList = []
    
    # 添加get_skill_list方法
    def get_skill_list():
        sort_order = ["常态攻击", "共鸣技能", "共鸣回路", "共鸣解放", "变奏技能", "延奏技能"]
        return sorted(skills, key=lambda x: sort_order.index(x.skill.type) if x.skill.type in sort_order else 999)
    
    role_detail.get_skill_list = get_skill_list
    
    return role_detail


def main():
    """主函数"""
    import os
    
    # 强制刷新输出
    print("\n" + "="*60, flush=True)
    print("卡提希娅角色练度卡片生成", flush=True)
    print("="*60, flush=True)
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    print(f"\n输出目录: {output_dir.absolute()}", flush=True)
    
    # 创建卡提希娅角色数据
    print("\n创建卡提希娅角色数据...", flush=True)
    try:
        role_detail = create_katixiya_role_detail()
        print(f"角色: {role_detail.role.roleName} (Lv.{role_detail.role.level})", flush=True)
        print(f"武器: {role_detail.weaponData.weapon.weaponName}", flush=True)
        print(f"命座: {sum(1 for c in role_detail.chainList if c.unlocked)}/6", flush=True)
        print(f"声骸: {len(role_detail.phantomData.equipPhantomList)}/5", flush=True)
        print(f"技能: {len(role_detail.skillList)}", flush=True)
    except Exception as e:
        print(f"创建角色数据失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return None
    
    # 渲染角色卡片
    print("\n渲染角色卡片...", flush=True)
    try:
        renderer = get_renderer()
        print("获取渲染器成功", flush=True)
        
        image_bytes = renderer.render_role_card(role_detail)
        print(f"渲染完成，图片大小: {len(image_bytes)} bytes", flush=True)
        
        # 保存图片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"katixiya_role_card_{timestamp}.png"
        filepath = output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        print(f"\n✓ 图片已保存到: {filepath}", flush=True)
        
        # 显示图片信息
        img = Image.open(filepath)
        print(f"图片尺寸: {img.size}", flush=True)
        print(f"图片模式: {img.mode}", flush=True)
        print(f"文件大小: {filepath.stat().st_size / 1024:.1f} KB", flush=True)
        
        print("\n" + "="*60, flush=True)
        print("生成完成!", flush=True)
        print("="*60, flush=True)
        
        return filepath
        
    except Exception as e:
        print(f"\n✗ 错误: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
