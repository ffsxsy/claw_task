<template>
  <div class="container">
    <h1>🎲 随机数生成器</h1>
    <div class="number">{{ number }}</div>
    <button @click="fetchRandom" class="btn-primary">获取随机数</button>
    <button @click="toggleAuto" :class="['btn-toggle', { active: isAutoRunning }]">
      自动刷新: {{ isAutoRunning ? '开' : '关' }}
    </button>
    <div class="status">{{ status }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const number = ref('--')
const status = ref('点击按钮获取随机数')
const isAutoRunning = ref(false)
let autoInterval = null

const API_URL = '/api/random'

const fetchRandom = async () => {
  try {
    status.value = '请求中...'
    const response = await fetch(API_URL)
    const data = await response.json()
    number.value = data.number
    status.value = `获取成功: ${data.number}`
  } catch (error) {
    status.value = '错误: ' + error.message
  }
}

const toggleAuto = () => {
  if (autoInterval) {
    clearInterval(autoInterval)
    autoInterval = null
    isAutoRunning.value = false
    status.value = '自动刷新已停止'
  } else {
    fetchRandom()
    autoInterval = setInterval(fetchRandom, 1000)
    isAutoRunning.value = true
    status.value = '自动刷新中 (每秒更新)'
  }
}
</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
  padding: 20px;
}

h1 {
  color: #333;
}

.number {
  font-size: 80px;
  font-weight: bold;
  color: #4CAF50;
  margin: 30px 0;
}

button {
  font-size: 18px;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 10px;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover {
  background-color: #1976D2;
}

.btn-toggle {
  background-color: #9E9E9E;
  color: white;
}

.btn-toggle:hover {
  background-color: #757575;
}

.btn-toggle.active {
  background-color: #FF9800;
}

.btn-toggle.active:hover {
  background-color: #F57C00;
}

.status {
  margin-top: 20px;
  color: #666;
}
</style>
