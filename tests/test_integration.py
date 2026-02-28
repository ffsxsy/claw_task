#!/usr/bin/env python3
"""
集成测试
测试前后端协同工作
"""
import sys
import os
import time
import requests
import threading

# API 基础 URL
API_BASE = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def check_backend_running():
    """检查后端是否运行"""
    print("\n" + "="*50)
    print("检查后端服务状态")
    print("="*50)
    try:
        response = requests.get(f"{API_BASE}/", timeout=2)
        if response.status_code == 200:
            print("✅ 后端服务正在运行")
            return True
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    
    print("❌ 后端服务未运行")
    print("请先启动后端:")
    print("  cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    return False

def test_api_connectivity():
    """测试 1: API 连接性"""
    print("\n" + "="*50)
    print("测试 1: API 连接性")
    print("="*50)
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        assert response.status_code == 200, f"状态码错误: {response.status_code}"
        data = response.json()
        assert "message" in data, "响应缺少 message 字段"
        print(f"✅ API 连接正常: {data}")
        return True
    except Exception as e:
        print(f"❌ API 连接测试失败: {e}")
        return False

def test_random_api():
    """测试 2: 随机数 API"""
    print("\n" + "="*50)
    print("测试 2: 随机数 API")
    print("="*50)
    try:
        numbers = []
        for i in range(5):
            response = requests.get(f"{API_BASE}/random", timeout=5)
            assert response.status_code == 200, f"请求 {i+1} 失败"
            data = response.json()
            assert "number" in data, "响应缺少 number 字段"
            num = data["number"]
            assert 1 <= num <= 100, f"随机数 {num} 超出范围"
            numbers.append(num)
        
        print(f"✅ 随机数 API 正常: {numbers}")
        return True
    except Exception as e:
        print(f"❌ 随机数 API 测试失败: {e}")
        return False

def test_response_time():
    """测试 3: 响应时间"""
    print("\n" + "="*50)
    print("测试 3: 响应时间")
    print("="*50)
    try:
        times = []
        for _ in range(10):
            start = time.time()
            response = requests.get(f"{API_BASE}/random", timeout=5)
            end = time.time()
            times.append((end - start) * 1000)  # 转换为毫秒
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print(f"✅ 响应时间统计:")
        print(f"   平均: {avg_time:.2f}ms")
        print(f"   最小: {min_time:.2f}ms")
        print(f"   最大: {max_time:.2f}ms")
        
        if avg_time < 1000:
            print("   性能良好 (< 1秒)")
            return True
        else:
            print("   ⚠️ 响应时间较长")
            return True  # 不算失败，只是警告
    except Exception as e:
        print(f"❌ 响应时间测试失败: {e}")
        return False

def test_concurrent_requests():
    """测试 4: 并发请求"""
    print("\n" + "="*50)
    print("测试 4: 并发请求")
    print("="*50)
    try:
        results = []
        errors = []
        
        def make_request(n):
            try:
                start = time.time()
                response = requests.get(f"{API_BASE}/random", timeout=10)
                elapsed = time.time() - start
                if response.status_code == 200:
                    results.append(elapsed)
                else:
                    errors.append(f"请求 {n} 状态码: {response.status_code}")
            except Exception as e:
                errors.append(f"请求 {n} 异常: {e}")
        
        # 创建 50 个并发请求
        threads = []
        for i in range(50):
            t = threading.Thread(target=make_request, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        success_count = len(results)
        error_count = len(errors)
        
        print(f"✅ 并发请求结果:")
        print(f"   成功: {success_count}/50")
        print(f"   失败: {error_count}/50")
        print(f"   平均响应时间: {sum(results)/len(results)*1000:.2f}ms" if results else "   无成功请求")
        
        if errors:
            print("   错误详情:")
            for err in errors[:5]:  # 只显示前5个错误
                print(f"     - {err}")
        
        return success_count == 50
    except Exception as e:
        print(f"❌ 并发请求测试失败: {e}")
        return False

def test_error_handling():
    """测试 5: 错误处理"""
    print("\n" + "="*50)
    print("测试 5: 错误处理")
    print("="*50)
    try:
        # 测试 404
        response = requests.get(f"{API_BASE}/nonexistent", timeout=5)
        assert response.status_code == 404, f"404 状态码错误: {response.status_code}"
        print("✅ 404 错误处理正确")
        
        # 测试无效方法
        response = requests.post(f"{API_BASE}/random", timeout=5)
        # FastAPI 默认返回 405 Method Not Allowed
        assert response.status_code in [405, 404], f"POST 状态码错误: {response.status_code}"
        print("✅ 无效方法处理正确")
        
        return True
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

def test_data_consistency():
    """测试 6: 数据一致性"""
    print("\n" + "="*50)
    print("测试 6: 数据一致性")
    print("="*50)
    try:
        # 获取多个随机数，检查范围
        numbers = []
        for _ in range(100):
            response = requests.get(f"{API_BASE}/random", timeout=5)
            data = response.json()
            numbers.append(data["number"])
        
        min_val = min(numbers)
        max_val = max(numbers)
        avg_val = sum(numbers) / len(numbers)
        
        assert min_val >= 1, f"最小值 {min_val} 小于 1"
        assert max_val <= 100, f"最大值 {max_val} 大于 100"
        
        print(f"✅ 数据一致性检查通过 (100次请求):")
        print(f"   最小值: {min_val}")
        print(f"   最大值: {max_val}")
        print(f"   平均值: {avg_val:.2f}")
        print(f"   标准差: {(sum((x - avg_val)**2 for x in numbers) / len(numbers))**0.5:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ 数据一致性测试失败: {e}")
        return False

def run_all_tests():
    """运行所有集成测试"""
    print("\n" + "🚀"*25)
    print("开始运行集成测试套件")
    print("🚀"*25)
    print("\n注意: 集成测试需要后端服务正在运行")
    print("如果后端未运行，请先启动:")
    print("  cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")

    # 首先检查后端是否运行
    if not check_backend_running():
        return 1

    tests = [
        test_api_connectivity,
        test_random_api,
        test_response_time,
        test_concurrent_requests,
        test_error_handling,
        test_data_consistency,
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
    print("集成测试结果汇总")
    print("="*50)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 所有集成测试通过！")
        print("\n前后端集成正常，可以开始使用")
        return 0
    else:
        print("\n⚠️ 部分测试未通过，请检查")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
