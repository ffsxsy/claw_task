#!/usr/bin/env python3
"""
前端结构与源码检查（Vue 3 + Vite）。
检查 index.html 与 src/App.vue 是否包含必要元素与 API 调用。
运行方式（项目根目录）：python tests/test_frontend.py
"""
from __future__ import annotations

import os
import sys

# 项目根目录
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND = os.path.join(ROOT, "frontend")
INDEX_HTML = os.path.join(FRONTEND, "index.html")
APP_VUE = os.path.join(FRONTEND, "src", "App.vue")
MAIN_JS = os.path.join(FRONTEND, "src", "main.js")


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_index_html_exists() -> None:
    """frontend/index.html 存在"""
    assert os.path.isfile(INDEX_HTML), f"不存在: {INDEX_HTML}"


def test_index_html_structure() -> None:
    """index.html 包含 DOCTYPE、#app 挂载点、脚本引用"""
    content = read_file(INDEX_HTML)
    assert "<!DOCTYPE html>" in content or "doctype" in content.lower()
    assert "id=\"app\"" in content or "id='app'" in content
    assert "main.js" in content or "src/" in content


def test_app_vue_exists() -> None:
    """src/App.vue 存在"""
    assert os.path.isfile(APP_VUE), f"不存在: {APP_VUE}"


def test_app_vue_has_api_call() -> None:
    """App.vue 中存在 fetch/API 调用与随机数逻辑"""
    content = read_file(APP_VUE)
    assert "fetch" in content or "axios" in content
    assert "random" in content.lower() or "/api" in content or "/random" in content


def test_app_vue_has_buttons_and_display() -> None:
    """App.vue 中有获取随机数、自动刷新与状态展示"""
    content = read_file(APP_VUE)
    assert "fetchRandom" in content or "fetch" in content
    assert "toggleAuto" in content or "setInterval" in content
    assert "number" in content and "status" in content
    assert "button" in content or "@click" in content


def test_app_vue_has_error_handling() -> None:
    """App.vue 中有错误处理（try/catch）"""
    content = read_file(APP_VUE)
    assert "catch" in content or "error" in content.lower()


def test_main_js_mounts_app() -> None:
    """main.js 挂载 Vue 应用"""
    content = read_file(MAIN_JS)
    assert "createApp" in content and "App" in content
    assert "mount" in content and "app" in content.lower()


def run_all() -> int:
    """执行所有前端检查"""
    print("前端结构/源码检查 (Vue 3)")
    print("=" * 50)
    tests = [
        test_index_html_exists,
        test_index_html_structure,
        test_app_vue_exists,
        test_app_vue_has_api_call,
        test_app_vue_has_buttons_and_display,
        test_app_vue_has_error_handling,
        test_main_js_mounts_app,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
        except FileNotFoundError as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
    print("=" * 50)
    if failed == 0:
        print("🎉 前端检查全部通过")
        return 0
    print(f"⚠️ {failed} 项失败")
    return 1


if __name__ == "__main__":
    sys.exit(run_all())
