import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Home from './views/Home.vue'
import Problems from './views/Problems.vue'
import Graph from './views/Graph.vue'
import Path from './views/Path.vue'
import Changes from './views/Changes.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/problems', component: Problems },
    { path: '/graph', component: Graph },
    { path: '/path', component: Path },
    { path: '/changes', component: Changes }
  ]
})

createApp(App).use(router).mount('#app')