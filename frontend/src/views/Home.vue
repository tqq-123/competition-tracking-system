<template>
  <div class="home">
    <h1>竞赛赛题追踪与学习路径生成系统</h1>
    <p class="subtitle">基于 OpenClaw 多智能体 + 知识图谱 + 大模型的竞赛服务平台</p>
    <div class="cards">
      <div class="card" @click="$router.push('/problems')">
        <h3>📋 赛题追踪</h3>
        <p>实时追踪蓝桥杯等竞赛赛题</p>
      </div>
      <div class="card" @click="$router.push('/graph')">
        <h3>🕸️ 知识图谱</h3>
        <p>竞赛-赛题-知识点语义关联</p>
      </div>
      <div class="card" @click="$router.push('/path')">
        <h3>🎯 学习路径</h3>
        <p>个性化备赛路径动态生成</p>
      </div>
      <div class="card" @click="$router.push('/changes')">
        <h3>📊 变更报告</h3>
        <p>赛题更新实时监测</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home { text-align: center; padding: 40px 20px; }
h1 { font-size: 32px; color: #333; margin-bottom: 12px; }
.subtitle { color: #666; margin-bottom: 40px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto; }
.card { background: white; padding: 30px 20px; border-radius: 12px; cursor: pointer; transition: all 0.3s; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(102,126,234,0.3); }
.card h3 { color: #667eea; margin-bottom: 10px; font-size: 18px; }
.card p { color: #888; font-size: 14px; }
</style>