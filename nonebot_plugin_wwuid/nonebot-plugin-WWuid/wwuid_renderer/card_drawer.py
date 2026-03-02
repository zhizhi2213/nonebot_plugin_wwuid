# coding=utf-8
"""
鸣潮角色练度图片渲染模块（改进版）
参考原项目XutheringWavesUID的实现
"""
import asyncio
import io
import re
from typing import Optional, Tuple, Dict, List
from PIL import Image, ImageDraw, ImageEnhance

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

try:
    from ..utils.resource_mgr import CHARINFO_PATH, BG_PATH
except ImportError:
    from utils.resource_mgr import CHARINFO_PATH, BG_PATH
from .utils import waves_font_origin
from .utils import (
    get_waves_bg, get_attribute_icon, get_weapon_type_icon,
    draw_text_with_shadow, add_footer, resize_and_center_image,
    load_resource_image, get_role_picture_sync,
    get_skill_icon_sync, get_phantom_icon_sync,
    get_chain_icon_sync, get_weapon_icon_sync
)


# 颜色定义
WHITE = (255, 255, 255, 255)
GOLD = (255, 215, 0, 255)
GREY = (180, 180, 180, 255)
DARK_BG = (30, 30, 40, 200)
LIGHT_BG = (50, 50, 60, 180)

# 属性名称映射
PROP_NAME_MAP = {
    "生命": "生命",
    "攻击": "攻击", 
    "防御": "防御",
    "共鸣效率": "共鸣效率",
    "暴击": "暴击",
    "暴击伤害": "暴击伤害",
    "属性伤害加成": "属性伤害加成",
    "治疗效果加成": "治疗效果加成",
    "普攻伤害加成": "普攻伤害加成",
    "重击伤害加成": "重击伤害加成",
    "共鸣技能伤害加成": "共鸣技能伤害加成",
    "共鸣解放伤害加成": "共鸣解放伤害加成",
}

# 技能类型顺序
SKILL_TYPE_ORDER = ["常态攻击", "共鸣技能", "共鸣回路", "共鸣解放", "变奏技能", "延奏技能"]


class RoleCardRenderer:
    """角色卡片渲染器（改进版）"""
    
    def __init__(self):
        self.TEXT_PATH = CHARINFO_PATH
        self.font_12 = waves_font_origin(12)
        self.font_14 = waves_font_origin(14)
        self.font_16 = waves_font_origin(16)
        self.font_18 = waves_font_origin(18)
        self.font_20 = waves_font_origin(20)
        self.font_24 = waves_font_origin(24)
        self.font_28 = waves_font_origin(28)
        self.font_30 = waves_font_origin(30)
        self.font_36 = waves_font_origin(36)
        self.font_40 = waves_font_origin(40)
        self.font_50 = waves_font_origin(50)
    
    def render_role_card(self, role_detail, account: Optional[Dict] = None, raw_detail: Optional[Dict] = None) -> bytes:
        """渲染角色练度卡片"""
        role = role_detail.role
        
        # 计算卡片高度（根据内容动态调整）
        card_height = 2000
        
        # 创建背景
        img = get_waves_bg((1200, card_height))
        
        # 绘制顶部信息栏（账号等级、世界等级等）
        self._draw_header_section(img, role_detail, account)
        
        # 绘制角色信息区域（左侧立绘 + 右侧属性）
        self._draw_role_section(img, role_detail)
        
        # 绘制属性面板
        self._draw_property_section(img, role_detail, raw_detail)
        
        # 绘制武器区域
        self._draw_weapon_section(img, role_detail)
        
        # 绘制技能区域
        self._draw_skill_section(img, role_detail)
        
        # 绘制命座区域
        self._draw_chain_section(img, role_detail)
        
        # 绘制声骸区域
        self._draw_phantom_section(img, role_detail)
        
        # 添加页脚
        img = add_footer(img)
        
        # 转换为字节
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def _draw_header_section(self, img: Image.Image, role_detail, account: Optional[Dict] = None):
        """绘制顶部信息栏"""
        draw = ImageDraw.Draw(img)
        
        # 顶部背景条 - 使用title_bar替代
        header_bg = load_resource_image("title_bar.png")
        if header_bg:
            header_bg = header_bg.resize((1200, 120))
            img.paste(header_bg, (0, 0), header_bg)
        else:
            # 使用纯色背景
            header_overlay = Image.new('RGBA', (1200, 120), (30, 30, 40, 200))
            img.paste(header_overlay, (0, 0), header_overlay)
        
        # 左侧账号信息：头像、昵称、UID
        if account:
            uid = account.get("uid")
            avatar_url = account.get("avatarUrl")
            avatar = None
            try:
                from .utils import get_avatar_sync
                avatar = get_avatar_sync(avatar_url, uid)
            except Exception:
                avatar = None
            if avatar:
                avatar = avatar.resize((80, 80))
                mask = Image.new('L', (80, 80), 0)
                mdraw = ImageDraw.Draw(mask)
                mdraw.ellipse([0, 0, 80, 80], fill=255)
                img.paste(avatar, (20, 20), mask)
            # 名称与UID
            acc_name = account.get("name") or "—"
            draw_text_with_shadow(img, acc_name, (120, 40), self.font_24, anchor="lm")
            if uid:
                draw_text_with_shadow(img, f"特征码: {uid}", (120, 70), self.font_16, anchor="lm")
            # 账号等级与世界等级
            lvl = account.get("accountLevel")
            wl = account.get("worldLevel")
            lvl_text = f"Lv.{lvl}" if lvl is not None else "Lv.-"
            wl_text = f"Lv.{wl}" if wl is not None else "Lv.-"
            draw_text_with_shadow(img, lvl_text, (950, 40), self.font_24, anchor="rm")
            draw_text_with_shadow(img, "账号等级", (950, 65), self.font_14, anchor="rm")
            draw_text_with_shadow(img, wl_text, (1100, 40), self.font_24, anchor="rm")
            draw_text_with_shadow(img, "世界等级", (1100, 65), self.font_14, anchor="rm")

        # 角色名称（左上角次级信息）
        role = role_detail.role
        role_name = role.roleName
        if "漂泊者" in role_name:
            role_name = "漂泊者"
        
        draw_text_with_shadow(
            img, role_name,
            (80, 120),
            self.font_36,
            anchor="lm"
        )
        
        # 等级
        draw_text_with_shadow(
            img, f"Lv.{role.level}",
            (80, 155),
            self.font_20,
            anchor="lm"
        )
        
        # 属性图标
        attr_icon = get_attribute_icon(role.attributeId or 1)
        if attr_icon:
            attr_icon = attr_icon.resize((40, 40))
            img.paste(attr_icon, (300, 35), attr_icon)
        
        # 武器类型图标
        weapon_icon = get_weapon_type_icon(role.weaponTypeId or 1)
        if weapon_icon:
            weapon_icon = weapon_icon.resize((35, 35))
            img.paste(weapon_icon, (350, 37), weapon_icon)
    
    def _draw_role_section(self, img: Image.Image, role_detail):
        """绘制角色信息区域（左侧立绘）"""
        role = role_detail.role
        
        # 角色立绘背景框 - 使用base_info_bg替代
        role_bg = load_resource_image("base_info_bg.png")
        if role_bg:
            role_bg = role_bg.resize((450, 700))
            img.paste(role_bg, (50, 150), role_bg)
        else:
            # 使用带边框的纯色背景
            role_area = Image.new('RGBA', (450, 700), (40, 40, 50, 180))
            img.paste(role_area, (50, 150), role_area)
            # 绘制边框
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 150, 500, 850], outline=(100, 100, 120, 200), width=2)
        
        # 加载并显示角色立绘
        if hasattr(role, 'rolePicUrl') and role.rolePicUrl:
            try:
                role_pic = get_role_picture_sync(role.rolePicUrl, role.roleId)
                if role_pic:
                    # 调整立绘大小并居中显示
                    role_pic = self._resize_role_picture(role_pic, (400, 650))
                    img.paste(role_pic, (75, 175), role_pic)
            except Exception as e:
                logger.warning(f"加载角色立绘失败: {e}")
        
        # 角色名称覆盖层（底部）
        draw = ImageDraw.Draw(img)
        role_name = role.roleName
        if "漂泊者" in role_name:
            role_name = "漂泊者"
        
        # 绘制角色名背景
        name_bg = Image.new('RGBA', (400, 60), (0, 0, 0, 150))
        img.paste(name_bg, (75, 780), name_bg)
        
        draw_text_with_shadow(
            img, f"{role_name} Lv.{role.level}",
            (275, 810),
            self.font_30,
            anchor="mm"
        )
    
    def _resize_role_picture(self, img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """调整角色立绘大小，保持比例"""
        img_w, img_h = img.size
        target_w, target_h = target_size
        
        # 计算缩放比例，保持宽高比
        scale = min(target_w / img_w, target_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        # 缩放图片
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 创建目标尺寸的背景
        result = Image.new('RGBA', target_size, (0, 0, 0, 0))
        
        # 居中粘贴
        paste_x = (target_w - new_w) // 2
        paste_y = (target_h - new_h) // 2
        result.paste(resized, (paste_x, paste_y), resized)
        
        return result
    
    def _draw_property_section(self, img: Image.Image, role_detail, raw_detail: Optional[Dict] = None):
        """绘制属性面板（右侧）"""
        draw = ImageDraw.Draw(img)
        
        # 属性面板背景
        prop_bg = load_resource_image("prop_bg.png")
        if prop_bg:
            prop_bg = prop_bg.resize((600, 500))
            img.paste(prop_bg, (550, 150), prop_bg)
        
        # 获取属性数据
        props = self._get_role_properties(role_detail, raw_detail)
        
        # 绘制属性标题
        draw.text((580, 170), "【属性】", font=self.font_24, fill=WHITE)
        
        # 属性布局 - 两列
        col1_x = 580
        col2_x = 850
        start_y = 210
        line_height = 45
        
        # 第一列属性
        col1_props = ["生命", "攻击", "防御", "共鸣效率"]
        for i, prop_name in enumerate(col1_props):
            y = start_y + i * line_height
            value = props.get(prop_name, "0")
            
            # 属性名
            draw.text((col1_x, y), prop_name, font=self.font_20, fill=GREY)
            # 属性值
            draw.text((col1_x + 120, y), str(value), font=self.font_20, fill=WHITE)
        
        # 第二列属性
        col2_props = ["暴击", "暴击伤害", "属性伤害加成", "治疗效果加成"]
        for i, prop_name in enumerate(col2_props):
            y = start_y + i * line_height
            value = props.get(prop_name, "0%")
            
            # 属性名
            draw.text((col2_x, y), prop_name, font=self.font_20, fill=GREY)
            # 属性值
            draw.text((col2_x + 150, y), str(value), font=self.font_20, fill=WHITE)
    
    def _get_role_properties(self, role_detail, raw_detail: Optional[Dict] = None) -> Dict[str, str]:
        """获取角色属性数据"""
        defaults = {
            "生命": "—",
            "攻击": "—",
            "防御": "—",
            "共鸣效率": "—",
            "暴击": "—",
            "暴击伤害": "—",
            "属性伤害加成": "—",
            "治疗效果加成": "—",
        }
        if not raw_detail:
            return defaults
        collected = {}
        def walk(obj):
            if isinstance(obj, dict):
                if "attributeName" in obj and "attributeValue" in obj:
                    name = str(obj.get("attributeName"))
                    val = str(obj.get("attributeValue"))
                    if name and name in defaults and name not in collected:
                        collected[name] = val
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)
        walk(raw_detail)
        for k in defaults:
            defaults[k] = collected.get(k, defaults[k])
        return defaults
    
    def _draw_weapon_section(self, img: Image.Image, role_detail):
        """绘制武器区域"""
        weapon_data = role_detail.weaponData
        if not weapon_data or not weapon_data.weapon:
            return
        
        weapon = weapon_data.weapon
        draw = ImageDraw.Draw(img)
        
        # 武器区域背景
        y_base = 680
        
        # 标题
        draw.text((550, y_base), "【武器信息】", font=self.font_24, fill=WHITE)
        
        # 武器背景
        weapon_bg = load_resource_image("weapon_bg.png")
        if weapon_bg:
            weapon_bg = weapon_bg.resize((600, 150))
            img.paste(weapon_bg, (550, y_base + 40), weapon_bg)
        
        # 武器图标背景（根据星级）
        star_level = weapon.weaponStarLevel or 4
        icon_bg_name = f"weapon_icon_bg_{star_level}.png"
        icon_bg = load_resource_image(icon_bg_name)
        if icon_bg:
            icon_bg = icon_bg.resize((100, 100))
            img.paste(icon_bg, (570, y_base + 60), icon_bg)
        
        # 尝试加载武器图标
        weapon_icon = None
        if hasattr(weapon, 'weaponIcon') and weapon.weaponIcon:
            try:
                weapon_icon = get_weapon_icon_sync(weapon.weaponId, weapon.weaponIcon)
            except Exception:
                pass
        
        if weapon_icon:
            weapon_icon = weapon_icon.resize((80, 80))
            img.paste(weapon_icon, (580, y_base + 70), weapon_icon)
        
        # 武器名称
        draw.text((690, y_base + 70), weapon.weaponName, 
                 font=self.font_28, fill=GOLD, anchor="lm")
        
        # 等级
        draw.text((690, y_base + 105), f"Lv.{weapon_data.level}/90",
                 font=self.font_20, fill=WHITE, anchor="lm")
        
        # 精炼等级
        reson_level = weapon_data.resonLevel or 1
        draw.rounded_rectangle([850, y_base + 55, 900, y_base + 85], 
                              radius=5, fill=(100, 100, 100, 200))
        draw.text((875, y_base + 70), f"精{reson_level}",
                 font=self.font_18, fill=WHITE, anchor="mm")
        
        # 突破图标
        promote_icon = load_resource_image("promote_icon.png")
        if promote_icon:
            breach = min(weapon_data.breach or 0, 6)
            for i in range(breach):
                icon = promote_icon.resize((20, 20))
                img.paste(icon, (690 + i * 25, y_base + 130), icon)
    
    def _draw_skill_section(self, img: Image.Image, role_detail):
        # 绘制技能区域（横向图标+等级）
        skill_list = role_detail.get_skill_list()
        if not skill_list:
            return
        
        draw = ImageDraw.Draw(img)
        y_base = 880
        
        # 标题
        draw.text((50, y_base), "【技能】", font=self.font_24, fill=WHITE)
        
        # 技能背景
        skill_bg = load_resource_image("skill_bg.png")
        if skill_bg:
            skill_bg = skill_bg.resize((1100, 120))
            img.paste(skill_bg, (50, y_base + 40), skill_bg)
        else:
            # 使用纯色背景
            skill_area = Image.new('RGBA', (1100, 120), (40, 40, 50, 150))
            img.paste(skill_area, (50, y_base + 40), skill_area)
        
        # 按类型排序技能
        sorted_skills = sorted(skill_list, 
                              key=lambda x: SKILL_TYPE_ORDER.index(x.skill.type) 
                              if x.skill.type in SKILL_TYPE_ORDER else 999)
        
        # 横向排列技能
        skill_x = 80
        skill_y = y_base + 50
        skill_spacing = 180
        
        for i, skill_data in enumerate(sorted_skills[:6]):
            skill = skill_data.skill
            # 原始接口返回的level即为展示等级，这里不再减1
            level = skill_data.level
            
            icon_bg_x = skill_x + i * skill_spacing
            icon_bg_y = skill_y
            
            # 尝试加载技能图标
            skill_icon = None
            if hasattr(skill, 'iconUrl') and skill.iconUrl:
                try:
                    skill_icon = get_skill_icon_sync(skill.id, skill.iconUrl)
                except Exception:
                    pass
            
            if skill_icon:
                # 使用下载的图标
                skill_icon = skill_icon.resize((60, 60))
                # 圆形遮罩
                mask = Image.new('L', (60, 60), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, 60, 60], fill=255)
                img.paste(skill_icon, (icon_bg_x, icon_bg_y), mask)
            else:
                # 绘制圆形背景作为占位
                draw.ellipse([icon_bg_x, icon_bg_y, icon_bg_x + 60, icon_bg_y + 60], 
                            fill=(60, 60, 70, 200), outline=(100, 100, 120, 200))
                # 显示技能类型首字
                draw.text((icon_bg_x + 30, icon_bg_y + 30), 
                         skill.type[:1], font=self.font_24, fill=WHITE, anchor="mm")
            
            # 技能类型名称
            draw.text((icon_bg_x + 30, icon_bg_y + 75), 
                     skill.type[:4], font=self.font_14, fill=GREY, anchor="mm")
            
            # 技能等级
            draw.text((icon_bg_x + 30, icon_bg_y + 95), 
                     f"Lv.{level}", font=self.font_16, fill=WHITE, anchor="mm")
        
        # 绘制总评分（参考源项目左侧声骸评分圆章）
        try:
            from ..utils.calculate import calc_phantom_score, calc_total_phantom_score
        except ImportError:
            from utils.calculate import calc_phantom_score, calc_total_phantom_score
        try:
            phantom_list = (role_detail.phantomData.equipPhantomList or []) if role_detail.phantomData else []
            scores = []
            for p in phantom_list:
                if not p:
                    continue
                main_props = p.mainProps or []
                sub_props = p.subProps or []
                score = calc_phantom_score(role_detail.role.roleId, main_props, sub_props, p.cost)
                scores.append(score)
            total = calc_total_phantom_score(scores)
            # 圆形徽章
            badge_center = (150, y_base + 120)
            badge_r = 60
            badge_bg = Image.new('RGBA', (badge_r * 2, badge_r * 2), (0, 0, 0, 0))
            badge_draw = ImageDraw.Draw(badge_bg)
            badge_draw.ellipse([0, 0, badge_r * 2, badge_r * 2], fill=(40, 40, 50, 220), outline=(100, 100, 120, 200), width=2)
            img.paste(badge_bg, (badge_center[0] - badge_r, badge_center[1] - badge_r), badge_bg)
            # 等级字母
            draw_text_with_shadow(img, total.grade, (badge_center[0], badge_center[1] - 10), self.font_36, anchor="mm")
            # 分数
            draw_text_with_shadow(img, f"{total.score}分", (badge_center[0], badge_center[1] + 28), self.font_16, anchor="mm")
        except Exception:
            pass
    
    def _draw_chain_section(self, img: Image.Image, role_detail):
        """绘制命座区域"""
        chain_list = role_detail.chainList or []
        if not chain_list:
            return
        
        draw = ImageDraw.Draw(img)
        y_base = 1050
        
        # 标题
        draw.text((50, y_base), "【命座】", font=self.font_24, fill=WHITE)
        
        # 命座背景 - 使用banner3替代
        chain_bg = load_resource_image("banner3.png")
        if chain_bg:
            chain_bg = chain_bg.resize((1100, 100))
            img.paste(chain_bg, (50, y_base + 40), chain_bg)
        else:
            # 使用纯色背景
            chain_area = Image.new('RGBA', (1100, 100), (40, 40, 50, 150))
            img.paste(chain_area, (50, y_base + 40), chain_area)
        
        # 横向排列命座
        chain_x = 80
        chain_y = y_base + 55
        chain_spacing = 180
        
        for i, chain in enumerate(chain_list[:6]):
            x = chain_x + i * chain_spacing
            
            # 尝试加载命座图标
            chain_icon = None
            if hasattr(chain, 'iconUrl') and chain.iconUrl:
                try:
                    chain_icon = get_chain_icon_sync(i + 1, chain.iconUrl)
                except Exception:
                    pass
            
            if chain_icon and chain.unlocked:
                # 使用下载的图标（仅解锁状态显示图标）
                chain_icon = chain_icon.resize((70, 70))
                img.paste(chain_icon, (x, chain_y), chain_icon)
                color = GOLD
            else:
                # 命座图标背景 - 使用菱形/六边形绘制
                if chain.unlocked:
                    color = GOLD
                    fill_color = (80, 60, 40, 200)
                else:
                    color = GREY
                    fill_color = (50, 50, 60, 150)
                
                # 绘制六边形背景
                self._draw_hexagon(draw, x + 35, chain_y + 35, 35, fill_color, color)
            
            # 命座序号
            draw.text((x + 35, chain_y + 75), f"{i+1}", font=self.font_14, fill=color, anchor="mm")
    
    def _draw_hexagon(self, draw: ImageDraw.Draw, cx: int, cy: int, size: int, fill_color: tuple, outline_color: tuple):
        """绘制六边形"""
        import math
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 2
            px = cx + size * math.cos(angle)
            py = cy + size * math.sin(angle)
            points.append((px, py))
        draw.polygon(points, fill=fill_color, outline=outline_color)
    
    def _draw_phantom_section(self, img: Image.Image, role_detail):
        """绘制声骸区域"""
        phantom_data = role_detail.phantomData
        if not phantom_data:
            return
        
        phantom_list = phantom_data.equipPhantomList or []
        valid_phantoms = [p for p in phantom_list if p]
        
        if not valid_phantoms:
            return
        
        draw = ImageDraw.Draw(img)
        y_base = 1200
        
        # 标题
        draw.text((50, y_base), "【声骸】", font=self.font_24, fill=WHITE)
        draw.text((150, y_base), f"{len(valid_phantoms)}/5", font=self.font_20, fill=GREY)
        
        # 声骸列表 - 横向排列
        ph_x = 50
        ph_y = y_base + 50
        ph_spacing = 220
        
        for i, phantom in enumerate(valid_phantoms[:5]):
            if not phantom:
                continue
            
            x = ph_x + i * ph_spacing
            prop = phantom.phantomProp
            name = prop.name if prop else "未知"
            
            # 声骸卡片背景 - 使用sh_bg替代
            ph_card_bg = load_resource_image("sh_bg.png")
            if ph_card_bg:
                ph_card_bg = ph_card_bg.resize((200, 280))
                img.paste(ph_card_bg, (x, ph_y), ph_card_bg)
            else:
                # 使用带边框的卡片背景
                card_bg = Image.new('RGBA', (200, 280), (40, 40, 50, 180))
                img.paste(card_bg, (x, ph_y), card_bg)
                draw.rectangle([x, ph_y, x + 200, ph_y + 280], outline=(100, 100, 120, 200), width=2)
            
            # 尝试加载声骸图标
            ph_icon = None
            if hasattr(prop, 'iconUrl') and prop.iconUrl:
                try:
                    ph_icon = get_phantom_icon_sync(prop.phantomId, prop.iconUrl)
                except Exception:
                    pass
            
            # 声骸名称（顶部）
            draw.text((x + 100, ph_y + 15), name, font=self.font_16, fill=WHITE, anchor="mm")
            
            # 等级和cost
            draw.text((x + 100, ph_y + 40), f"+{phantom.level} C{phantom.cost}", 
                     font=self.font_14, fill=GOLD, anchor="mm")
            
            # 声骸图标（中间偏上）
            icon_y = ph_y + 70
            if ph_icon:
                ph_icon = ph_icon.resize((60, 60))
                img.paste(ph_icon, (x + 70, icon_y), ph_icon)
            
            # 主词条（突出显示）
            main_props = phantom.mainProps or []
            main_y = ph_y + 140
            if main_props:
                main_prop = main_props[0]
                prop_text = f"{main_prop.attributeName}"
                prop_value = main_prop.attributeValue
                # 主词条背景
                draw.rectangle([x + 10, main_y, x + 190, main_y + 25], fill=(60, 60, 70, 200))
                draw.text((x + 100, main_y + 12), f"{prop_text}: {prop_value}", 
                         font=self.font_14, fill=GOLD, anchor="mm")
            
            # 副词条
            sub_props = phantom.subProps or []
            start_y = main_y + 35
            for j, sub_prop in enumerate(sub_props[:4]):
                sub_text = f"{sub_prop.attributeName}: {sub_prop.attributeValue}"
                draw.text((x + 100, start_y + j * 22), sub_text, 
                         font=self.font_12, fill=GREY, anchor="mm")
            
            # 声骸评分（如果有）
            try:
                from ..utils.calculate import calc_phantom_score
            except ImportError:
                from utils.calculate import calc_phantom_score
            if main_props or sub_props:
                try:
                    score_result = calc_phantom_score(
                        role_detail.role.roleId,
                        main_props,
                        sub_props,
                        phantom.cost
                    )
                    # 评分背景
                    score_bg_color = self._get_score_color(score_result.grade)
                    draw.rounded_rectangle([x + 50, ph_y + 235, x + 150, ph_y + 265], 
                                          radius=5, fill=score_bg_color)
                    draw.text((x + 100, ph_y + 250), f"{score_result.score}分", 
                             font=self.font_14, fill=WHITE, anchor="mm")
                except Exception:
                    pass
    
    def _get_score_color(self, grade: str) -> tuple:
        """根据评级获取颜色"""
        color_map = {
            "SS": (255, 100, 100, 200),
            "S": (255, 200, 50, 200),
            "A": (100, 200, 100, 200),
            "B": (100, 150, 255, 200),
            "C": (150, 100, 200, 200),
            "D": (150, 150, 150, 200),
        }
        return color_map.get(grade, (100, 100, 100, 200))


# 全局渲染器实例
_renderer: Optional[RoleCardRenderer] = None


def get_renderer() -> RoleCardRenderer:
    """获取渲染器实例"""
    global _renderer
    if _renderer is None:
        _renderer = RoleCardRenderer()
    return _renderer


def render_role_card(role_detail, account: Optional[Dict] = None, raw_detail: Optional[Dict] = None) -> bytes:
    """渲染角色练度卡片（便捷函数）"""
    renderer = get_renderer()
    return renderer.render_role_card(role_detail, account=account, raw_detail=raw_detail)
