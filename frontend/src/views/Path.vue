<template>
  <div>
    <h2>🎯 学习路径生成</h2>
    <div class="input-area">
      <label>已知知识点（用逗号分隔）：</label>
      <input v-model="knownStr" placeholder="例如：字符串遍历" />
      <button @click="generate">生成路径</button>
    </div>
    <div v-if="result" class="result">
      <h3>赛题：{{ result.problem_title }}</h3>
      <p>共 {{ result.total_steps }} 步学习路径</p>
      <div v-for="(s, i) in result.learning_path" :key="i" class="step">
        <span class="step-num">{{ i + 1 }}</span>
        <span class="kp">{{ s.knowledge }}</span>
        <span class="status">{{ s.status }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const knownStr = ref('字符串遍历')
const result = ref(null)

async function generate() {
  const known = knownStr.value.split(/[,，]/).map(s => s.trim()).filter(Boolean)
  const res = await axios.post('http://localhost:8000/api/path/generate', {
    problem_id: 504,
    known_knowledge: known
  })
  result.value = res.data
}
</script>

<style scoped>
.input-area { background: white; padding: 24px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.input-area label { display: block; margin-bottom: 10px; color: #666; }
.input-area input { width: 60%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.input-area button { margin-left: 12px; padding: 10px 24px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
.input-area button:hover { background: #5a6fd8; }
.result { background: white; padding: 24px; border-radius: 8px; }
.result h3 { color: #667eea; margin-bottom: 8px; }
.step { display: flex; align-items: center; padding: 14px; margin: 10px 0; background: #f8f9ff; border-radius: 6px; border-left: 4px solid #667eea; }
.step-num { display: inline-flex; width: 28px; height: 28px; background: #667eea; color: white; border-radius: 50%; align-items: center; justify-content: center; font-size: 14px; margin-right: 16px; }
.kp { flex: 1; font-weight: 500; }
.status { color: #888; font-size: 14px; }
</style>