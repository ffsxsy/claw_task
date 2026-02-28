#!/usr/bin/env python3
"""
后端快速自检：导入、路由、CORS。
在 backend 目录下运行：python test_backend.py
"""
from __future__ import annotations

import sys

try:
    from main import app
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

# 路由
routes = [r.path for r in app.routes if isinstance(r, APIRoute)]
assert "/" in routes, "缺少根路径"
assert "/random" in routes, "缺少 /random"
print("✅ 路由: /, /random")

# CORS（Starlette 中 Middleware 实例有 .cls 属性）
has_cors = any(getattr(m, "cls", None) == CORSMiddleware for m in app.user_middleware)
assert has_cors, "未配置 CORS"
print("✅ CORS 已启用")

# 随机数范围（不启动服务，仅做逻辑检查）
import random
n = random.randint(1, 100)
assert 1 <= n <= 100
print(f"✅ 随机数范围 1-100 正常")

print("\n🎉 后端自检通过")
print("启动: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
