#!/usr/bin/env python3
"""
集成测试：通过 HTTP 请求真实后端。
需先启动后端：cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
运行方式（项目根目录）：python tests/test_integration.py
依赖：pip install requests 或 uv pip install requests
"""
from __future__ import annotations

import sys
import time
from typing import NoReturn

try:
    import requests
except ImportError:
    print("❌ 请先安装 requests: pip install requests 或 uv pip install requests")
    sys.exit(1)

API_BASE = "http://localhost:8000"


def _fail(msg: str) -> NoReturn:
    print(f"❌ {msg}")
    sys.exit(1)


def check_backend() -> None:
    """确认后端已运行"""
    try:
        r = requests.get(f"{API_BASE}/", timeout=2)
        if r.status_code != 200:
            _fail(f"GET / 返回 {r.status_code}")
    except requests.RequestException as e:
        _fail(f"无法连接后端 {API_BASE}，请先启动: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000\n错误: {e}")


def test_root() -> None:
    """GET / 返回 API 信息"""
    r = requests.get(f"{API_BASE}/", timeout=5)
    assert r.status_code == 200, r.status_code
    data = r.json()
    assert "message" in data and data["message"] == "Random Number API"
    print("  ✅ GET / 正常")


def test_random_repeated() -> None:
    """GET /random 多次请求均返回 1-100"""
    for i in range(10):
        r = requests.get(f"{API_BASE}/random", timeout=5)
        assert r.status_code == 200, f"请求 {i+1} 状态码 {r.status_code}"
        data = r.json()
        assert "number" in data and isinstance(data["number"], int)
        n = data["number"]
        assert 1 <= n <= 100, f"number {n} 超出范围"
    print("  ✅ GET /random 多次请求正常")


def test_404() -> None:
    """不存在的路径返回 404"""
    r = requests.get(f"{API_BASE}/not-found-route", timeout=5)
    assert r.status_code == 404
    print("  ✅ 404 处理正常")


def test_response_time() -> None:
    """简单响应时间统计（不作为失败条件）"""
    times = []
    for _ in range(5):
        start = time.perf_counter()
        requests.get(f"{API_BASE}/random", timeout=5)
        times.append((time.perf_counter() - start) * 1000)
    avg = sum(times) / len(times)
    print(f"  ✅ 响应时间示例: 平均 {avg:.1f}ms")


def run_all() -> int:
    """执行所有集成测试"""
    print("集成测试（需后端已启动）")
    print("=" * 50)
    check_backend()
    test_root()
    test_random_repeated()
    test_404()
    test_response_time()
    print("=" * 50)
    print("🎉 集成测试全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(run_all())
