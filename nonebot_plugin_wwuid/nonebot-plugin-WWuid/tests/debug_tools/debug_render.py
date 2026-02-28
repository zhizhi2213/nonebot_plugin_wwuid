# coding=utf-8
"""
渲染调试工具
用于快速生成角色卡片和测试渲染效果

使用方法:
    python tests/debug_tools/debug_render.py

功能:
    1. 生成测试角色卡片
    2. 测试不同角色的渲染效果
    3. 对比渲染结果
    4. 测试资源加载
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PIL import Image

from nonebot_plugin_wwuid.renderer import render_role_card, get_renderer
from tests.debug_tools.test_data import create_mock_role_detail


class RenderDebugger:
    """渲染调试器"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.renderer = get_renderer()
    
    def save_image(self, image_bytes: bytes, name: str) -> Path:
        """保存图片到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        print(f"✓ 图片已保存到: {filepath}")
        return filepath
    
    def test_render_minimal(self):
        """测试最小化数据渲染"""
        print("\n" + "="*50)
        print("测试: 最小化数据渲染")
        print("="*50)
        
        try:
            # 创建最小化的角色数据
            role_detail = create_mock_role_detail(
                role_name="测试角色",
                level=1,
                with_weapon=False,
                with_chain=False,
                with_phantom=False,
                with_skill=False
            )
            
            image_bytes = self.renderer.render_role_card(role_detail)
            filepath = self.save_image(image_bytes, "render_minimal")
            
            # 获取图片尺寸
            img = Image.open(filepath)
            print(f"图片尺寸: {img.size}")
            print(f"图片模式: {img.mode}")
            
            return filepath
        except Exception as e:
            print(f"✗ 错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_render_full(self):
        """测试完整数据渲染"""
        print("\n" + "="*50)
        print("测试: 完整数据渲染")
        print("="*50)
        
        try:
            # 创建完整的角色数据
            role_detail = create_mock_role_detail(
                role_name="完整测试角色",
                level=90,
                with_weapon=True,
                with_chain=True,
                with_phantom=True,
                with_skill=True
            )
            
            image_bytes = self.renderer.render_role_card(role_detail)
            filepath = self.save_image(image_bytes, "render_full")
            
            # 获取图片尺寸
            img = Image.open(filepath)
            print(f"图片尺寸: {img.size}")
            print(f"图片模式: {img.mode}")
            
            return filepath
        except Exception as e:
            print(f"✗ 错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_render_different_roles(self):
        """测试不同角色的渲染"""
        print("\n" + "="*50)
        print("测试: 不同角色渲染")
        print("="*50)
        
        test_roles = [
            {"name": "漂泊者·男", "level": 90, "attr": 1},
            {"name": "漂泊者·女", "level": 80, "attr": 2},
            {"name": "测试角色A", "level": 70, "attr": 3},
            {"name": "测试角色B", "level": 60, "attr": 4},
        ]
        
        filepaths = []
        for i, role_info in enumerate(test_roles):
            try:
                print(f"\n渲染角色 {i+1}/{len(test_roles)}: {role_info['name']}")
                
                role_detail = create_mock_role_detail(
                    role_name=role_info["name"],
                    level=role_info["level"],
                    attribute_id=role_info["attr"],
                    with_weapon=True,
                    with_chain=True,
                    with_phantom=True,
                    with_skill=True
                )
                
                image_bytes = self.renderer.render_role_card(role_detail)
                filepath = self.save_image(image_bytes, f"render_role_{i+1}")
                filepaths.append(filepath)
                
            except Exception as e:
                print(f"✗ 渲染失败: {e}")
        
        return filepaths
    
    def test_resource_loading(self):
        """测试资源加载"""
        print("\n" + "="*50)
        print("测试: 资源加载")
        print("="*50)
        
        from nonebot_plugin_wwuid.renderer.utils import (
            get_waves_bg,
            get_attribute_icon,
            get_weapon_type_icon,
            load_resource_image,
        )
        
        # 测试背景加载
        print("\n1. 测试背景加载")
        try:
            bg = get_waves_bg((800, 600))
            print(f"   ✓ 背景加载成功: {bg.size}")
        except Exception as e:
            print(f"   ✗ 背景加载失败: {e}")
        
        # 测试属性图标加载
        print("\n2. 测试属性图标加载")
        for attr_id in range(1, 7):
            try:
                icon = get_attribute_icon(attr_id)
                if icon:
                    print(f"   ✓ 属性 {attr_id}: {icon.size}")
                else:
                    print(f"   ⚠ 属性 {attr_id}: 未找到")
            except Exception as e:
                print(f"   ✗ 属性 {attr_id}: {e}")
        
        # 测试武器类型图标加载
        print("\n3. 测试武器类型图标加载")
        for weapon_id in range(1, 6):
            try:
                icon = get_weapon_type_icon(weapon_id)
                if icon:
                    print(f"   ✓ 武器类型 {weapon_id}: {icon.size}")
                else:
                    print(f"   ⚠ 武器类型 {weapon_id}: 未找到")
            except Exception as e:
                print(f"   ✗ 武器类型 {weapon_id}: {e}")
        
        # 测试资源图片加载
        print("\n4. 测试资源图片加载")
        resource_names = [
            "base_info_bg.png",
            "char_mask.png",
            "char_fg.png",
            "banner2.png",
            "weapon_bg.png",
            "mz_bg.png",
            "skill_bg.png",
        ]
        
        for name in resource_names:
            try:
                img = load_resource_image(name)
                if img:
                    print(f"   ✓ {name}: {img.size}")
                else:
                    print(f"   ⚠ {name}: 未找到")
            except Exception as e:
                print(f"   ✗ {name}: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("鸣潮UID插件 - 渲染调试工具")
        print("="*50)
        
        # 测试资源加载
        self.test_resource_loading()
        
        # 测试最小化渲染
        self.test_render_minimal()
        
        # 测试完整渲染
        self.test_render_full()
        
        # 测试不同角色
        self.test_render_different_roles()
        
        print("\n" + "="*50)
        print("测试完成!")
        print(f"输出目录: {self.output_dir}")
        print("="*50)


def print_usage():
    """打印使用说明"""
    print("""
使用方法:
    python tests/debug_tools/debug_render.py [test_name]

参数:
    test_name   - 测试名称（可选）
                  minimal: 最小化数据渲染
                  full: 完整数据渲染
                  roles: 不同角色渲染
                  resources: 资源加载测试
                  all: 运行所有测试（默认）

示例:
    python tests/debug_tools/debug_render.py
    python tests/debug_tools/debug_render.py minimal
    python tests/debug_tools/debug_render.py resources
    """)


def main():
    """主函数"""
    import sys
    
    debugger = RenderDebugger()
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        
        if test_name == "minimal":
            debugger.test_render_minimal()
        elif test_name == "full":
            debugger.test_render_full()
        elif test_name == "roles":
            debugger.test_render_different_roles()
        elif test_name == "resources":
            debugger.test_resource_loading()
        elif test_name == "all":
            debugger.run_all_tests()
        else:
            print(f"未知测试: {test_name}")
            print_usage()
            sys.exit(1)
    else:
        debugger.run_all_tests()


if __name__ == "__main__":
    main()
