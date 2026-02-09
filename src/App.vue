<template>
  <div class="app-container" :class="{ 'dark-theme': isDark }">
    <nav>
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/jobs">Pretraga Poslova</router-link>
      </div>
      <button @click="toggleTheme" class="theme-toggle" :title="isDark ? 'Svetla tema' : 'Tamna tema'">
        <span v-if="isDark">☀️</span>
        <span v-else>🌙</span>
      </button>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  document.body.classList.toggle('dark-body', isDark.value)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.body.classList.add('dark-body')
  }
})
</script>

<style>
:root {
  --bg-color: #f8f9fa;
  --card-bg: #ffffff;
  --text-primary: #333333;
  --text-secondary: #666666;
  --border-color: #eeeeee;
  --accent-color: #1a73e8;
  --hover-bg: #f0f4f8;
}

.dark-theme {
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --text-primary: #e0e0e0;
  --text-secondary: #aaaaaa;
  --border-color: #333333;
  --accent-color: #4dabf7;
  --hover-bg: #2c2c2c;
}

body {
  margin: 0;
  background-color: var(--bg-color);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

body.dark-body {
  background-color: #121212;
}

.app-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.nav-links {
  display: flex;
  gap: 20px;
}

nav a {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 600;
  transition: color 0.2s;
}

nav a:hover {
  color: var(--accent-color);
}

nav a.router-link-active {
  color: var(--accent-color);
  position: relative;
}

nav a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -16px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: var(--accent-color);
}

.theme-toggle {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s, background-color 0.2s;
}

.theme-toggle:hover {
  transform: scale(1.1);
  background-color: var(--hover-bg);
}
</style>
