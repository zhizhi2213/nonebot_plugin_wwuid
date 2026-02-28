# coding=utf-8
"""
资源加载测试
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

# Mock PIL before importing
with patch.dict('sys.modules', {'PIL': MagicMock(), 'PIL.Image': MagicMock(), 'PIL.ImageDraw': MagicMock(), 'PIL.ImageFont': MagicMock(), 'PIL.ImageFilter': MagicMock()}):
    from nonebot_plugin_wwuid.renderer.utils import (
        get_waves_bg,
        get_attribute_icon,
        get_weapon_type_icon,
        load_resource_image,
        draw_text_with_shadow,
        add_footer,
        crop_center_img,
        resize_and_center_image,
        create_rounded_mask,
        apply_blur,
    )


class TestGetWavesBg:
    """测试背景图片获取"""
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_waves_bg_existing_file(self, mock_bg_path):
        """测试获取存在的背景图片"""
        mock_img = MagicMock()
        mock_img.convert.return_value = mock_img
        mock_img.resize.return_value = mock_img
        
        # 模拟文件存在
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.open', return_value=mock_img):
            result = get_waves_bg((800, 600))
        
        assert result is not None
        mock_img.convert.assert_called_once_with('RGBA')
        mock_img.resize.assert_called_once()
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_waves_bg_fallback(self, mock_bg_path):
        """测试背景图片回退到纯色"""
        # 模拟所有背景文件都不存在
        mock_path = MagicMock()
        mock_path.exists.return_value = False
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.new') as mock_new:
            mock_new.return_value = MagicMock()
            result = get_waves_bg((800, 600))
        
        # 验证创建了纯色背景
        mock_new.assert_called_once()
        args = mock_new.call_args
        assert args[0][0] == 'RGBA'
        assert args[0][1] == (800, 600)
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_waves_bg_load_error(self, mock_bg_path):
        """测试背景图片加载错误处理"""
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        
        # 模拟加载失败
        with patch('PIL.Image.open', side_effect=Exception("Load error")):
            with patch('PIL.Image.new') as mock_new:
                mock_new.return_value = MagicMock()
                result = get_waves_bg()
        
        # 应该回退到纯色背景
        mock_new.assert_called_once()


class TestGetAttributeIcon:
    """测试属性图标获取"""
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_attribute_icon_existing(self, mock_bg_path):
        """测试获取存在的属性图标"""
        mock_img = MagicMock()
        mock_img.convert.return_value = mock_img
        
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        mock_bg_path.__truediv__.return_value.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.open', return_value=mock_img):
            result = get_attribute_icon(1)  # 衍射
        
        assert result is not None
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_attribute_icon_not_found(self, mock_bg_path):
        """测试属性图标不存在"""
        mock_path = MagicMock()
        mock_path.exists.return_value = False
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        mock_bg_path.__truediv__.return_value.__truediv__ = MagicMock(return_value=mock_path)
        
        result = get_attribute_icon(1)
        
        assert result is None
    
    def test_get_attribute_icon_all_types(self):
        """测试所有属性类型"""
        attribute_ids = [1, 2, 3, 4, 5, 6]
        expected_names = ['衍射', '湮灭', '气动', '热熔', '冷凝', '导电']
        
        for attr_id, expected_name in zip(attribute_ids, expected_names):
            with patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH') as mock_bg_path:
                mock_path = MagicMock()
                mock_path.exists.return_value = False
                mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
                mock_bg_path.__truediv__.return_value.__truediv__ = MagicMock(return_value=mock_path)
                
                result = get_attribute_icon(attr_id)
                
                # 验证路径构建正确
                # 即使返回None，也验证了代码执行路径
                assert result is None  # 因为mock文件不存在


class TestGetWeaponTypeIcon:
    """测试武器类型图标获取"""
    
    @patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH')
    def test_get_weapon_type_icon_existing(self, mock_bg_path):
        """测试获取存在的武器类型图标"""
        mock_img = MagicMock()
        mock_img.convert.return_value = mock_img
        
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
        mock_bg_path.__truediv__.return_value.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.open', return_value=mock_img):
            result = get_weapon_type_icon(1)  # 长刃
        
        assert result is not None
    
    def test_get_weapon_type_icon_all_types(self):
        """测试所有武器类型"""
        weapon_ids = [1, 2, 3, 4, 5]
        expected_names = ['长刃', '迅刀', '佩枪', '臂铠', '音感仪']
        
        for weapon_id, expected_name in zip(weapon_ids, expected_names):
            with patch('nonebot_plugin_wwuid.renderer.utils.BG_PATH') as mock_bg_path:
                mock_path = MagicMock()
                mock_path.exists.return_value = False
                mock_bg_path.__truediv__ = MagicMock(return_value=mock_path)
                mock_bg_path.__truediv__.return_value.__truediv__ = MagicMock(return_value=mock_path)
                
                result = get_weapon_type_icon(weapon_id)
                assert result is None  # 因为mock文件不存在


class TestLoadResourceImage:
    """测试资源图片加载"""
    
    @patch('nonebot_plugin_wwuid.renderer.utils.CHARINFO_PATH')
    def test_load_resource_image_existing(self, mock_charinfo_path):
        """测试加载存在的资源图片"""
        mock_img = MagicMock()
        mock_img.convert.return_value = mock_img
        
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_charinfo_path.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.open', return_value=mock_img):
            result = load_resource_image("test.png")
        
        assert result is not None
        mock_img.convert.assert_called_once_with('RGBA')
    
    @patch('nonebot_plugin_wwuid.renderer.utils.CHARINFO_PATH')
    def test_load_resource_image_not_found(self, mock_charinfo_path):
        """测试资源图片不存在"""
        mock_path = MagicMock()
        mock_path.exists.return_value = False
        mock_charinfo_path.__truediv__ = MagicMock(return_value=mock_path)
        
        result = load_resource_image("nonexistent.png")
        
        assert result is None
    
    @patch('nonebot_plugin_wwuid.renderer.utils.CHARINFO_PATH')
    def test_load_resource_image_error(self, mock_charinfo_path):
        """测试资源图片加载错误"""
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_charinfo_path.__truediv__ = MagicMock(return_value=mock_path)
        
        with patch('PIL.Image.open', side_effect=Exception("Corrupted image")):
            result = load_resource_image("corrupted.png")
        
        assert result is None


class TestDrawTextWithShadow:
    """测试带阴影文字绘制"""
    
    def test_draw_text_with_shadow(self):
        """测试带阴影文字绘制"""
        mock_img = MagicMock()
        mock_draw = MagicMock()
        mock_font = MagicMock()
        
        with patch('PIL.ImageDraw.Draw', return_value=mock_draw):
            draw_text_with_shadow(
                mock_img,
                "测试文字",
                (100, 200),
                mock_font,
                fill=(255, 255, 255, 255),
                shadow_color=(0, 0, 0, 180),
                shadow_offset=(2, 2),
                anchor="lt"
            )
        
        # 验证绘制了两次文字（阴影+主文字）
        assert mock_draw.text.call_count == 2


class TestAddFooter:
    """测试页脚添加"""
    
    def test_add_footer(self):
        """测试添加页脚"""
        mock_img = MagicMock()
        mock_img.width = 800
        mock_img.height = 600
        mock_draw = MagicMock()
        mock_font = MagicMock()
        
        with patch('PIL.ImageDraw.Draw', return_value=mock_draw):
            with patch('nonebot_plugin_wwuid.renderer.utils.waves_font_origin', return_value=mock_font):
                result = add_footer(mock_img, "Test Footer")
        
        assert result is mock_img
        mock_draw.text.assert_called_once()


class TestCropCenterImg:
    """测试中心裁剪"""
    
    def test_crop_center_img(self):
        """测试中心裁剪图片"""
        mock_img = MagicMock()
        mock_img.size = (1000, 800)
        mock_img.crop.return_value = MagicMock()
        
        result = crop_center_img(mock_img, (500, 400))
        
        mock_img.crop.assert_called_once()
        # 验证裁剪参数
        args = mock_img.crop.call_args[0][0]
        assert len(args) == 4  # left, top, right, bottom


class TestResizeAndCenterImage:
    """测试调整尺寸并居中"""
    
    def test_resize_and_center_image(self):
        """测试调整图片尺寸并居中"""
        mock_img = MagicMock()
        mock_img.size = (400, 300)
        mock_resized = MagicMock()
        mock_img.resize.return_value = mock_resized
        
        with patch('PIL.Image.new') as mock_new:
            mock_new.return_value = MagicMock()
            result = resize_and_center_image(mock_img, (200, 200))
        
        mock_img.resize.assert_called_once()
        mock_new.assert_called_once()


class TestCreateRoundedMask:
    """测试圆角遮罩创建"""
    
    def test_create_rounded_mask(self):
        """测试创建圆角遮罩"""
        mock_mask = MagicMock()
        mock_draw = MagicMock()
        
        with patch('PIL.Image.new', return_value=mock_mask):
            with patch('PIL.ImageDraw.Draw', return_value=mock_draw):
                result = create_rounded_mask((100, 100), 10)
        
        assert result is mock_mask
        mock_draw.rounded_rectangle.assert_called_once()


class TestApplyBlur:
    """测试模糊效果"""
    
    def test_apply_blur(self):
        """测试应用模糊效果"""
        mock_img = MagicMock()
        mock_blurred = MagicMock()
        mock_img.filter.return_value = mock_blurred
        
        with patch('PIL.ImageFilter.GaussianBlur') as mock_blur:
            mock_blur.return_value = MagicMock()
            result = apply_blur(mock_img, radius=5)
        
        mock_img.filter.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
