# 测试说明

## 1. 结构

| 文件 | 说明 |
|------|------|
| `test_backend.py` | 后端 API 测试（FastAPI TestClient），无需启动服务 |
| `test_frontend.py` | 前端结构与源码检查（index.html、App.vue、main.js） |
| `test_integration.py` | 集成测试，请求真实后端，**需先启动后端** |
| `run_all_tests.sh` | 一键运行上述测试（集成测试可选） |
| `requirements.txt` | 仅集成测试依赖：`requests` |

此外，`backend/test_backend.py` 可在 backend 目录内做快速自检（导入、路由、CORS）。

## 2. 运行方式

**要求**：在**项目根目录**执行以下命令（或先 `cd /path/to/claw_task`）。

### 一键运行

```bash
bash tests/run_all_tests.sh
```

会依次执行后端测试、前端检查，并询问是否运行集成测试。

### 单独运行

```bash
# 后端（无需启动服务）
python tests/test_backend.py

# 前端检查
python tests/test_frontend.py

# 集成测试（需先启动后端）
python tests/test_integration.py
```

集成测试依赖 `requests`，若未安装：

```bash
pip install -r tests/requirements.txt
# 或 uv pip install requests
```

### 后端快速自检

```bash
cd backend
source .venv/bin/activate
python test_backend.py
```

## 3. 覆盖内容

- **test_backend.py**：`GET /`、`GET /random`、响应格式、number 范围、404、CORS、路由注册。
- **test_frontend.py**：index.html 结构、App.vue 中的 API 调用、按钮与状态、错误处理、main.js 挂载。
- **test_integration.py**：真实 HTTP 请求 `/`、`/random`、404、简单响应时间统计。

## 4. 启动命令参考

- 后端：`cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- 前端：`cd frontend && pnpm dev`

更多见项目根目录 README 与 `docs/DEVELOPMENT.md`。
