# coding=utf-8
"""
自动删除无效CK功能
"""
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger
from .models import WutheringWavesBind
from .config import get_config
from .constants import WAVES_GAME_ID


_driver = get_driver()


@_driver.on_startup
async def auto_delete_all_invalid_cookie():
    """定时任务：自动删除所有无效CK"""
    from nonebot_plugin_apscheduler import scheduler
    
    config = get_config()
    
    if not config.ENABLE_AUTO_DELETE_INVALID:
        return
    
    @scheduler.scheduled_job(
        "cron",
        hour=config.AUTO_DELETE_HOUR,
        minute=config.AUTO_DELETE_MINUTE
    )
    async def auto_delete():
        del_len = await WutheringWavesBind.delete_all_invalid_cookie(WAVES_GAME_ID)
        if del_len == 0:
            return
        
        msg = f"[鸣潮] 删除无效token【{del_len}】个"
        logger.info(f"[鸣潮] 自动删除无效token结果: {msg}")
        
        try:
            bot = get_bot()
            if bot:
                master_id = getattr(_driver.config, "master", None)
                if master_id:
                    if isinstance(master_id, list) and master_id:
                        master_id = master_id[0]
                    if master_id:
                        await bot.send_private_msg(
                            user_id=int(master_id),
                            message=msg
                        )
                        logger.info(f"[鸣潮] 已推送主人删除无效token结果")
        except Exception as e:
            logger.error(f"[鸣潮] 推送主人删除无效token结果失败: {e}")
