#!/usr/bin/env python3
"""测试前端 HTML 文件"""
import re
import sys

def test_frontend():
    html_file = "index.html"

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 找不到文件: {html_file}")
        return False

    tests = []

    # 测试 1: 检查 HTML 结构
    if '<!DOCTYPE html>' in content:
        tests.append(("HTML 文档类型", True))
    else:
        tests.append(("HTML 文档类型", False))

    # 测试 2: 检查 API URL
    if "http://localhost:8000/random" in content:
        tests.append(("API URL 配置", True))
    else:
        tests.append(("API URL 配置", False))

    # 测试 3: 检查 fetchRandom 函数
    if "function fetchRandom()" in content or "const fetchRandom" in content:
        tests.append(("fetchRandom 函数", True))
    else:
        tests.append(("fetchRandom 函数", False))

    # 测试 4: 检查自动刷新功能
    if "toggleAuto" in content:
        tests.append(("自动刷新功能", True))
    else:
        tests.append(("自动刷新功能", False))

    # 测试 5: 检查状态显示
    if "status" in content.lower():
        tests.append(("状态显示元素", True))
    else:
        tests.append(("状态显示元素", False))

    # 测试 6: 检查按钮
    button_count = len(re.findall(r'<button', content))
    if button_count >= 2:
        tests.append((f"按钮元素 ({button_count}个)", True))
    else:
        tests.append((f"按钮元素 ({button_count}个)", False))

    # 测试 7: 检查数字显示
    if 'number' in content and ('id="number"' in content or "id='number'" in content):
        tests.append(("数字显示元素", True))
    else:
        tests.append(("数字显示元素", False))

    # 打印结果
    print("前端测试结果:")
    print("=" * 40)
    passed = 0
    for name, result in tests:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if result:
            passed += 1

    print("=" * 40)
    print(f"通过: {passed}/{len(tests)}")

    if passed == len(tests):
        print("\n🎉 所有前端测试通过！")
        print("启动命令: python -m http.server 3000")
        return True
    else:
        print("\n⚠️ 部分测试未通过，请检查")
        return False

if __name__ == "__main__":
    success = test_frontend()
    sys.exit(0 if success else 1)
