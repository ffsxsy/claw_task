# 开发指南

更新日期：2026年02月28日

## 1. 开发环境搭建

### 1.1 必需工具

- **Python ≥ 3.13**：后端开发（以 `backend/.python-version` 或 pyproject.toml 为准）
- **Node.js 18+**、**pnpm**：前端开发
- **uv**（推荐）：后端 Python 包管理与虚拟环境
- **代码编辑器**：VS Code / PyCharm / Vim
- **浏览器**：Chrome / Firefox / Edge（带开发者工具）
- **API 测试**：Postman / curl / HTTPie 或访问 http://localhost:8000/docs

### 1.2 可选工具

- **Git**：版本控制
- **Docker**：容器化部署
- **Nginx**：反向代理

---

## 2. 项目初始化

### 2.1 克隆项目

```bash
git clone <repository-url>
cd claw_task
```

### 2.2 后端初始化

依赖以 `backend/pyproject.toml` 为准，使用 **uv**（推荐）：

```bash
cd backend

# 创建虚拟环境并安装依赖
uv venv --python 3.13
source .venv/bin/activate   # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

uv sync
```

若使用 pip（需先有 Python 3.13 与 venv）：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# 或：pip install fastapi "uvicorn[standard]" pydantic
```

### 2.3 前端初始化

前端为 Vue 3 + Vite，需安装依赖并构建/开发：

```bash
cd frontend
pnpm install
```

首次安装时 esbuild 会执行构建脚本（已在 `package.json` 的 `pnpm.onlyBuiltDependencies` 中配置）。

---

## 3. 开发工作流与运行命令

### 3.1 一键启动（推荐）

在项目根目录执行：

```bash
chmod +x start.sh stop.sh
./start.sh
```

会同时启动后端（http://localhost:8000）和前端（http://localhost:5173）。停止：`Ctrl+C` 或 `./stop.sh`。

### 3.2 分别启动

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

### 3.3 常用运行命令

| 场景 | 命令 |
|------|------|
| 后端开发（热重载） | `cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000` |
| 前端开发 | `cd frontend && pnpm dev` |
| 前端构建 | `cd frontend && pnpm build` |
| 前端预览构建结果 | `cd frontend && pnpm preview` |

### 3.4 开发流程

1. 修改代码
2. 后端自动重载（uvicorn --reload）
3. 前端 Vite 热更新，浏览器自动刷新
4. 在 http://localhost:8000/docs 或前端页面测试功能

### 3.5 代码规范

#### Python 代码风格

遵循 PEP 8 规范：

```python
# ✅ 好的命名
def get_random_number():
    """返回随机数"""
    return random.randint(1, 100)

# ❌ 避免
def getNum():
    return random.randint(1,100)
```

#### JavaScript / Vue 代码风格

```javascript
// ✅ 使用 const/let
const apiUrl = 'http://localhost:8000/random';

// ❌ 避免 var
var apiUrl = 'http://localhost:8000/random';
```

---

## 4. 调试技巧

### 4.1 后端调试

#### 1. 使用 print 调试

```python
@app.get("/random")
def get_random_number():
    num = random.randint(1, 100)
    print(f"生成的随机数: {num}")  # 控制台输出
    return {"number": num}
```

#### 2. 使用 Python 调试器

```python
import pdb; pdb.set_trace()  # 设置断点

# 或使用 ipdb（更好用）
import ipdb; ipdb.set_trace()
```

#### 3. 查看 FastAPI 文档

访问 http://localhost:8000/docs 进行交互式调试

### 4.2 前端调试

#### 1. 浏览器开发者工具

按 `F12` 或右键 → 检查

- **Console**: 查看 JavaScript 错误和日志
- **Network**: 查看网络请求
- **Elements**: 检查和修改 DOM

#### 2. console.log 调试

```javascript
async function fetchRandom() {
    console.log('开始请求...');  // 调试日志
    const response = await fetch(API_URL);
    console.log('响应状态:', response.status);
    const data = await response.json();
    console.log('返回数据:', data);
}
```

#### 3. 断点调试

在开发者工具 → Sources 中设置断点

---

## 5. 测试

项目测试分布在 `backend/`、`tests/` 和（可选）`frontend/` 目录，后端与集成测试与当前代码一致，前端为 Vue 3 后原有基于静态 HTML 的脚本可能需配合构建结果或手动验证。

### 5.1 后端测试

**方式一：快速检查（backend 目录内）**

`backend/test_backend.py` 校验应用导入、随机数范围、路由注册与 CORS，无需启动服务：

```bash
cd backend
source .venv/bin/activate
python test_backend.py
```

**方式二：完整 API 测试（项目根目录）**

`tests/test_backend.py` 使用 FastAPI `TestClient`，覆盖根路径、`/random`、响应格式、404、并发等：

```bash
# 在项目根目录执行（脚本会把 backend 加入路径）
python tests/test_backend.py
```

包含的用例示例：

- 应用导入、随机数生成、路由与 CORS
- `GET /` 响应与 `message` 内容
- `GET /random` 多次请求、范围 1–100、JSON 格式
- 404、并发请求

### 5.2 前端测试

**自动化脚本（针对 HTML 结构）**

`tests/test_frontend.py` 通过解析 `frontend/index.html` 检查文档结构、API URL、按钮与状态等。当前前端为 Vue 3 + Vite，入口 `index.html` 仅包含 `<div id="app">` 与脚本引用，逻辑在 `src/` 中，因此该脚本更适用于旧版静态单页或构建后的 `dist/index.html`（若需可改为读取构建产物）。

在项目根目录运行：

```bash
python tests/test_frontend.py
```

**可选：frontend 目录内简易检查**

```bash
cd frontend
python test_frontend.py
```

依赖当前目录下的 `index.html`（同上，Vue 项目下内容较少）。

**手动 / 浏览器验证建议**

- 执行 `pnpm dev` 后访问 http://localhost:5173
- 检查：页面加载、点击获取随机数、自动刷新、状态与错误提示

### 5.3 集成测试

`tests/test_integration.py` 通过 HTTP 请求真实后端，需**先启动后端**（如 `uvicorn main:app --reload --host 0.0.0.0 --port 8000`）。测试项包括：API 连通性、`/random`、响应时间、并发、404/错误处理、数据范围一致性。

```bash
# 终端 1：启动后端
cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 终端 2：在项目根目录运行集成测试
python tests/test_integration.py
```

集成测试依赖 `requests`，若未安装：`uv pip install requests` 或 `pip install requests`（在 backend 虚拟环境中或单独环境均可）。

### 5.4 一键运行所有测试

```bash
cd tests
bash run_all_tests.sh
```

会依次执行后端测试、前端测试，并询问是否运行集成测试（选「是」时需保证后端已启动）。脚本内提示的启动命令以当前文档为准（后端 uvicorn，前端 `pnpm dev`）。

---

## 6. 常见问题

### Q1: CORS 错误

**错误信息**: `Access to fetch at '...' has been blocked by CORS policy`

**解决方案**:
1. 确保后端已添加 CORSMiddleware
2. 检查 `allow_origins` 配置
3. 开发环境可以使用 `allow_origins=["*"]`

### Q2: 后端无法启动

**检查清单**:
```bash
# 1. 检查端口是否被占用
lsof -i :8000

# 2. 检查 Python 版本
python --version

# 3. 检查依赖是否安装
pip list | grep fastapi
```

### Q3: 前端无法连接后端

**检查清单**:
1. 后端是否正在运行
2. API_URL 是否正确（http://localhost:8000/random）
3. 浏览器控制台是否有错误信息

### Q4: 随机数范围不对

**解决方案**:
修改 `main.py` 中的范围参数：

```python
# 修改为 1-1000
return {"number": random.randint(1, 1000)}
```

---

## 7. 扩展功能建议

### 后端扩展

1. **添加更多 API 端点**
   ```python
   @app.get("/random/{min}/{max}")
   def get_random_range(min: int, max: int):
       return {"number": random.randint(min, max)}
   ```

2. **添加数据库支持**
   ```python
   # 存储历史记录
   from datetime import datetime
   history = []

   @app.post("/save")
   def save_number(number: int):
       history.append({
           "number": number,
           "timestamp": datetime.now().isoformat()
       })
       return {"status": "saved"}
   ```

3. **添加认证**
   ```python
   from fastapi import Depends, HTTPException, Header

   async def verify_token(x_token: str = Header(...)):
       if x_token != "secret-token":
           raise HTTPException(status_code=400, detail="Invalid token")
       return x_token
   ```

### 前端扩展

1. **添加图表可视化**
   ```javascript
   // 使用 Chart.js 显示历史数据
   const ctx = document.getElementById('chart').getContext('2d');
   const chart = new Chart(ctx, {
       type: 'line',
       data: { /* ... */ }
   });
   ```

2. **添加深色模式**
   ```javascript
   function toggleTheme() {
       document.body.classList.toggle('dark');
   }
   ```

3. **添加音效**
   ```javascript
   const audio = new Audio('sound.mp3');
   audio.play();
   ```

---

## 8. 性能优化

### 后端优化

1. **使用异步**
   ```python
   @app.get("/random")
   async def get_random_number():
       return {"number": random.randint(1, 100)}
   ```

2. **添加缓存**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.inmemory import InMemoryBackend

   FastAPICache.init(InMemoryBackend())

   @app.get("/random")
   @cache(expire=1)  # 缓存1秒
   async def get_random_number():
       return {"number": random.randint(1, 100)}
   ```

### 前端优化

1. **防抖处理**
   ```javascript
   function debounce(func, wait) {
       let timeout;
       return function(...args) {
           clearTimeout(timeout);
           timeout = setTimeout(() => func.apply(this, args), wait);
       };
   }
   ```

2. **请求缓存**
   ```javascript
   let cache = {};
   async function fetchWithCache(url) {
       if (cache[url]) return cache[url];
       const response = await fetch(url);
       cache[url] = await response.json();
       return cache[url];
   }
   ```

---

## 9. 学习资源

### FastAPI
- [官方文档](https://fastapi.tiangolo.com/)
- [教程](https://fastapi.tiangolo.com/tutorial/)

### JavaScript
- [MDN Web 文档](https://developer.mozilla.org/zh-CN/)
- [JavaScript.info](https://zh.javascript.info/)

### Web 开发
- [MDN Web 开发指南](https://developer.mozilla.org/zh-CN/docs/Learn)
- [freeCodeCamp](https://www.freecodecamp.org/chinese/)

---

## 10. 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

MIT License - 详见 LICENSE 文件
