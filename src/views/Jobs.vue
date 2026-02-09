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
      <p class="progress-text">{{ progress }}% - Pretražujem HelloWorld i Infostud...</p>
      <p class="sub-text">Ovo može potrajati par sekundi dok Selenium učita stranice.</p>
    </div>

    <div v-else class="results-section">
      <div v-if="jobs.length > 0">
        <div class="results-header">
          <p class="found-jobs">Pronađeno poslova: <strong>{{ jobs.length }}</strong></p>
        </div>
        <div class="job-list">
        <div v-for="job in jobs" :key="job.id" class="job-card-horizontal" @click="showJobModal(job)">
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
            <button class="secondary-btn" @click.stop="showJobModal(job)">Pogledaj detalje</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="searched" class="no-results">
        <p>Nismo pronašli poslove za vašu pretragu. Pokušajte sa drugim ključnim rečima.</p>
      </div>
    </div>

    <!-- Modal za detalje posla -->
    <div v-if="selectedJob" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <div class="job-source" :class="selectedJob.source.toLowerCase()">{{ selectedJob.source }}</div>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <h2 class="modal-title">{{ selectedJob.title }}</h2>
          <h3 class="modal-company">{{ selectedJob.company }}</h3>
          
          <div class="modal-meta">
            <div class="meta-item">
              <span class="icon">📍</span>
              <span>{{ selectedJob.location }}</span>
            </div>
            <div class="meta-item" v-if="selectedJob.date">
              <span class="icon">📅</span>
              <span>{{ selectedJob.date }}</span>
            </div>
          </div>

          <div class="modal-description" v-if="selectedJob.description">
            <h4>Opis posla:</h4>
            <p>{{ selectedJob.description }}</p>
          </div>

          <div class="modal-footer">
            <a :href="selectedJob.url" target="_blank" class="primary-btn apply-btn">Prijavi se na sajtu</a>
            <button @click="closeModal" class="secondary-btn">Zatvori</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const loading = ref(false)
const searched = ref(false)
const jobs = ref([])
const progress = ref(0)
const selectedJob = ref(null)
let progressInterval = null

const startProgress = () => {
  progress.value = 0
  progressInterval = setInterval(() => {
    if (progress.value < 95) {
      // Još sporije napredovanje do 95%
      const increment = progress.value < 40 ? 2 : (progress.value < 70 ? 0.8 : 0.2)
      progress.value = Math.min(95, parseFloat((progress.value + increment).toFixed(1)))
    }
  }, 600)
}

const stopProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progress.value = 100
  }
}

const showJobModal = (job) => {
  selectedJob.value = job
  document.body.style.overflow = 'hidden' // Spreči skrolovanje dok je modal otvoren
}

const closeModal = () => {
  selectedJob.value = null
  document.body.style.overflow = 'auto'
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


</script>

<style scoped>
.jobs-page {
  padding-bottom: 50px;
}

.header-section {
  background: var(--card-bg);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 40px;
  border: 1px solid var(--border-color);
}

h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: var(--accent-color);
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
  background: var(--card-bg);
  padding: 24px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.job-card-horizontal:hover {
  border-color: var(--accent-color);
  box-shadow: 0 4px 12px rgba(26, 115, 232, 0.1);
  transform: translateY(-2px);
}

.card-content {
  flex: 1;
}

.job-title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  color: var(--accent-color);
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
  color: var(--text-primary);
}

.meta-data {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.secondary-btn {
  background-color: transparent;
  color: var(--accent-color);
  border: 1.5px solid var(--accent-color);
}

.secondary-btn:hover {
  background-color: var(--hover-bg);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color);
}

.progress-container {
  width: 100%;
  max-width: 400px;
  height: 12px;
  background-color: var(--hover-bg);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress-bar {
  height: 100%;
  background-color: var(--accent-color);
  transition: width 0.5s ease;
}

.progress-text {
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 5px;
}

.sub-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 5px;
}

.results-header {
  margin-bottom: 20px;
  padding: 0 5px;
}

.found-jobs {
  font-size: 1.1rem;
  color: var(--text-primary);
}

.found-jobs strong {
  color: var(--accent-color);
  font-size: 1.3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--hover-bg);
  border-top: 4px solid var(--accent-color);
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
  color: var(--text-secondary);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: var(--card-bg);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  border-radius: 16px;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
  border: 1px solid var(--border-color);
  animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  background: var(--card-bg);
  z-index: 10;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: 30px;
}

.modal-title {
  margin: 0 0 10px 0;
  font-size: 1.8rem;
  color: var(--accent-color);
}

.modal-company {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
  color: var(--text-primary);
  font-weight: 600;
}

.modal-meta {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 15px;
  background: var(--hover-bg);
  border-radius: 8px;
  color: var(--text-primary);
}

.modal-description {
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: 40px;
  white-space: pre-wrap;
}

.modal-description h4 {
  margin-bottom: 15px;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.modal-footer {
  display: flex;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.primary-btn {
  background-color: var(--accent-color);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}

.primary-btn:hover {
  opacity: 0.9;
}

.apply-btn {
  flex: 1;
  text-align: center;
}
</style>
