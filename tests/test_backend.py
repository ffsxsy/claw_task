#!/usr/bin/env python3
"""
后端 API 自动化测试
使用 FastAPI TestClient 测试所有端点与中间件。
运行方式（在项目根目录）：python tests/test_backend.py
"""
from __future__ import annotations

import sys
import os

# 将 backend 加入路径以便导入 main（需在项目根目录运行本脚本）
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient

from main import app  # type: ignore[import-untyped]

client = TestClient(app)


def test_app_import() -> None:
    """应用可正常导入"""
    assert app is not None


def test_root_endpoint() -> None:
    """GET / 返回正确信息"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Random Number API"
    assert data.get("version") == "0.1.0"
    assert "endpoints" in data


def test_random_endpoint_status_and_shape() -> None:
    """GET /random 返回 200 且为 JSON 含 number"""
    response = client.get("/random")
    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "")
    data = response.json()
    assert isinstance(data, dict)
    assert "number" in data
    assert isinstance(data["number"], int)


def test_random_endpoint_range() -> None:
    """GET /random 的 number 在 1-100 之间"""
    for _ in range(20):
        response = client.get("/random")
        assert response.status_code == 200
        num = response.json()["number"]
        assert 1 <= num <= 100, f"number {num} 超出范围 [1, 100]"


def test_random_endpoint_optional_timestamp() -> None:
    """GET /random 可能包含 timestamp 字段"""
    response = client.get("/random")
    assert response.status_code == 200
    data = response.json()
    # 当前实现有 timestamp，不强制要求
    assert "number" in data


def test_404() -> None:
    """不存在的路径返回 404"""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_cors_middleware() -> None:
    """应用已挂载 CORS 中间件"""
    from fastapi.middleware.cors import CORSMiddleware

    # Starlette 的 user_middleware 元素为 Middleware 实例，.cls 为中间件类
    mounted = any(getattr(m, "cls", None) == CORSMiddleware for m in app.user_middleware)
    assert mounted, "未检测到 CORS 中间件"


def test_routes_registered() -> None:
    """根路径与 /random 已注册"""
    from fastapi.routing import APIRoute

    routes = [r.path for r in app.routes if isinstance(r, APIRoute)]
    assert "/" in routes
    assert "/random" in routes


def run_all() -> int:
    """顺序执行所有测试，返回 0 成功 1 失败"""
    tests = [
        test_app_import,
        test_root_endpoint,
        test_random_endpoint_status_and_shape,
        test_random_endpoint_range,
        test_random_endpoint_optional_timestamp,
        test_404,
        test_cors_middleware,
        test_routes_registered,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    print("后端 API 测试 (TestClient)")
    print("=" * 50)
    code = run_all()
    print("=" * 50)
    print("🎉 全部通过" if code == 0 else "⚠️ 存在失败")
    sys.exit(code)
