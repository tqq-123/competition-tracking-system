<template>
  <div>
    <h2>📊 变更报告</h2>
    <div v-if="report" class="report">
      <div class="meta">
        <p><strong>检查时间：</strong>{{ report.check_time }}</p>
        <p><strong>搜索关键词：</strong>{{ report.search }}</p>
      </div>
      <div class="stats">
        <div class="stat-card"><div class="num">{{ report.summary.added_count }}</div><div class="label">新增</div></div>
        <div class="stat-card"><div class="num">{{ report.summary.removed_count }}</div><div class="label">删除</div></div>
        <div class="stat-card"><div class="num">{{ report.summary.changed_count }}</div><div class="label">变化</div></div>
      </div>
      <p v-if="report.summary.added_count === 0 && report.summary.removed_count === 0 && report.summary.changed_count === 0" class="empty">
        ✅ 本次检查未发现赛题变化
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const report = ref(null)

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/changes')
  report.value = res.data
})
</script>

<style scoped>
.report { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.meta { margin-bottom: 24px; color: #666; }
.meta p { margin: 6px 0; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }
.stat-card { background: #f8f9ff; padding: 24px; border-radius: 8px; text-align: center; }
.stat-card .num { font-size: 36px; color: #667eea; font-weight: bold; }
.stat-card .label { color: #666; margin-top: 8px; }
.empty { text-align: center; color: #52c41a; padding: 20px; font-size: 16px; }
</style>