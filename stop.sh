#!/bin/bash
# 停止服务脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 读取 PID 文件
BACKEND_PID_FILE="logs/backend.pid"
FRONTEND_PID_FILE="logs/frontend.pid"

# 停止进程的函数
stop_process() {
    local pid_file=$1
    local name=$2

    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}⏹️  停止 $name (PID: $pid)...${NC}"
            kill $pid
            # 等待进程结束
            for i in {1..10}; do
                if ! ps -p $pid > /dev/null 2>&1; then
                    echo -e "${GREEN}✅ $name 已停止${NC}"
                    break
                fi
                sleep 1
            done
            # 如果还没停止，强制杀死
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid
                echo -e "${GREEN}✅ $name 已强制停止${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  $name 进程不存在${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}⚠️  未找到 $name 的 PID 文件${NC}"
    fi
}

echo ""
echo -e "${BLUE}🛑 停止服务${NC}"
echo ""

# 停止后端
stop_process "$BACKEND_PID_FILE" "后端服务"

# 停止前端
stop_process "$FRONTEND_PID_FILE" "前端服务"

echo ""
echo -e "${GREEN}✅ 所有服务已停止${NC}"
echo ""

# 显示日志位置
if [ -d "logs" ]; then
    echo -e "${BLUE}📝 日志文件:${NC}"
    ls -lh logs/
fi
