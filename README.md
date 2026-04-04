# FastAPI 头条项目
基于 FastAPI 构建的现代化头条类后端服务，采用分层架构设计，支持新闻、用户、收藏、历史记录等核心功能，集成 SQLAlchemy ORM、数据验证、缓存等企业级特性。

---

## 📋 项目简介
本项目是一个完整的 FastAPI 后端项目，模拟头条类应用的核心服务，实现了**用户管理、新闻管理、收藏功能、浏览历史**等核心业务，遵循 RESTful 设计规范，代码结构清晰、可扩展性强，适合作为 FastAPI 项目学习与二次开发的模板。

---

## 🎯 核心功能
- ✅ **用户管理**：用户注册、登录、信息管理（JWT 身份认证）
- ✅ **新闻管理**：新闻的增删改查、列表获取、详情查询
- ✅ **收藏功能**：用户收藏/取消收藏新闻、收藏列表查询
- ✅ **浏览历史**：用户浏览历史记录、历史列表查询
- ✅ **数据缓存**：新闻数据缓存优化，提升接口响应速度
- ✅ **分层架构**：严格按照 `models/crud/schemas/routers/utils/config` 分层，代码解耦
- ✅ **数据验证**：基于 Pydantic 的请求参数严格校验
- ✅ **异常处理**：统一异常捕获与标准化响应格式

---

## 📁 项目结构
头条项目 fastapi-python/├── FastAPIProject/ # 项目核心代码目录│ ├── cache/ # 缓存模块│ │ └── news_cache.py # 新闻缓存实现│ ├── config/ # 配置模块│ │ ├── cache_conf.py # 缓存配置│ │ └── db_conf.py # 数据库配置│ ├── crud/ # 数据库 CRUD 操作层│ │ ├── favorite.py # 收藏相关 CRUD│ │ ├── history.py # 历史相关 CRUD│ │ ├── news.py # 新闻相关 CRUD│ │ ├── news_cache.py # 缓存 CRUD│ │ └── users.py # 用户相关 CRUD│ ├── models/ # 数据库模型层（SQLAlchemy ORM）│ │ ├── favorite.py # 收藏模型│ │ ├── history.py # 历史模型│ │ ├── news.py # 新闻模型│ │ └── users.py # 用户模型│ ├── routers/ # 路由层（API 接口）│ │ ├── init.py│ │ ├── favorite.py # 收藏接口│ │ ├── history.py # 历史接口│ │ ├── news.py # 新闻接口│ │ └── users.py # 用户接口│ ├── schemas/ # 数据验证层（Pydantic 模型）│ │ ├── base.py # 基础模型│ │ ├── favorite.py # 收藏验证模型│ │ ├── history.py # 历史验证模型│ │ ├── news.py # 新闻验证模型│ │ └── users.py # 用户验证模型│ ├── utils/ # 工具函数层│ │ ├── auth.py # 认证相关工具│ │ ├── exception_handlers.py # 异常处理器│ │ ├── response.py # 统一响应工具│ │ └── security.py # 安全相关工具（JWT、加密）│ ├── main.py # 项目入口文件│ └── test_main.http # 接口测试文件├── 项目物料 / # 项目相关物料（可选）├── 头条项目.xmind # 项目思维导图├── .gitignore # Git 忽略文件配置└── 
README.md 
# 项目说明文档

---

## 🛠️ 运行环境
### 技术栈
- **后端框架**：FastAPI
- **数据库 ORM**：SQLAlchemy
- **数据验证**：Pydantic
- **身份认证**：JWT（JSON Web Token）
- **数据库**：SQLite（默认，可扩展 MySQL/PostgreSQL）
- **Python 版本**：Python 3.10+（推荐 3.12）

### 依赖包
```txt
fastapi>=0.100.0
uvicorn>=0.23.2
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

🚀 快速启动
1. 环境准备
# 1. 克隆项目
git clone https://github.com/lizhi2005/fastapi-toutiaoproject.git
cd fastapi-toutiaoproject/FastAPIProject

# 2. 创建虚拟环境（推荐）
python -m venv .venv
# Windows激活虚拟环境
.venv\Scripts\activate
# Linux/Mac激活虚拟环境
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
# 若没有requirements.txt，直接安装核心依赖
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib

2. 配置项目
数据库配置：修改 config/db_conf.py 中的数据库连接信息（默认使用 SQLite，无需额外配置）
缓存配置：修改 config/cache_conf.py 调整缓存参数
JWT 配置：在 utils/security.py 中修改密钥、过期时间等安全参数
3. 启动项目
bash
运行
# 方式1：直接运行main.py
python main.py

# 方式2：使用uvicorn启动（推荐，支持热重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
4. 访问接口
API 文档（自动生成）：http://127.0.0.1:8000/docs（Swagger UI）
API 文档（备选）：http://127.0.0.1:8000/redoc（ReDoc）
项目根路径：http://127.0.0.1:8000
📚 接口说明
核心接口分类
表格
模块	接口说明
用户模块	用户注册、登录、信息查询 / 修改
新闻模块	新闻列表、新闻详情、新闻管理
收藏模块	收藏 / 取消收藏、收藏列表查询
历史模块	浏览历史记录、历史列表查询
所有接口均遵循 RESTful 规范，详细参数与返回格式可直接访问 http://127.0.0.1:8000/docs 查看并在线调试。
📌 项目亮点
分层架构清晰：严格按照 models-crud-schemas-routers 分层，代码解耦，便于维护与扩展
企业级特性集成：JWT 认证、统一异常处理、标准化响应、数据缓存，符合生产环境要求
代码规范：遵循 Python PEP8 规范，结构清晰，注释完善，适合学习与二次开发
可扩展性强：模块化设计，可快速新增业务模块，支持数据库切换（MySQL/PostgreSQL）
自动文档生成：基于 FastAPI 自动生成交互式 API 文档，开箱即用
📝 后续优化方向
🔧 集成 Redis 缓存，提升高并发场景下的性能
🔧 接入 MySQL/PostgreSQL 生产级数据库
🔧 实现接口限流、权限控制
🔧 集成日志系统，完善项目监控
🔧 编写单元测试，提升代码健壮性
🔧 部署到 Docker，实现容器化运行

