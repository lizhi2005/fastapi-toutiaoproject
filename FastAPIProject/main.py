from fastapi import FastAPI
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境替换为你的前端域名，如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包含 OPTIONS
    allow_headers=["*"],  # 允许所有头，包含 Authorization
)

@app.get("/")
async def root():
    return {"code":200,"msg":"欢迎来到Tom&Jerry新闻系统"}

# 挂载路由/注册路由
app.include_router(history.router)
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
