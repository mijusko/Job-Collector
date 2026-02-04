<template>
  <div class="app-container">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/jobs">Pretraga Poslova</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script setup>
</script>

<style>
.app-container {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

nav {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

nav a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

nav a.router-link-active {
  color: #007bff;
}
</style>
