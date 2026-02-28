# Claw Task 文档索引

更新日期：2026年02月28日

## 1. 概述

Claw Task 是一个前后端分离的全栈 Web 应用：后端提供随机数 API，前端用 Vue 3 + Vite 实时展示。

## 2. 文档目录

| 文档 | 说明 |
|------|------|
| [API.md](API.md) | 后端 API 接口说明 |
| [DEVELOPMENT.md](DEVELOPMENT.md) | 开发环境搭建与日常开发命令 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 开发/生产环境部署与运行方式 |
| [cheatsheet.md](cheatsheet.md) | 常用命令与地址速查 |

## 3. 前后端环境搭建

### 3.1 环境要求

- **后端**：Python ≥ 3.13，[uv](https://docs.astral.sh/uv/)（推荐）或 pip
- **前端**：Node.js 18+，[pnpm](https://pnpm.io/)
- **系统**：Linux / macOS / Windows（WSL 推荐）

### 3.2 后端环境

在项目根目录下执行：

```bash
cd backend

# 使用 uv（推荐）
uv venv --python 3.13
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync

# 或使用 pip（需先创建 venv）
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# 若无可安装包则：pip install fastapi "uvicorn[standard]" pydantic
```

依赖以 `backend/pyproject.toml` 为准。

### 3.3 前端环境

在项目根目录下执行：

```bash
cd frontend
pnpm install
```

依赖以 `frontend/package.json` 为准；首次安装会执行 esbuild 的构建脚本（已在 `package.json` 的 `pnpm.onlyBuiltDependencies` 中配置）。

## 4. 运行命令

### 4.1 一键启动（推荐）

在项目根目录：

```bash
chmod +x start.sh stop.sh   # 首次需赋予执行权限
./start.sh
```

会同时启动后端（端口 8000）和前端（端口 5173）。停止时在对应终端按 `Ctrl+C`，或执行 `./stop.sh`。

### 4.2 分别启动

**后端（终端 1）：**

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端（终端 2）：**

```bash
cd frontend
pnpm dev
```

### 4.3 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:5173 |
| 后端 API | http://localhost:8000 |
| Swagger 文档 | http://localhost:8000/docs |
| ReDoc 文档 | http://localhost:8000/redoc |

### 4.4 常用脚本

| 场景 | 命令 |
|------|------|
| 前端开发 | `cd frontend && pnpm dev` |
| 前端构建 | `cd frontend && pnpm build` |
| 前端预览构建结果 | `cd frontend && pnpm preview` |
| 后端开发（热重载） | `cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000` |
| 后端生产式启动 | `cd backend && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000` |

## 5. 项目结构（当前）

```
claw_task/
├── backend/              # FastAPI 后端
│   ├── .venv/            # Python 虚拟环境（本地）
│   ├── main.py           # 应用入口
│   └── pyproject.toml    # 依赖与项目配置
├── frontend/             # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── docs/                 # 本文档目录
├── start.sh              # 启动脚本
└── stop.sh               # 停止脚本
```

## 6. 技术栈

- **后端**：Python 3.13、FastAPI、Uvicorn、uv（包管理）
- **前端**：Vue 3、Vite、pnpm

更多细节见 [DEVELOPMENT.md](DEVELOPMENT.md) 与 [DEPLOYMENT.md](DEPLOYMENT.md)。
