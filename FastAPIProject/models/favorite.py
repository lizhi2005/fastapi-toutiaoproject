from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime, UTC
from sqlalchemy import DateTime, String, Integer, ForeignKey, Index, Text, UniqueConstraint
from typing import Optional

from models.news import News
from models.users import User

class Base(DeclarativeBase):
    pass



class Favorite(Base):
    # 指定这个ORM 模型类对应的数据库表名
    __tablename__ = "favorite";
    # 给数据库表添加额外的表级配置 / 约束，是一个元组（也可以是字典）
    __table_args__=(
        UniqueConstraint("user_id",'news_id',name='user_news_unique'),
        Index('fk_favorite_user_idx','user_id'),
        Index('fk_favorite_news_idx', 'news_id')
     )
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id),nullable=False,comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id),nullable=False,comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), nullable=False, comment="收藏时间")

