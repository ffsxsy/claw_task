# 测试文档

本目录包含项目的所有自动化测试。

## 测试结构

```
tests/
├── README.md           # 本文件
├── test_backend.py     # 后端 API 测试
├── test_frontend.py    # 前端 HTML 测试
├── test_integration.py # 集成测试
└── run_all_tests.sh    # 运行所有测试的脚本
```

## 运行测试

### 运行所有测试
```bash
cd tests
bash run_all_tests.sh
```

### 单独运行测试
```bash
# 后端测试
python test_backend.py

# 前端测试
python test_frontend.py

# 集成测试（需要后端运行）
python test_integration.py
```

## 测试覆盖

### 后端测试 (test_backend.py)
- ✅ FastAPI 应用导入
- ✅ 随机数生成功能
- ✅ 路由注册检查
- ✅ CORS 中间件配置
- ✅ API 响应格式验证
- ✅ 错误处理测试

### 前端测试 (test_frontend.py)
- ✅ HTML 文档结构
- ✅ API URL 配置
- ✅ JavaScript 函数定义
- ✅ 自动刷新功能
- ✅ UI 元素检查
- ✅ 按钮和显示元素

### 集成测试 (test_integration.py)
- ✅ 前后端通信测试
- ✅ 实时数据更新测试
- ✅ 错误恢复测试
- ✅ 并发请求测试
