from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker,Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, func, Integer, String, Float,select
from datetime import datetime
from fastapi import FastAPI,Path,Query,HTTPException,Depends
from contextlib import asynccontextmanager  # 关键导入
from pydantic import BaseModel
from models.news import Base
# 配置相关


# app = FastAPI()
# 数据库类型+驱动://用户名:密码@主机地址:端口/数据库名?额外参数
# 数据库连接地址
ASYNC_DATABASE_URL = "mysql+aiomysql://root:lizhi20050914@localhost:3306/news_app?charset=utf8"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,#输出SQL日志
    pool_size=10,#设置连接池中保持的持久连接数
    max_overflow=20#设置连接池允许创建的额外连接数
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)
# 依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal(expire_on_commit=False) as session:
    # 告诉SQLAlchemy：数据库提交（commit）之后，不要把对象的属性过期
    # 原来默认是True，所以你commit之后，再访问user.id，SQLAlchemy
    # 会以为你要去数据库查新数据，就触发了懒加载 → 报错
    # 加了False之后，commit之后，user.id这些属性直接从内存里拿，不用查数据库，所以就不会报错了
        try:
            yield session  # 把会话交给路由使用
            await session.commit()
        except Exception:
            await session.rollback()  # 出错时回滚
            raise
        finally:
            await session.close()  # 最终关闭会话



