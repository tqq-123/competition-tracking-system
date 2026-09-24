<template>
  <div>
    <h2>📋 赛题追踪</h2>
    <p class="tip">数据来源：蓝桥杯官方题库（共 {{ count }} 道赛题）</p>
    <div v-if="loading">加载中...</div>
    <table v-else class="problem-table">
      <thead>
        <tr><th>题号</th><th>题目</th><th>标签</th><th>通过率</th><th>作答人数</th></tr>
      </thead>
      <tbody>
        <tr v-for="p in problems" :key="p.id">
          <td>{{ p.id }}</td>
          <td>{{ p.name }}</td>
          <td>{{ (p.tags || []).join(' / ') }}</td>
          <td>{{ (p.statistics?.pass_rate * 100).toFixed(1) }}%</td>
          <td>{{ p.statistics?.students_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const problems = ref([])
const count = ref(0)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/problems')
    problems.value = res.data.problems
    count.value = res.data.count
  } catch (e) {
    alert('加载失败：' + e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
h2 { margin-bottom: 8px; }
.tip { color: #666; margin-bottom: 20px; }
.problem-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.problem-table th, .problem-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
.problem-table th { background: #667eea; color: white; }
.problem-table tr:hover { background: #f8f9ff; }
</style>