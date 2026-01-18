import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import Totals from './views/Totals.vue'

// Simple router setup for navigation
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: App },
    { path: '/totals', name: 'Totals', component: Totals }
  ]
})

const app = createApp(App)

app.use(router)

// Custom directive to scale text to fit within container
app.directive('fit-text', {
  mounted(el) {
    const scaleText = () => {
      // Reset any previous transforms first
      el.style.transform = 'none'
      el.style.display = 'block'
      el.style.whiteSpace = 'normal'

      const container = el.parentElement
      if (!container) return

      const containerWidth = container.offsetWidth - 32 // Account for padding
      const textWidth = el.scrollWidth

      // Only scale down if text is too wide
      if (textWidth > containerWidth) {
        const scale = containerWidth / textWidth
        el.style.transform = `scale(${scale})`
        el.style.transformOrigin = 'center top'
        el.style.display = 'inline-block'
        el.style.whiteSpace = 'nowrap'
      } else {
        // Reset to normal if it fits
        el.style.transform = 'none'
        el.style.display = 'block'
        el.style.whiteSpace = 'normal'
      }
    }

    // Scale immediately
    scaleText()

    // Scale on window resize
    window.addEventListener('resize', scaleText)

    // Store the function for cleanup
    el._scaleText = scaleText
  },
  updated(el) {
    // Re-scale when text content changes
    el._scaleText()
  },
  unmounted(el) {
    window.removeEventListener('resize', el._scaleText)
  }
})

app.mount('#app')
