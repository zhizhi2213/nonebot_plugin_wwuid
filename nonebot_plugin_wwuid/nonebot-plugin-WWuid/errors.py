# coding=utf-8
"""
鸣潮错误代码定义
"""

WAVES_CODE_101 = 101
WAVES_CODE_102 = 102
WAVES_CODE_103 = 103
WAVES_CODE_999 = 999

ERROR_MESSAGES = {
    WAVES_CODE_101: "库街区暂未查询到角色数据",
    WAVES_CODE_102: "未绑定游戏账号或CK已失效，请使用 /添加ck 重新绑定",
    WAVES_CODE_103: "未找到角色信息，请先使用 /刷新面板 进行刷新",
    WAVES_CODE_999: "网络请求失败，请稍后重试",
}


def error_reply(code: int = 0, msg: str = "") -> str:
    """统一错误回复"""
    if msg:
        return f"❌ {msg}"
    
    error_msg = ERROR_MESSAGES.get(code, f"未知错误 (代码: {code})")
    return f"❌ {error_msg}"
