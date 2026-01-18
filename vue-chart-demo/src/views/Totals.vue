<template>
  <div class="totals-page">
    <div class="totals-header">
      <h1>Totals Page</h1>
      <div class="section-selector">
        <select v-model="selectedSection" @change="navigateToSection" class="section-dropdown">
          <option value="supplies">Supplies and Goods</option>
          <option value="technology">Technology</option>
          <option value="travel">Travel</option>
          <option value="food">Food</option>
        </select>
      </div>
    </div>
    <p>This page will show aggregated totals across all sections.</p>
    <!-- TODO: Add totals content here -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedSection = ref('supplies')

function navigateToSection() {
  // Save the selected section to sessionStorage so the home page can load it
  const saved = sessionStorage.getItem('mcfootprint-data')
  let data = {}
  if (saved) {
    data = JSON.parse(saved)
  }
  data.currentSection = selectedSection.value
  sessionStorage.setItem('mcfootprint-data', JSON.stringify(data))

  // Navigate back to home page
  router.push('/')
}

// TODO: Implement totals functionality
</script>

<style scoped>
.totals-page {
  padding: 2rem;
  text-align: center;
}

.totals-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 800px;
  margin-bottom: 2rem;
}

.totals-page h1 {
  color: #10b981;
  margin: 0;
}

.totals-page p {
  color: #666;
  font-size: 1.1rem;
}

.section-selector {
  display: flex;
  align-items: center;
}

.section-dropdown {
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--border);
  border-radius: 16px;
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  color: var(--text);
  font-size: 0.95em;
  font-family: inherit;
  cursor: pointer;
  min-width: 220px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.section-dropdown:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
}

.section-dropdown:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.5);
}
</style>
