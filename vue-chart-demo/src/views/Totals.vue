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
        <!-- Event Parameters -->
        <div class="event-params-section">
          <h2>Event Parameters</h2>
          <div class="params-grid">
            <div class="param-box">
              <label>Number of Participants:</label>
              <input v-model.number="participants" type="number" min="1" />
            </div>
            <div class="param-box">
              <label>Event Duration (hours):</label>
              <input v-model.number="hours" type="number" min="0.5" step="0.5" />
            </div>
            <button class="calculate-btn">
              Calculate Sustainability Score
            </button>
          </div>
        </div>

        <!-- Sustainability Score Meter -->
        <div class="score-section">
          <h2>Sustainability Score</h2>
          <div class="score-meter">
            <div class="meter-container">
              <div class="meter-fill" style="width: 65%"></div>
              <div class="meter-text">125.4</div>
            </div>
            <div class="score-rating">Green (Good Job)</div>
          </div>
        </div>

        <!-- Eco-Score Box -->
        <div class="eco-score-section">
          <h2>Eco-Score</h2>
          <div class="eco-score-box">eco-score</div>
        </div>

        <!-- Category Totals -->
        <div class="categories-section">
          <h2>Category Breakdown</h2>
          <div class="categories-grid">
            <div class="category-box">
              <h3>Supplies & Goods</h3>
              <div class="category-metrics">
                <div class="metric">CO2: 45.2 kg</div>
                <div class="metric">Water: 12.8 EIP</div>
                <div class="metric">Energy: 8.9 EIP</div>
                <div class="metric">GWI: 67.3 EIP</div>
              </div>
            </div>
            <div class="category-box">
              <h3>Technology</h3>
              <div class="category-metrics">
                <div class="metric">CO2: 23.1 kg</div>
                <div class="metric">Water: 15.2 EIP</div>
                <div class="metric">Energy: 45.6 EIP</div>
                <div class="metric">GWI: 34.7 EIP</div>
              </div>
            </div>
            <div class="category-box">
              <h3>Travel</h3>
              <div class="category-metrics">
                <div class="metric">CO2: 156.8 kg</div>
                <div class="metric">Water: 89.4 EIP</div>
                <div class="metric">Energy: 234.1 EIP</div>
                <div class="metric">GWI: 145.6 EIP</div>
              </div>
            </div>
            <div class="category-box">
              <h3>Food</h3>
              <div class="category-metrics">
                <div class="metric">CO2: 78.9 kg</div>
                <div class="metric">Water: 45.2 EIP</div>
                <div class="metric">Energy: 67.8 EIP</div>
                <div class="metric">GWI: 123.4 EIP</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Highest Impact Items -->
        <div class="impact-section">
          <h2>Highest Impact Items</h2>
          <div class="impact-grid">
            <div class="impact-box">
              <h4>Travel</h4>
              <p class="item-name">Plane (500km)</p>
              <p class="item-impact">Average Impact: 156.2 EIP</p>
            </div>
            <div class="impact-box">
              <h4>Food</h4>
              <p class="item-name">Paper - Meat</p>
              <p class="item-impact">Average Impact: 78.8 EIP</p>
            </div>
            <div class="impact-box">
              <h4>Technology</h4>
              <p class="item-name">Large Device</p>
              <p class="item-impact">Average Impact: 67.4 EIP</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedSection = ref('supplies')

// Data refs for all items
const suppliesItems = ref([])
const techItems = ref([])
const travelItems = ref([])
const foodItems = ref([])

// Event parameters
const participants = ref(1)
const hours = ref(1)

// Sustainability calculation results
const sustainabilityData = ref(null)
const errorMessage = ref('')

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

// Helper function to format numbers and remove trailing zeros
function formatNumber(num, maxDecimals = 4) {
  if (num === undefined || num === null || isNaN(num)) {
    console.warn('formatNumber received invalid value:', num)
    return '0'
  }
  if (num === 0) return '0'
  const fixed = num.toFixed(maxDecimals)
  // Remove trailing zeros and decimal point if unnecessary
  return fixed.replace(/\.?0+$/, '')
}

// Computed properties for category totals
const suppliesTotals = computed(() => ({
  co2: suppliesItems.value.reduce((sum, item) => sum + item.co2, 0),
  water: suppliesItems.value.reduce((sum, item) => sum + item.water, 0),
  energy: suppliesItems.value.reduce((sum, item) => sum + item.energy, 0),
  gwi: suppliesItems.value.reduce((sum, item) => sum + item.gwi, 0)
}))

const techTotals = computed(() => ({
  co2: techItems.value.reduce((sum, item) => sum + item.co2, 0),
  water: techItems.value.reduce((sum, item) => sum + item.water, 0),
  energy: techItems.value.reduce((sum, item) => sum + item.energy, 0),
  gwi: techItems.value.reduce((sum, item) => sum + item.gwi, 0)
}))

const travelTotals = computed(() => ({
  co2: travelItems.value.reduce((sum, item) => sum + item.co2, 0),
  water: travelItems.value.reduce((sum, item) => sum + item.water, 0),
  energy: travelItems.value.reduce((sum, item) => sum + item.energy, 0),
  gwi: travelItems.value.reduce((sum, item) => sum + item.gwi, 0)
}))

const foodTotals = computed(() => ({
  co2: foodItems.value.reduce((sum, item) => sum + item.co2, 0),
  water: foodItems.value.reduce((sum, item) => sum + item.water, 0),
  energy: foodItems.value.reduce((sum, item) => sum + item.energy, 0),
  gwi: foodItems.value.reduce((sum, item) => sum + item.gwi, 0)
}))

// Check if calculation can proceed
const canCalculate = computed(() => {
  return participants.value > 0 && hours.value > 0 &&
         (suppliesItems.value.length > 0 || techItems.value.length > 0 ||
          travelItems.value.length > 0 || foodItems.value.length > 0)
})

// Score percentage for meter (0-100 scale)
const scorePercentage = computed(() => {
  if (!sustainabilityData.value) return 0
  // Scale the score to 0-100% where 0 is best (Platinum) and 100% is worst
  const score = sustainabilityData.value.sustainability_score
  // Platinum: <100, Green: 100-149, High Impact: >=150
  if (score < 100) return Math.max(0, (score / 100) * 33) // 0-33% range
  if (score < 150) return 33 + ((score - 100) / 50) * 33 // 33-66% range
  return Math.min(100, 66 + ((score - 150) / 50) * 34) // 66-100% range
})

// Highest impact items across all categories
const highestImpactItems = computed(() => {
  const allItems = []

  // Add supplies items
  suppliesItems.value.forEach((item, index) => {
    const avgImpact = (item.co2 + item.water + item.energy + item.gwi) / 4
    allItems.push({
      id: `supplies-${index}`,
      category: 'Supplies',
      name: item.label,
      metric: 'Average Impact',
      value: avgImpact,
      unit: 'EIP'
    })
  })

  // Add tech items
  techItems.value.forEach((item, index) => {
    const avgImpact = (item.co2 + item.water + item.energy + item.gwi) / 4
    allItems.push({
      id: `tech-${index}`,
      category: 'Technology',
      name: item.type,
      metric: 'Average Impact',
      value: avgImpact,
      unit: 'EIP'
    })
  })

  // Add travel items
  travelItems.value.forEach((item, index) => {
    const avgImpact = (item.co2 + item.water + item.energy + item.gwi) / 4
    allItems.push({
      id: `travel-${index}`,
      category: 'Travel',
      name: `${item.mode} (${item.distance}km)`,
      metric: 'Average Impact',
      value: avgImpact,
      unit: 'EIP'
    })
  })

  // Add food items
  foodItems.value.forEach((item, index) => {
    const avgImpact = (item.co2 + item.water + item.energy + item.gwi) / 4
    allItems.push({
      id: `food-${index}`,
      category: 'Food',
      name: `${item.packaging} - ${item.diet}`,
      metric: 'Average Impact',
      value: avgImpact,
      unit: 'EIP'
    })
  })

  // Sort by impact (highest first) and take top 3
  return allItems
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
})

// Calculate sustainability score
async function calculateSustainabilityScore() {
  try {
    errorMessage.value = ''

    const response = await fetch('http://localhost:5001/total', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        physical_waste: [
          suppliesTotals.value.co2,
          suppliesTotals.value.water,
          suppliesTotals.value.energy,
          suppliesTotals.value.gwi
        ],
        travel: [
          travelTotals.value.co2,
          travelTotals.value.water,
          travelTotals.value.energy,
          travelTotals.value.gwi
        ],
        technology: [
          techTotals.value.co2,
          techTotals.value.water,
          techTotals.value.energy,
          techTotals.value.gwi
        ],
        food: [
          foodTotals.value.co2,
          foodTotals.value.water,
          foodTotals.value.energy,
          foodTotals.value.gwi
        ],
        participants: participants.value,
        hours: hours.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'API request failed')
    }

    const data = await response.json()
    sustainabilityData.value = data

  } catch (error) {
    console.error('Error calculating sustainability score:', error)
    errorMessage.value = `Failed to calculate score: ${error.message}`
    sustainabilityData.value = null
  }
}
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

/* Event Parameters Section */
.event-params-section {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.event-params-section h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.params-grid {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
  align-items: end;
}

.param-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.param-box label {
  font-weight: 600;
  color: var(--text);
  font-size: 0.9rem;
}

.param-box input {
  padding: 0.75rem;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.param-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2);
}

.calculate-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.calculate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Score Meter Section */
.score-section {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.score-section h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.score-meter {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.meter-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  border: 2px solid var(--border);
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%);
  transition: width 0.5s ease;
}

.meter-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.score-rating {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text);
  text-align: center;
}

/* Eco-Score Section */
.eco-score-section {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.eco-score-section h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.eco-score-box {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text);
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid var(--border);
}

/* Categories Section */
.categories-section {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.categories-section h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.category-box {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border);
}

.category-box h3 {
  color: var(--text);
  margin-bottom: 1rem;
  font-size: 1.1rem;
  text-align: center;
}

.category-metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric {
  font-size: 0.9rem;
  color: var(--text);
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Impact Section */
.impact-section {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-hover) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.impact-section h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.impact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.impact-box {
  background: rgba(239, 68, 68, 0.1);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  text-align: center;
}

.impact-box h4 {
  color: #ef4444;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.item-name {
  color: var(--text);
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.item-impact {
  color: #ef4444;
  font-weight: 500;
  font-size: 0.85rem;
}

/* Error Section */
.error-section {
  background: rgba(239, 68, 68, 0.1);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  margin-bottom: 2rem;
}

.error {
  color: #ef4444;
  margin: 0;
  font-weight: 500;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .totals-layout {
    flex-direction: column;
  }

  .totals-sidebar {
    flex: none;
    max-height: 50vh;
  }

  .params-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .calculate-btn {
    width: 100%;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }

  .impact-grid {
    grid-template-columns: 1fr;
  }
}
</style>
