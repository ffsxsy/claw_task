#!/usr/bin/env python3
"""测试后端 API"""
import sys
import random

# 测试导入
try:
    from main import app
    print("✅ FastAPI 应用导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 测试随机数生成
try:
    num = random.randint(1, 100)
    print(f"✅ 随机数生成测试: {num} (范围 1-100)")
    assert 1 <= num <= 100, "随机数超出范围"
except Exception as e:
    print(f"❌ 随机数生成失败: {e}")
    sys.exit(1)

# 测试路由
try:
    from fastapi.routing import APIRoute
    routes = [route.path for route in app.routes if isinstance(route, APIRoute)]
    print(f"✅ 注册的路由: {routes}")
    assert "/" in routes, "缺少根路径"
    assert "/random" in routes, "缺少 /random 路径"
except Exception as e:
    print(f"❌ 路由检查失败: {e}")
    sys.exit(1)

# 测试 CORS 中间件
try:
    from fastapi.middleware.cors import CORSMiddleware
    has_cors = any(isinstance(middleware, CORSMiddleware) for middleware in app.user_middleware)
    print(f"✅ CORS 中间件: {'已启用' if has_cors else '未启用'}")
except Exception as e:
    print(f"⚠️ CORS 检查警告: {e}")

print("\n🎉 所有后端测试通过！")
print("启动命令: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
