#!/bin/bash
# 随机数实时显示项目 - 快速启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_info "项目目录: $SCRIPT_DIR"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python 3，请先安装"
    exit 1
fi
print_success "Python 3 已安装"
echo ""

# 检查后端依赖
print_info "检查后端依赖..."
cd backend
if [ ! -d ".venv" ]; then
    print_warning "虚拟环境不存在，正在创建..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -r requirements.txt
    print_success "虚拟环境创建完成"
else
    print_success "虚拟环境已存在"
fi

# 激活虚拟环境并检查依赖
source .venv/bin/activate
python3 -c "import fastapi" 2>/dev/null || {
    print_warning "安装依赖中..."
    pip install -q -r requirements.txt
}
print_success "后端依赖检查完成"
cd ..
echo ""

# 运行测试
print_info "运行测试..."
cd backend && python3 test_backend.py
cd ../frontend && python3 test_frontend.py
cd ..
echo ""

# 启动服务
print_info "启动服务..."
echo ""

# 创建日志目录
mkdir -p logs

# 启动后端
print_info "启动后端服务 (端口 8000)..."
cd backend
source .venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# 等待后端启动
sleep 2

# 检查后端是否启动成功
if ps -p $BACKEND_PID > /dev/null; then
    print_success "后端服务启动成功 (PID: $BACKEND_PID)"
else
    print_error "后端服务启动失败，查看日志: logs/backend.log"
    exit 1
fi

# 启动前端
print_info "启动前端服务 (端口 3000)..."
cd frontend
nohup python3 -m http.server 3000 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# 检查前端是否启动成功
sleep 1
if ps -p $FRONTEND_PID > /dev/null; then
    print_success "前端服务启动成功 (PID: $FRONTEND_PID)"
else
    print_error "前端服务启动失败，查看日志: logs/frontend.log"
    exit 1
fi

echo ""
print_success "======================================"
print_success "🎉 服务启动完成！"
print_success "======================================"
echo ""
print_info "📍 访问地址:"
echo "   - 前端: http://localhost:3000"
echo "   - 后端: http://localhost:8000"
echo "   - API 文档: http://localhost:8000/docs"
echo ""
print_info "📋 进程信息:"
echo "   - 后端 PID: $BACKEND_PID"
echo "   - 前端 PID: $FRONTEND_PID"
echo ""
print_info "📝 日志文件:"
echo "   - 后端: logs/backend.log"
echo "   - 前端: logs/frontend.log"
echo ""
print_info "🛑 停止服务:"
echo "   运行: ./stop.sh"
echo ""
print_info "💡 提示: 按 Ctrl+C 停止监控，服务将继续运行"
echo ""

# 监控日志
print_info "监控日志 (按 Ctrl+C 退出监控)..."
echo ""
tail -f logs/backend.log logs/frontend.log
