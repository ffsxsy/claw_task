#!/bin/bash

# Claw Task 项目启动脚本

echo "🚀 启动 Claw Task 项目..."

# 检查并启动后端
if [ -d "backend/.venv" ]; then
    echo "📦 启动后端服务..."
    cd backend
    source .venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
else
    echo "⚠️  后端虚拟环境不存在，请先运行: cd backend && uv venv && uv sync"
fi

# 检查并启动前端
if [ -d "frontend/node_modules" ]; then
    echo "🎨 启动前端服务..."
    cd frontend
    pnpm dev &
    FRONTEND_PID=$!
    cd ..
    echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
else
    echo "⚠️  前端依赖未安装，请先运行: cd frontend && pnpm install"
fi

echo ""
echo "📌 服务地址:"
echo "   - 前端: http://localhost:5173"
echo "   - 后端: http://localhost:8000"
echo "   - API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待所有后台进程
wait
