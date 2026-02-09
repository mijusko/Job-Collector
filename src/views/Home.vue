<template>
  <div class="home-container">
    <div class="hero">
      <div class="hero-content">
        <h1>JobCollector</h1>
        <p class="subtitle">Svi IT poslovi sa helloworld.rs i infostud.com sajtova na jednom mestu.</p>
        <p class="description">
          Pretražite najnovije oglase za IT poslove brzo i lako uz naš automatizovani sistem za pretragu u realnom vremenu.
        </p>
        <router-link to="/jobs">
          <button class="cta-button">Započni pretragu</button>
        </router-link>
      </div>
      <div class="hero-image">
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
        <span class="feature-icon">⚡</span>
        <h3>Brzina</h3>
        <p>Optimizovana pretraga direktno po ključnim rečima za najbrže rezultate.</p>
      </div>
      <div class="feature-card">
        <span class="feature-icon">🌙</span>
        <h3>Dark Mode</h3>
        <p>Uživajte u pretrazi uz podršku za tamnu i svetlu temu prilagođenu vama.</p>
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
  color: var(--accent-color);
}

.subtitle {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 10px 0 20px 0;
  font-weight: 500;
}

.description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 30px;
  max-width: 500px;
}

.cta-button {
  padding: 15px 40px;
  font-size: 1.2rem;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(26, 115, 232, 0.4);
  transition: transform 0.2s, opacity 0.2s;
}

.cta-button:hover {
  transform: translateY(-2px);
  opacity: 0.9;
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
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.card-1 { width: 200px; height: 120px; top: 0; left: 0; z-index: 3; }
.card-2 { width: 180px; height: 100px; top: 50px; left: 60px; z-index: 2; opacity: 0.8; }
.card-3 { width: 160px; height: 80px; top: 100px; left: 120px; z-index: 1; opacity: 0.6; }

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 60px;
}

.feature-card {
  background: var(--card-bg);
  padding: 30px;
  border-radius: 16px;
  text-align: center;
  border: 1px solid var(--border-color);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
  display: block;
}

.feature-card h3 {
  margin: 0 0 15px 0;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}
</style>
