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

    <!-- Main Layout -->
    <div class="totals-layout">
      <!-- Sidebar with All Items -->
      <aside class="totals-sidebar">
        <!-- EIP Explanation -->
        <div class="eip-explanation">
          <p>The metric EIP refers to <a href="https://support.ecoinvent.org/impact-assessment" target="_blank">Environmental Impact Points</a></p>
        </div>

        <!-- All Items Display -->
        <div class="all-items-section">
          <h2>All Items</h2>

          <!-- Supplies Items -->
          <div v-if="suppliesItems.length > 0" class="section-items">
            <h3>Supplies</h3>
            <ul>
              <li v-for="(item, index) in suppliesItems" :key="index">
                <span class="label-box">{{ item.label }}</span>
                <span class="value-box">{{ item.value }}</span>
              </li>
            </ul>
          </div>

          <!-- Technology Items -->
          <div v-if="techItems.length > 0" class="section-items">
            <h3>Technology</h3>
            <ul>
              <li v-for="(item, index) in techItems" :key="index">
                <span class="label-box">{{ item.type }}</span>
                <span class="value-box">{{ item.num }} ({{ item.participants }} participants)</span>
              </li>
            </ul>
          </div>

          <!-- Travel Items -->
          <div v-if="travelItems.length > 0" class="section-items">
            <h3>Travel</h3>
            <ul>
              <li v-for="(item, index) in travelItems" :key="index">
                <span class="label-box">{{ item.mode }}</span>
                <span class="value-box">{{ item.distance }}km ({{ item.participants }} participants)</span>
              </li>
            </ul>
          </div>

          <!-- Food Items -->
          <div v-if="foodItems.length > 0" class="section-items">
            <h3>Food</h3>
            <ul>
              <li v-for="(item, index) in foodItems" :key="index">
                <span class="label-box">{{ item.packaging }} - {{ item.diet }}</span>
                <span class="value-box">{{ item.num }} meals</span>
              </li>
            </ul>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="totals-main">
        <p>This page will show aggregated totals across all sections.</p>
        <!-- TODO: Add totals content here -->
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedSection = ref('supplies')

// Data refs for all items
const suppliesItems = ref([])
const techItems = ref([])
const travelItems = ref([])
const foodItems = ref([])

// Load data from sessionStorage on mount
onMounted(() => {
  loadData()
})

function loadData() {
  const saved = sessionStorage.getItem('mcfootprint-data')
  if (saved) {
    const data = JSON.parse(saved)
    suppliesItems.value = data.supplies || []
    techItems.value = data.technology || []
    travelItems.value = data.travel || []
    foodItems.value = data.food || []
    selectedSection.value = data.currentSection || 'supplies'
  }
}

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

/* Layout styles */
.totals-layout {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.totals-sidebar {
  flex: 0 0 350px;
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
  height: fit-content;
  max-height: 80vh;
  overflow-y: auto;
}

.totals-main {
  flex: 1;
  min-width: 0;
}

/* EIP explanation */
.eip-explanation {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.eip-explanation p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.4;
}

.eip-explanation a {
  color: #10b981;
  text-decoration: none;
}

.eip-explanation a:hover {
  text-decoration: underline;
}

/* All items section */
.all-items-section h2 {
  color: #10b981;
  font-size: 1.4rem;
  margin-bottom: 1rem;
  text-align: center;
}

.section-items {
  margin-bottom: 1.5rem;
}

.section-items h3 {
  color: var(--text);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.25rem;
}

.section-items ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.section-items li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin-bottom: 0.25rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid var(--border);
}

.label-box {
  font-weight: 600;
  color: var(--text);
  flex: 1;
  text-align: left;
}

.value-box {
  font-weight: 500;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  border: 1px solid rgba(16, 185, 129, 0.2);
  text-align: center;
  min-width: 60px;
}
</style>
