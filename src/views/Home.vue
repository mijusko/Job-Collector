<template>
  <div class="home-container">
    <div class="hero">
      <div class="hero-content">
        <h1>JobCollector</h1>
        <p class="subtitle">Svi IT poslovi sa helloworld.rs i infostud.com sajtova na jednom mestu.</p>
        <p class="description">
          Pretražite najnovije oglase za posao, filtrirajte po lokaciji i saznajte detalje 
          brzo i lako uz naš automatizovani sistem za pretragu.
        </p>
        <router-link to="/jobs">
          <button class="cta-button">Započni pretragu</button>
        </router-link>
      </div>
      <div class="hero-image">
        <!-- Możemo dodati neku ilustraciju ovde -->
        <div class="illustration">
          <div class="card card-1"></div>
          <div class="card card-2"></div>
          <div class="card card-3"></div>
        </div>
      </div>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <span class="feature-icon">🔍</span>
        <h3>Brza pretraga</h3>
        <p>Direktno pretraživanje helloworld.rs i infostud.com platforme u realnom vremenu.</p>
      </div>
      <div class="feature-card">
        <span class="feature-icon">📍</span>
        <h3>Filteri</h3>
        <p>Lako filtriranje poslova po gradovima i remote opcijama.</p>
      </div>
      <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <h3>Bez naloga</h3>
        <p>Pristupite svim informacijama bez potrebe za registracijom.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 40px 0;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  padding: 60px 0;
}

.hero-content {
  flex: 1;
}

h1 {
  font-size: 3.5rem;
  margin: 0;
  color: #1a73e8;
}

.subtitle {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin: 10px 0 20px 0;
  font-weight: 500;
}

.description {
  font-size: 1.1rem;
  color: #70757a;
  line-height: 1.6;
  margin-bottom: 30px;
  max-width: 500px;
}

.cta-button {
  padding: 15px 40px;
  font-size: 1.2rem;
  box-shadow: 0 4px 14px rgba(26, 115, 232, 0.4);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.illustration {
  position: relative;
  width: 300px;
  height: 250px;
}

.card {
  position: absolute;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  border: 1px solid #eee;
}

.card-1 { width: 200px; height: 100px; top: 0; right: 0; transform: rotate(5deg); background: #f8fbff; }
.card-2 { width: 200px; height: 100px; top: 60px; left: 0; transform: rotate(-5deg); z-index: 1; }
.card-3 { width: 180px; height: 80px; bottom: 0; right: 20px; transform: rotate(2deg); background: #e8f0fe; }

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-top: 60px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #eee;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin: 10px 0;
  color: #1c1e21;
}

.feature-card p {
  color: #70757a;
  font-size: 0.95rem;
  line-height: 1.5;
}

@media (max-width: 992px) {
  .hero {
    flex-direction: column;
    text-align: center;
  }
  .hero-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .features {
    grid-template-columns: 1fr;
  }
  .hero-image {
    display: none;
  }
}
</style>
