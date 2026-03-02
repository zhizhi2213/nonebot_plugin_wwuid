# coding=utf-8
"""
卡提希娅角色练度卡片生成 - 使用真实API数据
从底层 API 获取数据并调用渲染引擎输出图片
"""
import os
import sys
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# 将项目根目录添加到 sys.path 以便导入模块
# 当前脚本在 plugin_debug_tests 目录下，父目录是 nonebot-plugin-WWuid
# 再上一级是 nonebot_plugin_wwuid 包目录
current_path = Path(__file__).parent
plugin_root = current_path.parent
sys.path.insert(0, str(plugin_root))

# 配置日志
# 尝试将日志文件创建在 nonebot-plugin-WWuid 目录下
log_file_path = plugin_root / "test_katixiya.log"
print(f"Attempting to write log to: {log_file_path}") # 打印日志路径
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler(sys.stdout) # 同时输出到控制台
    ]
)
logger = logging.getLogger(__name__)

logger.info("="*60)
logger.info("鸣潮角色练度卡片生成测试 - 使用真实 API 数据")
logger.info("="*60)

# 导入底层模块
try:
    from wwuid_api.client import WavesApi
    from wwuid_api.models import RoleDetailData, RoleList
    from wwuid_renderer import render_role_card
    from plugin_core.roles import get_role_id_by_name
    logger.info("  ✓ 核心模块导入成功")
except ImportError as e:
    logger.error(f"  ✗ 模块导入失败: {e}")
    # 打印 sys.path 以便调试
    logger.error(f"  Debug - sys.path: {sys.path}")
    sys.exit(1)

# 配置信息
COOKIE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkIjoxNzY1Nzg5NTMwMTY5LCJ1c2VySWQiOjEwMTYxNDU5fQ.o1mRTSxIno5L8AE_Ygxft_VXEU7sc_DJj2BsJYW0lsI"
DID = "7786E85B-6116-4112-A5E9-E9384AAB7C06"
ROLE_ID = "100276895"  # 特征码/UID
TARGET_ROLE_NAME = "卡提希娅"

# 创建输出目录
output_dir = current_path / "output"
output_dir.mkdir(exist_ok=True)
logger.info(f"  ✓ 输出目录: {output_dir}")

async def main():
    api = WavesApi()
    logger.info(f"\n[1/6] 正在请求访问令牌 (bat)...")
    
    success, bat = await api.get_request_token(ROLE_ID, COOKIE_TOKEN, DID)
    if not success:
        logger.error(f"  ✗ 获取访问令牌失败: {bat}")
        await api.close()
        return False
    logger.info(f"  ✓ 获取访问令牌成功")

    logger.info(f"\n[2/6] 正在获取账号列表（按游戏筛选）...")
    response = await api.get_role_info(ROLE_ID, COOKIE_TOKEN)
    if not response.success:
        logger.error(f"  ✗ 获取角色列表失败: {response.message}")
        await api.close()
        return False
    
    # 解析账号列表（这里返回的是账号维度，不是游戏内角色）
    if isinstance(response.data, list) and len(response.data) > 0:
        logger.info("  ✓ 成功获取账号信息（游戏ID=3）")
    else:
        logger.error("  ✗ 获取账号信息格式异常")
        logger.error(f"  原始数据: {response.data}")
        await api.close()
        return False

    # 读取基础信息（账号等级/世界等级/头像等）
    base_resp = await api.get_base_info(ROLE_ID, COOKIE_TOKEN)
    account_info = {
        "uid": ROLE_ID,
        "name": None,
        "accountLevel": None,
        "worldLevel": None,
        "avatarUrl": None,
    }
    # 从 role/list 取 name 与头像
    if isinstance(response.data, list) and len(response.data) > 0:
        first = response.data[0]
        account_info["name"] = first.get("roleName")
        account_info["avatarUrl"] = first.get("headPhotoUrl")
        try:
            account_info["accountLevel"] = int(first.get("gameLevel")) if first.get("gameLevel") is not None else None
        except Exception:
            pass
    # 基础信息优先覆盖世界等级
    if base_resp and base_resp.success and isinstance(base_resp.data, dict):
        account_info["worldLevel"] = base_resp.data.get("worldLevel")

    logger.info(f"\n[3/6] 正在获取已拥有角色列表（游戏内角色）...")
    owned_resp = await api.get_owned_role_info(ROLE_ID, COOKIE_TOKEN)
    if not owned_resp.success:
        logger.error(f"  ✗ 获取已拥有角色列表失败: {owned_resp.message}")
        await api.close()
        return False

    data = owned_resp.data
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            pass

    def _find_char_id(obj) -> Optional[str]:
        if isinstance(obj, dict):
            name = obj.get("roleName") or obj.get("name")
            cid = obj.get("id") or obj.get("roleId") or obj.get("characterId")
            if isinstance(name, str) and name == TARGET_ROLE_NAME and cid is not None:
                return str(cid)
            for v in obj.values():
                found = _find_char_id(v)
                if found:
                    return found
        elif isinstance(obj, list):
            for it in obj:
                found = _find_char_id(it)
                if found:
                    return found
        return None

    char_id = _find_char_id(data)
    if not char_id:
        # 使用补全的映射表
        role_id = get_role_id_by_name(TARGET_ROLE_NAME)
        if role_id:
            char_id = str(role_id)
            logger.warning(f"  ! 未在API返回中找到角色“{TARGET_ROLE_NAME}”，使用映射表ID {char_id}")
        else:
            debug_file = current_path / "owned_roles_debug.json"
            try:
                with open(debug_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
            logger.error(f"  ✗ 无法定位角色“{TARGET_ROLE_NAME}”的ID，已将原始数据保存至: {debug_file}")
            await api.close()
            return False

    logger.info(f"  ✓ 目标角色: {TARGET_ROLE_NAME} (角色ID: {char_id})")

    logger.info(f"\n[4/6] 正在获取角色详情数据...")
    detail_response = await api.get_role_detail_info(char_id, ROLE_ID, COOKIE_TOKEN, DID, bat)
    if not detail_response.success:
        logger.error(f"  ✗ 获取角色详情失败: {detail_response.throw_msg()}")
        logger.error(f"  API Code: {detail_response.code}, Message: {detail_response.message}")
        await api.close()
        return False
    
    # 解析角色详情
    try:
        dump_path = current_path / "last_role_detail.json"
        with open(dump_path, "w", encoding="utf-8") as f:
            json.dump(detail_response.data, f, ensure_ascii=False, indent=2)
        # 注意：API 返回的数据结构可能需要根据实际情况调整
        role_detail = RoleDetailData.model_validate(detail_response.data)
        logger.info(f"  ✓ 成功解析角色详情数据")
    except Exception as e:
        logger.error(f"  ✗ 解析角色详情失败: {e}")
        # 保存原始数据供调试
        debug_file = current_path / f"role_detail_debug_{char_id}.json"
        with open(debug_file, "w", encoding="utf-8") as f:
            json.dump(detail_response.data, f, ensure_ascii=False, indent=2)
        logger.error(f"  ! 原始数据已保存至: {debug_file}")
        await api.close()
        return False

    logger.info(f"\n[5/6] 正在调用渲染引擎生成图片...")
    try:
        image_bytes = render_role_card(role_detail, account=account_info, raw_detail=detail_response.data)
        logger.info(f"  ✓ 图片渲染成功 (大小: {len(image_bytes)/1024:.1f} KB)")
    except Exception as e:
        logger.error(f"  ✗ 图片渲染失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        await api.close()
        return False

    logger.info(f"\n[6/6] 正在保存结果...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{TARGET_ROLE_NAME}_{ROLE_ID}_{timestamp}.png"
    output_path = output_dir / file_name
    
    try:
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"  ✓ 图片已保存至: {output_path}")
    except Exception as e:
        logger.error(f"  ✗ 保存图片失败: {e}")
        await api.close()
        return False

    await api.close()
    return True

if __name__ == "__main__":
    # Windows 下 asyncio 的事件循环策略可能需要调整
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    success = asyncio.run(main())
    
    logger.info("\n" + "="*60)
    if success:
        logger.info("✓ 测试流程全部完成!")
    else:
        logger.error("✗ 测试过程中出现错误")
    logger.info("="*60)
    sys.exit(0 if success else 1)
