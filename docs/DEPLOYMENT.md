# 部署文档

## 开发环境部署

### 环境要求

- Python 3.8+
- pip 或 uv
- 现代浏览器

### 后端部署

#### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2. 启动服务

**开发模式（支持热重载）**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**生产模式**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 3. 验证服务

```bash
curl http://localhost:8000/
curl http://localhost:8000/random
```

### 前端部署

#### 1. 本地服务器

```bash
cd frontend
python -m http.server 3000
```

访问 http://localhost:3000

#### 2. 使用 Live Server (VS Code)

安装 "Live Server" 扩展，右键 `index.html` 选择 "Open with Live Server"

---

## 生产环境部署

### 方案 1: Nginx + Gunicorn

#### 后端部署

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend;
        index index.html;
        try_files $uri $uri/ =404;
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

### 方案 2: Docker 部署

#### Dockerfile (后端)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile (前端)

```dockerfile
FROM nginx:alpine

COPY frontend/ /usr/share/nginx/html/

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
docker-compose up -d
```

---

### 方案 3: 云平台部署

#### Vercel (前端)

```bash
npm i -g vercel
cd frontend
vercel
```

#### Render / Railway (后端)

连接 GitHub 仓库，配置：
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 环境变量配置

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

## 安全建议

1. **CORS 限制**: 生产环境指定允许的域名
2. **HTTPS**: 使用 SSL 证书（Let's Encrypt）
3. **Rate Limiting**: 添加请求频率限制
4. **日志监控**: 记录访问日志和错误
5. **防火墙**: 只开放必要端口

---

## 监控和维护

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

## 备份和恢复

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
