from click.testing import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update
from models.news import Category,News
from click.testing import Result

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 构建查询语句，获取所有分类，支持分页
    stm = select(Category).offset(skip).limit(limit)
    # 异步执行查询
    result = await db.execute(stm)
    # 返回所有分类列表
    return result.scalars().all()


async def get_new_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 查询指定分类下的新闻，支持分页
    stm = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # 异步执行查询
    result = await db.execute(stm)
    # 返回当前页的新闻列表
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    # 统计指定分类下的新闻总数量
    stm = select(func.count(News.category_id)).where(News.category_id == category_id)
    # 异步执行统计查询
    result = await db.execute(stm)
    # 返回唯一的统计结果
    return result.scalar_one()


async def get_detail(db: AsyncSession, new_id: int):
    # 根据新闻ID查询新闻详情
    stm = select(News).where(News.id == new_id)
    # 异步执行查询
    result = await db.execute(stm)
    # 返回唯一的新闻详情
    return result.scalar_one()


async def get_views(db: AsyncSession, new_id: int):
    # 新闻浏览量+1，更新数据库
    stm = update(News).where(News.id == new_id).values(views=News.views + 1)
    # 异步执行更新
    result: Result = await db.execute(stm)

    # 判断是否成功更新命中数据，返回布尔值
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, new_id: int, category_id: int, limit: int = 5):
    # 查询相关新闻：同分类、排除当前新闻，按浏览量和发布时间排序
    stm = select(News).where(
        News.category_id == category_id,
        News.id != new_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    # 异步执行查询
    result = await db.execute(stm)
    # 获取相关新闻列表
    related_news = result.scalars().all()

    # 手动序列化，统一字段名为驼峰格式，返回标准字典列表
    return [
        {
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "publish_time": news.publish_time,
            "categoryId": news.category_id,
            "views": news.views
        }
        for news in related_news
    ]
# async def get_categories(db: AsyncSession,skip:int=0,limit:int=100):
#     stm=select(Category).offset(skip).limit(limit)
#     result=await db.execute(stm)
#     return result.scalars().all()
#
#
# async def get_new_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
#     # 查询指定分类下的新闻
#     stm=select(News).where(News.category_id == category_id).offset(skip).limit(limit)
#     result=await db.execute(stm)
#     return result.scalars().all()
#
# async def get_news_count(db:AsyncSession,category_id:int):
#     # 指定分类下的新闻数量
#     stm=select(func.count(News.category_id)).where(News.category_id == category_id)
#     result=await db.execute(stm)
#     return result.scalar_one()#只能有一个结果
#
#
# async def get_detail(db:AsyncSession,new_id:int):
#     stm=select(News).where(News.id == new_id)
#     result=await db.execute(stm)
#     return result.scalar_one()
#
# async def get_views(db:AsyncSession,new_id:int):
#     stm=update(News).where(News.id==new_id).values(views=News.views+1)
#     result:Result=await db.execute(stm)
#
#     # await db.commit()
# # 更新  检查数据库是否真的命中了数据   命中了返回true
#     return result.rowcount>0
#
# async def get_related_news(db:AsyncSession,new_id:int,category_id:int,limit:int=5):
#     stm=select(News).where(News.category_id == category_id ,
#                            News.id!=new_id).order_by(
#                                 News.views.desc(),
#                                 News.publish_time.desc()
#                         ).limit(limit)
#     result=await db.execute(stm)
#     related_news=result.scalars().all()
#     # 手动序列化，统一字段名，避免ORM对象问题
#     return [
#         {
#             "id": news.id,
#             "title": news.title,
#             "content": news.content,
#             "image": news.image,
#             "author": news.author,
#             "publish_time": news.publish_time,
#             "categoryId": news.category_id,  # 统一用驼峰，和主新闻一致
#             "views": news.views
#         }
#         for news in related_news
#     ]
#








