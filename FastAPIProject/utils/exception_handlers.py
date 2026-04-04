# 导入traceback模块，用于捕获和格式化代码的详细异常堆栈信息
import traceback
# 从fastapi导入：HTTPException（主动抛出的业务异常）、Request（获取当前请求对象，如请求路径）
from fastapi import HTTPException,Request
# 导入JSONResponse，用于统一返回JSON格式的错误响应给前端
from fastapi.responses import JSONResponse
# 从sqlalchemy导入数据库相关异常：
# IntegrityError：数据库完整性错误（唯一键重复、外键不存在等）
# SQLAlchemyError：所有数据库操作异常的基类
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
# 从starlette导入HTTP状态码常量（如400、500），使用常量比写数字更规范、易读
from starlette import status
# 在你现在的教学 / 本地开发阶段：必须保持 DEBUG_MODE = True，因为这样你写代码报错时，控制台和接口才能告诉你具体是哪里错了（比如刚才的布尔值错误）。
# 在以后部署到真实服务器（上线）时：必须改为 DEBUG_MODE = False。
# 当你写成 DEBUG_MODE = True 时，程序处于开发模式，主要有这 3 大作用：
# 1. 报错时能看到 “详细的后台日志”（最直接的作用）
# 开启时（True）：如果代码报错（比如刚才的 TRUE 写错报错，或者数据库连不上），页面或接口会返回详细的错误代码、行数、堆栈信息。
# 效果：你能直接看到错在哪一行，像刚才的 NameError，只有在 Debug 模式下你才能快速定位。
# 关闭时（False）：如果报错，它不会把详细错误吐给前端 / 调用方，只返回一句 “服务器内部错误”。
# 效果：生产环境必须关，否则暴露系统细节给黑客。
# 2. 自动重启（热重载）
# 在 FastAPI 或 Flask 等框架中，开启 Debug 模式后：
# 一旦你修改了代码并保存，服务器会自动检测到文件变化并重启。
# 你不需要手动停掉服务再重启跑一遍，改完代码直接刷新浏览器就能看到最新效果。
# 3. 详细的告警信息
# 框架会在控制台打印更多的请求日志、警告信息，方便你排查逻辑漏洞。
# 如果在生产环境（给真实用户用）长期开启 DEBUG = True，会有两个致命后果：
# 敏感信息泄露（核弹级风险）：
# Debug 模式下，一旦出现系统崩溃，会把服务器的完整文件路径、源码、环境变量、甚至数据库账号密码全部暴露给前端用户。黑客只需一个错误就能把你系统家底全偷走。
# 性能损耗：
# Debug 模式会记录大量的调试状态，导致服务器运行变慢，并发量上不去。
# 开发模式：返回详细的错误信息
# 生产模式：返回简化的错误信息


# 开发阶段（教学/本地调试）：必须设为 True
# 生产环境（上线服务器）：必须设为 False
# 作用：控制是否返回详细错误堆栈、敏感信息

DEBUG_MODE = True
# DEBUG_MODE = True  # 教学项目保持开启
# http_exception_handler：处理主动抛出的业务异常（如参数错误、未登录）
# integrity_error_handler：处理数据库约束错误（用户名重复、外键错误）
# sqlalchemy_error_handler：处理数据库通用错误（连接失败、查询失败）
# general_exception_handler：兜底处理所有未知错误（防止程序崩溃）
# ===================== 异常处理函数 =====================
async def http_exception_handler(request:Request,exc:HTTPException):
    """
    处理 FastAPI 主动抛出的 HTTPException 异常
    这类异常通常是业务代码主动抛出的（如参数错误、权限不足、资源不存在）
    """
    # 处理HHTTPException异常
    # 通常是业务逻辑主动抛出的
    # 返回统一格式的JSON响应
    return JSONResponse(
        # 状态码使用异常本身定义的状态码（如400、401、404）
        status_code=exc.status_code,
        content={
            # 统一响应结构：code=状态码，message=错误信息，data=异常数据（这里无数据）
            'code':exc.status_code,
            'message':exc.detail,
            'data':None
        }
    )

async def integrity_error_handler(request:Request,exc:IntegrityError):
    """
    处理数据库完整性约束错误（IntegrityError）
    常见场景：用户名重复、手机号重复、外键关联数据不存在
    """
    # 处理数据库完整性约束错误
    # 获取数据库原始错误信息（字符串格式）
    error_msg=str(exc.orig)
    # 判断具体的约束错误类型
    # 根据原始错误信息，判断具体是哪种约束错误，返回友好提示
    if "username_UNION" in error_msg or "Duplicate entry" in error_msg:
        # 唯一键重复（如用户名已被注册）
        detail="用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        # 外键约束失败（关联数据不存在）
        detail="关联数据不存在"
    else:
        # 其他数据库约束错误
        detail="数据约束冲突，请检查输入"
    # 开发模式下返回详细错误信息
    # 定义错误详情数据，默认空
    error_data=None
    if DEBUG_MODE:
        # 开发模式下：返回详细错误信息（方便调试）
        error_data={
            "error_type":"IntegrityError",# 异常类型
            "error_detail":error_msg,# 原始错误信息
            "path":str(request.url) # 出错的接口路径
        }
        # 返回400客户端错误响应
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code":400,
            "message":detail,
            "data":error_data# 开发模式有详情，生产模式为空
        }
    )

async def sqlalchemy_error_handler(request:Request,exc:SQLAlchemyError):
    # 处理salalchemy数据库错误
    """
    处理通用数据库操作异常（SQLAlchemyError）
    如：数据库连接失败、SQL语法错误、查询超时等
    这类属于服务器端错误，返回500
    """
    error_data=None
    if DEBUG_MODE:
        # 开发模式：返回完整异常信息 + 堆栈 + 路径
        error_data={
            "error_type":type(exc).__name__,# 异常类名
            "error_detail":str(exc), # 异常描述
            "traceback":traceback.format_exc(), # 完整堆栈（关键：定位代码行）
            "path":str(request.url)# 请求路径
        }
        # 返回500服务器内部错误
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"数据库操作失败，请稍后重试",
            "data":error_data
        }
    )


async def general_exception_handler(request:Request,exc:Exception):
    # 处理所有未捕获的异常
    """
    全局兜底异常处理
    捕获所有**未被上面任何一个异常处理函数捕获**的错误
    确保程序不会崩溃，且前端永远能收到规范响应
    """
    error_data=None
    if DEBUG_MODE:
        error_data={
            "error_type":type(exc).__name__,# 异常类型
            "error_detail":str(exc),# 异常信息
            #格式化异常信息为字符串，方便日志记录和调试
            "traceback":traceback.format_exc(),# 完整堆栈
            "path":str(request.url)# 出错接口
        }
    # 返回500通用服务器错误
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"服务器内部错误",
            "data":error_data
        }
    )