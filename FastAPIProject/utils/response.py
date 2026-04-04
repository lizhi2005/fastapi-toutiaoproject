
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    # 目标：把任何的 FastAPI、Pydantic、ORM 对象 都要正常响应 → code、message、data
    return JSONResponse(content=jsonable_encoder(content))


# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Any, Optional
#
# def success_response(message: str = "success", data: Optional[Any] = None) -> JSONResponse:
#     """
#     统一成功响应工具函数
#     自动处理 Pydantic 模型、ORM 对象、普通字典的序列化
#     """
#     #  先序列化 data，再组装 content（顺序绝对不能错！）
#     if isinstance(data, BaseModel):
#         # Pydantic V2 用 model_dump()，V1 用 dict()
#         data = data.model_dump(by_alias=True)  # by_alias=True 会用别名 userInfo 而不是 user_info
#     elif isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
#         data = [item.model_dump(by_alias=True) for item in data]
#     #  用序列化后的 data 组装 content
#     content = {
#         "code": 200,
#         "message": message,
#         "data": data
#     }
#     # 3. 返回 JSONResponse（此时 content 全是可序列化的 Python 原生类型）
#     return JSONResponse(content=content)