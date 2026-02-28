# 随机数实时显示项目

一个简单的全栈 Web 应用，演示前后端分离架构。

## 项目结构

```
random-number-demo/
├── frontend/          # 前端代码
│   └── index.html    # 主页面
├── backend/          # 后端代码
│   ├── main.py       # FastAPI 应用
│   └── requirements.txt
└── docs/             # 项目文档
    ├── API.md        # API 文档
    ├── DEPLOYMENT.md # 部署文档
    └── DEVELOPMENT.md # 开发指南
```

## 功能特性

- 后端生成 1-100 的随机数
- 前端实时显示随机数
- 支持手动获取和自动刷新
- 跨域支持 (CORS)

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python main.py
# 或使用 uvicorn
uvicorn main:app --reload
```

后端将在 http://localhost:8000 运行

### 前端启动

直接用浏览器打开 `frontend/index.html`，或使用本地服务器：

```bash
cd frontend
python -m http.server 3000
```

访问 http://localhost:3000

## 技术栈

- **后端**: Python + FastAPI + Uvicorn
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **通信**: REST API + Fetch API

## API 接口

### GET /

返回欢迎信息

### GET /random

返回随机数

**响应示例:**
```json
{
  "number": 42
}
```

## 许可证

MIT License
