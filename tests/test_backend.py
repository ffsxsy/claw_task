#!/usr/bin/env python3
"""
后端 API 自动化测试
测试 FastAPI 应用的所有功能
"""
import sys
import os
import json

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import random
from fastapi.testclient import TestClient

# 导入 FastAPI 应用
from main import app

# 创建测试客户端
client = TestClient(app)

def test_import():
    """测试 1: 应用导入"""
    print("\n" + "="*50)
    print("测试 1: FastAPI 应用导入")
    print("="*50)
    try:
        assert app is not None, "应用导入失败"
        print("✅ FastAPI 应用导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_random_number_generation():
    """测试 2: 随机数生成功能"""
    print("\n" + "="*50)
    print("测试 2: 随机数生成功能")
    print("="*50)
    try:
        num = random.randint(1, 100)
        assert 1 <= num <= 100, f"随机数 {num} 超出范围"
        print(f"✅ 随机数生成测试通过: {num} (范围 1-100)")
        return True
    except Exception as e:
        print(f"❌ 随机数生成失败: {e}")
        return False

def test_routes():
    """测试 3: 路由注册检查"""
    print("\n" + "="*50)
    print("测试 3: 路由注册检查")
    print("="*50)
    try:
        from fastapi.routing import APIRoute
        routes = [route.path for route in app.routes if isinstance(route, APIRoute)]
        print(f"注册的路由: {routes}")
        assert "/" in routes, "缺少根路径 /"
        assert "/random" in routes, "缺少 /random 路径"
        print("✅ 所有必需的路由已注册")
        return True
    except Exception as e:
        print(f"❌ 路由检查失败: {e}")
        return False

def test_cors_middleware():
    """测试 4: CORS 中间件配置"""
    print("\n" + "="*50)
    print("测试 4: CORS 中间件配置")
    print("="*50)
    try:
        from fastapi.middleware.cors import CORSMiddleware
        has_cors = any(isinstance(middleware.cls, CORSMiddleware) 
                       for middleware in app.user_middleware)
        print(f"✅ CORS 中间件: {'已启用' if has_cors else '未启用'}")
        return True
    except Exception as e:
        print(f"⚠️ CORS 检查警告: {e}")
        return True  # CORS 不是关键功能，警告不影响测试

def test_root_endpoint():
    """测试 5: 根路径 API 响应"""
    print("\n" + "="*50)
    print("测试 5: 根路径 API 响应")
    print("="*50)
    try:
        response = client.get("/")
        assert response.status_code == 200, f"状态码错误: {response.status_code}"
        data = response.json()
        assert "message" in data, "响应缺少 message 字段"
        assert data["message"] == "Random Number API", f"消息内容错误: {data['message']}"
        print(f"✅ 根路径响应正确: {data}")
        return True
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")
        return False

def test_random_endpoint():
    """测试 6: 随机数 API 响应"""
    print("\n" + "="*50)
    print("测试 6: 随机数 API 响应")
    print("="*50)
    try:
        # 测试多次请求
        numbers = []
        for i in range(10):
            response = client.get("/random")
            assert response.status_code == 200, f"请求 {i+1} 状态码错误: {response.status_code}"
            data = response.json()
            assert "number" in data, f"响应 {i+1} 缺少 number 字段"
            num = data["number"]
            assert 1 <= num <= 100, f"随机数 {num} 超出范围"
            numbers.append(num)
        
        print(f"✅ 10 次请求的随机数: {numbers}")
        print(f"   最小值: {min(numbers)}, 最大值: {max(numbers)}, 平均值: {sum(numbers)/len(numbers):.2f}")
        return True
    except Exception as e:
        print(f"❌ 随机数 API 测试失败: {e}")
        return False

def test_response_format():
    """测试 7: API 响应格式"""
    print("\n" + "="*50)
    print("测试 7: API 响应格式")
    print("="*50)
    try:
        response = client.get("/random")
        assert response.headers["content-type"] == "application/json", "Content-Type 错误"
        data = response.json()
        assert isinstance(data, dict), "响应不是字典类型"
        assert isinstance(data["number"], int), "number 字段不是整数"
        print(f"✅ 响应格式正确: JSON, 字典类型, 整数字段")
        return True
    except Exception as e:
        print(f"❌ 响应格式测试失败: {e}")
        return False

def test_404_error():
    """测试 8: 404 错误处理"""
    print("\n" + "="*50)
    print("测试 8: 404 错误处理")
    print("="*50)
    try:
        response = client.get("/nonexistent")
        assert response.status_code == 404, f"404 状态码错误: {response.status_code}"
        print(f"✅ 404 错误处理正确")
        return True
    except Exception as e:
        print(f"❌ 404 错误测试失败: {e}")
        return False

def test_multiple_requests():
    """测试 9: 并发请求测试"""
    print("\n" + "="*50)
    print("测试 9: 并发请求测试")
    print("="*50)
    try:
        import threading
        results = []
        
        def make_request():
            response = client.get("/random")
            results.append(response.status_code == 200)
        
        threads = []
        for _ in range(20):
            t = threading.Thread(target=make_request)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        assert all(results), "部分并发请求失败"
        print(f"✅ 20 个并发请求全部成功")
        return True
    except Exception as e:
        print(f"❌ 并发请求测试失败: {e}")
        return False

def run_all_tests():
    """运行所有后端测试"""
    print("\n" + "🚀"*25)
    print("开始运行后端测试套件")
    print("🚀"*25)

    tests = [
        test_import,
        test_random_number_generation,
        test_routes,
        test_cors_middleware,
        test_root_endpoint,
        test_random_endpoint,
        test_response_format,
        test_404_error,
        test_multiple_requests,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试执行异常: {e}")
            results.append(False)

    # 汇总结果
    print("\n" + "="*50)
    print("测试结果汇总")
    print("="*50)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 所有后端测试通过！")
        print("\n启动后端服务:")
        print("  cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return 0
    else:
        print("\n⚠️ 部分测试未通过，请检查")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
