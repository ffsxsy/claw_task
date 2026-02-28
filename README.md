# 随机数实时显示项目

一个最简单的前后端分离项目，后端生成随机数，前端实时显示。

## 项目结构

```
claw_task/
├── backend/
│   ├── main.py          # FastAPI 后端
│   ├── requirements.txt # Python 依赖
│   └── test_backend.py  # 后端单元测试
├── frontend/
│   ├── index.html       # 纯 HTML/CSS/JS 前端
│   └── test_frontend.py # 前端单元测试
├── tests/
│   ├── README.md        # 测试文档
│   ├── test_backend.py  # 后端完整测试
│   ├── test_frontend.py # 前端完整测试
│   ├── test_integration.py # 集成测试
│   └── run_all_tests.sh # 运行所有测试
├── start.sh             # 启动脚本
├── stop.sh              # 停止脚本
└── README.md            # 本文件
```

## 快速开始

### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 运行项目

#### 方式 1: 使用启动脚本（推荐）
```bash
./start.sh
```

#### 方式 2: 手动启动

**后端 (FastAPI)**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
后端将在 http://localhost:8000 运行

**前端**
```bash
cd frontend
python3 -m http.server 3000
```
然后访问 http://localhost:3000

### 停止项目
```bash
./stop.sh
```

## 测试

### 运行所有测试
```bash
cd tests
bash run_all_tests.sh
```

### 单独运行测试
```bash
# 后端测试
cd tests
python test_backend.py

# 前端测试
cd tests
python test_frontend.py

# 集成测试（需要后端运行）
cd tests
python test_integration.py
```

### 测试覆盖
- ✅ 后端: FastAPI 应用、随机数生成、路由、CORS、API 响应、错误处理、并发请求
- ✅ 前端: HTML 结构、API 配置、JavaScript 函数、自动刷新、UI 元素、CSS 样式
- ✅ 集成: API 连接性、响应时间、并发请求、错误处理、数据一致性

## API 接口

- `GET /` - 欢迎信息
- `GET /random` - 返回随机数 (1-100)

## 功能

- 点击按钮获取随机数
- 开启自动刷新模式（每秒更新）
- 实时显示状态信息
