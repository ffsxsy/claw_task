# 🎲 Claw Task - 随机数生成器

一个现代化的全栈 Web 应用，使用 Vue 3 + FastAPI 构建。

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **pnpm** - 快速、节省磁盘空间的包管理器

### 后端
- **FastAPI** - 现代、快速的 Python Web 框架
- **Python 3.13** - 最新版本的 Python
- **uv** - 极速的 Python 包管理器

## 项目结构

```
claw_task/
├── backend/           # FastAPI 后端
│   ├── .venv/        # Python 虚拟环境
│   ├── main.py       # 主应用
│   └── pyproject.toml # 项目配置
├── frontend/         # Vue 3 前端
│   ├── src/
│   │   ├── App.vue   # 主组件
│   │   ├── main.js   # 入口文件
│   │   └── style.css # 全局样式
│   ├── index.html    # HTML 模板
│   ├── vite.config.js # Vite 配置
│   └── package.json  # 依赖配置
├── start.sh          # 启动脚本
└── stop.sh           # 停止脚本
```

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
uv venv --python 3.13
source .venv/bin/activate
uv sync
```

### 2. 安装前端依赖

```bash
cd frontend
pnpm install
```

### 3. 启动项目

#### 方式一：使用启动脚本（推荐）
```bash
cd claw_task
chmod +x start.sh stop.sh
./start.sh
```

#### 方式二：手动启动

**后端：**
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
pnpm dev
```

### 4. 访问应用

- **前端页面：** http://localhost:5173
- **后端 API：** http://localhost:8000
- **API 文档：** http://localhost:8000/docs

## 功能特性

- ✅ 实时随机数生成 (1-100)
- ✅ 手动获取随机数
- ✅ 自动刷新模式（每秒更新）
- ✅ 现代化 UI 设计
- ✅ 响应式布局
- ✅ 跨域支持
- ✅ API 文档自动生成

## API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | API 信息 |
| GET | `/random` | 获取随机数 (1-100) |

## 开发命令

### 后端
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload        # 开发模式
uvicorn main:app --host 0.0.0.0 --port 8000  # 生产模式
```

### 前端
```bash
cd frontend
pnpm dev        # 开发模式
pnpm build      # 构建生产版本
pnpm preview    # 预览生产构建
```

## 停止服务

```bash
./stop.sh
```

## 注意事项

1. 确保已安装 Python 3.13 和 pnpm
2. 首次运行需要安装依赖
3. 生产环境部署时请修改 CORS 配置
4. 后端默认端口 8000，前端默认端口 5173

## License

MIT
