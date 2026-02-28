#!/bin/bash

echo "🛑 停止 Claw Task 项目..."

# 停止后端
pkill -f "uvicorn main:app" && echo "✅ 后端服务已停止" || echo "⚠️  后端服务未运行"

# 停止前端
pkill -f "vite" && echo "✅ 前端服务已停止" || echo "⚠️  前端服务未运行"

echo "👋 所有服务已停止"
