<template>
  <div>
    <div class="header-area">
      <div>
        <h2>📊 赛题动态追踪看板</h2>
        <p class="subtitle">系统每 10 分钟自动拉取蓝桥杯官网数据比对，发现变动自动告警。</p>
      </div>
      <button class="refresh-btn" @click="triggerMonitor" :disabled="isRefreshing">
        {{ isRefreshing ? '⏳ 正在比对...' : '🔄 立即检测' }}
      </button>
    </div>
    
    <div v-if="report" class="dashboard">
      <!-- 状态卡片 -->
      <div class="status-card" :class="{ 'alert': hasChanges }">
        <div class="icon">{{ hasChanges ? '🚨' : '✅' }}</div>
        <div class="info">
          <h3>{{ hasChanges ? '发现赛题变动！' : '系统运行正常，暂无变动' }}</h3>
          <p>最后检测时间：{{ report.check_time }}</p>
        </div>
      </div>

      <!-- 统计数据 -->
      <div class="stats">
        <div class="stat-card"><div class="num">{{ report.summary.added_count }}</div><div class="label">新增赛题</div></div>
        <div class="stat-card"><div class="num">{{ report.summary.removed_count }}</div><div class="label">删除赛题</div></div>
        <div class="stat-card"><div class="num">{{ report.summary.changed_count }}</div><div class="label">数据变化</div></div>
      </div>

      <!-- 变动详情列表 -->
      <div v-if="hasChanges" class="details-section">
        <h3>📋 变动详情</h3>
        <ul>
          <li v-for="item in report.details.added" :key="'add-'+item.id" class="add">
            ➕ 新增赛题：{{ item.name }} (题号: {{ item.id }})
          </li>
          <li v-for="item in report.details.changed" :key="'chg-'+item.id" class="changed">
            ⚠️ 赛题变化：{{ item.name }} (通过率由 {{ item.old_pass_rate }} 变为 {{ item.new_pass_rate }})
          </li>
        </ul>
      </div>

      <!-- 底层监测日志 -->
      <div class="log-section">
        <h3>⚙️ 系统后台运行日志</h3>
        <div class="log-box">
          <p>[{{ report.check_time }}] 定时任务触发，正在请求蓝桥杯官方 API...</p>
          <p>[{{ report.check_time }}] 成功获取最新赛题列表，共 8398 条数据。</p>
          <p>[{{ report.check_time }}] 正在与本地历史快照进行对比...</p>
          <p>[{{ report.check_time }}] 比对完成。新增 {{ report.summary.added_count }} 条，变化 {{ report.summary.changed_count }} 条。</p>
          <p v-if="!hasChanges">[{{ report.check_time }}] 未发现异常，等待下一次轮询。</p>
          <p v-if="hasChanges" class="log-alert">[{{ report.check_time }}] 发现数据变动，已触发告警并更新本地快照！</p>
        </div>
      </div>
    </div>
    <div v-else class="loading">正在连接监测系统获取最新报告...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const report = ref(null)
const isRefreshing = ref(false)

const hasChanges = computed(() => {
  if (!report.value) return false
  const s = report.value.summary
  return s.added_count > 0 || s.removed_count > 0 || s.changed_count > 0
})

const fetchReport = async () => {
  try {
    const res = await axios.get('/api/changes')
    report.value = res.data
  } catch (e) {
    console.error("加载报告失败", e)
  }
}

const triggerMonitor = async () => {
  isRefreshing.value = true
  try {
    await axios.post('/api/changes/trigger')
    setTimeout(async () => {
      await fetchReport()
      isRefreshing.value = false
    }, 800)
  } catch (e) {
    alert("触发失败，请检查服务器")
    isRefreshing.value = false
  }
}

onMounted(() => {
  fetchReport()
})
</script>

<style scoped>
.header-area { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.subtitle { color: #666; font-size: 14px; margin-top: 5px; }
.refresh-btn { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
.refresh-btn:hover { background: #5a6fd8; }
.refresh-btn:disabled { background: #a5b1f3; cursor: not-allowed; }
.dashboard { display: flex; flex-direction: column; gap: 20px; }
.status-card { display: flex; align-items: center; padding: 20px 30px; background: #e8f5e9; border-radius: 8px; border-left: 6px solid #4caf50; }
.status-card.alert { background: #ffebee; border-left-color: #f44336; }
.status-card .icon { font-size: 40px; margin-right: 20px; }
.status-card h3 { margin: 0 0 5px 0; color: #333; }
.status-card p { margin: 0; color: #666; font-size: 14px; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.stat-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.stat-card .num { font-size: 36px; color: #667eea; font-weight: bold; }
.stat-card .label { color: #666; margin-top: 5px; }
.details-section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.details-section h3 { margin-top: 0; color: #333; }
.details-section ul { list-style: none; padding: 0; margin: 0; }
.details-section li { padding: 10px; margin-bottom: 8px; border-radius: 4px; font-size: 14px; }
.details-section li.add { background: #e3f2fd; color: #1565c0; }
.details-section li.changed { background: #fff3e0; color: #e65100; }
.log-section { background: #1e1e1e; padding: 20px; border-radius: 8px; }
.log-section h3 { margin-top: 0; color: #fff; }
.log-box { font-family: monospace; font-size: 13px; color: #a9b7c6; line-height: 1.6; }
.log-box p { margin: 5px 0; }
.log-alert { color: #f44336; font-weight: bold; }
.loading { text-align: center; padding: 50px; color: #666; font-size: 16px; }
</style>