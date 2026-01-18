<template>
  <!-- Main Dashboard Layout -->
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- EIP Explanation -->
      <div class="eip-explanation">
        <p>The metric EIP refers to <a href="https://support.ecoinvent.org/impact-assessment" target="_blank">Environmental Impact Points</a></p>
      </div>

      <!-- Supplies Section Inputs -->
      <div v-if="currentSection === 'supplies'">
        <h2>Add Supplies</h2>
        <form @submit.prevent="addItem" style="margin-bottom: 1rem;">
          <div class="custom-dropdown">
            <input
              v-model="searchQuery"
              @focus="openDropdown"
              @blur="closeDropdown"
              @keydown="handleKeyDown"
              class="dropdown-input"
              placeholder="Select or type an item"
              autocomplete="off"
            />
            <span class="dropdown-arrow" @click="toggleDropdown">▼</span>
            <div v-show="isDropdownOpen" class="dropdown-options">
              <div
                v-for="(item, index) in filteredItems"
                :key="item"
                class="dropdown-option"
                @mousedown.stop="selectItem(item)"
                :class="{ 'option-highlighted': highlightedIndex === index }"
              >
                {{ item }}
              </div>
            </div>
          </div>
          <input v-model.number="newValue" type="number" />
          <button>Add</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
        <div class="items-list" v-if="items.length > 0">
          <h3>Items</h3>
          <ul>
            <li v-for="(item, index) in items" :key="index">
              <span class="label-box">{{ item.label }}</span>
              <span v-if="editingIndex !== index" class="value-box" @click="startEdit(index)">{{ item.value }}</span>
              <input v-else class="value-box" v-model.number="item.value" @blur="stopEdit" @keyup.enter="stopEdit" />
              <button @click="deleteItem(index)" class="delete-btn">×</button>
            </li>
          </ul>
          <button @click="clearAll" class="clear-btn">Clear All</button>
        </div>
      </div>

      <!-- Technology Section Inputs -->
      <div v-if="currentSection === 'technology'">
        <h2>Add Technology</h2>
        <div class="input-group">
          <div class="input-box">
            <label>Type of Technology:</label>
            <select v-model="techType" class="tech-select">
              <option>AI Prompts</option>
              <option>Personal Device</option>
              <option>Large Device</option>
            </select>
          </div>
          <div class="input-box">
            <label>{{ quantityLabel }}</label>
            <input v-model.number="techNum" type="number" min="1" />
          </div>
          <div class="input-box">
            <label>Participants:</label>
            <input v-model.number="techParticipants" type="number" min="1" />
          </div>
          <button @click="calculateTech">Add Technology</button>
        </div>
        <div class="items-list" v-if="techItems.length > 0">
          <h3>Technology Items</h3>
          <ul>
            <li v-for="(item, index) in techItems" :key="index">
              <span class="label-box">{{ item.type }}</span>
              <span v-if="techEditingIndex !== index" class="value-box" @click="startEditTech(index)">{{ item.num }}</span>
              <input v-else class="value-box" v-model.number="item.num" @blur="stopEditTech(index)" @keyup.enter="stopEditTech(index)" />
              <span v-if="techEditingIndex !== index" class="value-box" @click="startEditTech(index)">{{ item.participants }}</span>
              <input v-else class="value-box" v-model.number="item.participants" @blur="stopEditTech(index)" @keyup.enter="stopEditTech(index)" />
              <button @click="deleteTechItem(index)" class="delete-btn">×</button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Travel Section Inputs -->
      <div v-if="currentSection === 'travel'">
        <h2>Add Travel</h2>
        <div class="input-group">
          <div class="input-box">
            <label>Mode of Transport:</label>
            <select v-model="travelMode" class="travel-select">
              <option>Car</option>
              <option>Bus</option>
              <option>Train</option>
              <option>Plane</option>
            </select>
          </div>
          <div class="input-box">
            <label>Distance (km):</label>
            <input v-model.number="travelDistance" type="number" min="0" />
          </div>
          <div class="input-box">
            <label>Participants:</label>
            <input v-model.number="travelParticipants" type="number" min="1" />
          </div>
          <button @click="calculateTravel">Add Travel</button>
        </div>
        <div class="items-list" v-if="travelItems.length > 0">
          <h3>Travel Items</h3>
          <ul>
            <li v-for="(item, index) in travelItems" :key="index">
              <span class="label-box">{{ item.mode }}</span>
              <span v-if="travelEditingIndex !== index" class="value-box" @click="startEditTravel(index)">{{ item.distance }}</span>
              <input v-else class="value-box" v-model.number="item.distance" @blur="stopEditTravel(index)" @keyup.enter="stopEditTravel(index)" />
              <span v-if="travelEditingIndex !== index" class="value-box" @click="startEditTravel(index)">{{ item.participants }}</span>
              <input v-else class="value-box" v-model.number="item.participants" @blur="stopEditTravel(index)" @keyup.enter="stopEditTravel(index)" />
              <button @click="deleteTravelItem(index)" class="delete-btn">×</button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Food Section Inputs -->
      <div v-if="currentSection === 'food'">
        <h2>Add Food</h2>
        <div class="input-group">
          <div class="input-box">
            <label>Packaging Type:</label>
            <select v-model="foodPackaging" class="food-select">
              <option>Reusable</option>
              <option>Compostable</option>
              <option>Paper</option>
            </select>
          </div>
          <div class="input-box">
            <label>Diet Type:</label>
            <select v-model="foodDiet" class="food-select">
              <option>Plant-Based</option>
              <option>Meat</option>
            </select>
          </div>
          <div class="input-box">
            <label>Number of Meals:</label>
            <input v-model.number="foodNum" type="number" min="1" />
          </div>
          <button @click="calculateFood">Add Food</button>
        </div>
        <div class="items-list" v-if="foodItems.length > 0">
          <h3>Food Items</h3>
          <ul>
            <li v-for="(item, index) in foodItems" :key="index">
              <span class="label-box">{{ item.packaging }} - {{ item.diet }}</span>
              <span v-if="foodEditingIndex !== index" class="value-box" @click="startEditFood(index)">{{ item.num }}</span>
              <input v-else class="value-box" v-model.number="item.num" @blur="stopEditFood(index)" @keyup.enter="stopEditFood(index)" />
              <button @click="deleteFoodItem(index)" class="delete-btn">×</button>
            </li>
          </ul>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
      <p style="text-align: center; font-size: 0.9em; color: #666;">Click on the chart to fullscreen it.</p>

      <!-- Individual Section Charts (Supplies, Technology, Travel, Food) -->
      <div class="charts-grid">
        <div class="chart-container">
          <h4>CO2: kg CO2</h4>
          <ChartComponent :data="currentCO2Data" title="CO2 Emissions" @chart-click="openModal" />
        </div>
        <div class="chart-container">
          <h4>Water Resources: EIP</h4>
          <ChartComponent :data="currentWaterData" title="Water Resources" @chart-click="openModal" />
        </div>
        <div class="chart-container">
          <h4>Energy Resource: EIP</h4>
          <ChartComponent :data="currentEnergyData" title="Energy Resources" @chart-click="openModal" />
        </div>
        <div class="chart-container">
          <h4>GWI: EIP</h4>
          <ChartComponent :data="currentGWIChartData" title="Global Warming Index" @chart-click="openModal" />
        </div>
      </div>

      <!-- Global Chart Modal -->
      <div v-if="modalOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <button class="close-btn" @click="closeModal">×</button>
          <h2>{{ modalChartTitle }}</h2>
          <canvas ref="modalCanvas"></canvas>
        </div>
      </div>

      <!-- Total Emissions Section -->
      <div class="totals-section" v-if="currentItems.length > 0">
        <h2>Total Emissions</h2>
        <div class="totals-grid">
          <div class="total-box">
            <h3>CO2</h3>
            <p v-fit-text>{{ formatNumber(currentTotalCO2, currentSection === 'supplies' ? 2 : 4) }} kg CO2</p>
          </div>
          <div class="total-box">
            <h3>Water</h3>
            <p v-fit-text>{{ formatNumber(currentTotalWater, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
          <div class="total-box">
            <h3>Energy</h3>
            <p v-fit-text>{{ formatNumber(currentTotalEnergy, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
          <div class="total-box">
            <h3>GWI</h3>
            <p v-fit-text>{{ formatNumber(currentTotalGWI, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
        </div>
      </div>

      <!-- Max Emissions Section -->
      <div v-if="currentMaxCO2Product" class="max-section">
        <h2>Items with Most Emissions</h2>
        <div class="max-grid">
          <div class="max-box">
            <h3>CO2</h3>
            <p>{{ currentMaxCO2Product.label || currentMaxCO2Product.mode || currentMaxCO2Product.type || (currentMaxCO2Product.packaging + ' - ' + currentMaxCO2Product.diet) }}</p>
            <p v-fit-text>{{ formatNumber(currentMaxCO2Product.co2, currentSection === 'supplies' ? 2 : 4) }} {{ currentSection === 'supplies' ? 'kg CO2' : 'EIP' }}</p>
          </div>
          <div class="max-box">
            <h3>Water</h3>
            <p>{{ currentMaxWaterProduct.label || currentMaxWaterProduct.mode || currentMaxWaterProduct.type || (currentMaxWaterProduct.packaging + ' - ' + currentMaxWaterProduct.diet) }}</p>
            <p v-fit-text>{{ formatNumber(currentMaxWaterProduct.water, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
          <div class="max-box">
            <h3>Energy</h3>
            <p>{{ currentMaxEnergyProduct.label || currentMaxEnergyProduct.mode || currentMaxEnergyProduct.type || (currentMaxEnergyProduct.packaging + ' - ' + currentMaxEnergyProduct.diet) }}</p>
            <p v-fit-text>{{ formatNumber(currentMaxEnergyProduct.energy, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
          <div class="max-box">
            <h3>GWI</h3>
            <p>{{ currentMaxGWIProduct.label || currentMaxGWIProduct.mode || currentMaxGWIProduct.type || (currentMaxGWIProduct.packaging + ' - ' + currentMaxGWIProduct.diet) }}</p>
            <p v-fit-text>{{ formatNumber(currentMaxGWIProduct.gwi, currentSection === 'supplies' ? 2 : 4) }} EIP</p>
          </div>
        </div>
      </div>

      <!-- Section-specific Suggestions -->
      <div v-if="currentSectionSuggestions.length > 0" class="suggestions-section">
        <h2>Optimization Suggestions</h2>
        <div class="suggestions-list">
          <div v-for="(suggestion, index) in currentSectionSuggestions" :key="index" class="suggestion-item">
            <div class="suggestion-header">
              <span class="suggestion-type">{{ suggestion.category }}</span>
              <span class="suggestion-savings">Potential savings: {{ suggestion.savings.toFixed(2) }} avg EIP</span>
            </div>
            <p>{{ suggestion.description }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue"
import Chart from "chart.js/auto"
import ChartComponent from "../components/ChartComponent.vue"

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

// Current section state
const currentSection = ref('supplies')

// Modal state
const modalOpen = ref(false)
const modalChartData = ref(null)
const modalChartTitle = ref('')
const modalCanvas = ref(null)

// Supplies data
const items = ref([])
const newLabel = ref("")
const newValue = ref(1)
const errorMessage = ref("")
const editingIndex = ref(-1)
const isDropdownOpen = ref(false)
const highlightedIndex = ref(-1)
const searchQuery = ref("")
const colors = ['#228B22', '#32CD32', '#006400', '#9ACD32', '#228B22', '#32CD32', '#006400', '#9ACD32', '#228B22', '#32CD32']
const allowedItems = [
  'Pen - Plastic',
  'Pen - Metal',
  'Pen - Biodegradable',
  'Sticker - Paper',
  'Sticker - Plastic',
  'Shirt - Cotton Fiber',
  'Shirt - Synthetic Fabric',
  'Papers - Paper',
  'Lanyard - Plastic',
  'Lanyard - Metal',
  'Lanyard - Biodegradable',
  'Tote - Cotton Fiber',
  'Tote - Synthetic Fabric'
]
const categories = {
  'CO2': ['Pen - Plastic', 'Pen - Metal', 'Pen - Biodegradable'],
  'Water Resource': ['Sticker - Paper', 'Sticker - Plastic'],
  'Energy Resource': ['Shirt - Cotton Fiber', 'Shirt - Synthetic Fabric'],
  'Global Warming Index': ['Papers - Paper']
}

// Technology data
const techItems = ref([])
const techEditingIndex = ref(-1)
const techType = ref('AI Prompts')
const techNum = ref(1)
const techParticipants = ref(1)

// Travel data
const travelItems = ref([])
const travelEditingIndex = ref(-1)
const travelMode = ref('Car')
const travelDistance = ref(0)
const travelParticipants = ref(1)

// Food data
const foodItems = ref([])
const foodEditingIndex = ref(-1)
const foodPackaging = ref('Reusable')
const foodDiet = ref('Plant-Based')
const foodNum = ref(1)

// Total calculation variables
const totalParticipants = ref(1)
const totalHours = ref(1)
const totalErrorMessage = ref('')
const sustainabilityScore = ref(null)

// Load data from sessionStorage on mount
onMounted(() => {
  loadData()
})

// Data persistence functions
function saveData() {
  const data = {
    supplies: items.value,
    technology: techItems.value,
    travel: travelItems.value,
    food: foodItems.value,
    currentSection: currentSection.value
  }
  sessionStorage.setItem('mcfootprint-data', JSON.stringify(data))
}

function loadData() {
  const saved = sessionStorage.getItem('mcfootprint-data')
  if (saved) {
    const data = JSON.parse(saved)
    items.value = data.supplies || []
    techItems.value = data.technology || []
    travelItems.value = data.travel || []
    foodItems.value = data.food || []
    currentSection.value = data.currentSection || 'supplies'
  }
}

function switchSection() {
  saveData()
}

const co2Total = ref(0)
const waterTotal = ref(0)
const energyTotal = ref(0)
const gwiTotal = ref(0)

const co2History = ref([])
const waterHistory = ref([])
const energyHistory = ref([])
const gwiHistory = ref([])

async function addItem() {
  newLabel.value = searchQuery.value.trim()
  console.log('Adding item:', newLabel.value, newValue.value)
  if (!newLabel.value) {
    errorMessage.value = 'Please enter an item.'
    return
  }
  if (!allowedItems.includes(newLabel.value)) {
    errorMessage.value = 'This item is not allowed.'
    return
  }
  if (newValue.value <= 0) {
    errorMessage.value = 'Please enter a positive quantity.'
    return
  }
  errorMessage.value = ''

  try {
    const response = await fetch('http://localhost:5001/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item: newLabel.value, quantity: newValue.value })
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'API request failed')
    }
    const data = await response.json()
    const { total_co2: co2, total_water: water, total_energy: energy, total_gwi: gwi } = data
    // console.log('Received data from API:', data)
    // co2Total.value += co2
    // waterTotal.value += water
    // energyTotal.value += energy
    // gwiTotal.value += gwi
    // co2History.value.push(co2Total)
    // waterHistory.value.push(waterTotal)
    // energyHistory.value.push(energyTotal)
    // gwiHistory.value.push(gwiHistory)

    const existingIndex = items.value.findIndex(item => item.label === newLabel.value)
    if (existingIndex >= 0) {
      // Update existing item reactively
      const existing = items.value[existingIndex]
      items.value[existingIndex] = {
        ...existing,
        value: existing.value + newValue.value,
        co2: existing.co2 + co2,
        water: existing.water + water,
        energy: existing.energy + energy,
        gwi: existing.gwi + gwi
      }
    } else {
      const color = colors[items.value.length % colors.length]
      items.value.push({ label: newLabel.value, value: newValue.value, color, co2, water, energy, gwi })
    }
    console.log('Current items:', items.value)

  } catch (error) {
    console.log('Error occurred:')
    errorMessage.value = `Failed to calculate impact: ${error.message}`
  }

  console.log('Current items:', items.value)

  newLabel.value = ""
  newValue.value = 0
  searchQuery.value = ""


}

function deleteItem(index) {
  items.value.splice(index, 1)
}

function startEdit(index) {
  editingIndex.value = index
}

async function stopEdit() {
  const index = editingIndex.value
  if (index >= 0 && index < items.value.length) {
    const item = items.value[index]
    try {
      const response = await fetch('http://localhost:5001/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item: item.label, quantity: item.value })
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'API request failed')
      }
      const data = await response.json()
      const { total_co2: co2, total_water: water, total_energy: energy, total_gwi: gwi } = data
      item.co2 = co2
      item.water = water
      item.energy = energy
      item.gwi = gwi
    } catch (error) {
      console.log('Error recalculating impacts:', error)
      errorMessage.value = `Failed to recalculate impact: ${error.message}`
    }
  }
  editingIndex.value = -1
}

function clearAll() {
  items.value = []
}

function getChartData(items, attribute, label) {
  return {
    labels: items.map(item => item.label || (item.packaging ? item.packaging + ' - ' + item.diet : item.type || item.mode)),
    datasets: [{
      label,
      data: items.map(item => item[attribute]),
      backgroundColor: items.map(item => item.color || '#228B22'),
      borderColor: items.map(item => item.color || '#228B22'),
      borderWidth: 1
    }]
  }
}

const co2Data = computed(() => getChartData(items.value, 'co2', 'CO2 Impact'))
const waterData = computed(() => getChartData(items.value, 'water', 'Water Impact'))
const energyData = computed(() => getChartData(items.value, 'energy', 'Energy Impact'))
const globalWarmingData = computed(() => getChartData(items.value, 'gwi', 'GWI Impact'))

const totalCO2 = computed(() => items.value.reduce((sum, item) => sum + item.co2, 0))
const totalWater = computed(() => items.value.reduce((sum, item) => sum + item.water, 0))
const totalEnergy = computed(() => items.value.reduce((sum, item) => sum + item.energy, 0))
const totalGWI = computed(() => items.value.reduce((sum, item) => sum + item.gwi, 0))

const maxCO2Product = computed(() => {
  if (items.value.length === 0) return null;
  return items.value.reduce((max, item) => item.co2 > max.co2 ? item : max);
})
const maxWaterProduct = computed(() => {
  if (items.value.length === 0) return null;
  return items.value.reduce((max, item) => item.water > max.water ? item : max);
})
const maxEnergyProduct = computed(() => {
  if (items.value.length === 0) return null;
  return items.value.reduce((max, item) => item.energy > max.energy ? item : max);
})
const maxGWIProduct = computed(() => {
  if (items.value.length === 0) return null;
  return items.value.reduce((max, item) => item.gwi > max.gwi ? item : max);
})

// Material alternatives database for suggestions
const materialAlternatives = {
  'Pen': ['Plastic', 'Metal', 'Biodegradable'],
  'Sticker': ['Paper', 'Plastic'],
  'Shirt': ['Cotton Fiber', 'Synthetic Fabric'],
  'Lanyard': ['Plastic', 'Metal', 'Biodegradable'],
  'Tote': ['Cotton Fiber', 'Synthetic Fabric'],
  'Papers': ['Paper']
}

// Equivalent items for waste reduction suggestions with quantity ratios
const equivalentItems = {
  'Sticker': [{ item: 'Papers - Paper', quantityRatio: 0.5 }] // 1 paper = 2 stickers (promotional equivalent)
}

const getAverageEmissions = (co2, water, energy, gwi) => {
  return (co2 + water + energy + gwi) / 4
}

const materialSuggestions = computed(() => {
  const allSuggestions = []

  items.value.forEach(item => {
    const itemType = item.label.split(' - ')[0]
    const currentMaterial = item.label.split(' - ')[1]
    const alternatives = materialAlternatives[itemType]

    if (alternatives && alternatives.length > 1) {
      const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)

      alternatives.forEach(altMaterial => {
        if (altMaterial !== currentMaterial) {
          // Calculate emissions for alternative material
          const altItemName = `${itemType} - ${altMaterial}`
          const materialImpacts = {
            'Plastic': { co2: 2.10, water: 0.198, energy: 622.0, gwi: 2110.0 },
            'Metal': { co2: 8.89, water: 36.2, energy: 1280.0, gwi: 8880.0 },
            'Biodegradable': { co2: 2.70, water: 2.97, energy: 451.0, gwi: 2710.0 },
            'Synthetic Fabric': { co2: 2.80, water: 1.02, energy: 600.0, gwi: 2810.0 },
            'Cotton Fiber': { co2: 2.94, water: 149.0, energy: 331.0, gwi: 2950.0 },
            'Paper': { co2: 0.701, water: 5.73, energy: 244.0, gwi: 737.0 }
          }

          const itemWeights = {
            'Pen': 0.02, 'Shirt': 0.17, 'Sticker': 0.002, 'Brochure': 0.018, 'Lanyard': 0.025, 'Tote': 0.15, 'Papers': 0.018
          }

          const weight = itemWeights[itemType]
          const altImpacts = materialImpacts[altMaterial]
          const altCo2 = item.value * weight * altImpacts.co2
          const altWater = item.value * weight * altImpacts.water
          const altEnergy = item.value * weight * altImpacts.energy
          const altGwi = item.value * weight * altImpacts.gwi
          const altAvg = getAverageEmissions(altCo2, altWater, altEnergy, altGwi)
          const savings = currentAvg - altAvg

          if (savings > 0) { // Only include positive savings
            allSuggestions.push({
              type: 'material',
              current: item.label,
              suggestion: altItemName,
              savings: savings,
              category: 'Material Alternative',
              description: `Switch from ${item.label} to ${altItemName} to reduce emissions`
            })
          }
        }
      })
    }
  })

  // Sort by savings and return top 3
  return allSuggestions
    .sort((a, b) => b.savings - a.savings)
    .slice(0, 3)
})

const quantitySuggestions = computed(() => {
  const suggestions = []
  items.value.forEach(item => {
    const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)
    const reducedQuantity = Math.max(1, Math.floor(item.value * 0.9))
    if (reducedQuantity < item.value) {
      const reductionFactor = reducedQuantity / item.value
      const newAvg = currentAvg * reductionFactor
      const savings = currentAvg - newAvg
      if (savings > 0) {
        suggestions.push({
          type: 'quantity',
          current: item.label,
          suggestion: `${reducedQuantity} instead of ${item.value}`,
          savings: savings,
          category: 'Quantity Reduction',
          description: `Reduce quantity of ${item.label} from ${item.value} to ${reducedQuantity} to lower emissions`
        })
      }
    }
  })
  return suggestions
})

const equivalentItemSuggestions = computed(() => {
  const suggestions = []
  items.value.forEach(item => {
    const itemType = item.label.split(' - ')[0]
    const equivalents = equivalentItems[itemType]

    if (equivalents) {
      const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)

      equivalents.forEach(equivData => {
        const equivItem = equivData.item
        const quantityRatio = equivData.quantityRatio

        const equivType = equivItem.split(' - ')[0]
        const equivMaterial = equivItem.split(' - ')[1]

        // Calculate emissions for equivalent item using quantity ratio
        const materialImpacts = {
          'Plastic': { co2: 2.10, water: 0.198, energy: 622.0, gwi: 2110.0 },
          'Metal': { co2: 8.89, water: 36.2, energy: 1280.0, gwi: 8880.0 },
          'Biodegradable': { co2: 2.70, water: 2.97, energy: 451.0, gwi: 2710.0 },
          'Synthetic Fabric': { co2: 2.80, water: 1.02, energy: 600.0, gwi: 2810.0 },
          'Cotton Fiber': { co2: 2.94, water: 149.0, energy: 331.0, gwi: 2950.0 },
          'Paper': { co2: 0.701, water: 5.73, energy: 244.0, gwi: 737.0 }
        }

        const itemWeights = {
          'Pen': 0.02, 'Shirt': 0.17, 'Sticker': 0.002, 'Brochure': 0.018, 'Lanyard': 0.025, 'Tote': 0.15, 'Papers': 0.018
        }

        // Use quantity ratio to calculate equivalent quantity
        const equivQuantity = item.value * quantityRatio
        const weight = itemWeights[equivType]
        const equivImpacts = materialImpacts[equivMaterial]

        const equivCo2 = equivQuantity * weight * equivImpacts.co2
        const equivWater = equivQuantity * weight * equivImpacts.water
        const equivEnergy = equivQuantity * weight * equivImpacts.energy
        const equivGwi = equivQuantity * weight * equivImpacts.gwi
        const equivAvg = getAverageEmissions(equivCo2, equivWater, equivEnergy, equivGwi)

        if (equivAvg < currentAvg) {
          const equivQuantityText = quantityRatio === 1 ? '' : ` (${Math.round(equivQuantity)} needed)`
          suggestions.push({
            type: 'equivalent',
            current: item.label,
            suggestion: equivItem + equivQuantityText,
            savings: currentAvg - equivAvg,
            category: 'Equivalent Item',
            description: `Use ${equivItem} instead of ${item.label} to reduce emissions`
          })
        }
      })
    }
  })
  return suggestions
})

const allSuggestions = computed(() => {
  return [...materialSuggestions.value, ...quantitySuggestions.value, ...equivalentItemSuggestions.value]
    .sort((a, b) => b.savings - a.savings) // Sort by savings first
})

const filteredItems = computed(() => {
  if (!searchQuery.value) return allowedItems
  return allowedItems.filter(item =>
    item.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
  if (!isDropdownOpen.value) {
    highlightedIndex.value = -1
  }
}

function selectItem(item) {
  newLabel.value = item
  searchQuery.value = item
  isDropdownOpen.value = false
  highlightedIndex.value = -1
}

function openDropdown() {
  isDropdownOpen.value = true
}

function closeDropdown() {
  // Delay closing to allow for click events
  setTimeout(() => {
    isDropdownOpen.value = false
    highlightedIndex.value = -1
  }, 150)
}

function handleKeyDown(event) {
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    if (!isDropdownOpen.value) {
      isDropdownOpen.value = true
      highlightedIndex.value = 0
    } else {
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, filteredItems.value.length - 1)
    }
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    highlightedIndex.value = Math.max(highlightedIndex.value - 1, 0)
  } else if (event.key === 'Enter') {
    event.preventDefault()
    if (isDropdownOpen.value && highlightedIndex.value >= 0) {
      selectItem(filteredItems.value[highlightedIndex.value])
    }
  } else if (event.key === 'Escape') {
    isDropdownOpen.value = false
    highlightedIndex.value = -1
  }
}

async function calculateTech() {
  const existingIndex = techItems.value.findIndex(item => item.type === techType.value)
  if (existingIndex >= 0) {
    const existing = techItems.value[existingIndex]
    const newNum = existing.num + techNum.value
    // Recalculate impacts
    try {
      const response = await fetch('http://localhost:5001/technology', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: existing.type, num: newNum, participants: existing.participants })
      })
      if (!response.ok) {
        throw new Error('API request failed')
      }
      const data = await response.json()
      // Update existing item reactively
      techItems.value[existingIndex] = {
        ...existing,
        num: newNum,
        co2: data.total_co2,
        water: data.total_water,
        energy: data.total_energy,
        gwi: data.total_gwi
      }
    } catch (error) {
      console.error('Error recalculating tech impact:', error)
    }
  } else {
    try {
      const response = await fetch('http://localhost:5001/technology', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: techType.value, num: techNum.value, participants: techParticipants.value })
      })
      if (!response.ok) {
        throw new Error('API request failed')
      }
      const data = await response.json()
      const impacts = { co2: data.total_co2, water: data.total_water, energy: data.total_energy, gwi: data.total_gwi }
      techItems.value.push({ type: techType.value, num: techNum.value, participants: techParticipants.value, ...impacts })
    } catch (error) {
      console.error('Error calculating tech impact:', error)
    }
  }
  techType.value = 'AI Prompts'
  techNum.value = 1
  techParticipants.value = 1
}

function deleteTechItem(index) {
  techItems.value.splice(index, 1)
}

function startEditTech(index) {
  techEditingIndex.value = index
}

async function stopEditTech(index) {
  const item = techItems.value[index]
  try {
    const response = await fetch('http://localhost:5001/technology', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: item.type, num: item.num, participants: item.participants })
    })
    if (!response.ok) {
      throw new Error('API request failed')
    }
    const data = await response.json()
    item.co2 = data.total_co2
    item.water = data.total_water
    item.energy = data.total_energy
    item.gwi = data.total_gwi
  } catch (error) {
    console.error('Error recalculating tech impact:', error)
  }
  techEditingIndex.value = -1
}

const techCO2Data = computed(() => getChartData(techItems.value, 'co2', 'CO2 Impact'))
const techWaterData = computed(() => getChartData(techItems.value, 'water', 'Water Impact'))
const techEnergyData = computed(() => getChartData(techItems.value, 'energy', 'Energy Impact'))
const techGWIChartData = computed(() => getChartData(techItems.value, 'gwi', 'GWI Impact'))

const techTotalCO2 = computed(() => techItems.value.reduce((sum, item) => sum + item.co2, 0))
const techTotalWater = computed(() => techItems.value.reduce((sum, item) => sum + item.water, 0))
const techTotalEnergy = computed(() => techItems.value.reduce((sum, item) => sum + item.energy, 0))
const techTotalGWI = computed(() => techItems.value.reduce((sum, item) => sum + item.gwi, 0))

const quantityLabel = computed(() => {
  if (techType.value === 'AI Prompts') return 'Prompts per Person'
  else return 'Hours per Person'
})

async function calculateTravel() {
  try {
    const response = await fetch('http://localhost:5001/travel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: travelMode.value, distance: travelDistance.value, participants: travelParticipants.value })
    })
    if (!response.ok) {
      throw new Error('API request failed')
    }
    const data = await response.json()
    const impacts = { co2: data.total_co2, water: data.total_water, energy: data.total_energy, gwi: data.total_gwi }
    travelItems.value.push({ mode: travelMode.value, distance: travelDistance.value, participants: travelParticipants.value, ...impacts })
    travelMode.value = 'Car'
    travelDistance.value = 0
    travelParticipants.value = 1
  } catch (error) {
    console.error('Error calculating travel impact:', error)
  }
}

function deleteTravelItem(index) {
  travelItems.value.splice(index, 1)
}

function startEditTravel(index) {
  travelEditingIndex.value = index
}

async function stopEditTravel(index) {
  const item = travelItems.value[index]
  try {
    const response = await fetch('http://localhost:5001/travel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: item.mode, distance: item.distance, participants: item.participants })
    })
    if (!response.ok) {
      throw new Error('API request failed')
    }
    const data = await response.json()
    item.co2 = data.total_co2
    item.water = data.total_water
    item.energy = data.total_energy
    item.gwi = data.total_gwi
  } catch (error) {
    console.error('Error recalculating travel impact:', error)
  }
  travelEditingIndex.value = -1
}

const travelCO2Data = computed(() => getChartData(travelItems.value, 'co2', 'CO2 Impact'))
const travelWaterData = computed(() => getChartData(travelItems.value, 'water', 'Water Impact'))
const travelEnergyData = computed(() => getChartData(travelItems.value, 'energy', 'Energy Impact'))
const travelGWIChartData = computed(() => getChartData(travelItems.value, 'gwi', 'GWI Impact'))

const travelTotalCO2 = computed(() => travelItems.value.reduce((sum, item) => sum + item.co2, 0))
const travelTotalWater = computed(() => travelItems.value.reduce((sum, item) => sum + item.water, 0))
const travelTotalEnergy = computed(() => travelItems.value.reduce((sum, item) => sum + item.energy, 0))
const travelTotalGWI = computed(() => travelItems.value.reduce((sum, item) => sum + item.gwi, 0))

async function calculateFood() {
  try {
    const response = await fetch('http://localhost:5001/food', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ packaging: foodPackaging.value, diet: foodDiet.value, num: foodNum.value })
    })
    if (!response.ok) {
      throw new Error('API request failed')
    }
    const data = await response.json()
    const impacts = { co2: data.total_co2, water: data.total_water, energy: data.total_energy, gwi: data.total_gwi }
    foodItems.value.push({ packaging: foodPackaging.value, diet: foodDiet.value, num: foodNum.value, ...impacts })
    foodPackaging.value = 'Reusable'
    foodDiet.value = 'Plant-Based'
    foodNum.value = 1
  } catch (error) {
    console.error('Error calculating food impact:', error)
  }
}

function deleteFoodItem(index) {
  foodItems.value.splice(index, 1)
}

function startEditFood(index) {
  foodEditingIndex.value = index
}

async function stopEditFood(index) {
  const item = foodItems.value[index]
  try {
    const response = await fetch('http://localhost:5001/food', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ packaging: item.packaging, diet: item.diet, num: item.num })
    })
    if (!response.ok) {
      throw new Error('API request failed')
    }
    const data = await response.json()
    item.co2 = data.total_co2
    item.water = data.total_water
    item.energy = data.total_energy
    item.gwi = data.total_gwi
  } catch (error) {
    console.error('Error recalculating food impact:', error)
  }
  foodEditingIndex.value = -1
}

const foodCO2Data = computed(() => getChartData(foodItems.value, 'co2', 'CO2 Impact'))
const foodWaterData = computed(() => getChartData(foodItems.value, 'water', 'Water Impact'))
const foodEnergyData = computed(() => getChartData(foodItems.value, 'energy', 'Energy Impact'))
const foodGWIChartData = computed(() => getChartData(foodItems.value, 'gwi', 'GWI Impact'))

const foodTotalCO2 = computed(() => foodItems.value.reduce((sum, item) => sum + item.co2, 0))
const foodTotalWater = computed(() => foodItems.value.reduce((sum, item) => sum + item.water, 0))
const foodTotalEnergy = computed(() => foodItems.value.reduce((sum, item) => sum + item.energy, 0))
const foodTotalGWI = computed(() => foodItems.value.reduce((sum, item) => sum + item.gwi, 0))

// Computed properties for current section
const currentItems = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return items.value
    case 'technology': return techItems.value
    case 'travel': return travelItems.value
    case 'food': return foodItems.value
    default: return []
  }
})

const currentCO2Data = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return co2Data.value
    case 'technology': return techCO2Data.value
    case 'travel': return travelCO2Data.value
    case 'food': return foodCO2Data.value
    default: return { labels: [], datasets: [] }
  }
})

const currentWaterData = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return waterData.value
    case 'technology': return techWaterData.value
    case 'travel': return travelWaterData.value
    case 'food': return foodWaterData.value
    default: return { labels: [], datasets: [] }
  }
})

const currentEnergyData = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return energyData.value
    case 'technology': return techEnergyData.value
    case 'travel': return travelEnergyData.value
    case 'food': return foodEnergyData.value
    default: return { labels: [], datasets: [] }
  }
})

const currentGWIChartData = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return globalWarmingData.value
    case 'technology': return techGWIChartData.value
    case 'travel': return travelGWIChartData.value
    case 'food': return foodGWIChartData.value
    default: return { labels: [], datasets: [] }
  }
})

const currentTotalCO2 = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return totalCO2.value
    case 'technology': return techTotalCO2.value
    case 'travel': return travelTotalCO2.value
    case 'food': return foodTotalCO2.value
    default: return 0
  }
})

const currentTotalWater = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return totalWater.value
    case 'technology': return techTotalWater.value
    case 'travel': return travelTotalWater.value
    case 'food': return foodTotalWater.value
    default: return 0
  }
})

const currentTotalEnergy = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return totalEnergy.value
    case 'technology': return techTotalEnergy.value
    case 'travel': return travelTotalEnergy.value
    case 'food': return foodTotalEnergy.value
    default: return 0
  }
})

const currentTotalGWI = computed(() => {
  switch (currentSection.value) {
    case 'supplies': return totalGWI.value
    case 'technology': return techTotalGWI.value
    case 'travel': return travelTotalGWI.value
    case 'food': return foodTotalGWI.value
    default: return 0
  }
})

// Max emission products for current section
const currentMaxCO2Product = computed(() => {
  const items = currentItems.value
  if (items.length === 0) return null
  return items.reduce((max, item) => item.co2 > max.co2 ? item : max)
})

const currentMaxWaterProduct = computed(() => {
  const items = currentItems.value
  if (items.length === 0) return null
  return items.reduce((max, item) => item.water > max.water ? item : max)
})

const currentMaxEnergyProduct = computed(() => {
  const items = currentItems.value
  if (items.length === 0) return null
  return items.reduce((max, item) => item.energy > max.energy ? item : max)
})

const currentMaxGWIProduct = computed(() => {
  const items = currentItems.value
  if (items.length === 0) return null
  return items.reduce((max, item) => item.gwi > max.gwi ? item : max)
})

// Section-specific suggestions
const currentSectionSuggestions = computed(() => {
  const suggestions = []

  switch (currentSection.value) {
    case 'technology':
      // Suggest more efficient technology options
      techItems.value.forEach(item => {
        const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)

        // Suggest reducing AI prompts by 50%
        if (item.type === 'AI Prompts' && item.num > 1) {
          const reducedNum = Math.max(1, Math.floor(item.num * 0.5))
          const reductionFactor = reducedNum / item.num
          const newAvg = currentAvg * reductionFactor
          const savings = currentAvg - newAvg

          if (savings > 0) {
            suggestions.push({
              category: 'Efficiency',
              description: `Reduce ${item.type} from ${item.num} to ${reducedNum} prompts per person`,
              savings: savings
            })
          }
        }

        // Suggest switching to more efficient device usage
        if (item.type.includes('Device')) {
          suggestions.push({
            category: 'Alternative',
            description: `Consider using cloud computing instead of ${item.type} to reduce energy consumption`,
            savings: currentAvg * 0.3 // Assume 30% savings
          })
        }
      })
      break

    case 'travel':
      // Suggest more efficient travel modes
      travelItems.value.forEach(item => {
        const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)

        // Travel mode alternatives
        const modeAlternatives = {
          'Car': { next: 'Bus', savings: 0.6 },
          'Bus': { next: 'Train', savings: 0.7 },
          'Train': { next: null, savings: 0 },
          'Plane': { next: 'Train', savings: 0.8 }
        }

        const alt = modeAlternatives[item.mode]
        if (alt && alt.next) {
          const newAvg = currentAvg * (1 - alt.savings)
          const savings = currentAvg - newAvg

          suggestions.push({
            category: 'Mode Switch',
            description: `Switch from ${item.mode} to ${alt.next} for ${item.distance}km trip`,
            savings: savings
          })
        }

        // Suggest carpooling for cars
        if (item.mode === 'Car' && item.participants === 1) {
          suggestions.push({
            category: 'Carpooling',
            description: `Carpool with 2-3 people to reduce per-person emissions by 60-70%`,
            savings: currentAvg * 0.65
          })
        }
      })
      break

    case 'food':
      // Suggest more sustainable food options
      foodItems.value.forEach(item => {
        const currentAvg = getAverageEmissions(item.co2, item.water, item.energy, item.gwi)

        // Diet alternatives
        if (item.diet === 'Meat') {
          const plantBasedAvg = currentAvg * 0.25 // Plant-based uses much less resources
          const savings = currentAvg - plantBasedAvg

          suggestions.push({
            category: 'Diet Change',
            description: `Switch from Meat to Plant-Based diet for ${item.num} meals`,
            savings: savings
          })
        }

        // Packaging alternatives
        const packagingAlternatives = {
          'Paper': { next: 'Reusable', savings: 0.9 },
          'Compostable': { next: 'Reusable', savings: 0.95 },
          'Reusable': { next: null, savings: 0 }
        }

        const alt = packagingAlternatives[item.packaging]
        if (alt && alt.next) {
          const newAvg = currentAvg * (1 - alt.savings)
          const savings = currentAvg - newAvg

          suggestions.push({
            category: 'Packaging',
            description: `Use ${alt.next} packaging instead of ${item.packaging} for ${item.num} meals`,
            savings: savings
          })
        }
      })
      break

    case 'supplies':
      // Debug: Add a test suggestion if no real suggestions
      let suppliesSuggestions = allSuggestions.value.slice(0, 3)
      if (suppliesSuggestions.length === 0 && items.value.length > 0) {
        // Add a debug suggestion to show the section is working
        suppliesSuggestions = [{
          category: 'Debug',
          description: `Consider eco-friendly alternatives for your ${items.value.length} item(s)`,
          savings: 0.1
        }]
      }
      return suppliesSuggestions
  }

  // Sort by savings and return top 3
  return suggestions
    .sort((a, b) => b.savings - a.savings)
    .slice(0, 3)
})

// Modal functions
function openModal(chartData) {
  modalOpen.value = true
  modalChartData.value = chartData.data
  modalChartTitle.value = chartData.title
  nextTick(() => {
    const modalChart = new Chart(modalCanvas.value, {
      type: "bar",
      data: modalChartData.value,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: '#10b981',
              font: {
                size: 16,
                weight: '700',
                family: 'Inter, sans-serif'
              }
            }
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#f1f5f9',
              font: {
                size: 14,
                weight: '600',
                family: 'Inter, sans-serif'
              },
              maxRotation: 45,
              minRotation: 0,
              padding: 10
            },
            grid: {
              color: 'rgba(71, 85, 105, 0.4)'
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: '#f1f5f9',
              font: {
                size: 14,
                weight: '600',
                family: 'Inter, sans-serif'
              },
              padding: 15
            },
            grid: {
              color: 'rgba(71, 85, 105, 0.4)'
            }
          }
        }
      }
    })
  })
}

// Computed properties for section totals
const suppliesTotals = computed(() => ({
  co2: items.value.reduce((sum, item) => sum + item.co2, 0),
  water: items.value.reduce((sum, item) => sum + item.water, 0),
  energy: items.value.reduce((sum, item) => sum + item.energy, 0),
  gwi: items.value.reduce((sum, item) => sum + item.gwi, 0)
}))

const technologyTotals = computed(() => ({
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

// Pie chart data for each metric showing source breakdown
const co2SourceData = computed(() => {
  const totalCo2 = suppliesTotals.value.co2 + technologyTotals.value.co2 + travelTotals.value.co2 + foodTotals.value.co2
  if (totalCo2 === 0) {
    return {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    }
  } else {
    return {
      labels: ['Supplies', 'Technology', 'Travel', 'Food'],
      datasets: [{
        data: [
          suppliesTotals.value.co2 || 0,
          technologyTotals.value.co2 || 0,
          travelTotals.value.co2 || 0,
          foodTotals.value.co2 || 0
        ],
        backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    }
  }
})

const waterSourceData = computed(() => {
  const totalWater = suppliesTotals.value.water + technologyTotals.value.water + travelTotals.value.water + foodTotals.value.water
  if (totalWater === 0) {
    return {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    }
  }
  return {
    labels: ['Supplies', 'Technology', 'Travel', 'Food'],
    datasets: [{
      data: [
        suppliesTotals.value.water || 0,
        technologyTotals.value.water || 0,
        travelTotals.value.water || 0,
        foodTotals.value.water || 0
      ],
      backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

const energySourceData = computed(() => {
  const totalEnergy = suppliesTotals.value.energy + technologyTotals.value.energy + travelTotals.value.energy + foodTotals.value.energy
  if (totalEnergy === 0) {
    return {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    }
  }
  return {
    labels: ['Supplies', 'Technology', 'Travel', 'Food'],
    datasets: [{
      data: [
        suppliesTotals.value.energy || 0,
        technologyTotals.value.energy || 0,
        travelTotals.value.energy || 0,
        foodTotals.value.energy || 0
      ],
      backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

const gwiSourceData = computed(() => {
  const totalGwi = suppliesTotals.value.gwi + technologyTotals.value.gwi + travelTotals.value.gwi + foodTotals.value.gwi
  if (totalGwi === 0) {
    return {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    }
  }
  return {
    labels: ['Supplies', 'Technology', 'Travel', 'Food'],
    datasets: [{
      data: [
        suppliesTotals.value.gwi || 0,
        technologyTotals.value.gwi || 0,
        travelTotals.value.gwi || 0,
        foodTotals.value.gwi || 0
      ],
      backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

// Pie chart data for each section
const suppliesPieData = computed(() => ({
  labels: ['CO2', 'Water', 'Energy', 'GWI'],
  datasets: [{
    data: [
      suppliesTotals.value.co2 || 0.1,
      suppliesTotals.value.water || 0.1,
      suppliesTotals.value.energy || 0.1,
      suppliesTotals.value.gwi || 0.1
    ],
    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
}))

const technologyPieData = computed(() => ({
  labels: ['CO2', 'Water', 'Energy', 'GWI'],
  datasets: [{
    data: [
      technologyTotals.value.co2 || 0.1,
      technologyTotals.value.water || 0.1,
      technologyTotals.value.energy || 0.1,
      technologyTotals.value.gwi || 0.1
    ],
    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
}))

const travelPieData = computed(() => ({
  labels: ['CO2', 'Water', 'Energy', 'GWI'],
  datasets: [{
    data: [
      travelTotals.value.co2 || 0.1,
      travelTotals.value.water || 0.1,
      travelTotals.value.energy || 0.1,
      travelTotals.value.gwi || 0.1
    ],
    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
}))

const foodPieData = computed(() => ({
  labels: ['CO2', 'Water', 'Energy', 'GWI'],
  datasets: [{
    data: [
      foodTotals.value.co2 || 0.1,
      foodTotals.value.water || 0.1,
      foodTotals.value.energy || 0.1,
      foodTotals.value.gwi || 0.1
    ],
    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731'],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
}))

async function calculateTotalSustainability() {
  if (totalParticipants.value <= 0 || totalHours.value <= 0) {
    throw new Error('Please enter valid participants and hours')
  }

  // Sum up totals from all sections
  const physicalWaste = [
    suppliesTotals.value.co2,
    suppliesTotals.value.water,
    suppliesTotals.value.energy,
    suppliesTotals.value.gwi
  ]

  const travel_totals = [
    travelTotals.value.co2,
    travelTotals.value.water,
    travelTotals.value.energy,
    travelTotals.value.gwi
  ]

  const technology_totals = [
    technologyTotals.value.co2,
    technologyTotals.value.water,
    technologyTotals.value.energy,
    technologyTotals.value.gwi
  ]

  const food_totals = [
    foodTotals.value.co2,
    foodTotals.value.water,
    foodTotals.value.energy,
    foodTotals.value.gwi
  ]

  const response = await fetch('http://localhost:5001/total', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      physical_waste: physicalWaste,
      travel: travel_totals,
      technology: technology_totals,
      food: food_totals,
      participants: totalParticipants.value,
      hours: totalHours.value
    })
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`HTTP ${response.status}: ${errorText}`)
  }

  const data = await response.json()
  return data
}

async function handleCalculateTotalSustainability() {
  try {
    totalErrorMessage.value = ''
    const result = await calculateTotalSustainability()
    sustainabilityScore.value = result
  } catch (error) {
    console.error('Error calculating total sustainability:', error)
    totalErrorMessage.value = error.message
    sustainabilityScore.value = null
  }
}

function closeModal() {
  modalOpen.value = false
  modalChartData.value = null
  modalChartTitle.value = ''
}
</script>
