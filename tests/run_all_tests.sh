#!/bin/bash
# 在项目根目录或 tests 目录执行：bash tests/run_all_tests.sh 或 cd tests && bash run_all_tests.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "  Claw Task 自动化测试"
echo "=========================================="
echo ""

PASS=0
FAIL=0

run_one() {
    if python3 "$SCRIPT_DIR/$1"; then
        PASS=$((PASS + 1))
        return 0
    else
        FAIL=$((FAIL + 1))
        return 1
    fi
}

echo "1. 后端测试 (TestClient)"
run_one "test_backend.py" || true
echo ""

echo "2. 前端结构/源码检查"
run_one "test_frontend.py" || true
echo ""

echo "3. 集成测试（需后端已启动）"
echo "   若未启动: cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
read -p "   是否运行集成测试? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_one "test_integration.py" || true
else
    echo "   跳过集成测试"
fi
echo ""

echo "=========================================="
echo "  结果: 通过 $PASS, 失败 $FAIL"
echo "=========================================="
if [ $FAIL -eq 0 ]; then
    echo "启动: ./start.sh  或 后端: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000  前端: cd frontend && pnpm dev"
    exit 0
else
    exit 1
fi
