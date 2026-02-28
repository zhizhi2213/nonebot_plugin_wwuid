# coding=utf-8
"""
调试测试脚本
"""
import sys
from pathlib import Path

print("Step 1: 检查当前目录")
print(f"当前目录: {Path.cwd()}")
print(f"脚本目录: {Path(__file__).parent}")

print("\nStep 2: 检查Python路径")
for i, p in enumerate(sys.path[:5]):
    print(f"  {i}: {p}")

print("\nStep 3: 尝试导入renderer模块")
try:
    from renderer import render_role_card
    print("  - 导入成功!")
except Exception as e:
    print(f"  - 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 4: 尝试创建模拟数据")
try:
    from unittest.mock import MagicMock
    
    role = MagicMock()
    role.roleId = 1604
    role.roleName = "卡提希娅"
    role.level = 90
    role.attributeId = 1
    role.weaponTypeId = 2
    
    role_detail = MagicMock()
    role_detail.role = role
    role_detail.weaponData = MagicMock()
    role_detail.weaponData.weapon = MagicMock()
    role_detail.weaponData.weapon.weaponName = "裁春"
    role_detail.weaponData.weapon.weaponStarLevel = 5
    role_detail.weaponData.level = 90
    role_detail.chainList = []
    role_detail.phantomData = MagicMock()
    role_detail.phantomData.equipPhantomList = []
    role_detail.skillList = []
    role_detail.get_skill_list = lambda: []
    
    print("  - 数据创建成功!")
except Exception as e:
    print(f"  - 数据创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 5: 尝试渲染")
try:
    image_bytes = render_role_card(role_detail)
    print(f"  - 渲染成功! 大小: {len(image_bytes)} bytes")
    
    # 保存
    output_path = Path(__file__).parent / "debug_output.png"
    with open(output_path, 'wb') as f:
        f.write(image_bytes)
    print(f"  - 已保存到: {output_path}")
except Exception as e:
    print(f"  - 渲染失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n完成!")
