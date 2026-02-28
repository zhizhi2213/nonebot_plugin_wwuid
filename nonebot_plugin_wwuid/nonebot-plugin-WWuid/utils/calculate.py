# coding=utf-8
"""
声骸评分计算模块
参考原项目XutheringWavesUID的评分算法
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from nonebot import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


@dataclass
class PhantomScore:
    """声骸评分结果"""
    score: float
    total_score: float
    grade: str  # 评级: S, A, B, C等
    color: str  # 颜色标识


# 声骸词条权重配置
# 格式: (词条名称, C4主词条权重, C3主词条权重, C1主词条权重, 副词条权重)
PHANTOM_WEIGHT_CONFIG = {
    "生命": (0, 0, 0, 0),
    "生命%": (0, 0, 0, 0),
    "攻击": (0, 0, 0, 0.5),
    "攻击%": (0, 0, 0, 1),
    "防御": (0, 0, 0, 0),
    "防御%": (0, 0, 0, 0),
    "共鸣效率": (0, 0, 0, 0.5),
    "暴击": (1, 1, 0, 1),
    "暴击伤害": (1, 1, 0, 1),
    "属性伤害加成": (1, 0, 0, 0.8),
    "治疗效果加成": (0, 0, 0, 0),
    "普攻伤害加成": (0, 0, 0, 0.8),
    "重击伤害加成": (0, 0, 0, 0.8),
    "共鸣技能伤害加成": (0, 0, 0, 0.8),
    "共鸣解放伤害加成": (0, 0, 0, 0.8),
}

# 评分等级映射
SCORE_GRADE_MAP = [
    (50, "SS", "#FF6B6B"),   # 50分以上 SS级
    (45, "S", "#FFD93D"),    # 45-50分 S级
    (40, "A", "#6BCB77"),    # 40-45分 A级
    (35, "B", "#4D96FF"),    # 35-40分 B级
    (30, "C", "#9B59B6"),    # 30-35分 C级
    (0, "D", "#95A5A6"),     # 30分以下 D级
]

# 角色评分模板（不同角色对词条的需求不同）
CHARACTER_TEMPLATES = {
    # 输出型角色模板
    "default_dps": {
        "暴击": 1.0,
        "暴击伤害": 1.0,
        "攻击%": 0.8,
        "属性伤害加成": 0.8,
        "攻击": 0.5,
        "共鸣效率": 0.3,
        "普攻伤害加成": 0.6,
        "重击伤害加成": 0.6,
        "共鸣技能伤害加成": 0.6,
        "共鸣解放伤害加成": 0.6,
    },
    # 辅助型角色模板
    "support": {
        "共鸣效率": 1.0,
        "生命%": 0.8,
        "防御%": 0.8,
        "治疗效果加成": 1.0,
        "生命": 0.5,
        "防御": 0.5,
    },
}


def get_grade_by_score(score: float) -> Tuple[str, str]:
    """
    根据分数获取评级和颜色
    
    Args:
        score: 声骸评分
    
    Returns:
        (评级, 颜色)
    """
    for threshold, grade, color in SCORE_GRADE_MAP:
        if score >= threshold:
            return grade, color
    return "D", "#95A5A6"


def get_prop_weight(prop_name: str, cost: int, is_main_prop: bool = False) -> float:
    """
    获取词条权重
    
    Args:
        prop_name: 词条名称
        cost: 声骸cost值 (1, 3, 4)
        is_main_prop: 是否为主词条
    
    Returns:
        权重值
    """
    if prop_name not in PHANTOM_WEIGHT_CONFIG:
        return 0
    
    weights = PHANTOM_WEIGHT_CONFIG[prop_name]
    
    if is_main_prop:
        # 根据cost选择主词条权重
        if cost == 4:
            return weights[0]
        elif cost == 3:
            return weights[1]
        else:
            return weights[2]
    else:
        # 副词条权重
        return weights[3]


def parse_prop_value(value_str: str) -> float:
    """
    解析属性值字符串为数值
    
    Args:
        value_str: 属性值字符串，如 "15.6%" 或 "1234"
    
    Returns:
        数值
    """
    try:
        if '%' in value_str:
            return float(value_str.replace('%', ''))
        else:
            return float(value_str)
    except (ValueError, TypeError):
        return 0


def calc_phantom_score(
    role_id: int,
    main_props: List[Dict],
    sub_props: List[Dict],
    cost: int,
    template: Optional[Dict] = None
) -> PhantomScore:
    """
    计算声骸评分
    
    Args:
        role_id: 角色ID
        main_props: 主词条列表
        sub_props: 副词条列表
        cost: 声骸cost值
        template: 评分模板（可选）
    
    Returns:
        PhantomScore对象
    """
    if template is None:
        # 默认使用DPS模板
        template = CHARACTER_TEMPLATES["default_dps"]
    
    total_score = 0
    
    # 计算主词条分数
    for prop in main_props:
        prop_name = prop.get("attributeName", "")
        prop_value = parse_prop_value(prop.get("attributeValue", "0"))
        weight = get_prop_weight(prop_name, cost, is_main_prop=True)
        
        if weight > 0:
            # 主词条满分按10分计算
            template_weight = template.get(prop_name, 0.5)
            score = 10 * weight * template_weight
            total_score += score
    
    # 计算副词条分数
    for prop in sub_props:
        prop_name = prop.get("attributeName", "")
        prop_value = parse_prop_value(prop.get("attributeValue", "0"))
        weight = get_prop_weight(prop_name, cost, is_main_prop=False)
        
        if weight > 0:
            # 副词条根据数值和权重计算
            template_weight = template.get(prop_name, 0.5)
            # 暴击和暴击伤害按最大值约30分计算
            if "暴击" in prop_name:
                max_value = 10.5 if "伤害" in prop_name else 21.0  # 暴击伤害最大10.5%，暴击最大21%
                score = (prop_value / max_value) * 30 * weight * template_weight
            # 百分比攻击按最大值约25分计算
            elif "攻击%" in prop_name:
                max_value = 30.0  # 攻击%最大30%
                score = (prop_value / max_value) * 25 * weight * template_weight
            # 其他词条
            else:
                score = 10 * weight * template_weight
            
            total_score += score
    
    # 获取评级
    grade, color = get_grade_by_score(total_score)
    
    return PhantomScore(
        score=round(total_score, 2),
        total_score=round(total_score, 2),
        grade=grade,
        color=color
    )


def calc_total_phantom_score(phantom_scores: List[PhantomScore]) -> PhantomScore:
    """
    计算总声骸评分
    
    Args:
        phantom_scores: 各个声骸的评分列表
    
    Returns:
        总评分
    """
    if not phantom_scores:
        return PhantomScore(0, 0, "D", "#95A5A6")
    
    total = sum(s.score for s in phantom_scores)
    avg = total / len(phantom_scores)
    
    grade, color = get_grade_by_score(avg)
    
    return PhantomScore(
        score=round(avg, 2),
        total_score=round(total, 2),
        grade=grade,
        color=color
    )


def get_character_template(role_id: int, role_name: str = "") -> Dict:
    """
    获取角色评分模板
    
    Args:
        role_id: 角色ID
        role_name: 角色名称
    
    Returns:
        评分模板字典
    """
    # TODO: 根据角色ID或名称返回对应的评分模板
    # 目前返回默认DPS模板
    
    # 辅助型角色列表
    support_chars = ["白芷", "维里奈", "守岸人"]
    
    if any(name in role_name for name in support_chars):
        return CHARACTER_TEMPLATES["support"]
    
    return CHARACTER_TEMPLATES["default_dps"]


# 便捷函数
def quick_calc_phantom(
    prop_name: str,
    prop_value: str,
    cost: int = 4,
    is_main: bool = False
) -> float:
    """
    快速计算单个词条的分数
    
    Args:
        prop_name: 词条名称
        prop_value: 词条值
        cost: cost值
        is_main: 是否主词条
    
    Returns:
        分数
    """
    weight = get_prop_weight(prop_name, cost, is_main)
    value = parse_prop_value(prop_value)
    
    if weight <= 0:
        return 0
    
    return round(value * weight * 0.1, 2)


if __name__ == "__main__":
    # 测试评分功能
    test_main_props = [
        {"attributeName": "暴击", "attributeValue": "30%"},
    ]
    
    test_sub_props = [
        {"attributeName": "暴击伤害", "attributeValue": "15.6%"},
        {"attributeName": "攻击%", "attributeValue": "10.5%"},
        {"attributeName": "生命", "attributeValue": "580"},
    ]
    
    score = calc_phantom_score(1401, test_main_props, test_sub_props, 4)
    print(f"声骸评分: {score.score}")
    print(f"评级: {score.grade}")
    print(f"颜色: {score.color}")
