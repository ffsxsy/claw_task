# 随机数实时显示项目

一个最简单的前后端分离项目，后端生成随机数，前端实时显示。

## 项目结构

```
random-number-demo/
├── backend/
│   ├── main.py          # FastAPI 后端
│   └── requirements.txt # Python 依赖
└── frontend/
    └── index.html       # 纯 HTML/CSS/JS 前端
```

## 运行方法

### 后端 (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端将在 http://localhost:8000 运行

### 前端

直接用浏览器打开 `frontend/index.html` 文件

或者使用简单的 HTTP 服务器：

```bash
cd frontend
python3 -m http.server 3000
```

然后访问 http://localhost:3000

## API 接口

- `GET /` - 欢迎信息
- `GET /random` - 返回随机数 (1-100)

## 功能

- 点击按钮获取随机数
- 开启自动刷新模式（每秒更新）
- 实时显示状态信息
