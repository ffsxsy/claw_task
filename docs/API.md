# API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **数据格式**: JSON
- **字符编码**: UTF-8

## 接口列表

### 1. 根路径

**请求**
```
GET /
```

**响应**
```json
{
  "message": "Random Number API"
}
```

**说明**
- 用于测试 API 是否正常运行
- 返回服务基本信息

---

### 2. 获取随机数

**请求**
```
GET /random
```

**响应**
```json
{
  "number": 42
}
```

**参数说明**
- 无需参数

**响应字段**
- `number`: 随机整数，范围 1-100

**状态码**
- `200 OK`: 请求成功
- `500 Internal Server Error`: 服务器错误

**使用示例**

**cURL**
```bash
curl http://localhost:8000/random
```

**JavaScript Fetch**
```javascript
fetch('http://localhost:8000/random')
  .then(res => res.json())
  .then(data => console.log(data.number));
```

**Python Requests**
```python
import requests
response = requests.get('http://localhost:8000/random')
print(response.json()['number'])
```

---

## CORS 配置

API 已配置允许跨域请求：

- `allow_origins`: `*` (允许所有来源)
- `allow_methods`: `*` (允许所有 HTTP 方法)
- `allow_headers`: `*` (允许所有请求头)
- `allow_credentials`: `true`

---

## 错误处理

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 常见错误

| 状态码 | 说明 |
|--------|------|
| 404 | 路径不存在 |
| 422 | 请求参数验证失败 |
| 500 | 服务器内部错误 |

---

## 测试 API

### 使用 Swagger UI

FastAPI 自动生成交互式文档：

访问 http://localhost:8000/docs

### 使用 ReDoc

访问 http://localhost:8000/redoc

---

## 性能说明

- 响应时间: < 10ms
- 并发支持: 取决于服务器配置
- 无状态设计: 可水平扩展
