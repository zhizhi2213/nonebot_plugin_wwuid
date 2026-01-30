# coding=utf-8
"""
鸣潮用户绑定数据模型
"""
from datetime import datetime
from nonebot_plugin_orm import Model
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class WutheringWavesBind(Model):
    """鸣潮用户绑定表"""
    
    # 主键ID，自增
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 用户QQ号，唯一索引（一个QQ只能绑定一个游戏账号）
    user_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    
    # 游戏UID
    game_uid: Mapped[str] = mapped_column(String(50))
    
    # 游戏Cookie/Token
    cookie: Mapped[str] = mapped_column(String(500))
    
    # 创建时间
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # 更新时间（每次修改绑定时更新）
    update_time: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now
    )