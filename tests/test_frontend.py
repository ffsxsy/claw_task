#!/usr/bin/env python3
"""
前端 HTML 自动化测试
测试前端 HTML 文件的结构和功能
"""
import re
import sys
import os

def test_frontend():
    """运行所有前端测试"""
    html_file = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')

    print("\n" + "🚀"*25)
    print("开始运行前端测试套件")
    print("🚀"*25)

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 找不到文件: {html_file}")
        return 1

    tests = []

    # 测试 1: HTML 文档结构
    print("\n" + "="*50)
    print("测试 1: HTML 文档结构")
    print("="*50)
    has_doctype = '<!DOCTYPE html>' in content
    has_html = '<html' in content
    has_head = '<head>' in content
    has_body = '<body>' in content
    result = all([has_doctype, has_html, has_head, has_body])
    tests.append(("HTML 文档结构", result))
    if result:
        print("✅ HTML 文档结构完整")
    else:
        print("❌ HTML 文档结构不完整")

    # 测试 2: API URL 配置
    print("\n" + "="*50)
    print("测试 2: API URL 配置")
    print("="*50)
    api_urls = re.findall(r'http[s]?://[^\s"\']+', content)
    has_api_url = any("localhost:8000/random" in url for url in api_urls)
    tests.append(("API URL 配置", has_api_url))
    if has_api_url:
        print(f"✅ API URL 已配置: {api_urls}")
    else:
        print(f"❌ 未找到正确的 API URL")

    # 测试 3: JavaScript 函数定义
    print("\n" + "="*50)
    print("测试 3: JavaScript 函数定义")
    print("="*50)
    functions = re.findall(r'(?:function|const|let|var)\s+(\w+)\s*\(', content)
    required_functions = ['fetchRandom', 'toggleAuto']
    has_functions = all(func in functions for func in required_functions)
    tests.append(("JavaScript 函数定义", has_functions))
    if has_functions:
        print(f"✅ 所需函数已定义: {functions}")
    else:
        print(f"❌ 缺少函数: {set(required_functions) - set(functions)}")

    # 测试 4: 自动刷新功能
    print("\n" + "="*50)
    print("测试 4: 自动刷新功能")
    print("="*50)
    has_toggle_auto = 'toggleAuto' in content
    has_interval = 'setInterval' in content or 'clearInterval' in content
    has_auto_refresh = has_toggle_auto and has_interval
    tests.append(("自动刷新功能", has_auto_refresh))
    if has_auto_refresh:
        print("✅ 自动刷新功能已实现")
    else:
        print("❌ 自动刷新功能不完整")

    # 测试 5: UI 元素检查
    print("\n" + "="*50)
    print("测试 5: UI 元素检查")
    print("="*50)
    has_number_display = bool(re.search(r'id=["\']number["\']', content))
    has_status_display = 'status' in content.lower()
    button_count = len(re.findall(r'<button', content))
    has_enough_buttons = button_count >= 2
    ui_elements_ok = all([has_number_display, has_status_display, has_enough_buttons])
    tests.append(("UI 元素", ui_elements_ok))
    if ui_elements_ok:
        print(f"✅ UI 元素完整 (按钮: {button_count}个)")
    else:
        print(f"❌ UI 元素不完整 (按钮: {button_count}个)")

    # 测试 6: CSS 样式
    print("\n" + "="*50)
    print("测试 6: CSS 样式")
    print("="*50)
    has_style = '<style>' in content or 'stylesheet' in content
    has_responsive = '@media' in content or 'viewport' in content
    css_ok = has_style
    tests.append(("CSS 样式", css_ok))
    if css_ok:
        print(f"✅ CSS 样式已定义 (响应式: {'是' if has_responsive else '否'})")
    else:
        print("❌ 缺少 CSS 样式")

    # 测试 7: 错误处理
    print("\n" + "="*50)
    print("测试 7: 错误处理")
    print("="*50)
    has_error_handling = 'catch' in content or 'error' in content.lower()
    tests.append(("错误处理", has_error_handling))
    if has_error_handling:
        print("✅ 错误处理已实现")
    else:
        print("⚠️ 未找到错误处理代码")

    # 测试 8: 事件监听器
    print("\n" + "="*50)
    print("测试 8: 事件监听器")
    print("="*50)
    has_event_listeners = 'addEventListener' in content or 'onclick' in content
    tests.append(("事件监听器", has_event_listeners))
    if has_event_listeners:
        print("✅ 事件监听器已配置")
    else:
        print("❌ 缺少事件监听器")

    # 测试 9: 状态管理
    print("\n" + "="*50)
    print("测试 9: 状态管理")
    print("="*50)
    has_state_var = 'let isAuto' in content or 'var isAuto' in content or 'const isAuto' in content
    tests.append(("状态管理", has_state_var))
    if has_state_var:
        print("✅ 状态变量已定义")
    else:
        print("⚠️ 未找到状态变量")

    # 测试 10: 页面加载初始化
    print("\n" + "="*50)
    print("测试 10: 页面加载初始化")
    print("="*50)
    has_onload = 'onload' in content or 'DOMContentLoaded' in content
    tests.append(("页面加载初始化", has_onload))
    if has_onload:
        print("✅ 页面加载初始化已配置")
    else:
        print("⚠️ 未找到页面加载初始化")

    # 打印汇总结果
    print("\n" + "="*50)
    print("测试结果汇总")
    print("="*50)
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print("="*50)
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 所有前端测试通过！")
        print("\n启动前端服务:")
        print("  cd frontend && python -m http.server 3000")
        return 0
    else:
        print("\n⚠️ 部分测试未通过，请检查")
        return 1

if __name__ == "__main__":
    sys.exit(test_frontend())
