<template>
  <canvas ref="canvas" @click="handleClick"></canvas>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import Chart from "chart.js/auto"

const props = defineProps({
  data: Object,
  title: String,
  chartType: {
    type: String,
    default: 'bar'
  }
})

const emit = defineEmits(['chart-click'])

const canvas = ref(null)
let chart = null

const getChartConfig = (type, data) => {
  const baseConfig = {
    data: {
      labels: data.labels,
      datasets: data.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          labels: {
            color: '#10b981',
            font: {
              size: 12,
              weight: '600',
              family: 'Inter, sans-serif'
            }
          }
        }
      }
    }
  }

  if (type === 'pie') {
    return {
      type: 'pie',
      ...baseConfig,
      options: {
        ...baseConfig.options,
        plugins: {
          ...baseConfig.options.plugins,
          legend: {
            ...baseConfig.options.plugins.legend,
            position: 'bottom'
          }
        }
      }
    }
  } else {
    // Bar chart
    return {
      type: 'bar',
      ...baseConfig,
      options: {
        ...baseConfig.options,
        scales: {
          x: {
            ticks: {
              color: '#cbd5e1',
              font: {
                size: 11,
                weight: '500',
                family: 'Inter, sans-serif'
              },
              maxRotation: 45,
              minRotation: 0
            },
            grid: {
              color: 'rgba(71, 85, 105, 0.3)'
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: '#cbd5e1',
              font: {
                size: 11,
                weight: '500',
                family: 'Inter, sans-serif'
              }
            },
            grid: {
              color: 'rgba(71, 85, 105, 0.3)'
            }
          }
        }
      }
    }
  }
}

onMounted(() => {
  const config = getChartConfig(props.chartType, props.data)
  chart = new Chart(canvas.value, config)
})

watch(
  () => props.data,
  (newData) => {
    if (chart) {
      chart.data.labels = newData.labels
      chart.data.datasets = newData.datasets
      chart.update()
    }
  },
  { deep: true }
)

watch(
  () => props.chartType,
  (newType) => {
    if (chart) {
      // Destroy old chart and create new one with different type
      chart.destroy()
      const config = getChartConfig(newType, props.data)
      chart = new Chart(canvas.value, config)
    }
  }
)

const handleClick = () => {
  emit('chart-click', {
    data: props.data,
    title: props.title
  })
}
</script>
