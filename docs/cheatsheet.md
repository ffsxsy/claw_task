# Claw Task 开发速查卡

更新日期：2026年02月28日

## 1. 快速启动

### 1.1 一键启动

在项目根目录执行：

```bash
./start.sh
```

### 1.2 手动启动

**后端：**

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端（新终端）：**

```bash
cd frontend
pnpm dev
```

### 1.3 停止服务

```bash
./stop.sh
```

或在运行 `start.sh` 的终端按 `Ctrl+C`。

---

## 2. 访问地址

| 服务 | 地址 |
|------|------|
| 前端应用 | http://localhost:5173 |
| 后端 API | http://localhost:8000 |
| API 文档 (Swagger) | http://localhost:8000/docs |
| API 文档 (ReDoc) | http://localhost:8000/redoc |

---

## 3. 环境搭建

### 3.1 后端 (FastAPI + uv)

在项目根目录下执行：

```bash
cd backend

# 创建虚拟环境
uv venv --python 3.13

# 激活虚拟环境（Windows: .venv\Scripts\activate）
source .venv/bin/activate

# 安装依赖（以 pyproject.toml 为准）
uv sync
```

### 3.2 前端 (Vue 3 + Vite + pnpm)

在项目根目录下执行：

```bash
cd frontend
pnpm install
```

---

## 4. 常用命令

### 4.1 后端

| 命令 | 说明 |
|------|------|
| `uv venv --python 3.13` | 创建虚拟环境 |
| `source .venv/bin/activate` | 激活虚拟环境 |
| `uv sync` | 同步依赖（按 pyproject.toml） |
| `uvicorn main:app --reload` | 启动开发服务器（热重载） |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | 启动生产服务器 |
| `uv add <pkg>` | 添加依赖并写入 pyproject.toml |

### 4.2 前端

| 命令 | 说明 |
|------|------|
| `pnpm install` | 安装依赖 |
| `pnpm add <pkg>` | 添加依赖 |
| `pnpm add -D <pkg>` | 添加开发依赖 |
| `pnpm dev` | 启动开发服务器 |
| `pnpm build` | 构建生产版本（输出到 dist/） |
| `pnpm preview` | 预览生产构建 |

---

## 5. API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | API 信息 |
| GET | `/random` | 获取随机数 (1-100) |

详见 [API.md](API.md)。

---

## 6. CORS 配置

后端 `main.py` 中已配置 CORS，开发时允许 `http://localhost:5173`。生产环境建议在 `allow_origins` 中只保留实际前端域名。

---

## 7. 项目结构（当前）

```
claw_task/
├── backend/
│   ├── .venv/           # Python 虚拟环境（本地）
│   ├── main.py          # FastAPI 主应用
│   └── pyproject.toml   # 依赖与项目配置
├── frontend/
│   ├── src/
│   │   ├── App.vue      # 根组件
│   │   ├── main.js      # 入口
│   │   └── style.css    # 全局样式
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── README.md
│   └── cheatsheet.md    # 本文档
├── start.sh
└── stop.sh
```

---

## 8. 故障排查

### 8.1 端口被占用

```bash
lsof -i :8000   # 后端
lsof -i :5173   # 前端
kill -9 <PID>
```

### 8.2 依赖问题

**后端：**

```bash
cd backend
source .venv/bin/activate
uv sync
```

**前端：**

```bash
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### 8.3 CORS 错误

确认后端已启动，且 `main.py` 中 `allow_origins` 包含前端地址（如 `http://localhost:5173`）。

### 8.4 后端虚拟环境不存在

按「3.1 后端」步骤执行：`cd backend && uv venv --python 3.13 && source .venv/bin/activate && uv sync`。

---

## 9. 技术栈

- **前端**：Vue 3、Vite、pnpm
- **后端**：FastAPI、Python 3.13、uv、Uvicorn
