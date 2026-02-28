from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(
    title="Random Number API",
    description="随机数生成器 API",
    version="0.1.0"
)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Random Number API",
        "version": "0.1.0",
        "endpoints": {
            "random": "/random - 获取随机数 (1-100)"
        }
    }

@app.get("/random")
def get_random_number():
    """返回一个随机数 (1-100)"""
    return {
        "number": random.randint(1, 100),
        "timestamp": random.random()  # 模拟时间戳
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
