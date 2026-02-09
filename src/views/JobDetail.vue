<template>
  <div v-if="job" class="job-detail">
    <button @click="$router.back()" class="back-btn">&larr; Nazad</button>
    <div class="detail-card">
      <h1>{{ job.title }}</h1>
      <h2 class="company">{{ job.company }}</h2>
      <div class="meta-info">
        <span><strong>Lokacija:</strong> {{ job.location }}</span>
        <span><strong>Datum:</strong> {{ job.date }}</span>
      </div>
      <div class="description">
        <h3>Opis posla</h3>
        <p>{{ job.description || 'Nema detaljnog opisa.' }}</p>
      </div>
      <div class="tags" v-if="job.tags && job.tags.length">
        <span v-for="tag in job.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
      <a :href="job.url" target="_blank" class="apply-link">Pogledaj na {{ job.source }}</a>
    </div>
  </div>
  <div v-else class="not-found">
    <p>Posao nije pronađen.</p>
    <router-link to="/jobs">Nazad na pretragu</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const job = ref(null)

onMounted(() => {
  const savedJob = localStorage.getItem('selectedJob')
  if (savedJob) {
    job.value = JSON.parse(savedJob)
  }
})
</script>

<style scoped>
.job-detail {
  padding: 20px 0;
}
.back-btn {
  background: none;
  color: #007bff;
  padding: 0;
  margin-bottom: 20px;
}
.back-btn:hover {
  text-decoration: underline;
  background: none;
}
.detail-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  border: 1px solid #ddd;
}
.company {
  color: #555;
  margin-top: 0;
}
.meta-info {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  color: #ffbb00;
}
.description {
  margin: 30px 0;
  line-height: 1.6;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
}
.tag {
  background: #e9ecef;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9em;
}
.apply-link {
  display: inline-block;
  background-color: #28a745;
  color: white;
  padding: 12px 25px;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
}
.apply-link:hover {
  background-color: #218838;
}
</style>
