<template>
  <div id="app">
    <nav class="navbar">
      <div class="logo">🏆 竞赛助手</div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/problems">赛题追踪</router-link>
        <router-link to="/graph">知识图谱</router-link>
        <router-link to="/path">学习路径</router-link>
        <router-link to="/changes">变更报告</router-link>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, "Microsoft YaHei", sans-serif; background: #f5f7fa; }
#app { min-height: 100vh; }

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.logo { font-size: 20px; font-weight: bold; }
.nav-links a {
  color: white;
  text-decoration: none;
  margin-left: 24px;
  padding: 8px 16px;
  border-radius: 6px;
  transition: background 0.3s;
}
.nav-links a:hover { background: rgba(255,255,255,0.2); }
.nav-links a.router-link-active { background: rgba(255,255,255,0.3); }

.main-content { padding: 30px 40px; max-width: 1400px; margin: 0 auto; }
</style>