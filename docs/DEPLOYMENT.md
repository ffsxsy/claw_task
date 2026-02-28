# 部署文档

更新日期：2026年02月28日

## 1. 开发环境部署

### 1.1 环境要求

- **后端**：Python ≥ 3.13，[uv](https://docs.astral.sh/uv/)（推荐）或 pip
- **前端**：Node.js 18+，[pnpm](https://pnpm.io/)
- 现代浏览器

### 1.2 后端环境与运行

**安装依赖（以 `backend/pyproject.toml` 为准）：**

```bash
cd backend
uv venv --python 3.13
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync
```

**启动服务：**

| 模式 | 命令 |
|------|------|
| 开发（热重载） | `uvicorn main:app --reload --host 0.0.0.0 --port 8000` |
| 生产（单进程） | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| 生产（多 worker） | `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4` |

**验证：**

```bash
curl http://localhost:8000/
curl http://localhost:8000/random
```

### 1.3 前端环境与运行

**安装依赖：**

```bash
cd frontend
pnpm install
```

**运行：**

| 场景 | 命令 | 说明 |
|------|------|------|
| 开发 | `pnpm dev` | 开发服务器，默认 http://localhost:5173，热更新 |
| 构建 | `pnpm build` | 输出到 `dist/` |
| 预览构建结果 | `pnpm preview` | 本地预览 `dist/` |

开发时访问 http://localhost:5173，无需再用 `python -m http.server` 或 Live Server。

### 1.4 一键启动

在项目根目录：

```bash
./start.sh
```

会同时启动后端（8000）与前端（5173）。停止：`Ctrl+C` 或 `./stop.sh`。

---

## 2. 生产环境部署

### 2.1 方案一：Nginx + Uvicorn/Gunicorn

**后端：**

```bash
cd backend
source .venv/bin/activate
# 直接多进程可用：
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用 Gunicorn（需安装：uv add gunicorn）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**前端：** 先构建再提供静态文件：

```bash
cd frontend
pnpm build
# 将 dist/ 目录部署到 Nginx 或任意静态服务器
```

**Nginx 配置示例：**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件（Vite 构建后的 dist）
    location / {
        root /path/to/claw_task/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

### 2.2 方案二：Docker 部署

#### Dockerfile（后端）

（构建上下文为项目根目录，例：`docker build -f backend/Dockerfile .` 时需调整 COPY 路径）

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY backend/ .
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile（前端）

前端需先构建，再由 Nginx 提供静态文件：

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

#### 启动服务

```bash
docker compose up -d
```

---

### 2.3 方案三：云平台部署

**Vercel / Netlify（前端）：**

```bash
cd frontend
pnpm build
# 将 dist/ 或配置构建命令为 pnpm build、发布目录为 dist
```

**Render / Railway（后端）：**

连接 GitHub 仓库，配置示例：
- Build：`cd backend && uv sync` 或 `pip install -e .`
- Start：`uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 3. 环境变量配置

创建 `.env` 文件（backend 目录）：

```bash
# 服务器配置
HOST=0.0.0.0
PORT=8000
WORKERS=4

# CORS 配置（生产环境建议指定域名）
ALLOWED_ORIGINS=https://your-domain.com
```

修改 `main.py`：

```python
import os
from dotenv import load_dotenv

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    # ...
)
```

---

## 4. 安全建议

1. **CORS 限制**: 生产环境指定允许的域名
2. **HTTPS**: 使用 SSL 证书（Let's Encrypt）
3. **Rate Limiting**: 添加请求频率限制
4. **日志监控**: 记录访问日志和错误
5. **防火墙**: 只开放必要端口

---

## 5. 监控和维护

### 健康检查

```bash
# 检查后端
curl http://localhost:8000/

# 检查进程
ps aux | grep uvicorn
```

### 日志查看

```bash
# 查看应用日志
tail -f /var/log/app.log

# 查看 Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 自动重启

使用 `systemd` 或 `supervisor` 管理进程

---

## 6. 备份和恢复

### 数据备份

```bash
# 备份代码
tar -czf backup-$(date +%Y%m%d).tar.gz /path/to/project

# 备份到云存储
aws s3 cp backup.tar.gz s3://backups/
```

### 恢复

```bash
tar -xzf backup-20240228.tar.gz
```
