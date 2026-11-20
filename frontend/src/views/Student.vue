<template>
  <div>
    <h2>🎓 学生备赛中心（能力画像与学习路径）</h2>
    
    <div class="profile-card">
      <h3>第一步：完善你的能力画像</h3>
      <p>请选择你已经掌握的知识点（系统将为你跳过这些基础）：</p>
      <div class="checkbox-group" v-if="allKnowledgePoints.length > 0">
        <label v-for="kp in allKnowledgePoints" :key="kp">
          <input type="checkbox" :value="kp" v-model="knownKnowledge"> {{ kp }}
        </label>
      </div>
      <p v-else>正在加载知识点...</p>
      
      <h3>第二步：选择你的目标赛题</h3>
      <select v-model="selectedProblemId">
        <option v-for="p in availableProblems" :key="p.id" :value="String(p.id)">
          {{ p.id }} - {{ p.name || '赛题 ' + p.id }}
        </option>
      </select>
      
      <button class="generate-btn" @click="generatePath" :disabled="loading">
        {{ loading ? '🤖 大模型正在为你规划路径...' : '🚀 生成我的专属备赛路径' }}
      </button>
    </div>

    <div v-if="result" class="result-card">
      <h3>📋 专属学习路径（动态生成）</h3>
      <p class="meta">目标赛题：{{ result.problem_title }} | 已掌握：{{ knownKnowledge.join(', ') || '无' }}</p>
      
      <!-- 新增：AI 导师建议 -->
      <div class="ai-tip">
        <strong>🤖 AI 导师建议：</strong> {{ result.ai_advice }}
      </div>
      
      <div class="timeline">
        <div v-for="(step, index) in result.learning_path" :key="index" class="step">
          <div class="step-icon">{{ index + 1 }}</div>
          <div class="step-content">
            <h4>{{ step.knowledge }}</h4>
            <p><strong>前置要求：</strong>{{ step.prerequisites.join(', ') || '无（可直接学习）' }}</p>
            <p class="status">当前状态：{{ step.status }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const allKnowledgePoints = ref([])
const availableProblems = ref([])
const knownKnowledge = ref([])
const selectedProblemId = ref('')
const result = ref(null)
const loading = ref(false)

// 页面加载时，同时获取图谱知识点和赛题列表
onMounted(async () => {
  try {
    // 1. 获取知识点用于画像
    const res = await axios.get('/api/graph')
    const kps = new Set()
    res.data.nodes.forEach(node => {
      if (node.type === 'Knowledge') kps.add(node.name)
    })
    allKnowledgePoints.value = Array.from(kps)
    
    // 2. 动态获取赛题列表（取前 100 道）
    const probRes = await axios.get('/api/problems')
    availableProblems.value = probRes.data.problems.slice(0, 100)
    
    // 3. 默认选中第一道题
    if (availableProblems.value.length > 0) {
      selectedProblemId.value = String(availableProblems.value[0].id)
    }
  } catch (e) {
    console.error("加载数据失败", e)
  }
})

const generatePath = async () => {
  if (!selectedProblemId.value) {
    alert("请先选择目标赛题");
    return;
  }
  loading.value = true
  try {
    const res = await axios.post('/api/path/generate', {
      problem_id: parseInt(selectedProblemId.value),
      known_knowledge: knownKnowledge.value
    })
    result.value = res.data
  } catch (e) {
    alert("生成失败：" + e.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-card, .result-card { background: white; padding: 24px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
h3 { margin-top: 0; color: #333; }
.checkbox-group { display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0; }
.checkbox-group label { background: #f0f2ff; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 14px; }
select { padding: 10px; border-radius: 6px; border: 1px solid #ccc; width: 300px; margin: 15px 0; }
.generate-btn { display: block; background: #667eea; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 20px; }
.generate-btn:disabled { background: #a5b1f3; }

/* 新增的 AI 建议样式 */
.ai-tip { 
  background: #e3f2fd; 
  color: #1565c0; 
  padding: 15px; 
  border-radius: 8px; 
  margin: 15px 0; 
  border-left: 4px solid #1976d2; 
  font-size: 15px; 
  line-height: 1.6;
}

.timeline { margin-top: 20px; border-left: 3px solid #667eea; padding-left: 20px; }
.step { display: flex; margin-bottom: 20px; position: relative; }
.step-icon { width: 30px; height: 30px; background: #667eea; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; position: absolute; left: -36px; top: 0; }
.step-content { background: #f9f9f9; padding: 15px; border-radius: 8px; flex: 1; }
.step-content h4 { margin: 0 0 8px 0; color: #333; }
.step-content p { margin: 5px 0; font-size: 14px; color: #666; }
.status { color: #f57c00; font-weight: bold; }
</style>