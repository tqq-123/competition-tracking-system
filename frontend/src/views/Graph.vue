<template>
  <div>
    <h2>🕸️ 知识图谱</h2>
    <p class="tip">共 {{ nodes.length }} 个节点，{{ relations.length }} 条关系</p>
    <div class="graph-container">
      <div class="section">
        <h3>节点</h3>
        <div v-for="(n, i) in nodes" :key="i" class="node" :class="n.type">
          <span class="type">{{ n.type }}</span>
          <span class="name">{{ n.name }}</span>
        </div>
      </div>
      <div class="section">
        <h3>关系</h3>
        <div v-for="(r, i) in relations" :key="i" class="relation">
          {{ r.source }} <span class="rel-type">—[{{ r.relation }}]→</span> {{ r.target }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const nodes = ref([])
const relations = ref([])

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/graph')
  nodes.value = res.data.nodes
  relations.value = res.data.relations
})
</script>

<style scoped>
.graph-container { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
.section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.section h3 { margin-bottom: 16px; color: #667eea; }
.node { padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; background: #f0f2ff; display: flex; justify-content: space-between; }
.node.Competition { background: #ffe8e8; }
.node.Problem { background: #e8f4ff; }
.node.Knowledge { background: #e8ffe8; }
.node.Skill { background: #fff8e8; }
.type { font-size: 12px; color: #666; }
.relation { padding: 10px 14px; margin-bottom: 8px; background: #fafafa; border-radius: 6px; font-size: 14px; }
.rel-type { color: #764ba2; font-weight: bold; }
</style>