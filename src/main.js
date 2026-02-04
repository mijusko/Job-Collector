import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Jobs from './views/Jobs.vue'
import JobDetail from './views/JobDetail.vue'
import './style.css'

const routes = [
  { path: '/', component: Home },
  { path: '/jobs', component: Jobs },
  { path: '/job/:id', component: JobDetail, name: 'job-detail' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
