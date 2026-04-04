from fastapi import APIRouter,Depends,HTTPException,Query
from crud import news, news_cache
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from crud.news import get_news_count, get_new_list, get_detail, get_views, get_related_news

# 创建APIRouter实例 prefix路由实例
router=APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db:AsyncSession=Depends(get_db)):
    # 先获取数据库分类→先定义类模型→封装查询数据的方法
    categories=await news_cache.get_categories(db,skip,limit)
    return {
        "code":200,
        "msg":"获取新闻分类成功",
        "data":categories
            }


@router.get("/list")
async def get_news_list(
        category_id:int=Query(...,alias="categoryId"),#alias起别名
        page:int=1,
        page_size:int=Query(10,alias="pageSize"),
        db:AsyncSession=Depends(get_db)
):#处理过分页规则 查询新闻列表 计算总量 计算是否还有更多
    offset=(page-1)*page_size
    new_list=await get_new_list(db,category_id,offset,page_size)
    total=await get_news_count(db,category_id)
    hasmore=(offset+len(new_list))<total
    return {"code":200,
            "message":"获取新闻列表成功",
            "data":{
                "list":new_list,
                "total":total,
                "hasMore":hasmore,
               }

            }




@router.get("/detail")
async def get_news_detail(new_id:int=Query(...,alias="id"),db:AsyncSession=Depends(get_db)):
    news_detail=await get_detail(db,new_id)
    view_res=await get_views(db,new_id)
    relatedNews=await get_related_news(db,news_detail.id,news_detail.category_id)
    if not view_res :
        raise HTTPException(status_code=404,detail="新闻不存在")
    if news_detail is None:
        raise HTTPException(status_code=404,detail="新闻不存在")
    return {
        "code":200,
        "message":"success",
        "data":{
           "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publish_time":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":relatedNews
        }
    }

























