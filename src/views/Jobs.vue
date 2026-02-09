<template>
  <div class="jobs-page">
    <div class="header-section">
      <h2>Pronađite svoj idealan posao</h2>
      <div class="search-filters">
        <div class="input-group">
          <input v-model="searchQuery" placeholder="Pozicija, tehnologija (npr. Python, Vue)..." @keyup.enter="searchJobs" />
        </div>
        <button @click="searchJobs" :disabled="loading">
          <span v-if="!loading">Pretraži</span>
          <span v-else class="loader"></span>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="progress-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
      <p>{{ progress }}% - Pretražujem HelloWorld i Infostud...</p>
      <p class="sub-text">Ovo može potrajati par sekundi dok Selenium učita stranice.</p>
    </div>

    <div v-else class="results-section">
      <div v-if="jobs.length > 0">
        <div class="results-header">
          <p class="found-jobs">Pronađeno poslova: <strong>{{ jobs.length }}</strong></p>
        </div>
        <div class="job-list">
        <div v-for="job in jobs" :key="job.id" class="job-card-horizontal" @click="viewDetails(job)">
          <div class="card-content">
            <div class="main-info">
              <div class="job-source" :class="job.source.toLowerCase()">{{ job.source }}</div>
              <h3 class="job-title">{{ job.title }}</h3>
              <p class="company-name">{{ job.company }}</p>
            </div>
            <div class="meta-data">
              <div class="meta-item">
                <span class="icon">📍</span>
                <span>{{ job.location }}</span>
              </div>
              <div class="meta-item" v-if="job.date">
                <span class="icon">📅</span>
                <span>{{ job.date }}</span>
              </div>
            </div>
          </div>
          <div class="card-action">
            <button class="secondary-btn" @click.stop="viewDetails(job)">Pogledaj detalje</button>
          </div>
        </div>
      </div>
      <div v-else-if="searched" class="no-results">
        <p>Nismo pronašli poslove za vašu pretragu. Pokušajte sa drugim ključnim rečima.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const searchQuery = ref('')
const loading = ref(false)
const searched = ref(false)
const jobs = ref([])
const progress = ref(0)
let progressInterval = null

const startProgress = () => {
  progress.value = 0
  progressInterval = setInterval(() => {
    if (progress.value < 95) {
      // Brže na početku, sporije pri kraju
      const increment = progress.value < 50 ? 5 : (progress.value < 80 ? 2 : 0.5)
      progress.value = Math.min(95, parseFloat((progress.value + increment).toFixed(1)))
    }
  }, 500)
}

const stopProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progress.value = 100
  }
}

const searchJobs = async () => {
  if (loading.value) return
  
  loading.value = true
  searched.value = true
  startProgress()
  
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001'
    const response = await axios.get(`${apiUrl}/scrape`, {
      params: {
        query: searchQuery.value
      },
      timeout: 120000 // Povećan timeout na 2 minuta jer je scraping spor
    })
    jobs.value = response.data
  } catch (error) {
    console.error('Greška pri pretrazi:', error)
    // Fallback na dummy podatke ako scraper nije pokrenut (za demo)
    if (error.code === 'ERR_NETWORK' || error.response?.status === 500) {
      const isLocal = window.location.hostname === 'localhost'
      const message = isLocal 
        ? 'Napomena: Python scraper API nije pokrenut na localhost:8001. Prikazujem demo podatke.'
        : 'Došlo je do greške pri komunikaciji sa serverom. Prikazujem demo podatke.'
      alert(message)
      jobs.value = [
        { id: '1', title: 'Senior Python Developer', company: 'Tech Solutions d.o.o.', location: 'Beograd', date: 'Pre 2 dana', url: 'https://helloworld.rs', description: 'Ovo je demo podatak jer API nije dostupan.' },
        { id: '2', title: 'Frontend Vue.js Inženjer', company: 'Innovate IT', location: 'Novi Sad', date: 'Danas', url: 'https://helloworld.rs', description: 'Ovo je demo podatak jer API nije dostupan.' }
      ]
    }
  } finally {
    stopProgress()
    setTimeout(() => {
      loading.value = false
    }, 500)
  }
}

const viewDetails = (job) => {
  localStorage.setItem('selectedJob', JSON.stringify(job))
  router.push({ name: 'job-detail', params: { id: job.id } })
}
</script>

<style scoped>
.jobs-page {
  padding-bottom: 50px;
}

.header-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 40px;
}

h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #1a73e8;
}

.search-filters {
  display: flex;
  gap: 15px;
  align-items: center;
}

.input-group {
  flex: 1;
}

.input-group input, .input-group select {
  width: 100%;
  box-sizing: border-box;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-card-horizontal {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 24px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.job-card-horizontal:hover {
  border-color: #1a73e8;
  box-shadow: 0 4px 12px rgba(26, 115, 232, 0.1);
  transform: translateY(-2px);
}

.card-content {
  flex: 1;
}

.job-title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  color: #1a73e8;
}

.job-source {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.job-source.helloworld {
  background: #e8f0fe;
  color: #1a73e8;
}

.job-source.infostud {
  background: #fff4e5;
  color: #ff9800;
}

.company-name {
  margin: 0 0 16px 0;
  font-weight: 600;
  color: #4a4a4a;
}

.meta-data {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: #70757a;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.secondary-btn {
  background-color: transparent;
  color: #1a73e8;
  border: 1.5px solid #1a73e8;
}

.secondary-btn:hover {
  background-color: #f8fbff;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.progress-container {
  width: 100%;
  max-width: 400px;
  height: 12px;
  background-color: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress-bar {
  height: 100%;
  background-color: #1a73e8;
  transition: width 0.5s ease;
}

.sub-text {
  font-size: 0.9rem;
  color: #666;
  margin-top: 5px;
}

.results-header {
  margin-bottom: 20px;
  padding: 0 5px;
}

.found-jobs {
  font-size: 1.1rem;
  color: #333;
}

.found-jobs strong {
  color: #1a73e8;
  font-size: 1.3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1a73e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #70757a;
}
</style>
