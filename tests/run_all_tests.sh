#!/bin/bash
# 运行所有测试的脚本

echo "=========================================="
echo "  随机数项目 - 自动化测试套件"
echo "=========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试结果统计
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 运行测试函数
run_test() {
    local test_name=$1
    local test_command=$2
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo ""
    echo "=========================================="
    echo "运行: $test_name"
    echo "=========================================="
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ $test_name 通过${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ $test_name 失败${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# 1. 后端测试
cd "$PROJECT_DIR/backend" || exit 1
run_test "后端测试" "python3 ../tests/test_backend.py"

# 2. 前端测试
cd "$PROJECT_DIR/frontend" || exit 1
run_test "前端测试" "python3 ../tests/test_frontend.py"

# 3. 集成测试（可选，需要后端运行）
echo ""
echo "=========================================="
echo "集成测试（需要后端服务运行）"
echo "=========================================="
echo -e "${YELLOW}是否运行集成测试？${NC}"
echo "集成测试需要后端服务正在运行"
echo "启动后端: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
read -p "运行集成测试? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$SCRIPT_DIR" || exit 1
    run_test "集成测试" "python3 test_integration.py"
else
    echo -e "${YELLOW}⏭️  跳过集成测试${NC}"
fi

# 打印汇总结果
cd "$SCRIPT_DIR" || exit 1
echo ""
echo "=========================================="
echo "  测试结果汇总"
echo "=========================================="
echo -e "总测试数: $TOTAL_TESTS"
echo -e "${GREEN}通过: $PASSED_TESTS${NC}"
echo -e "${RED}失败: $FAILED_TESTS${NC}"
echo "=========================================="

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    echo ""
    echo "启动项目:"
    echo "  后端: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo "  前端: cd frontend && python -m http.server 3000"
    exit 0
else
    echo -e "${RED}⚠️  有测试失败，请检查${NC}"
    exit 1
fi
