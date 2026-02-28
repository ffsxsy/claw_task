# 开发指南

## 开发环境搭建

### 必需工具

- **Python 3.8+**: 后端开发
- **代码编辑器**: VS Code / PyCharm / Vim
- **浏览器**: Chrome / Firefox / Edge（带开发者工具）
- **API 测试工具**: Postman / curl / HTTPie

### 可选工具

- **Git**: 版本控制
- **Docker**: 容器化部署
- **Nginx**: 反向代理
- **uv**: 快速 Python 包管理器

---

## 项目初始化

### 克隆项目

```bash
git clone <repository-url>
cd random-number-demo
```

### 后端初始化

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 或使用 uv（更快）
pip install uv
uv pip install -r requirements.txt
```

### 前端初始化

前端使用纯 HTML/CSS/JS，无需构建步骤。

---

## 开发工作流

### 1. 启动开发服务器

**后端（终端 1）**
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端（终端 2）**
```bash
cd frontend
python -m http.server 3000
```

### 2. 开发流程

1. 修改代码
2. 后端自动重载（uvicorn --reload）
3. 刷新浏览器查看前端变化
4. 测试功能是否正常

### 3. 代码规范

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

#### JavaScript 代码风格

```javascript
// ✅ 使用 const/let
const apiUrl = 'http://localhost:8000/random';

// ❌ 避免 var
var apiUrl = 'http://localhost:8000/random';
```

---

## 调试技巧

### 后端调试

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

### 前端调试

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

## 测试

### 后端测试

创建 `backend/test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Random Number API"}

def test_get_random_number():
    response = client.get("/random")
    assert response.status_code == 200
    assert "number" in response.json()
    assert 1 <= response.json()["number"] <= 100

if __name__ == "__main__":
    test_read_root()
    test_get_random_number()
    print("✅ 所有测试通过！")
```

运行测试：

```bash
cd backend
python test_main.py
# 或使用 pytest
pytest test_main.py -v
```

### 前端测试

手动测试清单：

- [ ] 页面正常加载
- [ ] 点击"获取随机数"按钮显示随机数
- [ ] 自动刷新功能正常工作
- [ ] 状态信息正确显示
- [ ] 网络错误时有错误提示

---

## 常见问题

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

## 扩展功能建议

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

## 性能优化

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

## 学习资源

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

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

MIT License - 详见 LICENSE 文件
